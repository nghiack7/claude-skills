---
name: otel
description: This skill should be used when the user asks to "add tracing", "instrument Lambda", "debug performance", "query traces", "set up OpenTelemetry", or mentions OTel, distributed tracing, span attributes, or trace analysis in StarRocks/Grafana.
---

## Related Skills

- **grafana** - View traces in Grafana dashboards
- **starrocks** - Query trace data in StarRocks
- **monitoring-observability** - Overall observability strategy

# OpenTelemetry Tracing

OTEL for distributed tracing in Go serverless functions.

## When to Use

- Adding tracing to a new Lambda function
- Debugging performance issues
- Querying traces in StarRocks/Grafana

## Quick Reference

| Resource | Location |
|----------|----------|
| **Tracer code** | See `tracer.go` in this skill folder |
| **Code examples** | See `examples.md` in this skill folder |
| **Attribute naming** | See `attribute-conventions.md` in this skill folder |

## Infrastructure

| Environment | OTEL Collector | Grafana | StarRocks |
|-------------|----------------|---------|-----------|
| **Production** | `<OTLP_ENDPOINT>:443` | `your-grafana.example.com` | `<STARROCKS_HOST>:9030` |
| **Staging** | `<OTLP_ENDPOINT_STAGING>:443` | `your-grafana-staging.example.com` | `<STARROCKS_HOST_STAGING>:9030` |

```
Lambda → OTEL Collector → StarRocks → Grafana
```

## WARNING: Do Not Wrap Payloads With Trace Context

**DO NOT use a `WrapPayloadWithTrace` pattern for cross-service calls.**

Reason: This changes the payload structure:

```go
// WrapPayloadWithTrace produces:
{
    "traceparent": "00-abc123...",
    "payload": { "shopId": 123, ... }  // ← nested payload
}

// But downstream services expect:
{
    "shopId": 123,  // ← top level
    "orderReturn": {...}
}
```

**Breaking change scenario:**

```
service-a (updated) → service-b (NOT updated) = ERROR
```

Downstream service cannot parse the payload because the structure changed.

**Only acceptable when:** ALL services in the call chain have been updated to handle the wrapped payload. Requires coordinated rollout.

**Alternative:** Use context propagation instead. Inject trace context into HTTP headers or SQS message attributes.

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **BatchSpanProcessor** | Non-blocking exports, buffering |
| **2s timeouts** | Fail fast, don't block Lambda |
| **No retry** | Avoid blocking during collector issues |
| **No TLS config** | Infrastructure handles TLS termination |
| **Graceful fallback** | Return noop provider on error, no error return |
| **Error logging** | Log with `[OTEL]` prefix, don't fail |

## Environment Variables

```yaml
# serverless.yml
environment:
  OTEL_SERVICE_NAME: my-service  # Static per repository, NOT per function
  OTEL_SDK_DISABLED: ${env:OTEL_SDK_DISABLED, 'true'}
  OTEL_EXPORTER_OTLP_ENDPOINT: ${env:OTEL_EXPORTER_OTLP_ENDPOINT, ''}
  OTEL_EXPORTER_OTLP_PROTOCOL: grpc
  SERVICE_VERSION: ${git:sha1}
```

| Variable | Purpose | Example |
|----------|---------|---------|
| `OTEL_SERVICE_NAME` | Service/repo name (static) | `orderfns`, `syncfns` |
| `OTEL_SDK_DISABLED` | Disable tracing | `false` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Collector URL | `otel-collector.example.com:443` |
| `SERVICE_VERSION` | Git commit hash | `${git:sha1}` |

## ServiceName vs SpanName (IMPORTANT)

```
┌─────────────────────────────────────────────────────────────────┐
│                   OTEL Trace Data Model                          │
├─────────────────────────────────────────────────────────────────┤
│  ServiceName = "orderfns"              ← OTEL_SERVICE_NAME      │
│  SpanName = "orders-prod-onOrdersCreate" ← AWS_LAMBDA_FUNCTION_NAME │
│  service.version = "5983ced"           ← SERVICE_VERSION        │
│  deployment.environment = "prod"       ← STAGE                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key points:**

| Field | Source | Use Case |
|-------|--------|----------|
| `ServiceName` | `OTEL_SERVICE_NAME` env var | Group all functions of a repo |
| `SpanName` | `otellambda` auto-sets from `AWS_LAMBDA_FUNCTION_NAME` | Identify individual function |

**DO NOT set `faas.name` manually** - `otellambda` already sets `SpanName` to the Lambda function name. Setting `faas.name` is redundant.

**Dashboard queries should use `SpanName`:**

```sql
-- ✅ Correct - use SpanName for function name
SELECT SpanName as Function, COUNT(*) as Requests
FROM otel.otel_traces
WHERE ServiceName = 'orderfns'
GROUP BY SpanName;

-- ❌ Wrong - extracting from JSON is slower
SELECT json_query(ResourceAttributes, '$."faas.name"') as Function
FROM otel.otel_traces;
```

## Adding OTEL to New Function

### Step 0: Validate reference code (CRITICAL)

Before applying the tracer pattern, **verify the skill's `tracer.go` matches production code**:

```bash
# Compare skill reference against actual production implementation
diff <(cat skills/otel/tracer.go) <(cat /path/to/repo/internal/otel/tracer.go)
```

If they differ, **update the skill's reference first**, then proceed. Stale references produce wrong implementations.

### Step 1: Copy tracer.go

Copy `tracer.go` from this skill folder to `internal/otel/tracer.go`

### Step 2: Setup main.go

```go
package main

