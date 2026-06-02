---
name: amplitude
description: Use when the user asks to "query Amplitude", "export events", "analyze user activity", "download cohort", "get user profile", "check product analytics", or mentions Amplitude, user behavior, event analytics, cohorts, or engagement metrics. Provides API patterns for export, segmentation, cohorts, taxonomy, and user profiles.
---

## Related Skills

- **chart-generator** - Visualize Amplitude analytics
- **bigquery** - Data warehouse for detailed analysis
- **intercom** - Customer support analytics complement

# Amplitude Analytics API

Access Amplitude product analytics data via the Analytics APIs.

## Connection

**Project:** `<AMPLITUDE_PROJECT_ID>`
**Dashboard:** https://app.amplitude.com/analytics/

**Credentials Required:**

- `API_KEY` - Project API key
- `SECRET_KEY` - Project secret key

**Secrets Location:** Store in your secrets manager or `.env` file

## Authentication

Most APIs use **Basic Auth** with base64-encoded `{api_key}:{secret_key}`:

```python
import base64
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AMPLITUDE_API_KEY')
secret_key = os.getenv('AMPLITUDE_SECRET_KEY')

# Basic auth header
credentials = base64.b64encode(f"{api_key}:{secret_key}".encode()).decode()
headers = {'Authorization': f'Basic {credentials}'}
```

**User Profile API** uses different auth:

```python
headers = {'Authorization': f'Api-Key {secret_key}'}
```

---

## API Endpoints Overview

| API                        | Endpoint                    | Purpose                                    |
| -------------------------- | --------------------------- | ------------------------------------------ |
| **Export API**             | `/api/2/export`             | Export raw event data                      |
| **Dashboard REST API**     | `/api/2/...`                | User activity, event segmentation, funnels |
| **Behavioral Cohorts API** | `/api/3/cohorts`            | List, download, upload cohorts             |
| **Taxonomy API**           | `/api/2/taxonomy/...`       | List event types, user properties          |
| **User Profile API**       | `profile-api.amplitude.com` | Get user profiles, recommendations         |
| **Chart Annotations API**  | `/api/2/annotations`        | Add/get chart annotations                  |

**Base URLs:**

- Standard: `https://amplitude.com`
- EU: `https://analytics.eu.amplitude.com`
- Profile API: `https://profile-api.amplitude.com`

---

## 1. Export API

Export raw event data for a time range.

### Endpoint

```
GET https://amplitude.com/api/2/export?start={start}&end={end}
```

### Parameters

| Parameter | Required | Format      | Description                      |
| --------- | -------- | ----------- | -------------------------------- |
| `start`   | Yes      | YYYYMMDDTHH | Start hour (e.g., `20241201T00`) |
| `end`     | Yes      | YYYYMMDDTHH | End hour (e.g., `20241201T23`)   |

### Constraints

- Max period: 365 days
- Max size: 4GB per request
- Data available: 2 hours after server receipt

### Python Example

```python
import requests
import base64
import os
import gzip
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AMPLITUDE_API_KEY')
secret_key = os.getenv('AMPLITUDE_SECRET_KEY')

# Export last 24 hours
response = requests.get(
    'https://amplitude.com/api/2/export',
    params={'start': '20241201T00', 'end': '20241201T23'},
    auth=(api_key, secret_key)
)

if response.status_code == 200:
    # Response is gzipped JSON lines
    content = gzip.decompress(response.content)
    for line in content.decode().strip().split('\n'):
        event = json.loads(line)
        print(f"{event['event_type']}: {event['user_id']}")
```

### Response Schema (per event)

| Field              | Type   | Description         |
| ------------------ | ------ | ------------------- |
| `event_type`       | String | Event name          |
| `user_id`          | String | User identifier     |
| `device_id`        | String | Device identifier   |
| `event_time`       | String | Event timestamp     |
| `event_properties` | Object | Event-specific data |
| `user_properties`  | Object | User attributes     |
| `country`          | String | User country        |
| `city`             | String | User city           |
| `platform`         | String | web/ios/android     |
| `os_name`          | String | Operating system    |
| `session_id`       | Long   | Session identifier  |

---

## 2. Dashboard REST API

### Rate Limits

- 5 concurrent requests
- 360 queries/hour for user activity/search
- Cost-based model for other endpoints

