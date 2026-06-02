#!/bin/bash
# Record check-out for an employee shift
# Usage: ./checkout.sh <employee_shift_id> [reason]
# Requires: TANCA_TOKEN, TANCA_DEVICE_HEADER, TANCA_TIMEZONE in .env

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <employee_shift_id> [reason]" >&2
  echo "Example: $0 678abc123def456789012345 'Manual check-out'" >&2
  exit 1
fi

# Load environment
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
elif [ -f .env.local ]; then
  export $(grep -v '^#' .env.local | xargs)
fi

SHIFT_ID=$1
REASON=${2:-"API check-out"}
BASE_URL=${TANCA_API_URL:-https://api.tanca.io/api/v4}
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S+07:00")

if [ -z "$TANCA_TOKEN" ]; then
  echo "Error: TANCA_TOKEN not set" >&2
  exit 1
fi

curl -s -X POST "${BASE_URL}/shift/check-in-out-shift" \
  -H "authorization: $TANCA_TOKEN" \
  -H "device: $TANCA_DEVICE_HEADER" \
  -H "is-admin: 1" \
  -H "lang: vi" \
  -H "timezone: ${TANCA_TIMEZONE:-Asia/Saigon}" \
  -H "Content-Type: application/json" \
  -d "{
    \"employee_shift_id\": \"$SHIFT_ID\",
    \"type\": \"check_out\",
    \"time\": \"$NOW\",
    \"reason\": \"$REASON\"
  }" | jq '.'
