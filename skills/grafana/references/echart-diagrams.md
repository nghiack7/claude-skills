# ECharts Diagram Patterns - Complete Examples

## Pattern 1: Service Map

Shows traffic between microservices with call counts, latency, and error rates.

### SQL Query

```sql
SELECT
  SpanName as fn,
  COUNT(*) as calls,
  SUM(CASE WHEN StatusCode = 'Error' THEN 1 ELSE 0 END) as errors,
  ROUND(100.0 * SUM(CASE WHEN StatusCode = 'Error' THEN 1 ELSE 0 END) / COUNT(*), 2) as err_pct,
  ROUND(percentile_approx(Duration, 0.50)/1000000, 0) as p50,
  ROUND(percentile_approx(Duration, 0.95)/1000000, 0) as p95,
  COUNT(DISTINCT get_json_string(SpanAttributes, 'shop_id')) as shops
FROM otel.otel_traces
WHERE $__timeFilter(Timestamp)
  AND ServiceName = 'my-service'
GROUP BY SpanName
ORDER BY calls DESC
```

### ECharts Code

```js
const series = context.panel.data.series;
if (!series.length) return { title: { text: 'No data' } };

// Parse query results into a map
const fnF = series[0].fields.find(f => f.name === 'fn');
const callsF = series[0].fields.find(f => f.name === 'calls');
const errF = series[0].fields.find(f => f.name === 'errors');
const errPctF = series[0].fields.find(f => f.name === 'err_pct');
const p50F = series[0].fields.find(f => f.name === 'p50');
const p95F = series[0].fields.find(f => f.name === 'p95');

if (!fnF) return { title: { text: 'Missing data' } };

const fnData = {};
for (let i = 0; i < fnF.values.length; i++) {
    fnData[fnF.values[i]] = {
        calls: callsF.values[i],
        errors: errF.values[i],
        errPct: errPctF.values[i],
        p50: p50F.values[i],
        p95: p95F.values[i]
    };
}

// Helper functions
function fmt(n) {
    if (!n) return '0';
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
    return String(n);
}

function healthColor(errPct) {
    if (!errPct) return '#52c41a';
    if (errPct >= 5) return '#f5222d';
    if (errPct >= 1) return '#fa8c16';
    if (errPct > 0) return '#fadb14';
    return '#52c41a';
}

// Rich text styles
const R = {
    h1: { fontSize: 12, fontWeight: 'bold', color: '#fff', lineHeight: 20 },
    sep: { fontSize: 4, color: 'rgba(255,255,255,0.08)', lineHeight: 6 },
    grn: { fontSize: 12, fontWeight: 'bold', color: '#52c41a', lineHeight: 18 },
    sm: { fontSize: 9, color: 'rgba(255,255,255,0.55)', lineHeight: 14 },
    xs: { fontSize: 8, color: 'rgba(255,255,255,0.35)', lineHeight: 12 },
    ok: { fontSize: 9, color: '#52c41a', lineHeight: 14 },
    red: { fontSize: 10, fontWeight: 'bold', color: '#f5222d', lineHeight: 16 }
};

function nodeStyle(borderColor) {
    return {
        color: 'rgba(255,255,255,0.03)',
        borderColor: borderColor,
        borderWidth: 2,
        shadowBlur: 8,
        shadowColor: borderColor + '33'
    };
}

const A = fnData['service-a'] || {};
const B = fnData['service-b'] || {};

const nodes = [
    {
        name: 'Service A', x: 100, y: 100,
        symbolSize: [150, 80], symbol: 'roundRect',
        itemStyle: nodeStyle(healthColor(A.errPct)),
        label: {
            show: true, position: 'inside',
            formatter: [
                '{h1|Service A}', '{sep|}',
                '{grn|' + fmt(A.calls) + '} {sm|calls}',
                '{xs|P50 ' + (A.p50||0) + 'ms  P95 ' + (A.p95||0) + 'ms}',
                (A.errors > 0 ? '{red|' + A.errors + ' errors}' : '{ok|0 errors}')
            ].join('\n'),
            rich: R
        }
    },
    {
        name: 'Service B', x: 400, y: 100,
        symbolSize: [150, 80], symbol: 'roundRect',
        itemStyle: nodeStyle(healthColor(B.errPct)),
        label: {
            show: true, position: 'inside',
            formatter: [
                '{h1|Service B}', '{sep|}',
                '{grn|' + fmt(B.calls) + '} {sm|calls}',
                '{xs|P50 ' + (B.p50||0) + 'ms  P95 ' + (B.p95||0) + 'ms}',
                (B.errors > 0 ? '{red|' + B.errors + ' errors}' : '{ok|0 errors}')
            ].join('\n'),
            rich: R
        }
    }
];

const ER = {
    val: { fontSize: 10, fontWeight: 'bold', lineHeight: 14,
           backgroundColor: 'rgba(20,20,40,0.92)', padding: [2,5], borderRadius: 3 },
    sub: { fontSize: 8, color: '#888', lineHeight: 12,
           backgroundColor: 'rgba(20,20,40,0.92)', padding: [1,4], borderRadius: 3 }
};

const edges = [
    {
        source: 'Service A', target: 'Service B',
        lineStyle: { width: 3, color: healthColor(B.errPct) },
        symbol: ['none', 'arrow'], symbolSize: [0, 10],
        label: {
            show: true,
            formatter: '{val|' + fmt(B.calls) + ' calls}\n{sub|HTTP/gRPC}',
            rich: { ...ER, val: { ...ER.val, color: healthColor(B.errPct) } }
        }
    }
];

return {
    tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(20,20,40,0.95)',
        borderColor: 'rgba(255,255,255,0.08)',
        textStyle: { color: '#fff', fontSize: 11 }
    },
    series: [{
        type: 'graph', layout: 'none', coordinateSystem: null,
        data: nodes, links: edges, roam: true,
        emphasis: { focus: 'adjacency' }
    }]
};
```

