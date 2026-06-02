#!/usr/bin/env python3
"""
Top Customers Analysis
Analyzes top revenue-generating customers and their metrics
"""

from google.cloud import bigquery
import argparse
import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID', '<GCP_PROJECT_ID>')
DATASET = os.getenv('BQ_DATASET', '<dataset>')

client = bigquery.Client(project=PROJECT_ID)


def get_top_customers_by_orders(limit: int = 20, days: int = 90):
    """Get top customers by order volume and revenue"""
    query = f"""
    SELECT
        customer_id,
        COUNT(*) as order_count,
        SUM(subtotal_price) as total_revenue,
        AVG(subtotal_price) as avg_order_value,
        MIN(processed_at) as first_order,
        MAX(processed_at) as last_order
    FROM `{PROJECT_ID}.{DATASET}.orders`
    WHERE processed_at >= FORMAT_DATE('%Y-%m-%d', DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY))
    GROUP BY customer_id
    ORDER BY total_revenue DESC
    LIMIT @limit
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("days", "INT64", days),
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*100}")
    print(f"TOP CUSTOMERS BY REVENUE (Last {days} Days)")
    print(f"{'='*100}\n")
    print(f"{'Rank':>4} {'CustomerID':>12} {'Orders':>10} {'Revenue':>14} {'AOV':>10} {'Last Order':<12}")
    print("-" * 100)

    for i, row in enumerate(results, 1):
        print(f"{i:>4} {row.customer_id:>12} {row.order_count:>10,} ${row.total_revenue:>12,.2f} "
              f"${row.avg_order_value:>8,.2f} {row.last_order[:10]:<12}")


def get_top_paying_customers(limit: int = 20):
    """Get top paying subscription customers"""
    query = f"""
    WITH customer_revenue AS (
        SELECT
            customer_id,
            STRING_AGG(DISTINCT plan_name, ', ') as plans,
            MAX(price) as current_price,
            MIN(activated_on) as first_subscription,
            COUNT(*) as subscription_count
        FROM `{PROJECT_ID}.{DATASET}.billing`
        WHERE status = 'active'
        GROUP BY customer_id
    )
    SELECT
        customer_id,
        plans,
        current_price,
        first_subscription,
        subscription_count
    FROM customer_revenue
    ORDER BY current_price DESC
    LIMIT @limit
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", limit)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*90}")
    print("TOP PAYING SUBSCRIBERS")
    print(f"{'='*90}\n")
    print(f"{'Rank':>4} {'CustomerID':>12} {'Plan(s)':<30} {'Price':>10} {'Since':<12}")
    print("-" * 90)

    for i, row in enumerate(results, 1):
        plans = row.plans[:28] + '..' if len(row.plans) > 30 else row.plans
        print(f"{i:>4} {row.customer_id:>12} {plans:<30} ${row.current_price:>8,.0f} {row.first_subscription:<12}")


