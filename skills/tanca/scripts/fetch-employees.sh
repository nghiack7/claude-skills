#!/bin/bash
# Fetch all employees from Tanca API
# Usage: ./fetch-employees.sh [page] [limit]
# Requires: TANCA_TOKEN, TANCA_DEVICE_HEADER, TANCA_TIMEZONE in .env

set -e

# Load environment
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
elif [ -f .env.local ]; then
  export $(grep -v '^#' .env.local | xargs)
fi

PAGE=${1:-1}
LIMIT=${2:-100}
BASE_URL=${TANCA_API_URL:-https://api.tanca.io/api/v4}

if [ -z "$TANCA_TOKEN" ]; then
  echo "Error: TANCA_TOKEN not set" >&2
  exit 1
fi

curl -s "${BASE_URL}/employee/list?page=${PAGE}&limit=${LIMIT}&is_inactive=0&is_no_need_timekeeping=0" \
  -H "authorization: $TANCA_TOKEN" \
  -H "device: $TANCA_DEVICE_HEADER" \
  -H "is-admin: 1" \
  -H "lang: vi" \
  -H "timezone: ${TANCA_TIMEZONE:-Asia/Saigon}" | jq '.'
