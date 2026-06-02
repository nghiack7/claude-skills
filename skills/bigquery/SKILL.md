---
name: bigquery
description: Use when the user asks to "query BigQuery", "analyze data warehouse", "check revenue metrics", "billing analytics", "ad insights query", or mentions BigQuery, data warehouse, business intelligence, or analytics tables. Provides generic BigQuery connection patterns, query templates, and ready-to-use analysis scripts.
---

## Related Skills

For visualization:

- `/grafana` - BigQuery dashboards
- `/chart-generator` - Create charts from BigQuery data

For other data sources:

- `/amplitude` - Amplitude product analytics
- `/intercom` - Customer support data export

For authentication:

- `/secret` - gcloud credentials setup

# BigQuery Data Warehouse

Access a BigQuery data warehouse containing production data exports, analytics, and business intelligence views.

## Connection

**Project:** `<GCP_PROJECT_ID>`
**Authentication:** gcloud application default credentials (`~/.config/gcloud/application_default_credentials.json`)

## Python Query Template

```python
from google.cloud import bigquery

# Auto-uses application default credentials
client = bigquery.Client(project='<GCP_PROJECT_ID>')

# Example query
query = """
SELECT customer_id, COUNT(*) as order_count, SUM(revenue) as total_revenue
FROM `<GCP_PROJECT_ID>.<dataset>.<table>`
WHERE created_at >= '2024-01-01'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10
"""

results = client.query(query)
for row in results:
    print(f"Customer {row.customer_id}: {row.order_count} orders, ${row.total_revenue:.2f}")
```

---

## Dataset Overview

Configure datasets to match your project structure. Typical layout:

| Dataset           | Location    | Purpose                                               |
| ----------------- | ----------- | ----------------------------------------------------- |
| `core`            | us-west1    | Core production data (orders, products, billing, ads) |
| `dashboard`       | us-west1    | Dashboard views and metrics (funnel, cohort, NRR)     |
| `analysis`        | us-west1    | Analysis views (revenue, churn, OKR metrics)          |
| `attribution`     | us-west1    | User attribution and behavior analysis                |
| `reporting`       | us-west1    | Looker views and reporting                            |
| `amplitude`       | us-west1    | Product analytics events                              |
| `customer_io`     | us-central1 | Email/marketing campaign data                         |

---

## Common Table Patterns

### orders

E-commerce orders with line items and profit calculations.

| Column              | Type     | Description                |
| ------------------- | -------- | -------------------------- |
| `customer_id`       | INTEGER  | Customer/shop ID           |
| `order_id`          | INTEGER  | Platform order ID          |
| `order_number`      | INTEGER  | Order number               |
| `processed_at`      | STRING   | Order processed timestamp  |
| `created_at`        | STRING   | Order created timestamp    |
| `subtotal_price`    | FLOAT    | Order subtotal             |
| `shipping_cost`     | FLOAT    | Shipping cost              |
| `customer`          | RECORD   | Customer info (ID, Email)  |
| `line_items`        | RECORD[] | Order line items with COGS |

### products

Products with variants and cost of goods sold.

| Column        | Type     | Description                            |
| ------------- | -------- | -------------------------------------- |
| `customer_id` | INTEGER  | Customer/shop ID                       |
| `id`          | INTEGER  | Platform product ID                    |
| `title`       | STRING   | Product title                          |
| `vendor`      | STRING   | Product vendor                         |
| `product_type`| STRING   | Product type                           |
| `cogs`        | FLOAT    | Cost of goods sold                     |
| `variants`    | RECORD[] | Product variants with SKU, price, COGS |
| `created_at`  | STRING   | Created timestamp                      |

### billing

Subscription billing records.

| Column        | Type    | Description         |
| ------------- | ------- | ------------------- |
| `id`          | INTEGER | Billing record ID   |
| `customer_id` | INTEGER | Customer/shop ID    |
| `plan_name`   | STRING  | Plan name           |
| `price`       | FLOAT   | Plan price          |
| `status`      | STRING  | Subscription status |
| `activated_on`| STRING  | Activation date     |
| `trial_ends_on`| STRING | Trial end date      |
| `cancelled_on`| STRING  | Cancellation date   |
| `billing_on`  | STRING  | Billing date        |

### ad_insights

Aggregated ad performance metrics.

| Column           | Type    | Description            |
| ---------------- | ------- | ---------------------- |
| `customer_id`    | INTEGER | Customer/shop ID       |
| `channel`        | STRING  | facebook/google/tiktok |
| `date`           | STRING  | Metrics date           |
| `account_id`     | STRING  | Platform account ID    |
| `campaign_id`    | STRING  | Campaign ID            |
| `ad_group_id`    | STRING  | Ad group ID            |
| `ad_id`          | STRING  | Ad ID                  |
| `impressions`    | INTEGER | Total impressions      |
| `clicks`         | INTEGER | Total clicks           |
| `spend`          | FLOAT   | Ad spend               |
| `purchases`      | INTEGER | Purchase conversions   |
| `purchases_value`| FLOAT   | Purchase value         |

---

## Event Tables

### amplitude.EVENTS_<AMPLITUDE_PROJECT_ID>

Amplitude product analytics events (partitioned by `event_time`).

