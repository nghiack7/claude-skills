---
name: grafana
description: "This skill should be used when the user asks to \"create dashboard\", \"check Grafana alerts\", \"query Grafana API\", \"create service map\", \"draw data flow diagram\", \"build state diagram\", \"visualize architecture\", or mentions Grafana dashboards, alerts, ECharts panels, or diagram visualization."
---

## Related Skills

- **otel** - Distributed tracing data source
- **coroot** - Alternative observability platform
- **kubectl** - Port-forward to access Grafana API
- **monitoring-observability** - Dashboard design principles

# Grafana API Access

When Google OAuth is the primary auth method, basic auth may be **blocked from external network** even though `[auth.basic] enabled = true`.

**To access the API via port-forward:**

```bash
kubectl --context <KUBE_CONTEXT> port-forward -n monitoring svc/grafana-operator-grafana-service 3333:3000
```

Then use basic auth against `localhost:3333`:

```bash
curl -s -u "admin:$GRAFANA_PASSWORD" \
  "http://localhost:3333/api/dashboards/uid/<uid>"
```

**Never try to auth directly against `your-grafana.example.com`** when OAuth is the primary auth - it will return 401 for basic auth.

**Grafana pod details (operator-managed):**
- Deployment: `grafana-operator-grafana-deployment` in `monitoring` namespace
- Config: `--config=/etc/grafana/grafana.ini`
- `grafana-cli` correct flags: `--homepath /opt/bitnami/grafana --config /etc/grafana/grafana.ini`

# Grafana Dashboard Management

## Folder Structure

| Folder | Purpose |
|--------|---------|
| **General** | System-wide overview dashboards |
| **AWS** | AWS services (CloudWatch, EC2, RDS, Lambda, EBS) |
| **Auth & User Alerts** | Authentication and user monitoring |
| **Business** | Revenue, transactions, business health |
| **Customer Support** | Support metrics |
| **Engineering** | GitLab, Jira, pipelines, team activity |
| **Temporal** | Temporal workflows |
| **StarRocks Alerts** | StarRocks database alerts |
| **Archive (zz_)** | Test/deprecated dashboards |

## Plugins

- **volkovlabs-echarts-panel** (v7.x, "Business Charts") - Custom ECharts visualizations.

**Critical:** Access data via `context.panel.data.series` (NOT `data.series`). Using `data` directly causes `data is not defined` runtime error.

**Data access pattern:**
```js
const series = context.panel.data.series;
if (!series.length) return { title: { text: 'No data' } };
const timeField = series[0].fields.find(f => f.name === 'time_sec');
const valueField = series[0].fields.find(f => f.name === 'my_value');
const times = timeField.values.map(t => new Date(t * 1000));
```

**Query format:** Use `format: "table"` (not `time_series`). Return raw seconds in time column, convert to `Date` in JS.

**Common EChart enhancements:**
- `visualMap` with `pieces` for color-coded thresholds (green/yellow/red zones)
- `markLine` for SLA/target reference lines
- Gradient `areaStyle` with `colorStops` for layered percentile charts (P50/P95/P99)

**Context object also provides:** `context.grafana.replaceVariables()`, `context.panel.data.request`, `context.grafana.eventBus`

### ECharts Graph Diagrams (Service Maps, Data Flows, State Diagrams)

All diagram types use ECharts `graph` series with `layout: 'none'` and manual `x/y` positioning. Never use force-directed layouts in dashboard panels.

```js
series: [{
    type: 'graph', layout: 'none', coordinateSystem: null,
    data: nodes, links: edges, roam: true,
    emphasis: { focus: 'adjacency' }
}]
```

**Diagram types:**

| Type | Layout | Use Case |
|------|--------|----------|
| Service Map | Left-to-right by tier | Traffic between services, error rates, latency |
| Data Flow | Multi-row columns (TRIGGER/ORCHESTRATOR/WORKERS/DATA STORES) | Request pipelines through Lambda, SQS, SNS |
| State Diagram | Top-to-bottom | Entity lifecycle, order states, sync status |
| Topology | Layered or zone-based | Infrastructure architecture, network topology |

**Standard helpers:**

