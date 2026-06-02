---
name: coroot
description: This skill should be used when the user asks to "check cluster health", "view application status", "check SLO metrics", "investigate service latency", "debug K8s app", or mentions Coroot, service availability, or incidents.
---

## Related Skills

- **kubectl** - K8s cluster operations
- **grafana** - Dashboard visualization
- **otel** - Distributed tracing
- **incident-response** - Incident handling workflow

# Coroot Observability Platform

Query Coroot for cluster health, application status, incidents, and SLO metrics.

## Activation

Use when:

- User mentions "coroot", "cluster health", "application incidents"
- Debugging Kubernetes application issues
- Checking SLO burn rates or availability metrics
- Investigating service latency or errors

## Configuration

```bash
# Coroot instance
COROOT_URL="https://your-internal-host.example.com"
COROOT_PROJECT_ID="<PROJECT_ID>"

# Credentials - load from your secrets manager
```

**Network Requirement:** VPN or internal network access may be required depending on your deployment.

## Authentication

Coroot uses session-based auth with HttpOnly cookies (7-day TTL).

**IMPORTANT:**

1. Always load credentials from secrets manager, never hardcode
2. Use long-form curl flags (`--silent --insecure --cookie`) instead of short flags

### Login Flow

```bash
# Step 1: Read credentials from secrets manager

# Step 2: Login to get session cookie
curl --silent --insecure -X POST "https://your-internal-host.example.com/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"<from-secrets>","password":"<from-secrets>"}' \
  -c /tmp/coroot-cookies.txt

# Step 3: Use cookie for subsequent requests
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/..."
```

**Important:**

- Use `email` field, NOT `username`
- Cookie name is `coroot_session`
- Session expires after 7 days

## API Endpoints

### Endpoints that return JSON

| Endpoint                          | Description                      |
| --------------------------------- | -------------------------------- |
| `GET /api/user`                   | Current user info + project list |
| `GET /api/project/{id}/status`    | Cluster health, nodes, apps      |
| `GET /api/project/{id}/incidents` | All incidents with SLO data      |

### Endpoints that return HTML (not REST)

App-specific routes like `/api/project/{id}/app/{appId}/overview` return HTML because Coroot is a Vue.js SPA. For app details, use the incidents endpoint and filter by `application_id`.

## Common Queries

**IMPORTANT:** Always use single-line commands with `2>&1` before pipe to avoid shell parsing errors.

### Get cluster status

```bash
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/project/<PROJECT_ID>/status" 2>&1 | jq '.context.status'
```

Response includes:

- `status`: ok/warning/critical
- `node_agent.nodes`: number of monitored nodes
- `kube_state_metrics.applications`: number of apps

### Get all incidents

```bash
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/project/<PROJECT_ID>/incidents" 2>&1 | jq '.data'
```

### Filter incidents by application

```bash
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/project/<PROJECT_ID>/incidents" 2>&1 | jq '.data[] | select(.application_id | contains("my-app"))'
```

### Get active (unresolved) incidents

```bash
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/project/<PROJECT_ID>/incidents" 2>&1 | jq '[.data[] | select(.resolved_at == null)]'
```

### Get application list

```bash
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/project/<PROJECT_ID>/status" 2>&1 | jq '.context.search.applications[]'
```

## Data Structures

### Application ID Format

```
{project}:{namespace}:{kind}:{name}
```

Examples:

- `<PROJECT_ID>:starrocks:StatefulSet:starrocks-shared-data-cn`
- `<PROJECT_ID>:my-app:Deployment:my-service`
- `external:external:ExternalService:api.stripe.com`

### Incident Structure

```json
{
  "application_id": "<PROJECT_ID>:namespace:Kind:name",
  "key": "unique-id",
  "opened_at": 1768460198000,
  "resolved_at": 1768462358000,
  "severity": "critical",
  "short_description": "High latency and errors",
  "impact": 8.97,
  "duration": 2160000,
  "details": {
    "availability_burn_rates": [...],
    "latency_burn_rates": [...],
    "availability_impact": {"percentage": 0.08},
    "latency_impact": {"percentage": 8.97}
  }
}
```

### SLO Burn Rate Thresholds

- **1h window**: threshold 14.4x (fast burn)
- **6h window**: threshold 6x (slow burn)

Severity becomes `critical` when burn rate exceeds threshold.

## Application Status Values

| Status     | Meaning              |
| ---------- | -------------------- |
| `ok`       | Healthy, within SLO  |
| `warning`  | Degraded performance |
| `critical` | SLO violation        |
| `unknown`  | No SLO configured    |

## Troubleshooting

### Shell parsing error with curl commands

**Error:**

```
(eval):1: permission denied:
curl: option : blank argument where content is expected
```

**Solution:** Always use single-line commands with `2>&1`:

```bash
# Correct - single line with 2>&1
curl --silent --insecure --cookie /tmp/coroot-cookies.txt "https://your-internal-host.example.com/api/..." 2>&1 | jq '.data'
```

### Connection timeout

Check VPN / network access - Coroot may be internal only.

### HTTP 401 Unauthorized

Session expired - re-login using credentials from secrets manager.

### HTTP 400 Bad Request on login

Using wrong field name - must be `email`, not `username`.

### App endpoint returns HTML

App-specific routes are SPA routes, not REST. Use incidents endpoint instead.

## Related Skills

For infrastructure access:

- `/kubectl` - K8s access for troubleshooting

For monitoring ecosystem:

- `/grafana` - Coroot dashboards
- `/otel` - OpenTelemetry traces integration
- `/monitoring-observability` - Monitoring best practices
- `/incident-response` - Incident troubleshooting

For related monitoring:

- `/dagster` - Pipeline monitoring in Coroot
- `/starrocks` - Application monitoring
