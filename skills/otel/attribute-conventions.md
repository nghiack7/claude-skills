# OTEL Attribute Conventions

Standard attribute names for distributed tracing. Engineers **MUST** use the correct names and types defined here.

## Naming Convention

**Rule:** Use `snake_case` for all custom business attributes.

```go
// Correct
attribute.Int64("shop_id", shopID)
attribute.String("ad_account_id", adAccountId)

// Wrong - do not use dot notation for custom attributes
attribute.Int64("shop.id", shopID)

// Wrong - do not use camelCase
attribute.Int64("shopId", shopID)
```

**Exception:** Semantic conventions (semconv) keep dot notation:
```go
semconv.ServiceNameKey.String(serviceName)      // service.name
semconv.FaaSNameKey.String(lambdaFuncName)      // faas.name

// Domain attributes for span classification (see "Span Classification" section)
attribute.String("db.system.name", "mongodb")           // db.*
attribute.String("faas.invoked_name", funcName)         // faas.*
attribute.String("messaging.system", "aws.sns")         // messaging.*
attribute.String("http.request.method", "GET")          // http.*
```

## Reserved Attributes

### Core Business Context

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `shop_id` | Int64 | **Yes** | Shop numeric ID - primary business context |
| `shop_domain` | String | No | Shop domain (e.g., `myshop.myshopify.com`) |

```go
span.SetAttributes(
    attribute.Int64("shop_id", shopID),
    attribute.String("shop_domain", domain),
)
```

### Correlation IDs

| Attribute | Type | Description |
|-----------|------|-------------|
| `job_id` | String | Background job identifier |
| `run_id` | String | Execution run identifier |
| `async_job_id` | String | Async job ID |
| `request_id` | String | HTTP request correlation ID |

### Span Classification (Semantic Conventions)

OTEL distinguishes operation type by **SpanKind + domain-specific attributes**, NOT custom `op_type`.

Observability tools (Datadog, New Relic, Grafana) automatically infer span category from these attributes. For example: seeing `db.system.name` → database span. Seeing `messaging.system` → messaging span.

**Do NOT create custom attributes to classify spans** — use semantic conventions below.

**SpanKind** — distinguishes relationship pattern:

| SpanKind | When to use |
|----------|-------------|
| `CLIENT` | Outgoing sync call: DB query, HTTP request, Lambda invoke, RPC |
| `PRODUCER` | Fire-and-forget: SNS publish, SQS send |
| `INTERNAL` | In-process logic, no I/O (default if not set) |

> `SERVER` and `CONSUMER` are set by `otellambda` on the root span — do not set manually.

**Domain attributes** — distinguish technology:

| Domain | SpanKind | Required Attributes | Optional |
|--------|----------|-------------------|----------|
| **Database** | `CLIENT` | `db.system.name` (`mongodb`, `starrocks`, `clickhouse`) | `db.operation.name`, `db.collection.name`, `db.namespace` |
| **Lambda invoke** | `CLIENT` | `faas.invoked_name` (function name) | `faas.invoked_provider` (`aws`) |
| **SNS publish** | `PRODUCER` | `messaging.system` (`aws.sns`) | `messaging.operation.type` (`send`), `messaging.destination.name` |
| **SQS send** | `PRODUCER` | `messaging.system` (`aws.sqs`) | `messaging.operation.type` (`send`), `messaging.destination.name` |
| **HTTP call** | `CLIENT` | `http.request.method`, `server.address` | `http.response.status_code`, `url.full` |

**Code examples:**

```go
// Database query
ctx, span := otel.StartSpan(ctx, "getConnectedPlatformKeys",
    trace.WithSpanKind(trace.SpanKindClient))
defer span.End()
span.SetAttributes(
    attribute.String("db.system.name", "mongodb"),
    attribute.String("db.operation.name", "countDocuments"),
    attribute.String("db.namespace", dbName),
)

// Lambda invoke
_, span := otel.StartSpan(ctx, "requestSyncFunction",
    trace.WithSpanKind(trace.SpanKindClient))
defer span.End()
span.SetAttributes(
    attribute.String("faas.invoked_name", funcName),
    attribute.String("faas.invoked_provider", "aws"),
)

// SNS publish
ctx, span := otel.StartSpan(ctx, "publishSyncNotification",
    trace.WithSpanKind(trace.SpanKindProducer))
defer span.End()
span.SetAttributes(
    attribute.String("messaging.system", "aws.sns"),
    attribute.String("messaging.operation.type", "send"),
    attribute.String("messaging.destination.name", topicName),
)

// Internal logic (no I/O)
ctx, span := otel.StartSpan(ctx, "transformData")
defer span.End()
// SpanKind defaults to INTERNAL — no domain attributes needed
```

