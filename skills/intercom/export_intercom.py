#!/usr/bin/env python3
"""
Export Intercom conversations from ClickHouse to JSON files.

This script pulls conversation data from the ClickHouse analytics database
(synced from Intercom via Airbyte) and exports it to JSON files.

Usage:
    python export_intercom.py                                    # Last 7 days
    python export_intercom.py --days 30                          # Last 30 days
    python export_intercom.py --start-date 2025-11-01            # From date to now
    python export_intercom.py --start-date 2025-11-01 --end-date 2025-11-30
    python export_intercom.py --source customer_initiated        # Only customer-initiated
    python export_intercom.py --state open                       # Only open tickets
    python export_intercom.py --conversation-id 215472099759184  # Single conversation
"""

import json
import os
import re
import ssl
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import click
from dotenv import load_dotenv

load_dotenv('secret/services/intercom.env')

# Create SSL context that doesn't verify certificates (for internal services)
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


CLICKHOUSE_URL = os.environ["CLICKHOUSE_URL"]
CLICKHOUSE_USER = os.environ["CLICKHOUSE_USER"]
CLICKHOUSE_PASSWORD = os.environ["CLICKHOUSE_PASSWORD"]
DEFAULT_OUTPUT_DIR = "data/customer-service/intercom"


def query_clickhouse(sql: str) -> dict:
    """Execute a query against ClickHouse and return JSON result."""
    req = Request(
        CLICKHOUSE_URL,
        data=sql.encode('utf-8'),
        headers={
            'X-ClickHouse-User': CLICKHOUSE_USER,
            'X-ClickHouse-Key': CLICKHOUSE_PASSWORD,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        method='POST'
    )

    try:
        with urlopen(req, timeout=120, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        click.echo(f"HTTP Error: {e.code} - {e.reason}", err=True)
        raise
    except URLError as e:
        click.echo(f"URL Error: {e.reason}", err=True)
        raise


def html_to_text(html: str) -> str:
    """Simple HTML to plain text conversion."""
    if not html:
        return ""

    text = html
    # Remove common HTML tags
    text = re.sub(r'<p[^>]*>', '', text)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'<br[^>]*/?\s*>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)

    # Decode entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    text = text.replace('\u00ad', '')
    text = text.replace('\u200b', '')

    # Clean whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def fetch_conversations(
    start_timestamp: int,
    end_timestamp: int,
    source_filter: Optional[str] = None,
    state_filter: Optional[str] = None,
    limit: int = 10000
) -> list:
    """Fetch conversations from ClickHouse."""

    where_clauses = [
        f"created_at >= {start_timestamp}",
        f"created_at <= {end_timestamp}"
    ]

    if state_filter:
        where_clauses.append(f"state = '{state_filter}'")

    where_sql = " AND ".join(where_clauses)

    sql = f"""
    SELECT
        id,
        title,
        state,
        open,
        fromUnixTimestamp(created_at) as created_at,
        fromUnixTimestamp(updated_at) as updated_at,
        source,
        assignee,
        contacts,
        tags,
        ai_agent_participated,
        conversation_rating,
        statistics,
        custom_attributes,
        conversation_message
    FROM default.intercom_conversations
    WHERE {where_sql}
    ORDER BY created_at DESC
    LIMIT {limit}
    FORMAT JSON
    """

    result = query_clickhouse(sql)
    conversations = result.get('data', [])

    # Filter by source type if specified (needs post-processing since it's JSON)
    if source_filter:
        filtered = []
        for conv in conversations:
            source = conv.get('source')
            if source:
                try:
                    source_data = json.loads(source) if isinstance(source, str) else source
                    if source_data.get('delivered_as') == source_filter:
                        filtered.append(conv)
                except (json.JSONDecodeError, TypeError):
                    pass
        conversations = filtered

    return conversations


def fetch_conversation_parts(conversation_ids: list, limit_per_conv: int = 500) -> list:
    """Fetch conversation parts (messages) for given conversation IDs."""
    if not conversation_ids:
        return []

    # Convert to integers for query
    ids_str = ", ".join([str(int(cid)) for cid in conversation_ids])

    sql = f"""
    SELECT
        conversation_id,
        id as part_id,
        part_type,
        body,
        author,
        fromUnixTimestamp(created_at) as created_at
    FROM default.intercom_conversation_parts
    WHERE conversation_id IN ({ids_str})
    ORDER BY conversation_id, created_at ASC
    FORMAT JSON
    """

    result = query_clickhouse(sql)
    return result.get('data', [])


def fetch_single_conversation(conversation_id: str) -> dict:
    """Fetch a single conversation with all its parts."""

    # Fetch conversation
    sql = f"""
    SELECT
        id,
        title,
        state,
        open,
        fromUnixTimestamp(created_at) as created_at,
        fromUnixTimestamp(updated_at) as updated_at,
        source,
        assignee,
        contacts,
        tags,
        ai_agent_participated,
        conversation_rating,
        statistics,
        custom_attributes,
        conversation_message
    FROM default.intercom_conversations
    WHERE id = '{conversation_id}'
    FORMAT JSON
    """

    result = query_clickhouse(sql)
    conversations = result.get('data', [])

    if not conversations:
        return None

    conv = conversations[0]

    # Fetch parts
    parts = fetch_conversation_parts([conversation_id])
    conv['parts'] = parts

    return conv


def process_conversation(conv: dict) -> dict:
    """Process and clean a conversation record."""
    processed = {
        'id': conv.get('id'),
        'title': conv.get('title'),
        'state': conv.get('state'),
        'is_open': conv.get('open'),
        'created_at': conv.get('created_at'),
        'updated_at': conv.get('updated_at'),
        'ai_agent_participated': conv.get('ai_agent_participated'),
    }

    # Parse JSON fields
    for field in ['source', 'assignee', 'contacts', 'tags', 'conversation_rating', 'statistics', 'custom_attributes']:
        value = conv.get(field)
        if value and isinstance(value, str):
            try:
                processed[field] = json.loads(value)
            except json.JSONDecodeError:
                processed[field] = value
        else:
            processed[field] = value

    # Extract key info
    if processed.get('source'):
        processed['source_type'] = processed['source'].get('delivered_as')
        processed['source_channel'] = processed['source'].get('type')

    if processed.get('assignee'):
        processed['assignee_name'] = processed['assignee'].get('name')

    # Parse initial message
    msg = conv.get('conversation_message')
    if msg and isinstance(msg, str):
        try:
            msg_data = json.loads(msg)
            processed['initial_message'] = html_to_text(msg_data.get('body', ''))
        except json.JSONDecodeError:
            processed['initial_message'] = None

    return processed


def process_part(part: dict) -> dict:
    """Process and clean a conversation part."""
    processed = {
        'conversation_id': part.get('conversation_id'),
        'part_id': part.get('part_id'),
        'part_type': part.get('part_type'),
        'created_at': part.get('created_at'),
        'body_html': part.get('body'),
        'body_text': html_to_text(part.get('body', '')),
    }

    # Parse author
    author = part.get('author')
    if author and isinstance(author, str):
        try:
            author_data = json.loads(author)
            processed['author_type'] = author_data.get('type')
            processed['author_name'] = author_data.get('name')
            processed['author_id'] = author_data.get('id')
        except json.JSONDecodeError:
            processed['author_type'] = None
            processed['author_name'] = None
    elif author:
        processed['author_type'] = author.get('type')
        processed['author_name'] = author.get('name')
        processed['author_id'] = author.get('id')

    return processed


def generate_summary(conversations: list, parts: list, start_date: datetime, end_date: datetime) -> dict:
    """Generate summary statistics."""

    total_conversations = len(conversations)

    # Count by state
    state_counts = {}
    source_counts = {}
    ai_handled = 0

    for conv in conversations:
        state = conv.get('state', 'unknown')
        state_counts[state] = state_counts.get(state, 0) + 1

        source = conv.get('source_type', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

        if conv.get('ai_agent_participated'):
            ai_handled += 1

    # Part stats
    part_type_counts = {}
    author_type_counts = {}

    for part in parts:
        ptype = part.get('part_type', 'unknown')
        part_type_counts[ptype] = part_type_counts.get(ptype, 0) + 1

        atype = part.get('author_type', 'unknown')
        author_type_counts[atype] = author_type_counts.get(atype, 0) + 1

    return {
        'export_date': datetime.now(timezone.utc).isoformat(),
        'date_range': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat(),
        },
        'totals': {
            'conversations': total_conversations,
            'messages': len(parts),
            'ai_handled_conversations': ai_handled,
        },
        'by_state': state_counts,
        'by_source': source_counts,
        'by_part_type': part_type_counts,
        'by_author_type': author_type_counts,
    }


def merge_conversations_with_parts(conversations: list, parts: list) -> list:
    """Merge conversations with their parts to create full threads."""

    # Group parts by conversation_id
    parts_by_conv = {}
    for part in parts:
        conv_id = str(part.get('conversation_id'))
        if conv_id not in parts_by_conv:
            parts_by_conv[conv_id] = []
        parts_by_conv[conv_id].append(part)

    # Merge
    full_threads = []
    for conv in conversations:
        conv_id = str(conv.get('id'))
        thread = dict(conv)
        thread['messages'] = parts_by_conv.get(conv_id, [])
        thread['message_count'] = len(thread['messages'])
        full_threads.append(thread)

    return full_threads


@click.command()
@click.option('--start-date', type=str, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', type=str, help='End date (YYYY-MM-DD)')
@click.option('--days', type=int, default=7, help='Days to fetch (default: 7)')
@click.option('--source', type=click.Choice(['customer_initiated', 'admin_initiated', 'automated']), help='Filter by source type')
@click.option('--state', type=click.Choice(['open', 'closed', 'snoozed']), help='Filter by state')
@click.option('--conversation-id', type=str, help='Fetch single conversation by ID')
@click.option('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR, help='Output directory')
@click.option('--limit', type=int, default=10000, help='Max conversations to fetch')
def main(start_date: str, end_date: str, days: int, source: str, state: str,
         conversation_id: str, output_dir: str, limit: int):
    """
    Export Intercom conversations from ClickHouse to JSON files.
    """

    # Handle single conversation export
    if conversation_id:
        click.echo(f"Fetching conversation {conversation_id}...")
        conv = fetch_single_conversation(conversation_id)
        if not conv:
            click.echo(f"Conversation {conversation_id} not found", err=True)
            sys.exit(1)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_file = output_path / f"conversation-{conversation_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(conv, f, indent=2, ensure_ascii=False)

        click.echo(f"Exported to {output_file}")
        return

    # Calculate date range
    now = datetime.now(timezone.utc)

    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    elif start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_dt = now
    else:
        start_dt = now - timedelta(days=days)
        end_dt = now

    start_timestamp = int(start_dt.timestamp())
    end_timestamp = int(end_dt.timestamp())

    click.echo(f"Fetching conversations from {start_dt.date()} to {end_dt.date()}...")

    # Fetch conversations
    conversations_raw = fetch_conversations(
        start_timestamp, end_timestamp,
        source_filter=source,
        state_filter=state,
        limit=limit
    )

    click.echo(f"Found {len(conversations_raw)} conversations")

    if not conversations_raw:
        click.echo("No conversations found for the given criteria")
        return

    # Process conversations
    conversations = [process_conversation(c) for c in conversations_raw]

    # Fetch conversation parts
    conv_ids = [c['id'] for c in conversations if c['id']]
    click.echo(f"Fetching messages for {len(conv_ids)} conversations...")

    parts_raw = fetch_conversation_parts(conv_ids)
    click.echo(f"Found {len(parts_raw)} messages")

    # Process parts
    parts = [process_part(p) for p in parts_raw]

    # Generate summary
    summary = generate_summary(conversations, parts, start_dt, end_dt)

    # Create full threads
    full_threads = merge_conversations_with_parts(conversations, parts)

    # Create output directory
    export_date = datetime.now().strftime('%Y-%m-%d')
    output_path = Path(output_dir) / f"export-{export_date}"
    output_path.mkdir(parents=True, exist_ok=True)

    # Write files
    files = {
        'conversations.json': conversations,
        'messages.json': parts,
        'summary.json': summary,
        'full_threads.json': full_threads,
    }

    for filename, data in files.items():
        filepath = output_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        click.echo(f"Written: {filepath}")

    click.echo(f"\nExport complete!")
    click.echo(f"  Conversations: {len(conversations)}")
    click.echo(f"  Messages: {len(parts)}")
    click.echo(f"  Output: {output_path}")


if __name__ == '__main__':
    main()
