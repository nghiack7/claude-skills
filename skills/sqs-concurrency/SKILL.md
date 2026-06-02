---
name: sqs-concurrency
description: >
  Expert guidance for analyzing and safely adjusting SQS Lambda consumer concurrency.
  Use when the user asks to "increase concurrency", "scale consumer", "adjust concurrency",
  "change batch size", "update event source mapping", "increase throughput", "scale up queue",
  "scale down queue", "set reserved concurrency", "update Lambda concurrency",
  or needs to MODIFY Lambda concurrency settings for SQS-triggered functions.
  This is an ACTION skill for changing queue consumer settings, NOT for health audits.
---

# SQS Concurrency Analysis & Scaling

A systematic workflow for analyzing a specific SQS queue's Lambda consumer and safely adjusting
its concurrency. This prevents blindly scaling consumers that might overwhelm downstream
services (databases, APIs, other queues).

## AWS CLI Requirements

All commands use:
- `--profile <AWS_PROFILE>`
- `--region <AWS_REGION>`

If SSO session expired, login first:
```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

## Workflow

Execute these steps in order. Each step informs the risk assessment for the next.

### Step 1: Queue Health Check

Get the full picture of the queue's current state.

```bash
aws sqs get-queue-attributes \
  --queue-url https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<QUEUE_NAME> \
  --attribute-names All \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Key metrics to report:**
| Metric | What it means |
|--------|--------------|
| `ApproximateNumberOfMessages` | Backlog size — how many messages waiting |
| `ApproximateNumberOfMessagesNotVisible` | Currently being processed |
| `ApproximateNumberOfMessagesDelayed` | Delayed messages |
| `VisibilityTimeout` | Must be >= Lambda timeout, or messages get reprocessed |
| `RedrivePolicy` | DLQ config — maxReceiveCount and target DLQ |

If a DLQ exists, also check its message count — a high DLQ count means the consumer is failing frequently:
```bash
aws sqs get-queue-attributes \
  --queue-url https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<QUEUE_NAME>-DLQ \
  --attribute-names ApproximateNumberOfMessages \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Step 2: Find Lambda Consumers

Identify which Lambda functions are subscribed to this queue.

```bash
aws lambda list-event-source-mappings \
  --event-source-arn arn:aws:sqs:<AWS_REGION>:<AWS_ACCOUNT_ID>:<QUEUE_NAME> \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Key info per consumer:**
- `FunctionArn` — which Lambda
- `BatchSize` — messages per invocation
- `State` — Enabled/Disabled
- `ScalingConfig.MaximumConcurrency` — current concurrency limit
- `UUID` — needed for updates

### Step 3: Lambda Configuration

For each consumer function, get its configuration.

```bash
aws lambda get-function-configuration \
  --function-name <FUNCTION_NAME> \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Check:**
- `MemorySize` — low memory + high concurrency can cause OOM
- `Timeout` — must be <= VisibilityTimeout
- `ReservedConcurrentExecutions` — hard upper limit (must be >= MaximumConcurrency)
- `Environment.Variables` — look for downstream service names (other Lambdas, queues, topics)

### Step 4: Code Inspection for Fanout

This is the critical safety step. Read the function's source code to check whether it calls
other services that could be overwhelmed by increased concurrency.

**Find the function handler in the codebase** — the service name usually matches the first part
of the function name (e.g., `reports-prod-generateSalesReports` → `reportfns/generate-sales-reports/`).

**Scan the code for fanout patterns:**

| Pattern | Risk | What to look for |
|---------|------|-----------------|
| Lambda invoke | HIGH | `lambda.Invoke`, `FUNC_NAME_*` env vars |
| SQS send | HIGH | `sqs.SendMessage`, `SQS_QUEUE_*` env vars |
| SNS publish | HIGH | `sns.Publish`, `SNS_TOPIC_*` env vars |
| MongoDB write | MEDIUM | `mongo`, `repository`, `repo.Insert/Update/Upsert` |
| HTTP calls | MEDIUM | `http.Get/Post`, external API calls |
| Read-only DB | LOW | `repo.Find`, `repo.Get` |

**Assessment:**
- **No fanout (DB reads/writes only):** Safe to scale. Most databases handle concurrent writes well.
- **Fanout to other Lambdas:** Check those Lambdas' concurrency limits too. Scaling this function
  will proportionally increase load on downstream Lambdas.
- **Fanout to SQS/SNS:** Generally safe — queues absorb bursts. But check the downstream consumers.
- **External API calls:** Risky — external APIs have rate limits. Check before scaling.

### Step 5: Impact Assessment

Present a summary before making changes:

```
## Concurrency Change Assessment

