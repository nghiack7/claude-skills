---
name: starrocks
description: This skill should be used when the user asks to "query StarRocks", "run OLAP query", "analyze data", "check analytics tables", or mentions StarRocks, OLAP, columnar analytics, or high-performance analytical queries.
---

## Related Skills

- **chart-generator** - Visualize StarRocks analytics
- **otel** - Trace data stored in StarRocks
- **grafana** - Dashboard from StarRocks queries
- **mongodb** - Operational data (StarRocks for analytics)

# StarRocks Query Guide

StarRocks uses MySQL protocol but **is NOT MySQL**. This skill covers common pitfalls and query patterns.

## Cluster Architecture

StarRocks can run multiple separate clusters in the same namespace. A common pattern is separating application data from engineering/observability data:

| Cluster | Service | Database | Data |
|---------|---------|----------|------|
| **primary** | `starrocks-primary-fe-service` | app databases | Application data (orders, transactions, etc.) |
| **analytics** | `starrocks-analytics-fe-service` | `engineering_analytics`, `otel` | Engineering data, OTel traces |

**Important:** When querying engineering data (Jira issues, GitLab MRs, commits, pipelines), connect to the correct cluster.

### Connect

```bash
# Application data cluster
kubectl --context <KUBE_CONTEXT> port-forward svc/starrocks-primary-fe-service 9030:9030 -n <NAMESPACE>

# Engineering analytics cluster
kubectl --context <KUBE_CONTEXT> port-forward svc/starrocks-analytics-fe-service 9031:9030 -n <NAMESPACE>
```

```bash
# Query app data
mysql -h 127.0.0.1 -P 9030 -u root -p<password> -e "USE mydb; ..."

# Query engineering analytics
mysql -h 127.0.0.1 -P 9031 -u root -p<password> -e "USE engineering_analytics; ..."
```

Get password from K8s secret:
```bash
kubectl --context <KUBE_CONTEXT> get secret rootcredential -n <NAMESPACE> -o jsonpath='{.data.password}' | base64 -d
```

### engineering_analytics Tables (example schema)

**Jira:** `jira_projects`, `jira_issues`, `jira_users`, `jira_boards`, `jira_sprints`, `jira_project_versions`
**GitLab:** `gitlab_repositories`, `gitlab_users`, `gitlab_commits`, `gitlab_merge_requests`, `gitlab_mr_loc`, `gitlab_pipelines`, `gitlab_pipeline_jobs`
**Cross-system:** `user_mappings` (GitLab ↔ Jira user mapping)

**Note:** Table `gitlab_group_members` does not exist by default; use `gitlab_users` instead.

## Documentation

