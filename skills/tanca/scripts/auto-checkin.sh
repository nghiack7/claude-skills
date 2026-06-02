#!/bin/bash
# Full workflow: Get today's shift and check-in if not already checked in
# Usage: ./auto-checkin.sh <user_id> [reason]
# Requires: TANCA_TOKEN, TANCA_DEVICE_HEADER, TANCA_TIMEZONE in .env

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <user_id> [reason]" >&2
  echo "Example: $0 5e982f71d016f838c42d4b30 'Auto check-in'" >&2
  exit 1
fi

# Load environment
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
elif [ -f .env.local ]; then
  export $(grep -v '^#' .env.local | xargs)
fi

USER_ID=$1
REASON=${2:-"Auto check-in"}
BASE_URL=${TANCA_API_URL:-https://api.tanca.io/api/v4}
TODAY=$(date +%Y-%m-%d)
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S+07:00")

if [ -z "$TANCA_TOKEN" ]; then
  echo "Error: TANCA_TOKEN not set" >&2
  exit 1
fi

echo "Fetching shift for user $USER_ID on $TODAY..."

# Get today's shift
SHIFT_RESPONSE=$(curl -s "${BASE_URL}/shift/summary-employee-shift?user_id=${USER_ID}&from_date=${TODAY}&to_date=${TODAY}" \
  -H "authorization: $TANCA_TOKEN" \
  -H "device: $TANCA_DEVICE_HEADER" \
  -H "is-admin: 1" \
  -H "lang: vi" \
  -H "timezone: ${TANCA_TIMEZONE:-Asia/Saigon}")

# Extract shift ID and check-in status
SHIFT_ID=$(echo "$SHIFT_RESPONSE" | jq -r '.data[0].id // empty')
CHECK_IN_TIME=$(echo "$SHIFT_RESPONSE" | jq -r '.data[0].check_in_time // empty')

if [ -z "$SHIFT_ID" ]; then
  echo "No shift found for today" >&2
  echo "$SHIFT_RESPONSE" | jq '.'
  exit 1
fi

echo "Found shift: $SHIFT_ID"

if [ -n "$CHECK_IN_TIME" ] && [ "$CHECK_IN_TIME" != "null" ]; then
  echo "Already checked in at: $CHECK_IN_TIME"
  exit 0
fi

echo "Checking in..."

# Perform check-in
curl -s -X POST "${BASE_URL}/shift/check-in-out-shift" \
  -H "authorization: $TANCA_TOKEN" \
  -H "device: $TANCA_DEVICE_HEADER" \
  -H "is-admin: 1" \
  -H "lang: vi" \
  -H "timezone: ${TANCA_TIMEZONE:-Asia/Saigon}" \
  -H "Content-Type: application/json" \
  -d "{
    \"employee_shift_id\": \"$SHIFT_ID\",
    \"type\": \"check_in\",
    \"time\": \"$NOW\",
    \"reason\": \"$REASON\"
  }" | jq '.'

echo "Check-in completed!"
