# Go Worker Best Practices

## Required Timeout Configuration

**Every workflow MUST have these timeouts:**

```go
activityOptions := workflow.ActivityOptions{
    StartToCloseTimeout:    10 * time.Minute,  // Max time for single attempt
    ScheduleToCloseTimeout: 15 * time.Minute,  // Max time including retries
    HeartbeatTimeout:       30 * time.Second,  // Detect stuck activities
    RetryPolicy: &temporal.RetryPolicy{
        InitialInterval:    time.Second,
        BackoffCoefficient: 2.0,
        MaximumInterval:    2 * time.Minute,
        MaximumAttempts:    3,
        NonRetryableErrorTypes: []string{
            "AuthenticationError",
            "PermissionDeniedError",
            "RateLimitError",
        },
    },
}
ctx = workflow.WithActivityOptions(ctx, activityOptions)
```

**Starter/Schedule MUST have workflow timeouts:**

```go
Action: &client.ScheduleWorkflowAction{
    ID:                       workflowID,
    TaskQueue:                taskQueue,
    Workflow:                 workflows.MyWorkflow,
    Args:                     []any{input},
    WorkflowExecutionTimeout: 2 * time.Hour,
    WorkflowRunTimeout:       2 * time.Hour,
},
```

## Required Worker Options

**Every worker MUST have concurrency limits:**

```go
w := worker.New(c, "my-task-queue", worker.Options{
    MaxConcurrentActivityExecutionSize:     10,
    MaxConcurrentWorkflowTaskExecutionSize: 5,
    MaxConcurrentActivityTaskPollers:       2,
    MaxConcurrentWorkflowTaskPollers:       2,
})
```

## Activity Heartbeats

**Long-running activities MUST call heartbeat:**

```go
func (a *Activities) SyncDataActivity(ctx context.Context, input Input) error {
    activity.RecordHeartbeat(ctx, "starting sync")

    activity.RecordHeartbeat(ctx, "fetching from API")
    data, err := a.client.FetchData(ctx)
    if err != nil {
        return err
    }

    activity.RecordHeartbeat(ctx, "writing to database")
    if err := a.db.Write(data); err != nil {
        return err
    }

    return nil
}
```

## Type-Safe Activity Registration

**ALWAYS use type-safe activity references, NOT strings:**

```go
// ✅ CORRECT: Type-safe activity reference
var acts *activities.Activities
err := workflow.ExecuteActivity(ctx, acts.SyncDataActivity, input).Get(ctx, &result)

// ❌ WRONG: String-based activity name (fragile, no compile-time check)
err := workflow.ExecuteActivity(ctx, "SyncDataActivity", input).Get(ctx, &result)
```

## Idempotent Activities

**Activities MUST be idempotent (safe to retry):**

```go
// ✅ CORRECT: Use Upsert for database writes
func (a *Activities) SaveMappingsActivity(ctx context.Context, mappings []Mapping) error {
    activity.RecordHeartbeat(ctx, "saving mappings")
    return a.db.UpsertMappings(mappings)  // Safe to retry
}

// ❌ WRONG: Insert will fail on retry with duplicates
func (a *Activities) SaveMappingsActivity(ctx context.Context, mappings []Mapping) error {
    return a.db.InsertMappings(mappings)  // Fails on retry!
}
```

## SQL Injection Prevention for StarRocks

**When building raw SQL, ALWAYS escape properly:**

```go
func escapeSQL(s string) string {
    // 1. Remove null bytes (can cause truncation)
    s = strings.ReplaceAll(s, "\x00", "")
    // 2. Escape backslashes FIRST
    s = strings.ReplaceAll(s, "\\", "\\\\")
    // 3. Escape single quotes by doubling
    s = strings.ReplaceAll(s, "'", "''")
    return "'" + s + "'"
}
```

**Order matters:** null bytes → backslashes → single quotes

## StarRocks DDL Syntax

```sql
-- CORRECT: PRIMARY KEY outside column definitions
CREATE TABLE IF NOT EXISTS my_table (
    id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME
)
PRIMARY KEY (id)
DISTRIBUTED BY HASH(id) BUCKETS 8
PROPERTIES ("replication_num" = "1")

-- WRONG: PRIMARY KEY inside (MySQL style)
CREATE TABLE IF NOT EXISTS my_table (
    id BIGINT NOT NULL,
    PRIMARY KEY (id)  -- Syntax error!
) ENGINE=OLAP
```

## Complete Worker Example

```go
package main

import (
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
)

func main() {
    c, _ := client.Dial(client.Options{
        HostPort:  "temporal-frontend.temporal.svc.cluster.local:7233",
        Namespace: "default",
    })
    defer c.Close()

    w := worker.New(c, "my-task-queue", worker.Options{
        MaxConcurrentActivityExecutionSize:     10,
        MaxConcurrentWorkflowTaskExecutionSize: 5,
        MaxConcurrentActivityTaskPollers:       2,
        MaxConcurrentWorkflowTaskPollers:       2,
    })

    w.RegisterWorkflow(workflows.MyWorkflow)
    w.RegisterActivity(acts.InitializeActivity)
    w.RegisterActivity(acts.SyncDataActivity)
    w.RegisterActivity(acts.SaveResultsActivity)

    w.Run(worker.InterruptCh())
}
```

## Code Review Checklist

### Timeouts ✓

- [ ] `StartToCloseTimeout` set (10 min)
- [ ] `ScheduleToCloseTimeout` set (15 min)
- [ ] `HeartbeatTimeout` set (30 sec)
- [ ] `WorkflowExecutionTimeout` in starter (2 hours)
- [ ] `WorkflowRunTimeout` in starter (2 hours)

### Worker Options ✓

- [ ] `MaxConcurrentActivityExecutionSize` (10)
- [ ] `MaxConcurrentWorkflowTaskExecutionSize` (5)
- [ ] `MaxConcurrentActivityTaskPollers` (2)
- [ ] `MaxConcurrentWorkflowTaskPollers` (2)

### Retry Policy ✓

- [ ] `InitialInterval` (1 second)
- [ ] `BackoffCoefficient` (2.0)
- [ ] `MaximumInterval` (2-5 minutes)
- [ ] `MaximumAttempts` (3-5)
- [ ] `NonRetryableErrorTypes` includes auth errors

### Activities ✓

- [ ] Type-safe activity references (not strings)
- [ ] Heartbeats before slow operations
- [ ] Idempotent (use upsert, not insert)
- [ ] No hardcoded credentials

### SQL Security ✓

- [ ] SQL strings properly escaped
- [ ] Null bytes removed
- [ ] Backslashes escaped before quotes