```js
function nodeStyle(borderColor, bgAlpha) {
    return { color: 'rgba(255,255,255,' + (bgAlpha || 0.03) + ')',
             borderColor, borderWidth: 2, shadowBlur: 8,
             shadowColor: borderColor + '33' };
}
function healthColor(errPct) {
    if (!errPct) return '#52c41a';
    if (errPct >= 5) return '#f5222d';
    if (errPct >= 1) return '#fa8c16';
    if (errPct > 0) return '#fadb14';
    return '#52c41a';
}
function fmt(n) {
    if (!n) return '0';
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
    return String(n);
}
```

**Color palette:**

| Component | Hex |
|-----------|-----|
| HTTP/Users | `#177ddc` |
| Lambda/OK | `#52c41a` |
| API Gateway | `#fa8c16` |
| SQS/Queue | `#13c2c2` |
| SNS/Events | `#eb2f96` |
| MongoDB/DB | `#b37feb` |
| Error | `#f5222d` |
| Warning | `#fadb14` |

**Edge patterns:**

| Pattern | lineStyle |
|---------|-----------|
| Primary flow | `{ width: 4, color: '#52c41a' }` |
| Async | `{ width: 3, color: '#fa8c16' }` |
| Queue-based | `{ width: 3, color: '#13c2c2' }` |
| Rare/optional | `{ width: 1, color: '#555', type: 'dashed' }` |
| Error path | `{ width: 2, color: '#f5222d', type: 'dotted' }` |

**Pitfalls:** Always use `layout: 'none'` (force layout is unstable). Use `curveness` on parallel edges to prevent overlap. Set panel height >= 400px and `roam: true`.

For complete working examples with full ECharts code, see **`references/echart-diagrams.md`**.

## Dashboard Naming Convention

**Format:** `[Service] - [What]`

**Rules:**
1. No redundant words: "Dashboard", "Monitoring", "Analytics" (context is Grafana)
2. Folder name not repeated in title (folder is already context)
3. Hyphen `-` separates service and description
4. Keep it short and scannable

**Examples:**
| ❌ Bad | ✅ Good |
|--------|---------|
| Business Health Dashboard | Business - Health |
| Engineering Analytics - GitLab Insights | Engineering - GitLab |
| Lambda Monitoring - Enhanced | Lambda - Overview |
| Customer Support Story: Intercom Journey | Support - Intercom Flow |

# Grafana Dashboard Debug

## Problem

Time series panels empty, but stat panels show data exists.

## Root Causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Single time bucket | Time conversion wrong | Check column type |
| Timestamp ~1970 or year 50000+ | Wrong unit (sec/ms/ns) | Verify arithmetic |
| No visible lines | MySQL DATETIME math | Use `UNIX_TIMESTAMP()` |

## Debug via Grafana API

```bash
curl -X POST "http://localhost:3333/api/ds/query" \
  -u "admin:$GRAFANA_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{"queries": [{"datasource": {"uid": "..."}, "format": "time_series", "rawQuery": true, "rawSql": "..."}]}'
```

Check response: `.results.A.frames[0].data.values[0]` = timestamps array

## Check Column Type First

```sql
SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'db' AND TABLE_NAME = 'table' AND COLUMN_NAME = 'Timestamp'
```

## Time Conversion Formulas

| Column Type | To Grafana Milliseconds |
|-------------|-------------------------|
| `DATETIME` | `FLOOR(UNIX_TIMESTAMP(col) / 60) * 60 * 1000` |
| `BIGINT` (seconds) | `FLOOR(col / 60) * 60 * 1000` |
| `BIGINT` (milliseconds) | `FLOOR(col / 60000) * 60000` |
| `BIGINT` (nanoseconds) | `FLOOR(col / 60000000000) * 60000` |

## Verify Timestamps

```sql
-- Should return current date range
SELECT
  FLOOR(UNIX_TIMESTAMP(Timestamp) / 60) * 60 * 1000 as time,
  FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(Timestamp) / 60) * 60) as readable
FROM table
LIMIT 1
```

## Push Dashboard Update

**Must use port-forward** (see "Grafana API Access" section above).

