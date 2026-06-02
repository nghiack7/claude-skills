---
name: intercom
description: Use when the user asks to "export Intercom conversations", "analyze support tickets", "query Intercom data", or mentions Intercom, ClickHouse conversation export, or customer support analytics. Provides patterns for exporting conversations from ClickHouse (Airbyte sync) or directly from the Intercom API.
---

# Intercom Conversation Export

Export Intercom conversations and messages from a ClickHouse analytics database (synced via Airbyte) to JSON files, or fetch directly from the Intercom API.

## Data Source

Data is synced from Intercom to ClickHouse via Airbyte. Tables available:

- `intercom_conversations` - Conversation metadata
- `intercom_conversation_parts` - Individual messages
- `intercom_contacts` - Customer contacts

## Export Script (ClickHouse-backed)

Use the Python script at `.claude/skills/intercom/export_intercom.py`:

```bash
# Export last 7 days (default)
python3 .claude/skills/intercom/export_intercom.py

# Export specific date range
python3 .claude/skills/intercom/export_intercom.py --start-date 2025-11-01 --end-date 2025-11-30

# Export only customer-initiated conversations
python3 .claude/skills/intercom/export_intercom.py --source customer_initiated

# Export only open tickets
python3 .claude/skills/intercom/export_intercom.py --state open

# Export single conversation by ID
python3 .claude/skills/intercom/export_intercom.py --conversation-id <CONVERSATION_ID>

# Custom output directory
python3 .claude/skills/intercom/export_intercom.py --output-dir ./my-export

# Limit results
python3 .claude/skills/intercom/export_intercom.py --days 30 --limit 100
```

## Output Files

The script creates a timestamped directory with:

```
data/customer-service/intercom/export-YYYY-MM-DD/
├── conversations.json      # All conversations with metadata
├── messages.json           # All conversation parts/messages
├── summary.json            # Statistics and summary
└── full_threads.json       # Conversations with messages merged
```

## Quick ClickHouse Queries

```bash
source <your-secrets-file>
```

**Get recent conversations:**

```bash
curl -s -X POST "$CLICKHOUSE_URL" \
  -H "X-ClickHouse-User: $CLICKHOUSE_USER" \
  -H "X-ClickHouse-Key: $CLICKHOUSE_PASSWORD" \
  -d "SELECT
    id, title, state,
    fromUnixTimestamp(created_at) as created_at,
    JSONExtractString(source, 'delivered_as') as source_type,
    ai_agent_participated
FROM default.intercom_conversations
WHERE created_at >= toUnixTimestamp(now() - INTERVAL 7 DAY)
ORDER BY created_at DESC
LIMIT 50
FORMAT JSON"
```

**Get messages for a conversation:**

```bash
curl -s -X POST "$CLICKHOUSE_URL" \
  -H "X-ClickHouse-User: $CLICKHOUSE_USER" \
  -H "X-ClickHouse-Key: $CLICKHOUSE_PASSWORD" \
  -d "SELECT
    conversation_id, part_type, body,
    JSONExtractString(author, 'type') as author_type,
    JSONExtractString(author, 'name') as author_name,
    fromUnixTimestamp(created_at) as created_at
FROM default.intercom_conversation_parts
WHERE conversation_id = '<CONVERSATION_ID>'
ORDER BY created_at ASC
FORMAT JSON"
```

**Daily conversation stats:**

```bash
curl -s -X POST "$CLICKHOUSE_URL" \
  -H "X-ClickHouse-User: $CLICKHOUSE_USER" \
  -H "X-ClickHouse-Key: $CLICKHOUSE_PASSWORD" \
  -d "SELECT
    toDate(fromUnixTimestamp(created_at)) as date,
    COUNT(*) as total,
    SUM(CASE WHEN JSONExtractString(source, 'delivered_as') = 'customer_initiated' THEN 1 ELSE 0 END) as customer_initiated,
    SUM(CASE WHEN ai_agent_participated = true THEN 1 ELSE 0 END) as ai_handled
FROM default.intercom_conversations
WHERE created_at >= toUnixTimestamp(now() - INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC
FORMAT JSON"
```

## Key Fields

### intercom_conversations

| Field                 | Type   | Description                      |
| --------------------- | ------ | -------------------------------- |
| id                    | String | Conversation ID                  |
| title                 | String | Conversation title               |
| state                 | String | open, closed, snoozed            |
| source                | JSON   | Source info (delivered_as, type) |
| created_at            | Int64  | Unix timestamp                   |
| ai_agent_participated | Bool   | Fin AI involvement               |
| assignee              | JSON   | Assigned agent                   |
| contacts              | JSON   | Customer info                    |
| tags                  | JSON   | Applied tags                     |
| conversation_rating   | JSON   | Customer rating                  |

### intercom_conversation_parts

| Field           | Type   | Description                     |
| --------------- | ------ | ------------------------------- |
| conversation_id | Int64  | Parent conversation             |
| part_type       | String | comment, note, assignment, etc. |
| body            | String | HTML message content            |
| author          | JSON   | Author info (type, name, id)    |
| created_at      | Int64  | Unix timestamp                  |

## Source Types (delivered_as)

- `customer_initiated` - Customer started conversation
- `admin_initiated` - Agent/admin started
- `automated` - Bot/workflow triggered

## Author Types

- `user` - Customer
- `admin` - Support agent
- `bot` - Fin AI or automation

## Related Skills

For data source:

- `/clickhouse` - Direct ClickHouse database queries
- `/secret` - Intercom API credentials

For related data:

- `/amplitude` - Product analytics events
- `/bigquery` - Alternative data warehouse

For customer support analytics:

- `/grafana` - Intercom dashboards
- `/chart-generator` - Create charts from conversation data