**Grafana queries by span category:**

```sql
-- Database spans
SELECT SpanName, COUNT(*) as Count, ROUND(AVG(Duration)/1e6, 0) as 'Avg(ms)'
FROM otel.otel_traces
WHERE ServiceName = 'my-service'
    AND get_json_string(SpanAttributes, 'db.system.name') IS NOT NULL
    AND Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY SpanName;

-- Lambda invoke spans
SELECT SpanName, get_json_string(SpanAttributes, 'faas.invoked_name') as Target
FROM otel.otel_traces
WHERE ServiceName = 'my-service'
    AND get_json_string(SpanAttributes, 'faas.invoked_name') IS NOT NULL
    AND Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);

-- Messaging spans
SELECT SpanName, get_json_string(SpanAttributes, 'messaging.system') as System
FROM otel.otel_traces
WHERE ServiceName = 'my-service'
    AND get_json_string(SpanAttributes, 'messaging.system') IS NOT NULL
    AND Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);
```

### Operation Status

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | Bool | Operation completed successfully |
| `skipped` | Bool | Operation was intentionally skipped |
| `skip_reason` | String | Why operation was skipped |
| `panic` | Bool | Operation recovered from panic |

```go
// Skipped operation
span.SetAttributes(
    attribute.Bool("skipped", true),
    attribute.String("skip_reason", "already_processed"),
)
```

### Error Tracking

| Attribute | Type | Description |
|-----------|------|-------------|
| `error_stage` | String | Stage where error occurred |
| `error_type` | String | Error classification |
| `total_attempts` | Int | Total retry attempts |
| `retry_count` | Int | Current retry number (0-indexed) |

```go
if err != nil {
    span.SetAttributes(attribute.String("error_stage", "parse_request"))
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
}
```

### Ad Platform

| Attribute | Type | Description |
|-----------|------|-------------|
| `ad_account_id` | String | Ad platform account ID |
| `campaign_id` | String | Campaign identifier |
| `ad_platform` | String | Platform name: `facebook`, `tiktok`, `google` |
| `rate_limited` | Bool | Hit rate limit |

### Authentication

| Attribute | Type | Description |
|-----------|------|-------------|
| `auth_flow` | String | Auth flow type: `sso_login`, `shopify_login`, `email_login` |
| `user_email` | String | User email (PII - use sparingly) |
| `sso_provider` | String | SSO provider: `google`, `shopify` |

### HTTP/API

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | Int | HTTP response status code |
| `body_size` | Int | Response body size in bytes |
| `endpoint` | String | API endpoint path |

### Counts/Metrics

| Attribute | Type | Description |
|-----------|------|-------------|
| `items_count` | Int | Number of items processed |
| `batch_size` | Int | Batch processing size |
| `duration_ms` | Int64 | Operation duration in milliseconds |

## DO NOT Use

| Wrong | Correct | Reason |
|-------|---------|--------|
| `shopId` | `shop_id` | Inconsistent casing |
| `shop.id` | `shop_id` | Reserved for semconv |
| `ShopId` | `shop_id` | Inconsistent casing |
| `errorStage` | `error_stage` | Inconsistent casing |
| `adAccountId` | `ad_account_id` | Inconsistent casing |
| `op_type` | `db.system.name` / `faas.invoked_name` / `messaging.system` | Use OTEL semantic conventions, not custom classification |
| `span_type` | (same as above) | Use OTEL semantic conventions |

## Type Rules

1. **IDs that are numeric** -> `Int64`
   ```go
   attribute.Int64("shop_id", shopID)
   ```

2. **IDs that are string/UUID** -> `String`
   ```go
   attribute.String("async_job_id", jobID)
   attribute.String("ad_account_id", id)
   ```

3. **Counts** -> `Int`
   ```go
   attribute.Int("items_count", len(items))
   ```

4. **Flags** -> `Bool`
   ```go
   attribute.Bool("success", true)
   ```

5. **Durations** -> `Int64` (milliseconds)
   ```go
   attribute.Int64("duration_ms", elapsed.Milliseconds())
   ```

## Adding New Attributes

1. Check this file first - a suitable attribute may already exist
2. Follow naming convention: `snake_case`
3. Choose the correct type per rules above
4. Update this file with the new attribute
5. Document in PR