## Pattern 2: Data Flow Diagram (Multi-Layer Pipeline)

Shows data flowing through infrastructure: triggers -> orchestrators -> workers -> data stores.

### Layout Strategy

Organize nodes in columns by role:

```
Column 1 (x~50):   TRIGGER        - Users, HTTP endpoints, scheduled events
Column 2 (x~200):  ORCHESTRATOR   - Main coordinator functions
Column 3 (x~440):  ASYNC WORKERS  - Fan-out workers, queues, topics
Column 4 (x~660):  DATA STORES    - Databases, S3, caches
```

Use rows for parallel processing stages:

```
Row 1 (y~80):   Entry path (trigger -> orchestrator)
Row 2 (y~220):  Primary worker path
Row 3 (y~370):  Secondary worker path (attribution, enrichment)
Row 4 (y~465):  Rare/optional paths (dashed borders)
```

### Infrastructure Component Styling

```js
// Primary function (has OTEL data)
{ symbolSize: [160, 85], symbol: 'roundRect',
  itemStyle: nodeStyle(healthColor(errPct), 0.05) }

// Infrastructure component (API GW, Queue)
{ symbolSize: [120, 50], symbol: 'roundRect',
  itemStyle: nodeStyle('#13c2c2', 0.03) }

// Rare/secondary path
{ symbolSize: [140, 50], symbol: 'roundRect',
  itemStyle: { color: 'rgba(255,255,255,0.02)',
               borderColor: '#555', borderWidth: 1, borderType: 'dashed' } }

// Database
{ symbolSize: [140, 80], symbol: 'roundRect',
  itemStyle: nodeStyle('#b37feb', 0.04) }
```

### Edge Types for Infrastructure

```js
// Sync invocation (Lambda.Invoke)
{ lineStyle: { width: 4, color: '#52c41a' },
  label: { formatter: '{val|27.4k}\n{sub|Lambda.Invoke (sync)}' } }

// Async invocation (Lambda.Invoke with InvocationType=Event)
{ lineStyle: { width: 3, color: '#fa8c16' },
  label: { formatter: '{val|186k}\n{sub|Lambda.Invoke (async)}' } }

// Queue message (SQS.SendMessage)
{ lineStyle: { width: 3, color: '#13c2c2' },
  label: { formatter: '{val|27.4k msg}\n{sub|SQS.SendMessage}' } }

// Topic publish (SNS.Publish)
{ lineStyle: { width: 2, color: '#eb2f96' },
  label: { formatter: '{sub|SNS.Publish}' } }

// Database write
{ lineStyle: { width: 3, color: '#b37feb' },
  label: { formatter: '{sub|write orders/attribution}' } }
```