```bash
# 1. Start port-forward
kubectl --context <KUBE_CONTEXT> port-forward -n monitoring svc/grafana-operator-grafana-service 3333:3000 &
sleep 3

# 2. Fetch existing dashboard
curl -s -u "admin:$GRAFANA_PASSWORD" "http://localhost:3333/api/dashboards/uid/<uid>" > dashboard.json

# 3. Modify and push
jq -n '{"dashboard": input, "overwrite": true, "message": "description"}' dashboard.json |
  curl -X POST "http://localhost:3333/api/dashboards/db" \
    -u "admin:$GRAFANA_PASSWORD" \
    -H "Content-Type: application/json" \
    --data @-

# 4. Cleanup
lsof -ti:3333 | xargs kill -9 2>/dev/null
```

## Key Points

1. **Grafana `time_series` format requires `time` column in milliseconds**
2. **MySQL `DATETIME` cannot do direct math** - use `UNIX_TIMESTAMP()`
3. **Always verify column type before timestamp arithmetic**
4. **Test queries via API, not just in UI**

## Alert Setup

### Create Alert Rule

```bash
curl -X POST "http://localhost:3333/api/v1/provisioning/alert-rules" \
  -u "admin:$GRAFANA_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "my-alert",
    "orgID": 1,
    "folderUID": "my-folder",
    "ruleGroup": "my-group",
    "title": "My Alert",
    "condition": "C",
    "data": [
      {
        "refId": "A",
        "relativeTimeRange": {"from": 300, "to": 0},
        "datasourceUid": "datasource-uid",
        "model": {"format": "table", "rawQuery": true, "rawSql": "SELECT ..."}
      },
      {
        "refId": "B",
        "datasourceUid": "__expr__",
        "model": {"expression": "A", "reducer": "last", "type": "reduce"}
      },
      {
        "refId": "C",
        "datasourceUid": "__expr__",
        "model": {
          "conditions": [{"evaluator": {"params": [threshold], "type": "gt"}}],
          "expression": "B",
          "type": "threshold"
        }
      }
    ],
    "for": "5m",
    "annotations": {
      "summary": "Alert: {{ $values.B.Value }}",
      "description": "Description here"
    },
    "labels": {"severity": "critical", "team": "backend"}
  }'
```

### Update Alert Threshold

```bash
curl -s "http://localhost:3333/api/v1/provisioning/alert-rules/alert-uid" -u "admin:$GRAFANA_PASSWORD" | \
  jq '.data[2].model.conditions[0].evaluator.params = [new_threshold]' | \
  curl -X PUT "http://localhost:3333/api/v1/provisioning/alert-rules/alert-uid" \
    -u "admin:$GRAFANA_PASSWORD" -H "Content-Type: application/json" -d @-
```

### Contact Point Message Format

Configure contact point to distinguish clearly between **FIRING** vs **RESOLVED**:

```json
{
  "name": "my-contact-point",
  "type": "googlechat",
  "settings": {
    "title": "{{ if eq .Status \"firing\" }}🔴 ALERT{{ else }}✅ RESOLVED{{ end }}: {{ .CommonLabels.alertname }}",
    "message": "{{ if eq .Status \"firing\" }}*Status:* 🔴 FIRING\n{{ else }}*Status:* ✅ RESOLVED\n{{ end }}{{ range .Alerts }}\n*Alert:* {{ .Labels.alertname }}\n*Severity:* {{ .Labels.severity }}\n*Service:* {{ .Labels.service }}\n{{ .Annotations.summary }}\n{{ .Annotations.description }}\n---\n{{ end }}",
    "url": "webhook-url"
  },
  "disableResolveMessage": false
}
```

### Annotation Best Practices

```yaml
annotations:
  # Include current value AND threshold
  summary: "Auth Error Rate: {{ $values.B.Value | printf \"%.2f\" }}% (threshold: >10%)"
  description: "Auth service error rate exceeded threshold. Check login functionality."
```

### Check Alert History

```bash
# Current firing alerts
curl -s "http://localhost:3333/api/alertmanager/grafana/api/v2/alerts" -u "admin:$GRAFANA_PASSWORD"

# Alert state history
curl -s "http://localhost:3333/api/annotations?type=alert&limit=50" -u "admin:$GRAFANA_PASSWORD"
```

### Common Alert Thresholds (Reference)

| Alert Type | Recommended Threshold |
|------------|----------------------|
| Error Rate | > 5-10% |
| P95 Latency | > 3-5 seconds |
| P99 Latency | > 1-2 seconds |
| No Requests | 0 for 10 minutes |
| Rate Spike | > 3x average |
