#!/usr/bin/env python3
"""
Onboarding Funnel Analysis
Analyzes user onboarding flow, step completion, and drop-off points
"""

from google.cloud import bigquery
import argparse
import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID', '<GCP_PROJECT_ID>')
DASHBOARD_DATASET = os.getenv('BQ_DASHBOARD_DATASET', '<dashboard_dataset>')

client = bigquery.Client(project=PROJECT_ID)


def get_funnel_overview(days: int = 30):
    """Get overall funnel metrics"""
    query = f"""
    SELECT
        COUNT(*) as total_started,
        COUNT(step1_datetime) as step1_completed,
        COUNT(step2_datetime) as step2_completed,
        COUNT(step3_datetime) as step3_completed,
        COUNT(step4_datetime) as step4_completed,
        COUNT(step5_datetime) as step5_completed,
        COUNT(step6_datetime) as step6_completed,
        SAFE_DIVIDE(COUNT(step1_datetime), COUNT(*)) * 100 as step1_rate,
        SAFE_DIVIDE(COUNT(step2_datetime), COUNT(step1_datetime)) * 100 as step2_rate,
        SAFE_DIVIDE(COUNT(step3_datetime), COUNT(step2_datetime)) * 100 as step3_rate,
        SAFE_DIVIDE(COUNT(step4_datetime), COUNT(step3_datetime)) * 100 as step4_rate,
        SAFE_DIVIDE(COUNT(step5_datetime), COUNT(step4_datetime)) * 100 as step5_rate,
        SAFE_DIVIDE(COUNT(step6_datetime), COUNT(step5_datetime)) * 100 as step6_rate,
        SAFE_DIVIDE(COUNT(step6_datetime), COUNT(*)) * 100 as overall_completion_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
    WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = list(client.query(query, job_config=job_config))

    if results:
        r = results[0]
        print(f"\n{'='*70}")
        print(f"ONBOARDING FUNNEL OVERVIEW (Last {days} Days)")
        print(f"{'='*70}\n")

        steps = [
            ("Step 0: Started", r.total_started, 100),
            ("Step 1", r.step1_completed, r.step1_rate),
            ("Step 2", r.step2_completed, r.step2_rate),
            ("Step 3", r.step3_completed, r.step3_rate),
            ("Step 4", r.step4_completed, r.step4_rate),
            ("Step 5", r.step5_completed, r.step5_rate),
            ("Step 6: Completed", r.step6_completed, r.step6_rate),
        ]

        print(f"{'Step':<25} {'Users':>12} {'Step Rate':>12} {'Funnel %':>12}")
        print("-" * 70)

        for name, users, rate in steps:
            funnel_pct = (users / r.total_started * 100) if r.total_started else 0
            rate_str = f"{rate:.1f}%" if rate else "N/A"
            print(f"{name:<25} {users:>12,} {rate_str:>12} {funnel_pct:>11.1f}%")

        print("-" * 70)
        print(f"Overall Completion Rate: {r.overall_completion_rate:.1f}%")


def get_funnel_timing(days: int = 30):
    """Analyze time between onboarding steps"""
    query = f"""
    SELECT
        AVG(mins_from_s0_to_s1) as avg_step1_mins,
        AVG(mins_from_s1_to_s2) as avg_step2_mins,
        AVG(mins_from_s2_to_s3) as avg_step3_mins,
        AVG(mins_from_s3_to_s4) as avg_step4_mins,
        AVG(mins_from_s4_to_s5) as avg_step5_mins,
        AVG(mins_from_s5_to_s6) as avg_step6_mins,
        PERCENTILE_CONT(mins_from_s0_to_s1, 0.5) OVER() as median_step1_mins,
        PERCENTILE_CONT(mins_from_s5_to_s6, 0.5) OVER() as median_final_step_mins
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
    WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
      AND step6_datetime IS NOT NULL
    LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = list(client.query(query, job_config=job_config))

    if results:
        r = results[0]
        print(f"\n{'='*60}")
        print(f"ONBOARDING TIMING ANALYSIS (Last {days} Days)")
        print(f"{'='*60}\n")
        print("Average Time Between Steps (for completed users):\n")

        steps = [
            ("Step 0 → 1", r.avg_step1_mins),
            ("Step 1 → 2", r.avg_step2_mins),
            ("Step 2 → 3", r.avg_step3_mins),
            ("Step 3 → 4", r.avg_step4_mins),
            ("Step 4 → 5", r.avg_step5_mins),
            ("Step 5 → 6", r.avg_step6_mins),
        ]

        for name, mins in steps:
            if mins:
                if mins < 60:
                    print(f"  {name}: {mins:.1f} mins")
                else:
                    print(f"  {name}: {mins/60:.1f} hours ({mins:.0f} mins)")