### Column Headers and Legend via graphic

```js
graphic: [
    // Column labels at top
    { type: 'text', left: 25, top: 8,
      style: { text: 'TRIGGER', fill: 'rgba(255,255,255,0.2)',
               fontSize: 9, fontWeight: 'bold' } },
    { type: 'text', left: 155, top: 8,
      style: { text: 'ORCHESTRATOR', fill: 'rgba(255,255,255,0.2)',
               fontSize: 9, fontWeight: 'bold' } },
    { type: 'text', left: 350, top: 8,
      style: { text: 'ASYNC WORKERS', fill: 'rgba(255,255,255,0.2)',
               fontSize: 9, fontWeight: 'bold' } },
    { type: 'text', left: 580, top: 8,
      style: { text: 'DATA STORES', fill: 'rgba(255,255,255,0.2)',
               fontSize: 9, fontWeight: 'bold' } },

    // Color-coded legend at bottom
    { type: 'group', left: 15, bottom: 8, children: [
        { type: 'rect', shape: { width: 8, height: 8, r: 1 },
          style: { fill: '#177ddc' }, left: 0, top: 0 },
        { type: 'text', style: { text: 'HTTP', fill: '#666', fontSize: 8 },
          left: 12, top: 0 },
        { type: 'rect', shape: { width: 8, height: 8, r: 1 },
          style: { fill: '#52c41a' }, left: 42, top: 0 },
        { type: 'text', style: { text: 'Lambda', fill: '#666', fontSize: 8 },
          left: 54, top: 0 },
        // ... add more legend items
    ]},

    // Data freshness note
    { type: 'text', right: 15, bottom: 8,
      style: { text: 'Live metrics from OTEL traces', fill: '#444',
               fontSize: 8, fontStyle: 'italic' } }
]
```

## Pattern 3: State Diagram

Shows entity lifecycle with state transitions.

### Layout Strategy

```
         [START]
            |
        [PENDING] <--retry-- [RETRY]
            |
      +-----+------+
      |             |
  [PROCESSING]  [CANCELLED]
      |
  +---+---+
  |       |
[SUCCESS] [FAILED] --> [DEAD_LETTER]
```

### Node Styles by State Type

```js
// Start state (circle)
{ name: 'START', x: 250, y: 30,
  symbolSize: 30, symbol: 'circle',
  itemStyle: { color: '#52c41a', borderColor: '#52c41a', borderWidth: 2 },
  label: { show: true, position: 'bottom', formatter: 'START',
           color: 'rgba(255,255,255,0.5)', fontSize: 9 } }

// Normal state (roundRect)
{ name: 'Processing', x: 250, y: 180,
  symbolSize: [120, 45], symbol: 'roundRect',
  itemStyle: nodeStyle('#177ddc', 0.05),
  label: { show: true, position: 'inside',
           formatter: '{h2|Processing}\n{sm|count: ' + count + '}',
           rich: R } }

// Terminal success state
{ name: 'Success', x: 150, y: 320,
  symbolSize: [120, 45], symbol: 'roundRect',
  itemStyle: nodeStyle('#52c41a', 0.08),
  label: { ... } }

// Terminal error state
{ name: 'Failed', x: 350, y: 320,
  symbolSize: [120, 45], symbol: 'roundRect',
  itemStyle: nodeStyle('#f5222d', 0.08),
  label: { ... } }

// Decision diamond (use rotated rect or diamond symbol)
{ name: 'Check', x: 250, y: 250,
  symbolSize: [60, 60], symbol: 'diamond',
  itemStyle: nodeStyle('#fadb14', 0.05),
  label: { show: true, position: 'inside',
           formatter: '{xs|check}', rich: R } }
```

