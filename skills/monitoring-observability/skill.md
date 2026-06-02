---
name: monitoring-observability
description: This skill should be used when the user asks to "set up monitoring", "add metrics", "configure logging", "implement tracing", "define SLO", or mentions RED method, USE method, observability design, alerting strategy, or SRE practices.
patterns: []
---

## Related Skills

- **otel** - Distributed tracing implementation
- **grafana** - Dashboard and visualization
- **coroot** - APM and SLO monitoring
- **incident-response** - Alert-driven incident handling

# Monitoring & Observability Skill

Knowledge of monitoring, logging, and observability best practices.

## What This Skill Provides

- Metrics frameworks (RED, USE)
- Logging strategies
- Distributed tracing
- Alerting best practices

## The Three Pillars

### 1. Metrics
Numerical measurements over time
- Request rate, error rate, latency
- Resource utilization
- Business metrics

### 2. Logs
Discrete events with context
- Application logs
- Access logs
- Error logs

### 3. Traces
Request flow through system
- Distributed tracing
- Performance profiling
- Bottleneck identification

## RED Method (Services)

**For user-facing services:**

- **Rate:** Requests per second
- **Errors:** Error rate (%)
- **Duration:** Response time (P50, P95, P99)

**Example:**
```
Rate: 1000 req/s
Errors: 0.1%
Duration: P95 = 180ms
```

## USE Method (Resources)

**For infrastructure resources:**

- **Utilization:** % busy (CPU, memory, disk)
- **Saturation:** Queue depth, wait time
- **Errors:** Error count

**Example:**
```
CPU Utilization: 65%
CPU Saturation: 0 (no queue)
CPU Errors: 0
```

## Logging Best Practices

### Structured Logging
```json
{
  "timestamp": "2025-10-20T10:30:00Z",
  "level": "ERROR",
  "service": "api",
  "trace_id": "abc123",
  "user_id": "user_456",
  "message": "Payment processing failed",
  "error": "Insufficient funds"
}
```

### Log Levels
- **DEBUG:** Detailed info for debugging
- **INFO:** General informational messages
- **WARN:** Warning but not error
- **ERROR:** Error occurred, action needed
- **FATAL:** Critical failure

### What to Log
✅ Errors and exceptions
✅ Authentication events
✅ Business events (purchases, signups)
✅ Performance issues

❌ Sensitive data (passwords, tokens)
❌ Excessive debug in production
❌ Non-actionable noise

## Distributed Tracing

### Concepts
- **Trace:** End-to-end request flow
- **Span:** Single operation
- **Trace ID:** Unique identifier

### Example Flow
```
HTTP Request (trace: abc123)
  ├─ API Gateway (span: 50ms)
  ├─ Auth Service (span: 20ms)
  ├─ Business Logic (span: 100ms)
  │  ├─ Database Query (span: 80ms)
  │  └─ Cache Lookup (span: 5ms)
  └─ Response (total: 250ms)
```

## Alerting

### Alert Criteria
**Good alerts:**
- Actionable
- Precise (not noisy)
- User-impacting
- Include context

**Bad alerts:**
- "Server CPU at 60%" (not actionable)
- Daily false positives (noise)

### Alert Levels

**P0 (Critical):**
- Service down
- Data loss
- Security breach
→ Page on-call, immediate action

**P1 (High):**
- Error rate spike
- Performance degradation
→ Notify team, action within 1 hour

**P2 (Medium):**
- Non-critical errors
- Capacity warnings
→ Review during business hours

## Observability Tools

### Metrics
- Prometheus, Grafana
- CloudWatch, Datadog
- Custom dashboards

### Logging
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk, Datadog
- Centralized logging

### Tracing
- Jaeger, Zipkin
- OpenTelemetry
- APM tools

## Dashboard Design

### Key Principles
- Most important metrics top
- Time-series graphs
- Color-code thresholds
- Auto-refresh

### Essential Dashboards

**Service Health:**
- Request rate (RED)
- Error rate
- Latency (P50, P95, P99)
- Uptime

**Infrastructure:**
- CPU, Memory (USE)
- Disk I/O
- Network traffic

**Business:**
- Active users
- Conversions
- Revenue

## See Also

- `deployment-strategies` - Monitoring deployments
- `incident-response` - Using metrics during incidents
- `scalability-design` - Performance monitoring
