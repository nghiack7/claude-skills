#!/usr/bin/env python3
"""
List and download Amplitude cohorts.

Usage:
    python cohorts.py --list
    python cohorts.py --download COHORT_ID --output cohort.json
    python cohorts.py --download-all --output-dir cohorts/
"""

import argparse
import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv('secret/services/amplitude.env')

API_KEY = os.getenv('AMPLITUDE_API_KEY')
SECRET_KEY = os.getenv('AMPLITUDE_SECRET_KEY')


def list_cohorts() -> list:
    """List all cohorts."""
    response = requests.get(
        'https://amplitude.com/api/3/cohorts',
        params={'includeSyncInfo': 'true'},
        auth=(API_KEY, SECRET_KEY)
    )

    if response.status_code == 200:
        return response.json().get('cohorts', [])
    return []


def download_cohort(cohort_id: str, include_props: bool = True) -> dict:
    """Download cohort members (3-step async process)."""
    # Step 1: Request cohort
    response = requests.get(
        f'https://amplitude.com/api/5/cohorts/request/{cohort_id}',
        params={'props': 1 if include_props else 0},
        auth=(API_KEY, SECRET_KEY)
    )

    if response.status_code != 202:
        print(f"Error requesting cohort: {response.status_code}")
        return {}

    request_id = response.json().get('request_id')
    print(f"  Request ID: {request_id}")

    # Step 2: Poll for completion
    max_attempts = 60
    for attempt in range(max_attempts):
        response = requests.get(
            f'https://amplitude.com/api/5/cohorts/request-status/{request_id}',
            auth=(API_KEY, SECRET_KEY)
        )

        if response.status_code != 200:
            print(f"  Error checking status: {response.status_code}")
            return {}

        status = response.json().get('async_status')
        if status == 'JOB COMPLETED':
            break

        print(f"  Status: {status} (attempt {attempt + 1}/{max_attempts})")
        time.sleep(2)
    else:
        print("  Timeout waiting for cohort")
        return {}

    # Step 3: Download file
    response = requests.get(
        f'https://amplitude.com/api/5/cohorts/request/{request_id}/file',
        auth=(API_KEY, SECRET_KEY),
        allow_redirects=True
    )

    if response.status_code == 200:
        try:
            return response.json()
        except:
            return {'raw': response.text}

    return {}


def main():
    parser = argparse.ArgumentParser(description='Manage Amplitude cohorts')
    parser.add_argument('--list', '-l', action='store_true', help='List all cohorts')
    parser.add_argument('--download', '-d', help='Download cohort by ID')
    parser.add_argument('--download-all', action='store_true', help='Download all cohorts')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--output-dir', help='Output directory for --download-all')
    args = parser.parse_args()

    if args.list:
        cohorts = list_cohorts()
        print(f"Found {len(cohorts)} cohorts:\n")
        print(f"{'ID':<15} {'Size':>10} {'Name'}")
        print("-" * 60)
        for c in sorted(cohorts, key=lambda x: -x.get('size', 0)):
            print(f"{c['id']:<15} {c.get('size', 0):>10,} {c['name']}")

    elif args.download:
        print(f"Downloading cohort: {args.download}")
        data = download_cohort(args.download)

        if data:
            output = args.output or f"cohort_{args.download}.json"
            with open(output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved to {output}")
        else:
            print("Failed to download cohort")

    elif args.download_all:
        output_dir = args.output_dir or 'cohorts'
        os.makedirs(output_dir, exist_ok=True)

        cohorts = list_cohorts()
        print(f"Downloading {len(cohorts)} cohorts to {output_dir}/\n")

        for c in cohorts:
            cohort_id = c['id']
            name = c['name'].replace('/', '_').replace(' ', '_')
            print(f"Downloading: {c['name']} ({c.get('size', 0):,} users)")

            data = download_cohort(cohort_id)
            if data:
                output = os.path.join(output_dir, f"{name}.json")
                with open(output, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  Saved to {output}\n")
            else:
                print(f"  Failed\n")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
