---
name: dagster
description: This skill should be used when the user asks to "check Dagster pipeline", "monitor Celery workers", "check SQS throughput", "view Flower dashboard", "webhook processing status", or mentions Dagster, Celery, SQS queues, or pipeline monitoring.
---

# Dagster Pipeline Monitor

Monitor Dagster pipelines running on Kubernetes (EKS production cluster).

## Web UIs (VPN Required)

| Service        | URL                           | Purpose                           |
| -------------- | ----------------------------- | --------------------------------- |
| **Dagster UI** | https://dagster.your-internal-host.example.com | Pipeline runs, sensors, schedules |
| **Flower**     | https://flower.your-internal-host.example.com  | Celery workers, task monitoring   |
| **Grafana**    | https://your-grafana.example.com | Metrics dashboards                |

## Quick Start

**Requires:**

- `kubectl` with context `<KUBE_CONTEXT>`
- `aws` CLI with appropriate profile
- `jq` for JSON parsing
- VPN connection for web UIs

## Metrics Displayed

**Code Servers:**

- `code-marketing` - Ad platform sync (Facebook/Google Ads)
- `code-payment` - Payment transaction sync
- `code-sync-webhook-order` - Webhook processing (SQS)

**Dagster Core:**

- `daemon` - Scheduler, sensor daemon
- `webserver` - Dagster UI
- `workers` - Celery workers for job execution

**SQS Queue Depth (Webhook processing):**

- `orders_create` - New order webhooks
- `orders_update` - Order update webhooks
- `orders_delete` - Order delete webhooks
- `refunds_create` - Refund webhooks
- `returns_process` - Return processing webhooks
- `order_transactions` - Transaction webhooks

**Throughput:**

- Total pending messages across all queues
- Processing rate (msg/s) - queue shrinking/growing

## Architecture

```
External Service → EventBridge → SQS Queues → Dagster Sensors → Jobs → StarRocks
                                                    ↓
                                        code-sync-webhook-order
```

**Data Flow:**

1. External service sends webhooks to EventBridge
2. EventBridge routes to SQS queues by event type
3. Dagster sensors poll SQS queues
4. Sensors trigger jobs with message data
5. Jobs process and write to StarRocks

## SQS Queues

| Queue                                            | Event Type                | Sensor                                        |
| ------------------------------------------------ | ------------------------- | --------------------------------------------- |
| `DagsterEventBridgeOrdersCreateQueue`            | orders/create             | `sqs_webhook_order_create_sensor`             |
| `DagsterEventBridgeOrdersUpdatedV2Queue`         | orders/updated            | `sqs_webhook_order_update_sensor`             |
| `DagsterEventBridgeOrdersDeleteQueue`            | orders/delete             | `sqs_webhook_order_delete_sensor`             |
| `DagsterEventBridgeRefundsCreateQueue`           | refunds/create            | `sqs_webhook_refund_create_sensor`            |
| `DagsterEventBridgeReturnsProcessQueue`          | returns/process           | `sqs_webhook_return_process_sensor`           |
| `DagsterEventBridgeOrderTransactionsCreateQueue` | order_transactions/create | `sqs_webhook_order_transaction_create_sensor` |

## Troubleshooting

**High queue depth (>100K):**

- Check if sensors are running: Dagster UI → Sensors
- Check worker count: should scale with KEDA
- Check for errors in sensor logs

**code-marketing CrashLoopBackOff:**

- Check logs: `kubectl logs -n dagster -l app=code-marketing --tail=100`
- Common cause: missing dependencies in Docker image

**Slow processing:**

- Check Celery worker count
- Check StarRocks write throughput
- Monitor network latency to SQS

## Celery Workers (Job Executor)

Dagster uses Celery as the executor for running jobs.

**Cluster Components:**

| Component                        | Pods | Purpose                 |
| -------------------------------- | ---- | ----------------------- |
| `dagster-workers-worker-dagster` | 5    | Celery workers          |
| `dagster-flower`                 | 1    | Celery monitoring UI    |
| `dagster-daemon`                 | 1    | Scheduler/sensor daemon |
| `dagster-dagster-webserver`      | 2    | Dagster UI              |

**Worker Configuration:**

```yaml
Command: dagster-celery worker start -A dagster_celery.app
Queue: dagster
Concurrency: 4 per worker (total: 20 concurrent tasks)
Resources:
  requests: 500m CPU, 512Mi RAM
  limits: 2 CPU, 2Gi RAM
```

**Celery Commands:**

```bash
# Check Celery worker logs
kubectl --context <KUBE_CONTEXT> logs -f -l app=dagster-workers-worker-dagster -n dagster --tail=100

# Check worker pod details
kubectl --context <KUBE_CONTEXT> describe pod -l app=dagster-workers-worker-dagster -n dagster

# Scale workers (if needed)
kubectl --context <KUBE_CONTEXT> scale deployment dagster-workers-worker-dagster -n dagster --replicas=10
```

**Flower UI:** https://flower.your-internal-host.example.com (VPN required)

- View active/completed/failed tasks
- Monitor worker status and performance
- Terminate stuck tasks
- View task arguments and results

## Manual Commands

```bash
# Check pod status
kubectl --context <KUBE_CONTEXT> get pods -n dagster

# Check SQS queue depth
aws sqs get-queue-attributes \
  --queue-url "https://sqs.<REGION>.amazonaws.com/<ACCOUNT_ID>/<QUEUE_NAME>" \
  --attribute-names ApproximateNumberOfMessages \
  --region <REGION> \
  --profile <AWS_PROFILE>

# Check sensor status in Dagster
kubectl --context <KUBE_CONTEXT> exec -n dagster deploy/dagster-daemon -- \
  dagster sensor list -w /dagster-workspace/workspace.yaml
```

**Dagster UI:** https://dagster.your-internal-host.example.com (VPN required)

## OTEL Integration

Dagster workers can be instrumented with OpenTelemetry tracing.

**To enable OTEL tracing in workers:**

Add env vars to the dagster workers deployment:

```yaml
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://otel-collector-collector.monitoring.svc.cluster.local:4317"
  - name: OTEL_SERVICE_NAME
    value: "dagster-worker"
  - name: OTEL_TRACES_SAMPLER
    value: "parentbased_always_on"
```

**Query traces in Grafana:**

```sql
SELECT
  DATE_TRUNC('minute', Timestamp) as time,
  SpanAttributes->'$.dagster.run_id' as run_id,
  SpanName,
  Duration / 1000000 as duration_ms
FROM otel.otel_traces
WHERE ServiceName LIKE 'dagster%'
  AND Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY time;
```

## Related Skills

For infrastructure access:

- `/kubectl` - K8s access to Dagster pods
- `/aws` - AWS SQS/CloudWatch commands

For data and monitoring:

- `/starrocks` - Query analytics data written by Dagster
- `/grafana` - Create dashboards for Dagster metrics
- `/otel` - OpenTelemetry tracing setup
- `/coroot` - Application observability

For incident handling:

- `/incident-response` - Pipeline failure troubleshooting