- [StarRocks Docs](https://docs.starrocks.io/docs/introduction/StarRocks_intro/)
- [SQL Reference](https://docs.starrocks.io/docs/sql-reference/sql-statements/keywords/)
- [Reserved Keywords](https://docs.starrocks.io/docs/sql-reference/sql-statements/keywords/)
- [Functions](https://docs.starrocks.io/docs/sql-reference/sql-functions/overview-of-functions/)
- [Date Functions](https://docs.starrocks.io/docs/sql-reference/sql-functions/date-time-functions/date_trunc/)
- [Primary Key Table](https://docs.starrocks.io/docs/table_design/table_types/primary_key_table/)

## CRITICAL: MySQL vs StarRocks Differences

### Reserved Keywords

StarRocks has additional reserved keywords. **Rename columns**, don't use backticks.

| Keyword  | Use Instead  |
| -------- | ------------ |
| `read`   | `is_read`    |
| `load`   | `data_load`  |
| `delete` | `is_deleted` |
| `index`  | `idx`        |
| `key`    | `key_name`   |

```sql
-- WRONG: "Unexpected input 'read'"
CREATE TABLE t (read BOOLEAN)

-- CORRECT
CREATE TABLE t (is_read BOOLEAN)
```

### Unsupported Functions

| MySQL Function                         | StarRocks Alternative                         |
| -------------------------------------- | --------------------------------------------- |
| `WEEKDAY(date)`                        | `DATE_TRUNC('week', date)`                    |
| `DAYOFWEEK(date)`                      | `DAYOFWEEK(date)` exists but returns 1=Sunday |
| `DATE_SUB(d, INTERVAL WEEKDAY(d) DAY)` | `DATE(DATE_TRUNC('week', d))`                 |

```sql
-- WRONG: "No matching function with signature: weekday(datetime)"
SELECT DATE(DATE_SUB(created_at, INTERVAL WEEKDAY(created_at) DAY)) as week_start

-- CORRECT
SELECT DATE(DATE_TRUNC('week', created_at)) as week_start
```

### DDL Syntax (Different from MySQL!)

```sql
-- WRONG: MySQL style
CREATE TABLE t (
    id BIGINT NOT NULL PRIMARY KEY,  -- Error!
    name VARCHAR(255)
)

-- CORRECT: StarRocks style
CREATE TABLE t (
    id BIGINT NOT NULL,
    name VARCHAR(255)
)
PRIMARY KEY (id)
DISTRIBUTED BY HASH(id) BUCKETS 8
PROPERTIES ("replication_num" = "1")
```

**Bucket sizing:**

- < 10K rows: 4 buckets
- 10K - 100K rows: 8 buckets
- 100K+ rows: 16 buckets

### Common Errors & Fixes

| Error                           | Cause                        | Fix                              |
| ------------------------------- | ---------------------------- | -------------------------------- |
| `Unexpected input 'read'`       | Reserved keyword             | Rename column to `is_read`       |
| `No matching function: weekday` | Function not supported       | Use `DATE_TRUNC('week', date)`   |
| `Syntax error near ')'`         | Empty IN clause from Grafana | Use REGEXP with `allValue: ".*"` |
| `Column not found`              | Trailing spaces              | Use `TRIM(column)`               |

## Grafana Multi-Select Variables

**DON'T use** these formats with StarRocks:

- `${var:sqlstring}`
- `${var:singlequote}`
- `${var:csv}`

**Use REGEXP approach:**

```json
{
  "name": "fix_version",
  "type": "query",
  "multi": true,
  "includeAll": true,
  "allValue": ".*",
  "query": "SELECT DISTINCT TRIM(column) as __value FROM table WHERE column IS NOT NULL"
}
```

```sql
-- Works for both "All" (.*) and multi-select (val1|val2|val3)
SELECT * FROM table
WHERE TRIM(column) REGEXP '${fix_version:pipe}'
```

**Explanation:**

- `${fix_version:pipe}` → `val1|val2|val3` (Grafana pipe format)
- `allValue: ".*"` → When "All" selected, variable = `.*` matches everything
- `REGEXP 'val1|val2'` → Matches any of the values

## OLAP Best Practices

### 1. Avoid JOINs

StarRocks is OLAP, JOINs are slow. **Denormalize data**.

```sql
-- BAD: Join at query time
SELECT i.*, u.name
FROM issues i
JOIN users u ON i.assignee_id = u.id

-- GOOD: Denormalized table with embedded data
SELECT issue_key, assignee_name
FROM issues_denormalized
```

### 2. Batch Upsert

When syncing large datasets, save each page immediately:

```go
// BAD: Collect all then save
allContacts := []Contact{}
for page := range pages {
    allContacts = append(allContacts, page...)
}
db.Save(allContacts)  // Memory explosion!

// GOOD: Save each page
for page := range pages {
    db.Save(page)  // Incremental progress
    heartbeat()
}
```

### 3. Use PRIMARY KEY Tables

StarRocks PRIMARY KEY tables auto-upsert on INSERT (like MySQL ON DUPLICATE KEY UPDATE).

```sql
INSERT INTO users (id, name, email)
VALUES (1, 'John', 'john@example.com')
-- If id=1 exists, it updates instead of insert
```

## Query Tips

1. **Always filter by partition key**: Use partition columns to limit scope
2. **Use date ranges**: Filter by date columns for performance
3. **JSON columns**: Use `JSON_QUERY()` or `->` operator for JSON fields
4. **Aggregate first**: StarRocks is optimized for aggregations
5. **TRIM strings**: Use `TRIM(column)` to handle trailing spaces

## Related Skills

For visualization and dashboards:

- `/grafana` - StarRocks dashboards and monitoring
- `/chart-generator` - Create charts from StarRocks data

For data pipelines:

- `/dagster` - Data pipelines that write to StarRocks
- `/mongodb` - Source data for StarRocks ingestion

For cluster management:

- `/kubectl` - K8s access to StarRocks on EKS
- `/aws` - AWS EKS operations

For related databases:

- `/mongodb` - MongoDB real-time data