def get_customer_growth_leaders(limit: int = 20):
    """Get customers with highest growth in order volume"""
    query = f"""
    WITH monthly_orders AS (
        SELECT
            customer_id,
            DATE_TRUNC(PARSE_DATE('%Y-%m-%d', SUBSTR(processed_at, 1, 10)), MONTH) as order_month,
            COUNT(*) as orders,
            SUM(subtotal_price) as revenue
        FROM `{PROJECT_ID}.{DATASET}.orders`
        WHERE processed_at >= FORMAT_DATE('%Y-%m-%d', DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH))
        GROUP BY customer_id, order_month
    ),
    growth AS (
        SELECT
            customer_id,
            MAX(orders) as max_monthly_orders,
            MAX(revenue) as max_monthly_revenue,
            MIN(orders) as min_monthly_orders,
            AVG(orders) as avg_monthly_orders,
            SAFE_DIVIDE(MAX(orders) - MIN(orders), MIN(orders)) * 100 as order_growth_pct
        FROM monthly_orders
        GROUP BY customer_id
        HAVING COUNT(*) >= 3  -- At least 3 months of data
    )
    SELECT *
    FROM growth
    WHERE order_growth_pct > 0
    ORDER BY order_growth_pct DESC
    LIMIT @limit
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("limit", "INT64", limit)]
    )

    results = client.query(query, job_config=job_config)

    print(f"\n{'='*90}")
    print("FASTEST GROWING CUSTOMERS (Last 6 Months)")
    print(f"{'='*90}\n")
    print(f"{'Rank':>4} {'CustomerID':>12} {'Min Orders':>12} {'Max Orders':>12} {'Avg Orders':>12} {'Growth':>10}")
    print("-" * 90)

    for i, row in enumerate(results, 1):
        print(f"{i:>4} {row.customer_id:>12} {row.min_monthly_orders:>12,.0f} {row.max_monthly_orders:>12,.0f} "
              f"{row.avg_monthly_orders:>12,.1f} {row.order_growth_pct:>9.1f}%")


def get_customer_details(customer_id: int):
    """Get detailed information about a specific customer"""
    # Orders summary
    orders_query = f"""
    SELECT
        COUNT(*) as total_orders,
        SUM(subtotal_price) as total_revenue,
        AVG(subtotal_price) as avg_order_value,
        MIN(processed_at) as first_order,
        MAX(processed_at) as last_order
    FROM `{PROJECT_ID}.{DATASET}.orders`
    WHERE customer_id = @customer_id
    """

    # Billing info
    billing_query = f"""
    SELECT
        plan_name as plan,
        price,
        status,
        activated_on,
        cancelled_on
    FROM `{PROJECT_ID}.{DATASET}.billing`
    WHERE customer_id = @customer_id
    ORDER BY activated_on DESC
    LIMIT 5
    """

    # Products count
    products_query = f"""
    SELECT COUNT(*) as product_count
    FROM `{PROJECT_ID}.{DATASET}.products`
    WHERE customer_id = @customer_id
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("customer_id", "INT64", customer_id)]
    )

    print(f"\n{'='*60}")
    print(f"CUSTOMER DETAILS: {customer_id}")
    print(f"{'='*60}\n")

    # Orders
    orders = list(client.query(orders_query, job_config=job_config))
    if orders and orders[0].total_orders:
        o = orders[0]
        print("ORDERS SUMMARY:")
        print(f"  Total Orders:     {o.total_orders:>10,}")
        print(f"  Total Revenue:    ${o.total_revenue:>10,.2f}")
        print(f"  Avg Order Value:  ${o.avg_order_value:>10,.2f}")
        print(f"  First Order:      {o.first_order}")
        print(f"  Last Order:       {o.last_order}")
    else:
        print("ORDERS: No orders found")

    # Products
    products = list(client.query(products_query, job_config=job_config))
    if products:
        print(f"\nPRODUCTS: {products[0].product_count:,}")

    # Billing
    billing = list(client.query(billing_query, job_config=job_config))
    if billing:
        print("\nSUBSCRIPTION HISTORY:")
        print(f"  {'Plan':<25} {'Price':>8} {'Status':<12} {'Activated':<12}")
        print("  " + "-" * 55)
        for b in billing:
            print(f"  {b.plan:<25} ${b.price:>6,.0f} {b.status:<12} {b.activated_on:<12}")


def get_customer_distribution():
    """Get customer distribution by order volume"""
    query = f"""
    WITH customer_orders AS (
        SELECT
            customer_id,
            COUNT(*) as order_count
        FROM `{PROJECT_ID}.{DATASET}.orders`
        WHERE processed_at >= FORMAT_DATE('%Y-%m-%d', DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
        GROUP BY customer_id
    )
    SELECT
        CASE
            WHEN order_count <= 10 THEN '1-10'
            WHEN order_count <= 50 THEN '11-50'
            WHEN order_count <= 100 THEN '51-100'
            WHEN order_count <= 500 THEN '101-500'
            WHEN order_count <= 1000 THEN '501-1000'
            WHEN order_count <= 5000 THEN '1001-5000'
            ELSE '5000+'
        END as order_bucket,
        COUNT(*) as customer_count
    FROM customer_orders
    GROUP BY 1
    ORDER BY
        CASE
            WHEN order_bucket = '1-10' THEN 1
            WHEN order_bucket = '11-50' THEN 2
            WHEN order_bucket = '51-100' THEN 3
            WHEN order_bucket = '101-500' THEN 4
            WHEN order_bucket = '501-1000' THEN 5
            WHEN order_bucket = '1001-5000' THEN 6
            ELSE 7
        END
    """

    results = client.query(query)

    print(f"\n{'='*40}")
    print("CUSTOMER DISTRIBUTION BY ORDER VOLUME (90 Days)")
    print(f"{'='*40}\n")
    print(f"{'Orders':<15} {'Customers':>12}")
    print("-" * 40)

    total = 0
    for row in results:
        print(f"{row.order_bucket:<15} {row.customer_count:>12,}")
        total += row.customer_count

    print("-" * 40)
    print(f"{'TOTAL':<15} {total:>12,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Top Customers Analysis')
    parser.add_argument('--limit', type=int, default=20, help='Number of top customers to show')
    parser.add_argument('--days', type=int, default=90, help='Days to look back')
    parser.add_argument('--customer', type=int, help='Specific customer ID to analyze')
    parser.add_argument('--section', choices=['all', 'revenue', 'paying', 'growth', 'distribution', 'details'],
                        default='all', help='Which section to show')
    args = parser.parse_args()

    if args.customer:
        get_customer_details(args.customer)
    else:
        if args.section in ['all', 'revenue']:
            get_top_customers_by_orders(args.limit, args.days)
        if args.section in ['all', 'paying']:
            get_top_paying_customers(args.limit)
        if args.section in ['all', 'growth']:
            get_customer_growth_leaders(args.limit)
        if args.section in ['all', 'distribution']:
            get_customer_distribution()