def get_funnel_by_device(days: int = 30):
    """Analyze onboarding completion by device type"""
    query = f"""
    SELECT
        COALESCE(device, 'unknown') as device_type,
        COUNT(*) as total_started,
        COUNT(step6_datetime) as completed,
        SAFE_DIVIDE(COUNT(step6_datetime), COUNT(*)) * 100 as completion_rate,
        AVG(TIMESTAMP_DIFF(step6_datetime, step0_datetime, MINUTE)) as avg_completion_mins
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
    WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
    GROUP BY device
    ORDER BY total_started DESC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*70}")
    print(f"ONBOARDING BY DEVICE (Last {days} Days)")
    print(f"{'='*70}\n")
    print(f"{'Device':<20} {'Started':>12} {'Completed':>12} {'Rate':>10} {'Avg Time':>12}")
    print("-" * 70)

    for row in results:
        avg_time = f"{row.avg_completion_mins:.0f} mins" if row.avg_completion_mins else "N/A"
        print(f"{row.device_type:<20} {row.total_started:>12,} {row.completed:>12,} "
              f"{row.completion_rate:>9.1f}% {avg_time:>12}")


def get_funnel_by_app_version(days: int = 30):
    """Analyze onboarding by app version"""
    query = f"""
    SELECT
        COALESCE(app_version, 'unknown') as version,
        COUNT(*) as total_started,
        COUNT(step6_datetime) as completed,
        SAFE_DIVIDE(COUNT(step6_datetime), COUNT(*)) * 100 as completion_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
    WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
    GROUP BY app_version
    ORDER BY total_started DESC
    LIMIT 10
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*60}")
    print(f"ONBOARDING BY APP VERSION (Last {days} Days)")
    print(f"{'='*60}\n")
    print(f"{'Version':<25} {'Started':>12} {'Completed':>10} {'Rate':>10}")
    print("-" * 60)

    for row in results:
        print(f"{row.version:<25} {row.total_started:>12,} {row.completed:>10,} {row.completion_rate:>9.1f}%")


def get_dropoff_analysis(days: int = 30):
    """Analyze where users drop off in the funnel"""
    query = f"""
    WITH funnel AS (
        SELECT
            customer_id,
            CASE
                WHEN step6_datetime IS NOT NULL THEN 'Completed'
                WHEN step5_datetime IS NOT NULL THEN 'Dropped at Step 6'
                WHEN step4_datetime IS NOT NULL THEN 'Dropped at Step 5'
                WHEN step3_datetime IS NOT NULL THEN 'Dropped at Step 4'
                WHEN step2_datetime IS NOT NULL THEN 'Dropped at Step 3'
                WHEN step1_datetime IS NOT NULL THEN 'Dropped at Step 2'
                WHEN step0_datetime IS NOT NULL THEN 'Dropped at Step 1'
                ELSE 'Never started'
            END as status
        FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
        WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
    )
    SELECT
        status,
        COUNT(*) as user_count,
        SAFE_DIVIDE(COUNT(*), SUM(COUNT(*)) OVER()) * 100 as percentage
    FROM funnel
    GROUP BY status
    ORDER BY
        CASE status
            WHEN 'Completed' THEN 1
            WHEN 'Dropped at Step 6' THEN 2
            WHEN 'Dropped at Step 5' THEN 3
            WHEN 'Dropped at Step 4' THEN 4
            WHEN 'Dropped at Step 3' THEN 5
            WHEN 'Dropped at Step 2' THEN 6
            WHEN 'Dropped at Step 1' THEN 7
            ELSE 8
        END
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*60}")
    print(f"DROP-OFF ANALYSIS (Last {days} Days)")
    print(f"{'='*60}\n")
    print(f"{'Status':<25} {'Users':>12} {'Percentage':>12}")
    print("-" * 60)

    for row in results:
        print(f"{row.status:<25} {row.user_count:>12,} {row.percentage:>11.1f}%")


def get_daily_funnel_trend(days: int = 30):
    """Get daily funnel completion trend"""
    query = f"""
    SELECT
        DATE(step0_datetime) as date,
        COUNT(*) as started,
        COUNT(step6_datetime) as completed,
        SAFE_DIVIDE(COUNT(step6_datetime), COUNT(*)) * 100 as completion_rate
    FROM `{PROJECT_ID}.{DASHBOARD_DATASET}.onboarding_funnel`
    WHERE step0_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
    GROUP BY date
    ORDER BY date DESC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("days", "INT64", days)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*55}")
    print(f"DAILY FUNNEL TREND (Last {days} Days)")
    print(f"{'='*55}\n")
    print(f"{'Date':<12} {'Started':>10} {'Completed':>12} {'Rate':>10}")
    print("-" * 55)

    for row in results:
        print(f"{str(row.date):<12} {row.started:>10,} {row.completed:>12,} {row.completion_rate:>9.1f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Onboarding Funnel Analysis')
    parser.add_argument('--days', type=int, default=30, help='Days to look back')
    parser.add_argument('--section', choices=['all', 'overview', 'timing', 'device', 'version', 'dropoff', 'trend'],
                        default='all', help='Which section to show')
    args = parser.parse_args()

    if args.section in ['all', 'overview']:
        get_funnel_overview(args.days)
    if args.section in ['all', 'dropoff']:
        get_dropoff_analysis(args.days)
    if args.section in ['all', 'timing']:
        get_funnel_timing(args.days)
    if args.section in ['all', 'device']:
        get_funnel_by_device(args.days)
    if args.section in ['all', 'version']:
        get_funnel_by_app_version(args.days)
    if args.section in ['all', 'trend']:
        get_daily_funnel_trend(args.days)
