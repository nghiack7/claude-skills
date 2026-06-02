#!/usr/bin/env python3
"""
Get event volumes/counts for date range.

Usage:
    python event_volumes.py --start 20241101 --end 20241130
    python event_volumes.py --days 30
    python event_volumes.py --days 7 --event "COGs - Save COGs Success"
"""

import argparse
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('secret/services/amplitude.env')

API_KEY = os.getenv('AMPLITUDE_API_KEY')
SECRET_KEY = os.getenv('AMPLITUDE_SECRET_KEY')


def get_event_types() -> list:
    """Get all event types from taxonomy."""
    response = requests.get(
        'https://amplitude.com/api/2/taxonomy/event',
        auth=(API_KEY, SECRET_KEY)
    )
    if response.status_code == 200:
        return [e['event_type'] for e in response.json().get('data', [])]
    return []


def get_event_volume(event_type: str, start: str, end: str) -> int:
    """Get total event count for a date range."""
    response = requests.get(
        'https://amplitude.com/api/2/events/segmentation',
        params={
            'e': json.dumps({"event_type": event_type}),
            'start': start,
            'end': end,
            'm': 'totals'
        },
        auth=(API_KEY, SECRET_KEY),
        timeout=60
    )

    if response.status_code == 200:
        data = response.json().get('data', {})
        series = data.get('series', [[0]])
        return sum(series[0]) if series and series[0] else 0
    return 0


def get_event_unique_users(event_type: str, start: str, end: str) -> int:
    """Get unique users for an event."""
    response = requests.get(
        'https://amplitude.com/api/2/events/segmentation',
        params={
            'e': json.dumps({"event_type": event_type}),
            'start': start,
            'end': end,
            'm': 'uniques'
        },
        auth=(API_KEY, SECRET_KEY),
        timeout=60
    )

    if response.status_code == 200:
        data = response.json().get('data', {})
        series = data.get('series', [[0]])
        return sum(series[0]) if series and series[0] else 0
    return 0


def main():
    parser = argparse.ArgumentParser(description='Get Amplitude event volumes')
    parser.add_argument('--start', help='Start date (YYYYMMDD)')
    parser.add_argument('--end', help='End date (YYYYMMDD)')
    parser.add_argument('--days', type=int, help='Last N days')
    parser.add_argument('--event', '-e', help='Specific event type')
    parser.add_argument('--top', type=int, default=20, help='Show top N events')
    parser.add_argument('--category', '-c', help='Filter by category prefix')
    args = parser.parse_args()

    if args.days:
        end = datetime.now()
        start = end - timedelta(days=args.days)
        start_str = start.strftime('%Y%m%d')
        end_str = end.strftime('%Y%m%d')
    elif args.start and args.end:
        start_str = args.start
        end_str = args.end
    else:
        parser.error('Either --days or --start/--end required')
        return

    print(f"Event volumes from {start_str} to {end_str}\n")

    if args.event:
        # Single event details
        vol = get_event_volume(args.event, start_str, end_str)
        users = get_event_unique_users(args.event, start_str, end_str)
        print(f"Event: {args.event}")
        print(f"  Total: {vol:,}")
        print(f"  Unique users: {users:,}")
        if users > 0:
            print(f"  Avg per user: {vol/users:.1f}")
    else:
        # All events
        event_types = get_event_types()

        if args.category:
            event_types = [e for e in event_types if e.startswith(args.category)]

        print(f"Checking {len(event_types)} event types...")

        results = []
        for i, event_type in enumerate(event_types):
            vol = get_event_volume(event_type, start_str, end_str)
            if vol > 0:
                results.append((event_type, vol))
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{len(event_types)}")

        results.sort(key=lambda x: -x[1])

        print(f"\nTop {args.top} events by volume:")
        print("-" * 50)
        for name, vol in results[:args.top]:
            print(f"  {vol:>10,}  {name}")


if __name__ == '__main__':
    main()
