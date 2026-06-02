#!/usr/bin/env python3
"""
Search users and get their activity history.

Usage:
    python user_activity.py --search "user@example.com"
    python user_activity.py --user 12345678 --limit 100
    python user_activity.py --search "shop.myshopify.com"
"""

import argparse
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv('secret/services/amplitude.env')

API_KEY = os.getenv('AMPLITUDE_API_KEY')
SECRET_KEY = os.getenv('AMPLITUDE_SECRET_KEY')


def search_users(query: str) -> list:
    """Search for users by ID/email."""
    response = requests.get(
        'https://amplitude.com/api/2/usersearch',
        params={'user': query},
        auth=(API_KEY, SECRET_KEY)
    )

    if response.status_code == 200:
        return response.json().get('matches', [])
    return []


def get_user_activity(amplitude_id: str, limit: int = 100, offset: int = 0) -> dict:
    """Get event history for a user."""
    response = requests.get(
        'https://amplitude.com/api/2/useractivity',
        params={
            'user': amplitude_id,
            'limit': limit,
            'offset': offset
        },
        auth=(API_KEY, SECRET_KEY)
    )

    if response.status_code == 200:
        return response.json()
    return {}


def get_user_profile(user_id: str) -> dict:
    """Get user profile via Profile API."""
    response = requests.get(
        'https://profile-api.amplitude.com/v1/userprofile',
        params={
            'user_id': user_id,
            'get_amp_props': 'true',
            'get_cohort_ids': 'true'
        },
        headers={'Authorization': f'Api-Key {SECRET_KEY}'}
    )

    if response.status_code == 200:
        return response.json()
    return {}


def main():
    parser = argparse.ArgumentParser(description='Get Amplitude user activity')
    parser.add_argument('--search', '-s', help='Search for user by ID/email')
    parser.add_argument('--user', '-u', help='Amplitude user ID')
    parser.add_argument('--limit', type=int, default=50, help='Events to return')
    parser.add_argument('--profile', action='store_true', help='Get user profile')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()

    if args.search:
        print(f"Searching for: {args.search}\n")
        users = search_users(args.search)

        if not users:
            print("No users found")
            return

        print(f"Found {len(users)} user(s):\n")
        for u in users:
            print(f"  Amplitude ID: {u.get('amplitude_id')}")
            print(f"  User ID: {u.get('user_id')}")
            print(f"  Last seen: {u.get('last_seen')}")
            print()

        # If single user, get their activity
        if len(users) == 1:
            amp_id = users[0].get('amplitude_id')
            print(f"Getting activity for {amp_id}...\n")
            activity = get_user_activity(amp_id, args.limit)
            events = activity.get('events', [])

            print(f"Last {len(events)} events:")
            print("-" * 60)
            for e in events[:20]:
                print(f"  {e.get('event_time')}: {e.get('event_type')}")

            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(activity, f, indent=2)
                print(f"\nSaved to {args.output}")

    elif args.user:
        if args.profile:
            print(f"Getting profile for user: {args.user}\n")
            profile = get_user_profile(args.user)

            user_data = profile.get('userData', {})
            props = user_data.get('amp_props', {})
            cohorts = user_data.get('cohort_ids', [])

            print("User Properties:")
            for k, v in list(props.items())[:20]:
                print(f"  {k}: {v}")

            print(f"\nCohorts: {cohorts}")

            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(profile, f, indent=2)
                print(f"\nSaved to {args.output}")
        else:
            print(f"Getting activity for Amplitude ID: {args.user}\n")
            activity = get_user_activity(args.user, args.limit)
            events = activity.get('events', [])

            print(f"Found {len(events)} events:")
            print("-" * 60)
            for e in events:
                props = e.get('event_properties', {})
                props_str = json.dumps(props)[:50] + '...' if len(json.dumps(props)) > 50 else json.dumps(props)
                print(f"  {e.get('event_time')}: {e.get('event_type')}")
                if props:
                    print(f"    {props_str}")

            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(activity, f, indent=2)
                print(f"\nSaved to {args.output}")
    else:
        parser.error('Either --search or --user required')


if __name__ == '__main__':
    main()