### 2.1 User Activity

Get event history for a specific user.

```
GET https://amplitude.com/api/2/useractivity?user={amplitude_id}
```

| Parameter   | Required | Description                      |
| ----------- | -------- | -------------------------------- |
| `user`      | Yes      | Amplitude ID                     |
| `offset`    | No       | Starting point (0-indexed)       |
| `limit`     | No       | Events to return (max 1000)      |
| `direction` | No       | "earliest" or "latest" (default) |

```python
response = requests.get(
    'https://amplitude.com/api/2/useractivity',
    params={'user': '12345678', 'limit': 100},
    auth=(api_key, secret_key)
)

data = response.json()
for event in data.get('events', []):
    print(f"{event['event_time']}: {event['event_type']}")
```

### 2.2 User Search

Search for users by ID.

```
GET https://amplitude.com/api/2/usersearch?user={search_term}
```

```python
response = requests.get(
    'https://amplitude.com/api/2/usersearch',
    params={'user': 'user@example.com'},
    auth=(api_key, secret_key)
)

users = response.json().get('matches', [])
for user in users:
    print(f"Amplitude ID: {user['amplitude_id']}, User ID: {user['user_id']}")
```

### 2.3 Event Segmentation

Get metrics for events with segmentation.

```
GET https://amplitude.com/api/2/events/segmentation
```

| Parameter | Required | Description                               |
| --------- | -------- | ----------------------------------------- |
| `e`       | Yes      | Event definition (JSON)                   |
| `start`   | Yes      | Start date (YYYYMMDD)                     |
| `end`     | Yes      | End date (YYYYMMDD)                       |
| `m`       | No       | Metric: uniques, totals, pct_dau, average |
| `g`       | No       | Group by property                         |
| `s`       | No       | Segment definition                        |

```python
import json
import urllib.parse

event = {"event_type": "page_view"}
event_encoded = urllib.parse.quote(json.dumps(event))

response = requests.get(
    'https://amplitude.com/api/2/events/segmentation',
    params={
        'e': json.dumps(event),
        'start': '20241101',
        'end': '20241130',
        'm': 'uniques',
        'g': 'country'
    },
    auth=(api_key, secret_key)
)

data = response.json()
print(f"Series: {data.get('data', {}).get('series', [])}")
```

### 2.4 Additional Endpoints

| Endpoint                  | Purpose                     |
| ------------------------- | --------------------------- |
| `/api/2/users`            | Active/new user counts      |
| `/api/2/sessions/length`  | Session length distribution |
| `/api/2/sessions/average` | Average session length      |
| `/api/2/retention`        | Retention analysis          |
| `/api/2/funnels`          | Funnel analysis             |
| `/api/2/revenue/ltv`      | Revenue LTV metrics         |
| `/api/2/realtime`         | Real-time active users      |
| `/api/2/composition`      | User composition            |

---

## 3. Behavioral Cohorts API

### 3.1 List Cohorts

```
GET https://amplitude.com/api/3/cohorts
```

```python
response = requests.get(
    'https://amplitude.com/api/3/cohorts',
    params={'includeSyncInfo': 'true'},
    auth=(api_key, secret_key)
)

cohorts = response.json().get('cohorts', [])
for cohort in cohorts:
    print(f"{cohort['id']}: {cohort['name']} ({cohort['size']} users)")
```

### 3.2 Download Cohort (3-step process)

**Step 1: Request cohort**

```python
cohort_id = 'abc123'
response = requests.get(
    f'https://amplitude.com/api/5/cohorts/request/{cohort_id}',
    params={'props': 1},  # Include user properties
    auth=(api_key, secret_key)
)
request_id = response.json()['request_id']
```

**Step 2: Poll status**

```python
import time

while True:
    response = requests.get(
        f'https://amplitude.com/api/5/cohorts/request-status/{request_id}',
        auth=(api_key, secret_key)
    )
    status = response.json()['async_status']
    if status == 'JOB COMPLETED':
        break
    time.sleep(5)
```

**Step 3: Download file**

```python
response = requests.get(
    f'https://amplitude.com/api/5/cohorts/request/{request_id}/file',
    auth=(api_key, secret_key),
    allow_redirects=True
)
# Response contains user IDs and properties
```