### Self-Loop for Retry

Self-loop edges are not natively supported. Simulate with a helper node:

```js
// Invisible helper node offset from main node
{ name: 'retry_helper', x: 350, y: 100,
  symbolSize: 1, symbol: 'circle',
  itemStyle: { color: 'transparent' },
  label: { show: false } }

// Two edges to create visual loop
{ source: 'Pending', target: 'retry_helper',
  lineStyle: { width: 1, color: '#fadb14', curveness: 0.3 },
  symbol: ['none', 'none'] },
{ source: 'retry_helper', target: 'Pending',
  lineStyle: { width: 1, color: '#fadb14', curveness: 0.3 },
  symbol: ['none', 'arrow'], symbolSize: [0, 8],
  label: { show: true, formatter: '{sub|retry}', rich: ER } }
```

### Transition Edges

```js
// Normal transition
{ source: 'Pending', target: 'Processing',
  lineStyle: { width: 2, color: '#177ddc' },
  symbol: ['none', 'arrow'], symbolSize: [0, 10],
  label: { show: true, formatter: '{sub|start processing}', rich: ER } }

// Error transition
{ source: 'Processing', target: 'Failed',
  lineStyle: { width: 2, color: '#f5222d', type: 'dashed' },
  symbol: ['none', 'arrow'], symbolSize: [0, 10],
  label: { show: true, formatter: '{sub|error after 3 retries}', rich: ER } }

// Conditional transition (from decision)
{ source: 'Check', target: 'Success',
  lineStyle: { width: 2, color: '#52c41a' },
  label: { show: true, formatter: '{sub|valid}', rich: ER } }
```

## Pattern 4: Tooltip with Dynamic Data

```js
tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(20,20,40,0.95)',
    borderColor: 'rgba(255,255,255,0.08)',
    textStyle: { color: '#fff', fontSize: 11 },
    formatter: function(p) {
        if (p.dataType === 'edge') {
            return '<b>' + p.data.source.replace(/\n/g,' ') +
                   '</b> -> <b>' + p.data.target.replace(/\n/g,' ') + '</b>';
        }
        // Look up metrics from parsed data
        const d = fnData[p.name];
        if (!d) return '<b>' + p.name.replace(/\n/g,' ') + '</b>';
        return '<b>' + p.name.replace(/\n/g,' ') + '</b><br/>' +
            'Calls: ' + d.calls.toLocaleString() + '<br/>' +
            'P50: ' + d.p50 + 'ms | P95: ' + d.p95 + 'ms<br/>' +
            'Errors: ' + d.errors + ' (' + d.errPct + '%)';
    }
}
```

## Grafana Panel Configuration

### Recommended Panel Settings

```json
{
    "type": "volkovlabs-echarts-panel",
    "gridPos": { "h": 16, "w": 24, "x": 0, "y": 0 },
    "options": {
        "renderer": "canvas",
        "editor": { "height": 600, "format": "auto" }
    },
    "targets": [{
        "datasource": { "uid": "datasource-uid" },
        "format": "table",
        "rawQuery": true,
        "rawSql": "SELECT ... FROM ... WHERE $__timeFilter(Timestamp) ..."
    }]
}
```

### Panel Height Guidelines

| Diagram Type | Min Height (h) | Recommended |
|-------------|----------------|-------------|
| Service Map (3-5 nodes) | 10 | 12 |
| Data Flow (10+ nodes) | 14 | 16-18 |
| State Diagram (5-8 states) | 10 | 14 |
| Full Architecture | 16 | 20+ |

Always set `roam: true` to allow pan/zoom for complex diagrams.

## Animation

```js
{
    animationDuration: 1200,
    series: [{
        type: 'graph',
        animation: true,
        // ... rest of config
    }]
}
```

For emphasis on hover:

```js
emphasis: {
    focus: 'adjacency',        // Dim unrelated nodes
    lineStyle: { width: 6 },   // Thicken connected edges
    itemStyle: {
        shadowBlur: 15,
        shadowColor: 'rgba(255,255,255,0.2)'
    }
}
```
