# OTEL Code Examples

## main.go Pattern

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

    lambdaGo.Start(otellambda.InstrumentHandler(handler.HandleLambdaEvent,
        otellambda.WithTracerProvider(tp),
        otellambda.WithFlusher(tp),
    ))
}
```

## Handler Pattern

```go
func HandleLambdaEvent(ctx context.Context, rawMessage json.RawMessage) (err error) {
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

    span.SetAttributes(
        attribute.Int64("shop_id", shopId),
        attribute.String("job_id", jobId),
    )

    // Business logic...
    return nil
}
```

## Child Span Patterns

Each child span MUST set the correct `SpanKind` + domain attributes per `attribute-conventions.md`.

```go
// Database query — SpanKind: CLIENT + db.* attributes
func queryPlatforms(ctx context.Context, dbName string) error {
    ctx, span := otelutil.StartSpan(ctx, "queryPlatforms",
        trace.WithSpanKind(trace.SpanKindClient))
    defer span.End()

    span.SetAttributes(
        attribute.String("db.system.name", "mongodb"),
        attribute.String("db.operation.name", "countDocuments"),
        attribute.String("db.namespace", dbName),
    )

    // ... query logic
    return nil
}

// Lambda invoke — SpanKind: CLIENT + faas.* attributes
func invokeSyncFunction(ctx context.Context, funcName string) error {
    ctx, span := otelutil.StartSpan(ctx, "invokeSyncFunction",
        trace.WithSpanKind(trace.SpanKindClient))
    defer span.End()

    span.SetAttributes(
        attribute.String("faas.invoked_name", funcName),
        attribute.String("faas.invoked_provider", "aws"),
    )

    // ... invoke logic
    return nil
}

// SNS publish — SpanKind: PRODUCER + messaging.* attributes
func publishNotification(ctx context.Context, topicName string) error {
    ctx, span := otelutil.StartSpan(ctx, "publishNotification",
        trace.WithSpanKind(trace.SpanKindProducer))
    defer span.End()

    span.SetAttributes(
        attribute.String("messaging.system", "aws.sns"),
        attribute.String("messaging.operation.type", "send"),
        attribute.String("messaging.destination.name", topicName),
    )

    // ... publish logic
    return nil
}

// HTTP call — SpanKind: CLIENT + http.* attributes
func callExternalAPI(ctx context.Context, url string) error {
    ctx, span := otelutil.StartSpan(ctx, "callExternalAPI",
        trace.WithSpanKind(trace.SpanKindClient))
    defer span.End()

    span.SetAttributes(
        attribute.String("http.request.method", "GET"),
        attribute.String("server.address", "api.example.com"),
    )

    // ... http call
    span.SetAttributes(attribute.Int("http.response.status_code", resp.StatusCode))
    return nil
}
```

## Error Handling Patterns

```go
// Pattern 1: Explicit error with stage
if err != nil {
    span.SetAttributes(attribute.String("error_stage", "parse_request"))
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
    return err
}

// Pattern 2: Non-fatal warning
if err := optionalStep(); err != nil {
    span.SetAttributes(attribute.String("warning", err.Error()))
    // Don't RecordError - not fatal
}

// Pattern 3: Early exit (not an error)
if shouldSkip {
    span.SetAttributes(
        attribute.Bool("skipped", true),
        attribute.String("skip_reason", "condition_not_met"),
    )
    return nil
}
```

## Common Attributes

| Attribute        | Type   | Usage                |
| ---------------- | ------ | -------------------- |
| `shop_id`        | Int64  | Business context     |
| `job_id`         | String | Correlation ID       |
| `error_stage`    | String | Where error occurred |
| `success`        | Bool   | Operation outcome    |
| `skipped`        | Bool   | Early exit indicator |
| `skip_reason`    | String | Why skipped          |
| `attempt`        | Int    | Retry tracking       |
| `status_code`    | Int    | HTTP response code   |

## Span Kinds

```go
trace.WithSpanKind(trace.SpanKindServer)   // Incoming request (otellambda sets this on root span)
trace.WithSpanKind(trace.SpanKindClient)   // Outgoing sync: DB query, HTTP call, Lambda invoke, RPC
trace.WithSpanKind(trace.SpanKindProducer) // Outgoing async: SNS publish, SQS send
trace.WithSpanKind(trace.SpanKindInternal) // In-process logic, no I/O (default if not set)
```

**Choose SpanKind based on communication pattern, NOT technology:**
- Sync request-response → `CLIENT` (whether DB, HTTP, or Lambda invoke)
- Async fire-and-forget → `PRODUCER` (whether SNS, SQS, or Kafka)
- Internal logic → `INTERNAL` or unset (default)

## otellambda Options

```go
otellambda.InstrumentHandler(handler,
    otellambda.WithTracerProvider(tp),          // Required
    otellambda.WithFlusher(tp),                 // Required for Lambda
    otellambda.WithPropagator(propagator),      // Custom propagator
    otellambda.WithEventToCarrier(fn),          // Extract from API Gateway/SQS/SNS
)
```

## Attributes Added by otellambda

| Attribute                | Description                      |
| ------------------------ | -------------------------------- |
| `faas.name`              | Lambda function name (from Init) |
| `faas.invocation_id`     | Lambda request ID                |
| `aws.lambda.invoked_arn` | Full ARN                         |
| `cloud.account.id`       | AWS account ID                   |