### 3.3 Upload Cohort

```python
cohort_data = {
    'name': 'High Value Users',
    'app_id': '<AMPLITUDE_PROJECT_ID>',
    'id_type': 'BY_USER_ID',
    'ids': ['user1', 'user2', 'user3'],
    'owner': 'analyst@company.com',
    'published': True
}

response = requests.post(
    'https://amplitude.com/api/3/cohorts/upload',
    json=cohort_data,
    auth=(api_key, secret_key)
)
```

### Limits

- 500 download requests/month (Growth/Enterprise)
- Max cohort size: 2 million users
- 100,000 IDs per upload request

---

## 4. Taxonomy API

### 4.1 List Event Types

```python
response = requests.get(
    'https://amplitude.com/api/2/taxonomy/event',
    auth=(api_key, secret_key)
)

events = response.json().get('data', [])
for event in events:
    print(f"{event['event_type']}: {event.get('description', 'No description')}")
```

### 4.2 List User Properties

```python
response = requests.get(
    'https://amplitude.com/api/2/taxonomy/user-property',
    auth=(api_key, secret_key)
)

properties = response.json().get('data', [])
for prop in properties:
    print(f"{prop['user_property']}: {prop.get('type', 'unknown')}")
```

---

## 5. User Profile API

Get user profiles with properties, cohorts, and recommendations.

**Note:** Uses different auth header: `Api-Key {secret_key}`

```
GET https://profile-api.amplitude.com/v1/userprofile
```

| Parameter        | Description                        |
| ---------------- | ---------------------------------- |
| `user_id`        | User ID (required if no device_id) |
| `device_id`      | Device ID (required if no user_id) |
| `get_amp_props`  | Include user properties            |
| `get_cohort_ids` | Include cohort memberships         |
| `get_recs`       | Include recommendations            |

```python
response = requests.get(
    'https://profile-api.amplitude.com/v1/userprofile',
    params={
        'user_id': 'user@example.com',
        'get_amp_props': 'true',
        'get_cohort_ids': 'true'
    },
    headers={'Authorization': f'Api-Key {secret_key}'}
)

profile = response.json()
print(f"User Properties: {profile.get('userData', {}).get('amp_props', {})}")
print(f"Cohorts: {profile.get('userData', {}).get('cohort_ids', [])}")
```

**Rate Limit:** 600 requests/minute per org

---

## 6. Chart Annotations API

### List Annotations

```python
response = requests.get(
    'https://amplitude.com/api/2/annotations',
    auth=(api_key, secret_key)
)

annotations = response.json().get('data', [])
for ann in annotations:
    print(f"{ann['date']}: {ann['label']}")
```

### Create Annotation

```python
annotation = {
    'app_id': '<AMPLITUDE_PROJECT_ID>',
    'date': '2024-12-01',
    'label': 'New Feature Launch',
    'details': 'Released feature v2.0'
}

response = requests.post(
    'https://amplitude.com/api/2/annotations',
    json=annotation,
    auth=(api_key, secret_key)
)
```

---

## Common Query Scripts

### Export Events to JSON

```python
import requests
import gzip
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AMPLITUDE_API_KEY')
secret_key = os.getenv('AMPLITUDE_SECRET_KEY')

def export_events(start_date, end_date, output_file):
    """Export Amplitude events to JSON file"""
    response = requests.get(
        'https://amplitude.com/api/2/export',
        params={'start': start_date, 'end': end_date},
        auth=(api_key, secret_key)
    )

    if response.status_code == 200:
        content = gzip.decompress(response.content)
        events = [json.loads(line) for line in content.decode().strip().split('\n')]

        with open(output_file, 'w') as f:
            json.dump(events, f, indent=2)

        print(f"Exported {len(events)} events to {output_file}")
        return events
    else:
        print(f"Error: {response.status_code}")
        return []

# Export last 7 days
export_events('20241125T00', '20241201T23', 'amplitude_events.json')
```

### Get Event Counts by Type

