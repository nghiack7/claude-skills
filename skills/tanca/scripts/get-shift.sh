#!/bin/bash
# Get employee's shift for today (or specified date)
# Usage: ./get-shift.sh <user_id> [date]
# Requires: TANCA_TOKEN, TANCA_DEVICE_HEADER, TANCA_TIMEZONE in .env

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <user_id> [date]" >&2
  echo "Example: $0 5e982f71d016f838c42d4b30 2024-01-15" >&2
  exit 1
fi

# Load environment
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
elif [ -f .env.local ]; then
  export $(grep -v '^#' .env.local | xargs)
fi

USER_ID=$1
DATE=${2:-$(date +%Y-%m-%d)}
BASE_URL=${TANCA_API_URL:-https://api.tanca.io/api/v4}

if [ -z "$TANCA_TOKEN" ]; then
  echo "Error: TANCA_TOKEN not set" >&2
  exit 1
fi

curl -s "${BASE_URL}/shift/summary-employee-shift?user_id=${USER_ID}&from_date=${DATE}&to_date=${DATE}" \
  -H "authorization: $TANCA_TOKEN" \
  -H "device: $TANCA_DEVICE_HEADER" \
  -H "is-admin: 1" \
  -H "lang: vi" \
  -H "timezone: ${TANCA_TIMEZONE:-Asia/Saigon}" | jq '.'
