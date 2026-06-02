#!/usr/bin/env python3
"""
Churn Analysis
Analyzes customer churn patterns, uninstalls, and cancellations
"""

from google.cloud import bigquery
import argparse
import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID', '<GCP_PROJECT_ID>')
DATASET = os.getenv('BQ_DATASET', '<dataset>')

client = bigquery.Client(project=PROJECT_ID)


def get_uninstall_by_type():
    """Get uninstall breakdown by type"""
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.uninstalled_type`
    ORDER BY 1 DESC
    LIMIT 12
    """

    results = client.query(query)
    rows = list(results)

    print(f"\n{'='*80}")
    print("UNINSTALL BY TYPE")
    print(f"{'='*80}\n")

    if rows:
        schema = results.schema
        headers = [field.name for field in schema]
        print(" | ".join(f"{h:<15}" for h in headers))
        print("-" * 80)

        for row in rows:
            values = [str(getattr(row, h, '')) for h in headers]
            print(" | ".join(f"{v:<15}" for v in values))


def get_churn_by_customer_type():
    """Get churn breakdown by customer type"""
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.churn_by_type`
    ORDER BY 1 DESC
    LIMIT 20
    """

    results = client.query(query)
    rows = list(results)

    print(f"\n{'='*80}")
    print("CHURN BY CUSTOMER TYPE")
    print(f"{'='*80}\n")

    if rows:
        schema = results.schema
        headers = [field.name for field in schema]
        print(" | ".join(f"{h:<15}" for h in headers[:6]))  # First 6 columns
        print("-" * 80)

        for row in rows:
            values = [str(getattr(row, h, ''))[:15] for h in headers[:6]]
            print(" | ".join(f"{v:<15}" for v in values))


def get_cancellation_trends():
    """Get subscription cancellation trends"""
    query = f"""
    SELECT
        DATE_TRUNC(PARSE_DATE('%Y-%m-%d', cancelled_on), MONTH) as cancel_month,
        plan_name,
        COUNT(*) as cancellations,
        SUM(price) as lost_mrr
    FROM `{PROJECT_ID}.{DATASET}.billing`
    WHERE cancelled_on IS NOT NULL
      AND cancelled_on != ''
      AND PARSE_DATE('%Y-%m-%d', cancelled_on) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
    GROUP BY 1, 2
    ORDER BY 1 DESC, 4 DESC
    """

    results = client.query(query)

    print(f"\n{'='*70}")
    print("CANCELLATION TRENDS (Last 12 Months)")
    print(f"{'='*70}\n")
    print(f"{'Month':<12} {'Plan':<25} {'Cancellations':>14} {'Lost MRR':>12}")
    print("-" * 70)

    current_month = None
    for row in results:
        month_str = str(row.cancel_month)
        if month_str != current_month:
            if current_month:
                print()
            current_month = month_str
        print(f"{month_str:<12} {row.plan_name:<25} {row.cancellations:>14,} ${row.lost_mrr:>10,.2f}")


def get_recent_churned_customers(days: int = 30):
    """Get recently churned customers with details"""
    query = f"""
    WITH churned AS (
        SELECT
            customer_id,
            plan_name,
            price,
            activated_on,
            cancelled_on,
            DATE_DIFF(
                PARSE_DATE('%Y-%m-%d', cancelled_on),
                PARSE_DATE('%Y-%m-%d', activated_on),
                DAY
            ) as days_subscribed
        FROM `{PROJECT_ID}.{DATASET}.billing`
        WHERE cancelled_on IS NOT NULL
          AND cancelled_on != ''
          AND PARSE_DATE('%Y-%m-%d', cancelled_on) >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
    )
    SELECT
        customer_id,
        plan_name,
        price,
        activated_on,
        cancelled_on,
        days_subscribed
    FROM churned
    ORDER BY cancelled_on DESC
    LIMIT 50
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*100}")
    print(f"RECENTLY CHURNED CUSTOMERS (Last {days} Days)")
    print(f"{'='*100}\n")
    print(f"{'CustomerID':>12} {'Plan':<25} {'Price':>8} {'Activated':<12} {'Cancelled':<12} {'Days Sub':>10}")
    print("-" * 100)

    for row in results:
        print(f"{row.customer_id:>12} {row.plan_name:<25} ${row.price:>6,.0f} "
              f"{row.activated_on:<12} {row.cancelled_on:<12} {row.days_subscribed:>10}")


def get_churn_by_tenure():
    """Analyze churn by subscription tenure"""
    query = f"""
    WITH churned AS (
        SELECT
            DATE_DIFF(
                PARSE_DATE('%Y-%m-%d', cancelled_on),
                PARSE_DATE('%Y-%m-%d', activated_on),
                DAY
            ) as days_subscribed,
            price
        FROM `{PROJECT_ID}.{DATASET}.billing`
        WHERE cancelled_on IS NOT NULL
          AND cancelled_on != ''
          AND PARSE_DATE('%Y-%m-%d', cancelled_on) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
    )
    SELECT
        CASE
            WHEN days_subscribed <= 7 THEN '0-7 days'
            WHEN days_subscribed <= 30 THEN '8-30 days'
            WHEN days_subscribed <= 90 THEN '1-3 months'
            WHEN days_subscribed <= 180 THEN '3-6 months'
            WHEN days_subscribed <= 365 THEN '6-12 months'
            ELSE '12+ months'
        END as tenure_bucket,
        COUNT(*) as churned_count,
        SUM(price) as lost_mrr,
        AVG(price) as avg_price
    FROM churned
    GROUP BY 1
    ORDER BY
        CASE
            WHEN tenure_bucket = '0-7 days' THEN 1
            WHEN tenure_bucket = '8-30 days' THEN 2
            WHEN tenure_bucket = '1-3 months' THEN 3
            WHEN tenure_bucket = '3-6 months' THEN 4
            WHEN tenure_bucket = '6-12 months' THEN 5
            ELSE 6
        END
    """

    results = client.query(query)

    print(f"\n{'='*60}")
    print("CHURN BY SUBSCRIPTION TENURE (Last 12 Months)")
    print(f"{'='*60}\n")
    print(f"{'Tenure':<15} {'Churned':>10} {'Lost MRR':>12} {'Avg Price':>12}")
    print("-" * 60)

    total_churned = 0
    total_lost = 0
    for row in results:
        print(f"{row.tenure_bucket:<15} {row.churned_count:>10,} ${row.lost_mrr:>10,.0f} ${row.avg_price:>10,.2f}")
        total_churned += row.churned_count
        total_lost += row.lost_mrr

    print("-" * 60)
    print(f"{'TOTAL':<15} {total_churned:>10,} ${total_lost:>10,.0f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Churn Analysis')
    parser.add_argument('--days', type=int, default=30, help='Days to look back for recent churn')
    parser.add_argument('--section', choices=['all', 'type', 'cancellations', 'recent', 'tenure'], default='all',
                        help='Which section to show')
    args = parser.parse_args()

    if args.section in ['all', 'type']:
        get_uninstall_by_type()
    if args.section in ['all', 'cancellations']:
        get_cancellation_trends()
    if args.section in ['all', 'tenure']:
        get_churn_by_tenure()
    if args.section in ['all', 'recent']:
        get_recent_churned_customers(args.days)
