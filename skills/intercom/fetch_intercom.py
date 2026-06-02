#!/usr/bin/env python3
"""
Fetch conversations from Intercom and save as JSONL file.

This script fetches conversations from Intercom API and saves them to a JSONL file,
appending data as it's fetched for better performance and reliability.

Requirements:
- INTERCOM_ACCESS_TOKEN environment variable set with your Intercom access token
- python-intercom package installed

Usage:
    python fetch_intercom.py --start-date 2025-01-01 --end-date 2025-01-31 --output-file ./intercom-conversations.jsonl
    python fetch_intercom.py --days 7 --output-file ./intercom-conversations.jsonl  # Last 7 days
    python fetch_intercom.py --help  # Show all options
"""

import os
import sys
import json
import click
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import re

from dotenv import load_dotenv
from dateutil.parser import parse as parse_date
from intercom import Intercom

load_dotenv()
from intercom.errors import BadRequestError, UnauthorizedError


class IntercomConversationFetcher:
    """Fetches conversations from Intercom and saves them as JSONL file."""

    def __init__(self, access_token: str, output_file: str, filter_state: str = 'all', filter_type: str = None, include_parts: bool = True):
        """
        Initialize the Intercom conversation fetcher.

        Args:
            access_token: Intercom access token
            output_file: Path to output JSONL file
            filter_state: Filter by conversation state
            filter_type: Filter by ticket type
            include_parts: Whether to include conversation parts
        """
        self.client = Intercom(token=access_token)
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.conversations_fetched = 0
        self.filter_state = filter_state
        self.filter_type = filter_type
        self.include_parts = include_parts

    def html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to markdown."""
        if not html_content or not isinstance(html_content, str):
            return ""

        content = html_content

        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<br[^>]*/?>', r'\n', content)
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
        content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
        content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
        content = re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2) + '\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<ul[^>]*>', r'', content)
        content = re.sub(r'</ul>', r'\n', content)
        content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
        content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = content.strip()

        content = content.replace('&amp;', '&')
        content = content.replace('&lt;', '<')
        content = content.replace('&gt;', '>')
        content = content.replace('&quot;', '"')
        content = content.replace('&#39;', "'")
        content = content.replace('&nbsp;', ' ')
        content = content.replace('­', '')

        return content

    def fetch_conversations_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        per_page: int = 50
    ) -> None:
        """
        Fetch conversations within a date range and save to JSONL file.

        Args:
            start_date: Start date for fetching conversations
            end_date: End date for fetching conversations
            per_page: Number of conversations per API call
        """

        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        click.echo(f"Fetching conversations from {start_date.date()} to {end_date.date()}...")
        click.echo(f"Output file: {self.output_file}")

        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                page = 1

                while True:
                    click.echo(f"Fetching page {page}...")

                    if page > 1:
                        time.sleep(0.5)

                    try:
                        response = self.client.conversations.search(
                            query={
                                "field": "updated_at",
                                "operator": ">",
                                "value": start_timestamp
                            },
                            pagination={
                                "per_page": per_page,
                                "page": page
                            }
                        )

                        conversations = []
                        if hasattr(response, 'items'):
                            conversations = response.items
                        elif hasattr(response, 'conversations'):
                            conversations = response.conversations

                        click.echo(f"Found {len(conversations)} conversations on page {page}")

                        if not conversations:
                            click.echo("No conversations found on this page, breaking...")
                            break

                        saved_count = 0
                        for conv in conversations:
                            if self.filter_state != 'all':
                                if getattr(conv, 'state', '') != self.filter_state:
                                    continue

                            if hasattr(conv, 'source') and conv.source and hasattr(conv.source, 'type'):
                                if getattr(conv.source, 'type', '') == 'email':
                                    continue

                            conv_data = self._extract_conversation_data(conv)

                            conv_created_at = conv_data.get('created_at')
                            if conv_created_at:
                                if isinstance(conv_created_at, int):
                                    conv_date = datetime.fromtimestamp(conv_created_at, tz=timezone.utc)
                                else:
                                    conv_date = parse_date(str(conv_created_at))

                                if conv_date < start_date or conv_date > end_date:
                                    continue

                            if self.filter_type:
                                ticket_type = conv_data.get('custom_attributes', {}).get('Type', '')
                                if ticket_type.lower() != self.filter_type.lower():
                                    continue

                            f.write(json.dumps(conv_data) + '\n')
                            f.flush()
                            self.conversations_fetched += 1
                            saved_count += 1

                        click.echo(f"Processed {len(conversations)} conversations, saved {saved_count}. Total saved: {self.conversations_fetched}")

                        if len(conversations) < per_page:
                            break

                        page += 1

                    except (BadRequestError, Exception) as e:
                        if isinstance(e, BadRequestError) or "400" in str(e):
                            click.echo("Complex query failed, trying simpler listing...")
                            try:
                                response = self.client.conversations.list(
                                    per_page=per_page,
                                    page=page
                                )
                                conversations = response.conversations if hasattr(response, 'conversations') else []
                                click.echo(f"Fallback query found {len(conversations)} conversations")
                            except Exception as fallback_error:
                                click.echo(f"Fallback query also failed: {fallback_error}")
                                conversations = []
                                break
                        elif "429" in str(e):
                            click.echo("Rate limit hit, waiting 60 seconds...")
                            time.sleep(60)
                            continue
                        else:
                            click.echo(f"API Error: {str(e)}")
                            raise

            click.echo(f"Total conversations fetched: {self.conversations_fetched}")

        except Exception as e:
            click.echo(f"Error fetching conversations: {str(e)}", err=True)
            sys.exit(1)

        click.echo(f"Total conversations fetched: {self.conversations_fetched}")

    def _extract_conversation_data(self, conversation) -> Dict[str, Any]:
        """Extract conversation data as JSON-serializable dictionary."""
        try:
            data = {}

            basic_fields = ['id', 'title', 'state', 'priority', 'created_at', 'updated_at',
                          'waiting_since', 'snoozed_until', 'open', 'read']

            for field in basic_fields:
                if hasattr(conversation, field):
                    data[field] = getattr(conversation, field)

            if hasattr(conversation, 'source') and conversation.source:
                try:
                    source_data = {}
                    source_fields = ['type', 'id', 'delivered_as', 'subject', 'body', 'url', 'redacted']
                    for field in source_fields:
                        if hasattr(conversation.source, field):
                            value = getattr(conversation.source, field)
                            if field == 'body' and value:
                                value = self.html_to_markdown(value)
                            source_data[field] = value

                    if hasattr(conversation.source, 'author') and conversation.source.author:
                        author_data = {}
                        author_fields = ['type', 'id', 'name', 'email']
                        for field in author_fields:
                            if hasattr(conversation.source.author, field):
                                author_data[field] = getattr(conversation.source.author, field)
                        source_data['author'] = author_data

                    if hasattr(conversation.source, 'attachments'):
                        attachments = getattr(conversation.source, 'attachments', [])
                        source_data['attachments'] = [str(att) for att in attachments] if attachments else []

                    data['source'] = source_data
                except Exception as e:
                    data['source'] = f"Error extracting source: {str(e)}"

            if hasattr(conversation, 'contacts') and conversation.contacts:
                try:
                    contacts_data = []
                    if hasattr(conversation.contacts, 'contacts'):
                        contacts = conversation.contacts.contacts
                    elif hasattr(conversation.contacts, 'items'):
                        contacts = conversation.contacts.items
                    else:
                        contacts = []

                    for contact in contacts:
                        contact_data = {}
                        contact_fields = ['id', 'name', 'email', 'phone', 'user_id', 'external_id']
                        for field in contact_fields:
                            if hasattr(contact, field):
                                contact_data[field] = getattr(contact, field)
                        contacts_data.append(contact_data)

                    data['contacts'] = contacts_data
                except Exception as e:
                    data['contacts'] = f"Error extracting contacts: {str(e)}"

            if hasattr(conversation, 'statistics') and conversation.statistics:
                try:
                    data['statistics'] = json.loads(json.dumps(conversation.statistics.__dict__ if hasattr(conversation.statistics, '__dict__') else str(conversation.statistics)))
                except:
                    data['statistics'] = str(conversation.statistics)

            if self.include_parts and hasattr(conversation, 'conversation_parts') and conversation.conversation_parts:
                try:
                    parts_data = []
                    if hasattr(conversation.conversation_parts, 'conversation_parts'):
                        parts = conversation.conversation_parts.conversation_parts
                    elif hasattr(conversation.conversation_parts, 'items'):
                        parts = conversation.conversation_parts.items
                    else:
                        parts = conversation.conversation_parts

                    for part in parts:
                        part_data = {}
                        part_fields = ['id', 'part_type', 'body', 'created_at', 'updated_at']
                        for field in part_fields:
                            if hasattr(part, field):
                                value = getattr(part, field)
                                if field == 'body' and value:
                                    value = self.html_to_markdown(value)
                                part_data[field] = value

                        if hasattr(part, 'author') and part.author:
                            author_data = {}
                            author_fields = ['type', 'id', 'name', 'email']
                            for field in author_fields:
                                if hasattr(part.author, field):
                                    author_data[field] = getattr(part.author, field)
                            part_data['author'] = author_data

                        parts_data.append(part_data)

                    data['conversation_parts'] = parts_data
                except Exception as e:
                    data['conversation_parts'] = f"Error extracting conversation parts: {str(e)}"

            if hasattr(conversation, 'tags') and conversation.tags:
                try:
                    if hasattr(conversation.tags, 'tags'):
                        tags = [getattr(tag, 'name', str(tag)) for tag in conversation.tags.tags]
                    else:
                        tags = [getattr(tag, 'name', str(tag)) for tag in conversation.tags]
                    data['tags'] = tags
                except Exception as e:
                    data['tags'] = f"Error extracting tags: {str(e)}"

            if hasattr(conversation, 'assignee') and conversation.assignee:
                try:
                    assignee_data = {}
                    assignee_fields = ['type', 'id', 'name', 'email']
                    for field in assignee_fields:
                        if hasattr(conversation.assignee, field):
                            assignee_data[field] = getattr(conversation.assignee, field)
                    data['assignee'] = assignee_data
                except Exception as e:
                    data['assignee'] = f"Error extracting assignee: {str(e)}"

            if hasattr(conversation, 'custom_attributes'):
                data['custom_attributes'] = getattr(conversation, 'custom_attributes', {})

            data['summary'] = {
                'conversation_length': len(data.get('conversation_parts', [])),
                'has_attachments': data.get('custom_attributes', {}).get('Has attachments', False),
                'language': data.get('custom_attributes', {}).get('Language', 'Unknown'),
                'ticket_type': data.get('custom_attributes', {}).get('Type', 'Unknown'),
                'ticket_status': data.get('custom_attributes', {}).get('Status', 'Unknown'),
                'topic': data.get('custom_attributes', {}).get('Topic', 'Unknown'),
                'ai_agent_used': data.get('custom_attributes', {}).get('Fin AI Agent: Preview', False)
            }

            data['fetched_at'] = datetime.now(timezone.utc).isoformat()

            return data

        except Exception as e:
            return {
                'id': getattr(conversation, 'id', 'unknown'),
                'error': f"Failed to extract data: {str(e)}",
                'fetched_at': datetime.now(timezone.utc).isoformat()
            }


@click.command()
@click.option('--start-date', type=str, help='Start date (YYYY-MM-DD format).')
@click.option('--end-date', type=str, help='End date (YYYY-MM-DD format).')
@click.option('--days', type=int, default=7, help='Number of days to fetch from today (backwards). Default: 7 days.')
@click.option('--output-file', type=str, default='data/intercom/conversations.jsonl', help='Output JSONL file path.')
@click.option('--per-page', type=int, default=50, help='Number of conversations per API call. Default: 50')
@click.option('--access-token', type=str, envvar='INTERCOM_ACCESS_TOKEN', help='Intercom access token (or set INTERCOM_ACCESS_TOKEN env var)')
@click.option('--filter-state', type=click.Choice(['open', 'closed', 'all']), default='all', help='Filter conversations by state. Default: all')
@click.option('--filter-type', type=str, help='Filter by ticket type (e.g., Bug, User Guide, etc.)')
@click.option('--include-conversation-parts', is_flag=True, default=True, help='Include conversation messages (default: True)')
def main(start_date: str, end_date: str, days: int, output_file: str, per_page: int, access_token: str, filter_state: str, filter_type: str, include_conversation_parts: bool):
    """
    Fetch Intercom conversations and save as JSONL file.

    Examples:
        python fetch_intercom.py --start-date 2025-01-01 --end-date 2025-01-31
        python fetch_intercom.py --days 7
        python fetch_intercom.py --days 15 --output-file ./conversations.jsonl
    """
    if not access_token:
        click.echo("Error: INTERCOM_ACCESS_TOKEN environment variable not set or --access-token not provided", err=True)
        click.echo("Set your token with: export INTERCOM_ACCESS_TOKEN=your_token_here")
        sys.exit(1)

    now = datetime.now(timezone.utc)

    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        except ValueError:
            click.echo("Error: Invalid date format. Use YYYY-MM-DD", err=True)
            sys.exit(1)
    elif start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = now
        except ValueError:
            click.echo("Error: Invalid date format. Use YYYY-MM-DD", err=True)
            sys.exit(1)
    else:
        start_dt = now - timedelta(days=days)
        end_dt = now

    fetcher = IntercomConversationFetcher(
        access_token=access_token,
        output_file=output_file,
        filter_state=filter_state,
        filter_type=filter_type,
        include_parts=include_conversation_parts
    )

    filters = []
    if filter_state != 'all':
        filters.append(f"state={filter_state}")
    if filter_type:
        filters.append(f"type={filter_type}")
    if not include_conversation_parts:
        filters.append("exclude conversation parts")

    if filters:
        click.echo(f"Filters applied: {', '.join(filters)}")

    fetcher.fetch_conversations_by_date_range(start_dt, end_dt, per_page)

    click.echo(f"\nCompleted! Fetched {fetcher.conversations_fetched} conversations to {output_file}")


if __name__ == '__main__':
    main()