### Current State
- Queue: <QUEUE_NAME>
- Backlog: {N} messages
- Current concurrency: {N}
- Current reserved concurrency: {N}
- Estimated drain time at current rate: {N} minutes

### Consumer: <FUNCTION_NAME>
- Fanout: {None / List of downstream services}
- Risk level: {LOW / MEDIUM / HIGH}
- Bottleneck: {database / downstream Lambda / external API / none}

### Proposed Change
- New concurrency: {N}
- New reserved concurrency: {N}
- Estimated drain time at new rate: {N} minutes
- Throughput increase: {N}x

### Risks
- {List specific risks based on code inspection}
```

**Drain time formula:**
```
drain_minutes = backlog_messages / (new_concurrency / avg_processing_seconds_per_message)
```
Use the Lambda timeout as a conservative estimate for avg processing time if actual metrics aren't available.

### Step 6: Apply Changes (with user confirmation)

Always ask for user confirmation before applying changes. Two updates are needed:

**1. Update Reserved Concurrency** (must be >= new MaximumConcurrency):
```bash
aws lambda put-function-concurrency \
  --function-name <FUNCTION_NAME> \
  --reserved-concurrent-executions <NEW_VALUE> \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**2. Update Event Source Mapping Concurrency:**
```bash
aws lambda update-event-source-mapping \
  --uuid <EVENT_SOURCE_UUID> \
  --scaling-config '{"MaximumConcurrency": <NEW_VALUE>}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Order matters:** Always update reserved concurrency first, then event source mapping.
AWS rejects event source mapping updates where MaximumConcurrency > ReservedConcurrentExecutions.

### Step 7: Post-Change Monitoring

After applying changes, monitor for a few minutes:

```bash
# Check queue is draining
aws sqs get-queue-attributes \
  --queue-url https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<QUEUE_NAME> \
  --attribute-names ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# Check for errors in the consumer
aws logs tail /aws/lambda/<FUNCTION_NAME> \
  --filter-pattern "ERROR" \
  --since 5m \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# Check DLQ isn't growing
aws sqs get-queue-attributes \
  --queue-url https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<QUEUE_NAME>-DLQ \
  --attribute-names ApproximateNumberOfMessages \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

## Scaling Guidelines

| Scenario | Recommended max concurrency |
|----------|---------------------------|
| Database-only (no fanout) | 50-100 |
| Fanout to other Lambdas | Match downstream reserved concurrency |
| External API calls | Check API rate limit, usually 5-10 |
| Memory-intensive (>256MB) | Start conservative, monitor OOM |

## Rollback

If errors spike after scaling:

```bash
# Reduce event source concurrency
aws lambda update-event-source-mapping \
  --uuid <EVENT_SOURCE_UUID> \
  --scaling-config '{"MaximumConcurrency": <ORIGINAL_VALUE>}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# Reduce reserved concurrency
aws lambda put-function-concurrency \
  --function-name <FUNCTION_NAME> \
  --reserved-concurrent-executions <ORIGINAL_VALUE> \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

## Common Queue Name Patterns

Queues commonly follow a pattern like: `{service}-{stage}-{QueueName}`

Examples:
- `reports-prod-GenerateSaleReportQueue`
- `orders-prod-ProcessOrderQueue`
- `reports-prod-UpdateCustomerQueue.fifo`

To find a queue URL when you only have a partial name:
```bash
aws sqs list-queues \
  --queue-name-prefix <partial-name> \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```
