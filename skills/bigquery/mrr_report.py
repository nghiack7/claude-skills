#!/usr/bin/env python3
"""
MRR (Monthly Recurring Revenue) Report
Generates monthly revenue metrics: MRR, new MRR, churned MRR, expansion, NRR
"""

from google.cloud import bigquery
import argparse
import os
from datetime import datetime

PROJECT_ID = os.getenv('GCP_PROJECT_ID', '<GCP_PROJECT_ID>')
DASHBOARD_DATASET = os.getenv('BQ_DASHBOARD_DATASET', '<dashboard_dataset>')
CORE_DATASET = os.getenv('BQ_CORE_DATASET', '<core_dataset>')

client = bigquery.Client(project=PROJECT_ID)


def get_mrr_report(months: int = 12):
    """Get MRR breakdown for the last N months"""
    query = f"""
    SELECT
        report_month,
        MRR,
        new_MRR,
        expansion_MRR,
        contraction_MRR,
        churned_MRR,
        NRR,
        GRR
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.nrr_by_month`
    ORDER BY report_month DESC
    LIMIT @months
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("months", "INT64", months)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*80}")
    print(f"MRR REPORT - Last {months} Months")
    print(f"{'='*80}\n")
    print(f"{'Month':<12} {'MRR':>12} {'New':>10} {'Expansion':>10} {'Contraction':>12} {'Churned':>10} {'NRR':>8} {'GRR':>8}")
    print("-" * 80)

    for row in results:
        print(f"{row.report_month:<12} ${row.MRR:>10,.0f} ${row.new_MRR:>8,.0f} ${row.expansion_MRR:>8,.0f} "
              f"${row.contraction_MRR:>10,.0f} ${row.churned_MRR:>8,.0f} {row.NRR:>7.1f}% {row.GRR:>7.1f}%")


def get_revenue_by_plan():
    """Get current MRR breakdown by plan"""
    query = f"""
    SELECT
        plan_name,
        COUNT(*) as subscribers,
        SUM(price) as mrr,
        AVG(price) as avg_price
    FROM `{PROJECT_ID}.{CORE_DATASET}.billing`
    WHERE status = 'active'
    GROUP BY plan_name
    ORDER BY mrr DESC
    """

    results = client.query(query)

    print(f"\n{'='*60}")
    print("CURRENT MRR BY PLAN")
    print(f"{'='*60}\n")
    print(f"{'Plan':<30} {'Subs':>8} {'MRR':>12} {'Avg Price':>10}")
    print("-" * 60)

    total_subs = 0
    total_mrr = 0

    for row in results:
        print(f"{row.plan_name:<30} {row.subscribers:>8} ${row.mrr:>10,.2f} ${row.avg_price:>8,.2f}")
        total_subs += row.subscribers
        total_mrr += row.mrr

    print("-" * 60)
    print(f"{'TOTAL':<30} {total_subs:>8} ${total_mrr:>10,.2f}")


def get_revenue_trend():
    """Get monthly revenue trend"""
    query = f"""
    SELECT
        cal_month,
        recurring_revenue,
        usage_based_revenue,
        total_revenue,
        net_revenue,
        ARPPU,
        CLTV
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.revenue_by_month`
    ORDER BY cal_month DESC
    LIMIT 12
    """

    results = client.query(query)

    print(f"\n{'='*100}")
    print("MONTHLY REVENUE TREND")
    print(f"{'='*100}\n")
    print(f"{'Month':<12} {'Recurring':>12} {'Usage':>10} {'Total':>12} {'Net':>12} {'ARPPU':>10} {'CLTV':>10}")
    print("-" * 100)

    for row in results:
        print(f"{row.cal_month:<12} ${row.recurring_revenue:>10,.0f} ${row.usage_based_revenue:>8,.0f} "
              f"${row.total_revenue:>10,.0f} ${row.net_revenue:>10,.0f} ${row.ARPPU:>8,.2f} ${row.CLTV:>8,.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MRR Report Generator')
    parser.add_argument('--months', type=int, default=12, help='Number of months to show')
    parser.add_argument('--section', choices=['all', 'mrr', 'plan', 'trend'], default='all',
                        help='Which section to show')
    args = parser.parse_args()

    if args.section in ['all', 'mrr']:
        get_mrr_report(args.months)
    if args.section in ['all', 'plan']:
        get_revenue_by_plan()
    if args.section in ['all', 'trend']:
        get_revenue_trend()
