#!/usr/bin/env python3
"""
List Amplitude taxonomy: event types and user properties.

Usage:
    python taxonomy.py --events
    python taxonomy.py --properties
    python taxonomy.py --events --category "COGs"
    python taxonomy.py --all --output taxonomy.json
"""

import argparse
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv('secret/services/amplitude.env')

API_KEY = os.getenv('AMPLITUDE_API_KEY')
SECRET_KEY = os.getenv('AMPLITUDE_SECRET_KEY')


def get_event_types() -> list:
    """Get all event types."""
    response = requests.get(
        'https://amplitude.com/api/2/taxonomy/event',
        auth=(API_KEY, SECRET_KEY)
    )
    if response.status_code == 200:
        return response.json().get('data', [])
    return []


def get_user_properties() -> list:
    """Get all user properties."""
    response = requests.get(
        'https://amplitude.com/api/2/taxonomy/user-property',
        auth=(API_KEY, SECRET_KEY)
    )
    if response.status_code == 200:
        return response.json().get('data', [])
    return []


def categorize_events(events: list) -> dict:
    """Group events by category (prefix before ' - ')."""
    categories = {}
    for e in events:
        name = e['event_type']
        if ' - ' in name:
            cat = name.split(' - ')[0]
        elif name.startswith('[Amplitude]'):
            cat = 'Amplitude (Auto)'
        else:
            cat = 'Uncategorized'

        if cat not in categories:
            categories[cat] = []
        categories[cat].append(name)

    return categories


def main():
    parser = argparse.ArgumentParser(description='List Amplitude taxonomy')
    parser.add_argument('--events', '-e', action='store_true', help='List event types')
    parser.add_argument('--properties', '-p', action='store_true', help='List user properties')
    parser.add_argument('--all', '-a', action='store_true', help='List all')
    parser.add_argument('--category', '-c', help='Filter by category')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()

    result = {}

    if args.events or args.all:
        events = get_event_types()
        categories = categorize_events(events)

        print(f"EVENT TYPES ({len(events)} total)")
        print("=" * 50)

        if args.category:
            # Filter specific category
            if args.category in categories:
                print(f"\n{args.category} ({len(categories[args.category])} events):")
                for name in sorted(categories[args.category]):
                    print(f"  • {name}")
            else:
                print(f"Category '{args.category}' not found")
                print(f"Available: {', '.join(sorted(categories.keys()))}")
        else:
            # Show all categories
            for cat in sorted(categories.keys(), key=lambda x: -len(categories[x])):
                print(f"\n{cat} ({len(categories[cat])} events):")
                for name in sorted(categories[cat])[:5]:
                    print(f"  • {name}")
                if len(categories[cat]) > 5:
                    print(f"  ... and {len(categories[cat]) - 5} more")

        result['events'] = events
        result['categories'] = categories

    if args.properties or args.all:
        props = get_user_properties()

        print(f"\nUSER PROPERTIES ({len(props)} total)")
        print("=" * 50)

        # Group by type
        groups = {
            'Experiments': [],
            'UTM/Marketing': [],
            'Business Metrics': [],
            'App/Shop': [],
            'Other': []
        }

        for p in props:
            name = p['user_property']
            if 'experiment' in name.lower() or name.startswith('exp_'):
                groups['Experiments'].append(name)
            elif name.startswith('initial_') or 'utm' in name.lower():
                groups['UTM/Marketing'].append(name)
            elif any(x in name.lower() for x in ['revenue', 'order', 'roas', 'cost', 'spend', 'profit']):
                groups['Business Metrics'].append(name)
            elif any(x in name.lower() for x in ['plan', 'shop', 'app', 'version']):
                groups['App/Shop'].append(name)
            else:
                groups['Other'].append(name)

        for group, items in groups.items():
            if items:
                print(f"\n{group} ({len(items)}):")
                for name in sorted(items)[:10]:
                    print(f"  • {name}")
                if len(items) > 10:
                    print(f"  ... and {len(items) - 10} more")

        result['properties'] = props
        result['property_groups'] = groups

    if args.output and result:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved to {args.output}")

    if not (args.events or args.properties or args.all):
        parser.print_help()


if __name__ == '__main__':
    main()