```python
def get_event_counts(start_date, end_date):
    """Get event counts grouped by event type"""
    # First get all event types
    response = requests.get(
        'https://amplitude.com/api/2/taxonomy/event',
        auth=(api_key, secret_key)
    )
    event_types = [e['event_type'] for e in response.json().get('data', [])]

    # Then get counts for top events
    for event_type in event_types[:10]:
        event_def = {"event_type": event_type}
        response = requests.get(
            'https://amplitude.com/api/2/events/segmentation',
            params={
                'e': json.dumps(event_def),
                'start': start_date,
                'end': end_date,
                'm': 'totals'
            },
            auth=(api_key, secret_key)
        )
        data = response.json().get('data', {})
        total = sum(data.get('series', [[0]])[0])
        print(f"{event_type}: {total}")

get_event_counts('20241101', '20241130')
```

### Download All Cohorts

```python
def download_all_cohorts(output_dir='cohorts'):
    """Download all cohort member lists"""
    import os
    import time

    os.makedirs(output_dir, exist_ok=True)

    # List cohorts
    response = requests.get(
        'https://amplitude.com/api/3/cohorts',
        auth=(api_key, secret_key)
    )
    cohorts = response.json().get('cohorts', [])

    for cohort in cohorts:
        cohort_id = cohort['id']
        cohort_name = cohort['name'].replace('/', '_')

        # Request download
        response = requests.get(
            f'https://amplitude.com/api/5/cohorts/request/{cohort_id}',
            auth=(api_key, secret_key)
        )

        if response.status_code != 202:
            print(f"Failed to request {cohort_name}")
            continue

        request_id = response.json()['request_id']

        # Poll until ready
        while True:
            response = requests.get(
                f'https://amplitude.com/api/5/cohorts/request-status/{request_id}',
                auth=(api_key, secret_key)
            )
            if response.json()['async_status'] == 'JOB COMPLETED':
                break
            time.sleep(2)

        # Download
        response = requests.get(
            f'https://amplitude.com/api/5/cohorts/request/{request_id}/file',
            auth=(api_key, secret_key),
            allow_redirects=True
        )

        with open(f'{output_dir}/{cohort_name}.json', 'w') as f:
            f.write(response.text)

        print(f"Downloaded: {cohort_name} ({cohort['size']} users)")

download_all_cohorts()
```

---

## Tips

1. **Rate Limits:** 5 concurrent requests max, 360/hour for user endpoints
2. **URL Encoding:** Encode event names with spaces (e.g., `Play%20Song`)
3. **Custom Properties:** Prefix with `gp:` (e.g., `gp:utm_campaign`)
4. **Export Size:** Max 4GB per request, max 365 days
5. **Cohort Downloads:** 500/month limit on Growth/Enterprise
6. **Read-Only:** These APIs are for analysis - do not modify production data
7. **EU Region:** Use `analytics.eu.amplitude.com` for EU data residency

---

## CLI Tools

Pre-built Python scripts in this skill folder:

| Script             | Purpose                     | Example                                             |
| ------------------ | --------------------------- | --------------------------------------------------- |
| `export_events.py` | Export raw events to JSON   | `python export_events.py --days 7 -o events.json`   |
| `event_volumes.py` | Get event counts/volumes    | `python event_volumes.py --days 30 --top 20`        |
| `user_activity.py` | Search users & get activity | `python user_activity.py --search "user@email.com"` |
| `cohorts.py`       | List & download cohorts     | `python cohorts.py --list`                          |
| `taxonomy.py`      | List events & properties    | `python taxonomy.py --events`                       |

### Quick Examples

```bash
# Export last 7 days of events
python .claude/skills/amplitude/export_events.py --days 7 -o events.json

# Get top 20 events by volume
python .claude/skills/amplitude/event_volumes.py --days 30 --top 20

# Search for a user and get their activity
python .claude/skills/amplitude/user_activity.py --search "user@example.com"

# List all cohorts
python .claude/skills/amplitude/cohorts.py --list

# List event types grouped by category
python .claude/skills/amplitude/taxonomy.py --events
```

---

## Related Skills

For alternative data sources:

- `/bigquery` - Amplitude events also exported to BigQuery (`<GCP_PROJECT_ID>.amplitude.EVENTS_<AMPLITUDE_PROJECT_ID>`)
- `/clickhouse` - Developer analytics
- `/intercom` - Customer support data

For visualization:

- `/grafana` - Amplitude dashboards
- `/chart-generator` - Create charts from Amplitude data

For authentication:

- `/secret` - Amplitude API credentials
