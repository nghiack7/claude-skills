---
name: temporal
description: This skill should be used when the user asks to "run backfill", "trigger Temporal workflow", "start workflow", "check workflow status", or mentions Temporal, workflow execution, or backfill operations via kubectl.
---

## Related Skills

- **kubectl** - K8s operations for Temporal admintools
- **starrocks** - Database that pipelines write into (see cluster architecture)
- **dagster** - Alternative pipeline orchestration
- **coroot** - Monitor workflow health

## Sync Pipelines Overview

Temporal workers running in the `temporal` namespace on Kubernetes can be used for a variety of sync pipelines. A common pattern is syncing engineering data (Jira, GitLab, etc.) into an analytics database on a schedule.

Example worker pattern:

| Deployment | Task Queue | Writes to | Schedule |
|------------|-----------|-----------|----------|
| `jira-sync` | `jira-sync` | StarRocks analytics cluster | Every 3 hours |
| `gitlab-sync` | `gitlab-sync` | StarRocks analytics cluster | Every 3 hours |
| `user-mapping` | `user-mapping` | StarRocks analytics cluster | Every 3 hours |

**Important:** Sync pipelines that write engineering analytics data should write to the dedicated analytics cluster, not the application data cluster. See the `starrocks` skill for cluster architecture details.

### Example: Jira sync
- Projects: configured via `JIRA_PROJECTS` env var
- Sync: users → projects (issues, boards, sprints, versions)
- Incremental sync based on `updated_at`

### Example: GitLab sync
- Group: configured via `GITLAB_GROUP` env var (include subgroups)
- Sync: group members → repositories → (commits, pipelines, pipeline_jobs, merge_requests) per repo
- Parallelism: configurable (e.g. max 3 repos concurrently)

# Temporal Admin via kubectl

```bash
# Find admintools pod
kubectl get pods -n temporal | grep admintools

# Trigger workflow
kubectl exec -n temporal temporal-admintools-XXX -- temporal workflow start \
  --task-queue TASK_QUEUE \
  --workflow-id WORKFLOW_ID \
  --type WORKFLOW_TYPE \
  --input '{"GroupPath":"your-group","Backfill":true}'

# Check status
kubectl exec -n temporal temporal-admintools-XXX -- temporal workflow describe \
  -w WORKFLOW_ID -r RUN_ID
```

## Common backfills

```bash
# GitLab
kubectl exec -n temporal temporal-admintools-XXX -- temporal workflow start \
  --task-queue gitlab-sync --workflow-id gitlab-backfill \
  --type GitLabSyncWorkflow --input '{"GroupPath":"your-group","Backfill":true}'

# Jira
kubectl exec -n temporal temporal-admintools-XXX -- temporal workflow start \
  --task-queue jira-sync --workflow-id jira-backfill \
  --type JiraSyncWorkflow --input '{"Projects":"PROJECT1,PROJECT2","Backfill":true}'
```
