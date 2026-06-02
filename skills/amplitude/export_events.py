#!/usr/bin/env python3
"""
Export Amplitude events for a date range to JSON file.

Usage:
    python export_events.py --start 20241201T00 --end 20241201T23 --output events.json
    python export_events.py --days 7  # Last 7 days
"""

import argparse
import gzip
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('secret/services/amplitude.env')

API_KEY = os.getenv('AMPLITUDE_API_KEY')
SECRET_KEY = os.getenv('AMPLITUDE_SECRET_KEY')


def export_events(start: str, end: str) -> list:
    """Export events for a time range. Format: YYYYMMDDTHH"""
    response = requests.get(
        'https://amplitude.com/api/2/export',
        params={'start': start, 'end': end},
        auth=(API_KEY, SECRET_KEY)
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    content = gzip.decompress(response.content)
    events = [json.loads(line) for line in content.decode().strip().split('\n') if line]
    return events


def main():
    parser = argparse.ArgumentParser(description='Export Amplitude events')
    parser.add_argument('--start', help='Start time (YYYYMMDDTHH)')
    parser.add_argument('--end', help='End time (YYYYMMDDTHH)')
    parser.add_argument('--days', type=int, help='Export last N days')
    parser.add_argument('--output', '-o', default='amplitude_events.json', help='Output file')
    args = parser.parse_args()

    if args.days:
        end = datetime.now()
        start = end - timedelta(days=args.days)
        start_str = start.strftime('%Y%m%dT00')
        end_str = end.strftime('%Y%m%dT%H')
    elif args.start and args.end:
        start_str = args.start
        end_str = args.end
    else:
        parser.error('Either --days or --start/--end required')
        return

    print(f"Exporting events from {start_str} to {end_str}...")
    events = export_events(start_str, end_str)

    with open(args.output, 'w') as f:
        json.dump(events, f, indent=2)

    print(f"Exported {len(events):,} events to {args.output}")

    # Summary by event type
    if events:
        by_type = {}
        for e in events:
            t = e.get('event_type', 'unknown')
            by_type[t] = by_type.get(t, 0) + 1

        print("\nTop 10 event types:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1])[:10]:
            print(f"  {c:>8,}  {t}")


if __name__ == '__main__':
    main()