| Column             | Type      | Description         |
| ------------------ | --------- | ------------------- |
| `event_time`       | TIMESTAMP | Event timestamp     |
| `event_type`       | STRING    | Event type          |
| `user_id`          | STRING    | User identifier     |
| `device_id`        | STRING    | Device identifier   |
| `event_properties` | JSON      | Event-specific data |
| `user_properties`  | JSON      | User attributes     |
| `country`          | STRING    | User country        |
| `city`             | STRING    | User city           |
| `platform`         | STRING    | web/ios/android     |
| `os_name`          | STRING    | Operating system    |

### App event tables (partitioned by `event_timestamp`)

Examples:
- `event_app_install` - App installation events
- `event_app_uninstall` - App uninstallation events
- `event_plan_subscribed` - Plan subscription events
- `event_onboarding` - Onboarding funnel events

---

## Common Query Patterns

### Revenue by Customer

```python
from google.cloud import bigquery

client = bigquery.Client(project='<GCP_PROJECT_ID>')

query = """
SELECT
    customer_id,
    COUNT(*) as order_count,
    SUM(subtotal_price) as revenue,
    AVG(subtotal_price) as avg_order_value
FROM `<GCP_PROJECT_ID>.<dataset>.orders`
WHERE created_at >= '2024-01-01'
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 20
"""

for row in client.query(query):
    print(f"Customer {row.customer_id}: {row.order_count} orders, ${row.revenue:.2f} revenue")
```

### Active Subscriptions

```python
query = """
SELECT
    plan_name,
    COUNT(*) as subscribers,
    SUM(price) as mrr
FROM `<GCP_PROJECT_ID>.<dataset>.billing`
WHERE status = 'active'
GROUP BY plan_name
ORDER BY mrr DESC
"""
```

### Ad Performance by Channel

```python
query = """
SELECT
    channel,
    SUM(spend) as total_spend,
    SUM(purchases) as total_purchases,
    SAFE_DIVIDE(SUM(spend), SUM(purchases)) as cost_per_purchase
FROM `<GCP_PROJECT_ID>.<dataset>.ad_insights`
WHERE date >= '2024-01-01'
GROUP BY channel
ORDER BY total_spend DESC
"""
```

### Product Profit Margins

```python
query = """
SELECT
    p.title,
    p.cogs,
    AVG(v.price) as avg_price,
    AVG(v.price) - p.cogs as margin
FROM `<GCP_PROJECT_ID>.<dataset>.products` p,
UNNEST(variants) as v
WHERE p.cogs > 0
GROUP BY p.title, p.cogs
ORDER BY margin DESC
LIMIT 20
"""
```

### Amplitude Event Analysis

```python
query = """
SELECT
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM `<GCP_PROJECT_ID>.amplitude.EVENTS_<AMPLITUDE_PROJECT_ID>`
WHERE event_time >= TIMESTAMP('2024-01-01')
GROUP BY event_type
ORDER BY event_count DESC
LIMIT 20
"""
```

---

## CLI Query Examples

```bash
# Simple query
bq query --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`<GCP_PROJECT_ID>.<dataset>.<table>\`"

# Query to JSON
bq query --use_legacy_sql=false --format=json \
  "SELECT customer_id, COUNT(*) as cnt FROM \`<GCP_PROJECT_ID>.<dataset>.orders\` GROUP BY 1 LIMIT 10"

# Show table schema
bq show --schema --format=prettyjson <GCP_PROJECT_ID>:<dataset>.<table>

# List tables in dataset
bq ls <GCP_PROJECT_ID>:<dataset>
```

---

## Tips

1. **Partitioned tables:** Event tables are partitioned by timestamp - always include date filters to reduce costs
2. **String dates:** Most date columns are STRING type - use string comparison or PARSE_DATE()
3. **RECORD types:** Use UNNEST() to query nested arrays (line_items, variants)
4. **JSON columns:** Use JSON_EXTRACT_SCALAR() for Amplitude event_properties
5. **Read-only:** These queries are for analysis only - do not modify data
6. **Costs:** BigQuery charges by data scanned - use LIMIT and SELECT specific columns

---

## Authentication

BigQuery uses gcloud application default credentials:

```bash
# Login (one-time)
gcloud auth application-default login

# Set project
gcloud config set project <GCP_PROJECT_ID>

# Verify
gcloud config list
```

Python automatically uses these credentials via `google.cloud.bigquery.Client()`.

---

## Ready-to-Use Scripts

Pre-built scripts for common analytics tasks. Run with `python3 <script>.py --help` for options.

| Script                 | Purpose                                  | Key Options                                                      |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------- |
| `mrr_report.py`        | MRR, NRR, revenue trends, plan breakdown | `--months`, `--section [mrr\|plan\|trend]`                       |
| `cohort_analysis.py`   | Cohort retention, ACL, paid customers    | `--cohorts`, `--section [cohort\|acl\|customers\|funnel]`        |
| `churn_analysis.py`    | Churn patterns, cancellations, tenure    | `--days`, `--section [type\|cancellations\|tenure\|recent]`      |
| `top_customers.py`     | Top revenue customers, growth leaders    | `--customer ID`, `--section [revenue\|paying\|growth\|distribution]` |
| `onboarding_funnel.py` | Step completion, drop-off, timing        | `--days`, `--section [overview\|dropoff\|timing\|device]`        |

### Quick Examples

```bash
# MRR report for last 6 months
python3 mrr_report.py --months 6

# Cohort retention only
python3 cohort_analysis.py --section cohort

# Details for a specific customer
python3 top_customers.py --customer 12345

# Onboarding drop-off analysis
python3 onboarding_funnel.py --section dropoff --days 14
```

---