import (
    "context"
    lambdaGo "github.com/aws/aws-lambda-go/lambda"
    "go.opentelemetry.io/contrib/instrumentation/github.com/aws/aws-lambda-go/otellambda"
    otelutil "your-module/internal/otel"
    "your-module/internal/handler"
)

func main() {
    ctx := context.Background()
    tp := otelutil.Init(ctx, "service-name")
    defer tp.Shutdown(ctx)

    lambdaGo.Start(otellambda.InstrumentHandler(handler.Handle,
        otellambda.WithTracerProvider(tp),
        otellambda.WithFlusher(tp),
    ))
}
```

### Step 3: Handler

```go
func Handle(ctx context.Context, event Event) (err error) {
    span := trace.SpanFromContext(ctx)
    defer func() {
        if r := recover(); r != nil {
            stack := string(debug.Stack())
            span.AddEvent("panic", trace.WithAttributes(
                attribute.String("stacktrace", stack),
            ))
            err = fmt.Errorf("panic: %v\n%s", r, stack)
            span.RecordError(err)
            span.SetStatus(codes.Error, "panic")
        } else if err != nil {
            span.RecordError(err)
            span.SetStatus(codes.Error, err.Error())
        }
    }()

    // Use snake_case for attributes - see attribute-conventions.md
    span.SetAttributes(attribute.Int64("shop_id", shopId))
    // ... business logic
}
```

### Step 4: Child spans for external calls

```go
ctx, span := otelutil.StartSpan(ctx, "CallAPI", trace.WithSpanKind(trace.SpanKindClient))
defer span.End()
```

### Step 5: Add dependencies

```bash
go get go.opentelemetry.io/contrib/instrumentation/github.com/aws/aws-lambda-go/otellambda@latest
```

## Configuration

Enable tracing via your secrets manager:

```bash
# Staging
OTEL_SDK_DISABLED=false
OTEL_EXPORTER_OTLP_ENDPOINT=<OTLP_ENDPOINT_STAGING>:4317

# Production
OTEL_SDK_DISABLED=false
OTEL_EXPORTER_OTLP_ENDPOINT=<OTLP_ENDPOINT>:4317
```

## StarRocks Queries

**Access StarRocks:**

```bash
# Port forward to StarRocks FE
kubectl --context <KUBE_CONTEXT> port-forward svc/<STARROCKS_FE_SERVICE> 9030:9030 -n <NAMESPACE>

# Connect
mysql -h 127.0.0.1 -P 9030 -u root
```

**Common queries:**

```sql
-- Traces by function (last 30 min)
SELECT
    SpanName as Function,
    COUNT(*) as Requests,
    SUM(CASE WHEN StatusCode = 'Error' THEN 1 ELSE 0 END) as Errors,
    ROUND(AVG(Duration)/1000000, 0) as 'Avg(ms)',
    ROUND(percentile_approx(Duration, 0.99)/1000000, 0) as 'P99(ms)'
FROM otel.otel_traces
WHERE ServiceName = 'my-service'
    AND Timestamp > DATE_SUB(NOW(), INTERVAL 30 MINUTE)
GROUP BY SpanName
ORDER BY Requests DESC;

-- Recent errors with context
SELECT
    SpanName as Function,
    get_json_string(SpanAttributes, 'shop_id') as ShopID,
    SUBSTRING(StatusMessage, 1, 80) as Error,
    ROUND(Duration/1000000, 0) as 'Duration(ms)'
FROM otel.otel_traces
WHERE ServiceName = 'my-service'
    AND StatusCode = 'Error'
    AND Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY Timestamp DESC
LIMIT 20;

-- Delete old traces (cleanup)
DELETE FROM otel.otel_traces
WHERE ServiceName IN ('service-a', 'service-b')
    AND Timestamp < DATE_SUB(NOW(), INTERVAL 7 DAY);
```

## Troubleshooting

### Traces not appearing

1. Check `OTEL_SDK_DISABLED` != `true`
2. Check `OTEL_EXPORTER_OTLP_ENDPOINT` has a value
3. Check Lambda logs for `[OTEL]` errors
4. Verify collector accessible from Lambda VPC

### Lambda slow with OTEL

- ForceFlush timeout is 2s (by design)
- If collector is down, it will fail fast
- **Fix**: Check collector connectivity

### Connection errors

```
rpc error: code = Unavailable desc = "connection refused"
```

- Check endpoint and port (gRPC: 4317)
- Check security groups
- Note: TLS handled by infrastructure

### delegating_resolver: invalid target address

```
rpc error: code = Unavailable desc = delegating_resolver: invalid target address "": missing address
```

**Root cause:** gRPC library does not auto-resolve `OTEL_EXPORTER_OTLP_ENDPOINT` env var correctly. Must explicitly pass endpoint via `WithEndpoint()`.

**Fix:** In `tracer.go`, ensure you use `otlptracegrpc.WithEndpoint(endpoint)`:

```go
endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
exporter, err := otlptracegrpc.New(ctx,
    otlptracegrpc.WithEndpoint(endpoint),  // ← REQUIRED
    otlptracegrpc.WithTimeout(defaultOtelTimeout),
)
```

**Do NOT** rely on the library auto-reading the env var - it will fail silently.

### Spans lost

- BatchSpanProcessor buffers up to 100 spans
- ForceFlush runs after each invocation
- Check logs for export errors

## Reference Files

- **`attribute-conventions.md`**: **Required** attribute naming standards
- **`tracer.go`**: Full tracer implementation - copy to `internal/otel/`
- **`examples.md`**: Handler patterns, child spans, error handling, attributes
