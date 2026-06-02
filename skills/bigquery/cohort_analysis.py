#!/usr/bin/env python3
"""
Cohort Retention Analysis
Analyzes customer retention by signup cohort month
"""

from google.cloud import bigquery
import argparse
import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID', '<GCP_PROJECT_ID>')
DASHBOARD_DATASET = os.getenv('BQ_DASHBOARD_DATASET', '<dashboard_dataset>')

client = bigquery.Client(project=PROJECT_ID)


def get_cohort_retention(cohorts: int = 12):
    """Get cohort retention data"""
    query = f"""
    SELECT
        cohort_month,
        paid_period,
        paid_customers,
        paid_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.cohort_retention`
    WHERE cohort_month >= DATE_SUB(CURRENT_DATE(), INTERVAL @cohorts MONTH)
    ORDER BY cohort_month DESC, paid_period ASC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("cohorts", "INT64", cohorts)]
    )

    results = list(client.query(query, job_config=job_config))

    # Organize by cohort
    cohorts_data = {}
    for row in results:
        cohort = str(row.cohort_month)
        if cohort not in cohorts_data:
            cohorts_data[cohort] = {}
        cohorts_data[cohort][row.paid_period] = {
            'customers': row.paid_customers,
            'rate': row.paid_rate
        }

    # Find max period
    max_period = max(row.paid_period for row in results) if results else 0

    print(f"\n{'='*120}")
    print("COHORT RETENTION ANALYSIS")
    print(f"{'='*120}\n")

    # Header
    header = f"{'Cohort':<12}"
    for p in range(max_period + 1):
        header += f"{'M'+str(p):>8}"
    print(header)
    print("-" * 120)

    # Data rows
    for cohort in sorted(cohorts_data.keys(), reverse=True):
        row_str = f"{cohort:<12}"
        for p in range(max_period + 1):
            if p in cohorts_data[cohort]:
                rate = cohorts_data[cohort][p]['rate']
                row_str += f"{rate:>7.1f}%"
            else:
                row_str += f"{'':>8}"
        print(row_str)


def get_acl_metrics():
    """Get Average Customer Lifetime metrics"""
    query = f"""
    SELECT
        report_month,
        cumulative_customers,
        total_timespan,
        avg_timespan
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.avg_customer_lifetime`
    ORDER BY report_month DESC
    LIMIT 12
    """

    results = client.query(query)

    print(f"\n{'='*70}")
    print("AVERAGE CUSTOMER LIFETIME (ACL)")
    print(f"{'='*70}\n")
    print(f"{'Month':<12} {'Cumulative Customers':>22} {'Total Timespan':>16} {'Avg Lifetime':>14}")
    print("-" * 70)

    for row in results:
        print(f"{row.report_month:<12} {row.cumulative_customers:>22,} {row.total_timespan:>16,.0f} {row.avg_timespan:>12.2f} mo")


def get_paid_customers():
    """Get paid customer analysis"""
    query = f"""
    SELECT
        cal_month,
        active_customers,
        paying_customers,
        new_paying_customers,
        churn_paying_customers,
        paying_churn_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.paid_customers_by_month`
    ORDER BY cal_month DESC
    LIMIT 12
    """

    results = client.query(query)

    print(f"\n{'='*90}")
    print("PAID CUSTOMER ANALYSIS")
    print(f"{'='*90}\n")
    print(f"{'Month':<12} {'Active':>10} {'Paying':>10} {'New Paid':>10} {'Churned':>10} {'Churn Rate':>12}")
    print("-" * 90)

    for row in results:
        print(f"{row.cal_month:<12} {row.active_customers:>10,} {row.paying_customers:>10,} "
              f"{row.new_paying_customers:>10,} {row.churn_paying_customers:>10,} {row.paying_churn_rate:>11.2f}%")


def get_funnel_conversion():
    """Get conversion funnel metrics"""
    query = f"""
    SELECT
        COUNT(*) as total_installs,
        COUNT(activated_date) as activated,
        COUNT(first_paid_date) as converted_to_paid,
        SAFE_DIVIDE(COUNT(activated_date), COUNT(*)) * 100 as activation_rate,
        SAFE_DIVIDE(COUNT(first_paid_date), COUNT(activated_date)) * 100 as conversion_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.customer_funnel`
    WHERE installed_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    """

    results = list(client.query(query))
    if results:
        row = results[0]
        print(f"\n{'='*50}")
        print("FUNNEL CONVERSION (Last 90 Days)")
        print(f"{'='*50}\n")
        print(f"Total Installs:    {row.total_installs:>10,}")
        print(f"Activated:         {row.activated:>10,} ({row.activation_rate:.1f}%)")
        print(f"Converted to Paid: {row.converted_to_paid:>10,} ({row.conversion_rate:.1f}% of activated)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cohort Retention Analysis')
    parser.add_argument('--cohorts', type=int, default=12, help='Number of cohort months to analyze')
    parser.add_argument('--section', choices=['all', 'cohort', 'acl', 'customers', 'funnel'], default='all',
                        help='Which section to show')
    args = parser.parse_args()

    if args.section in ['all', 'cohort']:
        get_cohort_retention(args.cohorts)
    if args.section in ['all', 'acl']:
        get_acl_metrics()
    if args.section in ['all', 'customers']:
        get_paid_customers()
    if args.section in ['all', 'funnel']:
        get_funnel_conversion()
