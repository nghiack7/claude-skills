---
name: tanca
description: This skill should be used when the user asks to "check attendance", "list employees", "check-in", "check-out", "view shifts", "sync Tanca", "approve requests", "reject requests", "pending requests", "direct reports", "xem ca lam", "duyet don", or mentions Tanca, timekeeping, HR integration, or employee management.
---

## Preferred: Use tanca-cli

Use the `tanca-cli` binary instead of raw curl — simpler, no manual header construction needed.

**Install:** `go install github.com/nguyenvanduocit/tanca-mcp/cmd/tanca-cli@latest`

**Setup:**
```bash
# Load credentials from tanca.env
TANCA_ENV="<PATH_TO_TANCA_ENV_FILE>"
```

**Common Commands:**
```bash
# List employees
tanca-cli --env "$TANCA_ENV" list-employees --limit 50

# Get today's shifts for employee
tanca-cli --env "$TANCA_ENV" get-today-shift --user-id <USER_ID>

# Get shift summary (date range)
tanca-cli --env "$TANCA_ENV" get-shift-summary --user-id <USER_ID> --start-date 2026-03-01 --end-date 2026-03-13

# Check-in
tanca-cli --env "$TANCA_ENV" check-in --shift-id <SHIFT_ID>

# Check-out
tanca-cli --env "$TANCA_ENV" check-out --shift-id <SHIFT_ID>

# JSON output for processing
tanca-cli --env "$TANCA_ENV" list-employees --output json | jq '.[] | {id, name}'
```

> The raw curl scripts below remain as reference for operations not yet supported by tanca-cli (e.g., request approval workflows).

## Related Skills

- **secret** - Tanca API credentials
- **mongodb** - Employee data storage

# Tanca API Integration

## Quick Start

**Credentials:** `secret/tanca.env`

**Required headers** (all requests):
```
authorization: Bearer <JWT_TOKEN>
device: <Base64 device JSON>
is-admin: 1
lang: vi
timezone: Asia/Saigon
```

**Response structure:** `{ data: { items: [...], meta: { total, count, per_page, current_page, total_pages } } }`
Access via `.data.items[]` NOT `.data[]`

## Key Endpoints

### Employees

| Endpoint | Purpose | Notes |
|----------|---------|-------|
| `GET /employee-list/get-dynamic-list` | Basic employee list | No `direct_manager_id` |
| `GET /employee/list` | Full employee data | Includes `direct_manager_id` for hierarchy |
| `GET /employee-custom-field-setup/get-fields` | Custom fields | `?is_all=1` |

**Employee list params:** `shop_id`, `page`, `limit`, `is_inactive`, `is_quit`, `start_date`, `end_date`

**Legacy endpoint (for hierarchy):**
```
GET /employee/list?shop_id=<ID>&page=1&limit=100&is_inactive=0
```

Response includes:
```json
{
  "data": {
    "items": [{
      "id": "user_id",
      "name": "Name",
      "identification": "FG-00123",
      "direct_manager_id": "manager_id",
      "direct_manager": { "id": "...", "name": "Manager Name" },
      "department_obj": { "id": "...", "name": "Dept" },
      "position_obj": { "id": "...", "name": "Position" }
    }]
  }
}
```

### Shifts & Timekeeping

| Endpoint | Purpose |
|----------|---------|
| `GET /shift/summary-employee-shift` | Get shifts with check-in/out status |
| `GET /shift/get-proccess-timekeeperlog` | Timekeeper logs |
| `GET /shift/list-shift-assignment-with-shift-v2` | Shift templates |
| `POST /shift/check-in-out-shift` | Record check-in/out |

**Shift summary params:** `shop_id`, `start_date`, `end_date`, `user_ids[]`, `limit`

**Check-in/out:**
```json
POST /shift/check-in-out-shift
{
  "employee_shift_id": "shift_id_from_summary",
  "type": "check_in",
  "time": "2024-01-15T08:30:00+07:00",
  "reason": "Optional note",
  "latitude": 10.762622,
  "longitude": 106.660172
}
```

### Requests

| Endpoint | Purpose |
|----------|---------|
| `GET /request/list-request` | List all requests |
| `GET /request/detail?id=<ID>` | Request details |
| `GET /request/list-request-types` | Request types |
| `POST /request/confirm-request` | **Approve/reject requests** |

**List requests params:** `from_date`, `to_date`, `type`, `status` (0=pending, 1=approved, 2=rejected), `page`

**Request Types:** `employee-shift` (thay đổi giờ vào/ra), `onleave` (nghỉ phép), `overtime` (làm thêm), etc.

**Approve/Reject request:**
```
POST /request/confirm-request?type=<TYPE>&id=<REQUEST_ID>&status=<STATUS>&status_value=<VALUE>&confirm_reason=<REASON>
```

Parameters:
- `type` - Request type from the request (`employee-shift`, `onleave`, `overtime`, etc.)
- `id` - Request ID
- `status` - `1` = approve, `2` = reject
- `status_value` - `1` = approve, `2` = reject
- `confirm_reason` - Optional reason for approval/rejection

**Important:** Always use the `type` field from each request object. Different request types have different `type` values.

### Other

| Category | Endpoints |
|----------|-----------|
| Auth | `/auth/login-with-qr-code`, `/auth/security-center`, `/auth/organization` |
| Shop | `/shop/detail`, `/shop/get-brand-color` |
| Menu | `/menu/list-tree`, `/element/list-business-field`, `/element/list` |
| Open Shifts | `/open-shift/list?start_date=&end_date=` |
| Payroll | `/employee-payroll/list-column`, `/employee-payroll/list-payroll` |
| Survey | `/survey/latest-activity` |

## Scripts

**IMPORTANT:** JWT tokens are 400+ chars. Always use `grep` + `cut`, never `source`.

### Setup (all scripts)
```bash
TANCA_ENV="<PATH_TO_TANCA_ENV_FILE>"
TANCA_API_URL="https://api.tanca.io/api/v4"
TANCA_TOKEN=$(grep "^TANCA_TOKEN=" "$TANCA_ENV" | cut -d= -f2-)
TANCA_DEVICE_HEADER=$(grep "^TANCA_DEVICE_HEADER=" "$TANCA_ENV" | cut -d= -f2-)
TANCA_SHOP_ID=$(grep "^TANCA_SHOP_ID=" "$TANCA_ENV" | cut -d= -f2-)
```

### Get Current User from JWT
```bash
payload=$(echo "$TANCA_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null)
USER_ID=$(echo "$payload" | grep -o '"sub":"[^"]*"' | cut -d'"' -f4)
```

### List All Employees (paginated)
```bash
page=1
while true; do
  response=$(curl -s "${TANCA_API_URL}/employee-list/get-dynamic-list?shop_id=${TANCA_SHOP_ID}&page=${page}&is_quit=0" \
    -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon")
  echo "$response" | jq -r '.data.items[] | "\(.identification) | \(.name) | \(.department)"'
  [ "$(echo "$response" | jq -r '.data.meta.count')" -lt 15 ] && break || page=$((page+1))
done
```

### Get Direct Reports
```bash
# Extract user ID from JWT or pass as argument
MANAGER_ID=$1
if [ -z "$MANAGER_ID" ]; then
  payload=$(echo "$TANCA_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null)
  MANAGER_ID=$(echo "$payload" | grep -o '"sub":"[^"]*"' | cut -d'"' -f4)
fi

# Use LEGACY endpoint - only one with direct_manager_id
curl -s "${TANCA_API_URL}/employee/list?shop_id=${TANCA_SHOP_ID}&limit=100&is_inactive=0" \
  -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon" | \
  jq -r --arg MID "$MANAGER_ID" '.data.items[] | select(.direct_manager_id == $MID) | "\(.identification) | \(.name) | \(.position // "N/A")"'
```

### Get Employee Shifts
```bash
USER_ID="<user_id>"
START_DATE=$(date +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

curl -s "${TANCA_API_URL}/shift/summary-employee-shift?shop_id=${TANCA_SHOP_ID}&start_date=${START_DATE}&end_date=${END_DATE}&limit=10&user_ids%5B0%5D=${USER_ID}" \
  -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon" | jq '.'
```

### Check-in/Check-out
```bash
SHIFT_ID="<shift_id_from_summary>"
TYPE="check_in"  # or check_out
REASON="API check-in"

curl -s -X POST "${TANCA_API_URL}/shift/check-in-out-shift" \
  -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon" \
  -H "Content-Type: application/json" \
  -d "{\"employee_shift_id\":\"$SHIFT_ID\",\"type\":\"$TYPE\",\"time\":\"$(date -u +%Y-%m-%dT%H:%M:%S+07:00)\",\"reason\":\"$REASON\"}" | jq '.'
```

### Get Pending Requests from Direct Reports
```bash
FROM_DATE=$(date -v-1m +%Y-%m-%d 2>/dev/null || date -d "1 month ago" +%Y-%m-%d)
TO_DATE=$(date +%Y-%m-%d)
MANAGER_ID="<your_user_id>"

page=1
while true; do
  response=$(curl -s "${TANCA_API_URL}/request/list-request?from_date=${FROM_DATE}&to_date=${TO_DATE}&page=${page}" \
    -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon")
  echo "$response" | jq -r --arg MID "$MANAGER_ID" '.data.items[] | select(.user_obj.direct_manager_id == $MID) | "\(.created_at) | \(.user_obj.name) | \(.type) | \(.status) | \(.reason)"'
  [ "$(echo "$response" | jq -r '.data.meta.count')" -lt 15 ] && break || page=$((page+1))
done
```

### Approve/Reject All Pending Requests
```bash
FROM_DATE=$(date -v-1m +%Y-%m-%d 2>/dev/null || date -d "1 month ago" +%Y-%m-%d)
TO_DATE=$(date +%Y-%m-%d)
MANAGER_ID="<your_user_id>"  # or leave empty to approve ALL pending requests
ACTION="approve"  # or "reject"
REASON="${2:-}"  # optional reason

# Get manager ID from JWT if not provided
if [ -z "$MANAGER_ID" ]; then
  payload=$(echo "$TANCA_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null)
  MANAGER_ID=$(echo "$payload" | grep -o '"sub":"[^"]*"' | cut -d'"' -f4)
fi

# Set status values
[ "$ACTION" = "approve" ] && STATUS=1 || STATUS=2

# Collect pending request IDs
page=1
request_ids=()

while true; do
  response=$(curl -s "${TANCA_API_URL}/request/list-request?from_date=${FROM_DATE}&to_date=${TO_DATE}&page=${page}" \
    -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon")
  count=$(echo "$response" | jq -r '.data.meta.count // 0')

  # Filter: if MANAGER_ID is set, only get direct reports; otherwise get ALL pending
  if [ -n "$MANAGER_ID" ]; then
    filter='select(.user_obj.direct_manager_id == $MID and .status == 0)'
  else
    filter='select(.status == 0)'
  fi

  while IFS= read -r line; do request_ids+=("$line"); done < <(echo "$response" | jq -r --arg MID "$MANAGER_ID" ".data.items[] | $filter | "\(.id)|\(.user_obj.name)|\(.type)"')

  [ "$count" -lt 15 ] && break || page=$((page+1))
done

echo "Found ${#request_ids[@]} pending requests"
echo ""

# Approve/reject each request
# NOTE: Uses the .type field from each request (employee-shift, onleave, overtime, etc.)
approved=0; failed=0
for req in "${request_ids[@]}"; do
  IFS='|' read -r req_id emp_name req_type <<< "$req"
  echo -n "$ACTION: [$req_type] $emp_name ($req_id)... "

  result=$(curl -s -X POST "${TANCA_API_URL}/request/confirm-request?type=${req_type}&id=${req_id}&status=${STATUS}&status_value=${STATUS}&confirm_reason=${REASON}" \
    -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon")

  if [ "$(echo "$result" | jq -r '.error_code')" = "0" ]; then
    echo "✓"; approved=$((approved+1))
  else
    echo "✗ $(echo "$result" | jq -r '.message // .error_code // "Unknown"')"; failed=$((failed+1))
  fi
  sleep 0.2
done

echo ""
echo "Done: $approved succeeded, $failed failed"
```

**Quick approve ALL pending (any type, any employee):**
```bash
TANCA_ENV="<PATH_TO_TANCA_ENV_FILE>"
TANCA_TOKEN=$(grep "^TANCA_TOKEN=" "$TANCA_ENV" | cut -d= -f2-)
TANCA_DEVICE_HEADER=$(grep "^TANCA_DEVICE_HEADER=" "$TANCA_ENV" | cut -d= -f2-)

page=1; approved=0
while true; do
  response=$(curl -s "https://api.tanca.io/api/v4/request/list-request?from_date=$(date -v-1m +%Y-%m-%d 2>/dev/null || date -d '1 month ago' +%Y-%m-%d)&to_date=$(date +%Y-%m-%d)&page=${page}" \
    -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon")

  while IFS='|' read -r id name type; do
    curl -s -X POST "https://api.tanca.io/api/v4/request/confirm-request?type=${type}&id=${id}&status=1&status_value=1&confirm_reason=" \
      -H "authorization: $TANCA_TOKEN" -H "device: $TANCA_DEVICE_HEADER" -H "is-admin: 1" -H "lang: vi" -H "timezone: Asia/Saigon" > /dev/null
    echo "✓ [$type] $name"; approved=$((approved+1))
  done < <(echo "$response" | jq -r '.data.items[] | select(.status == 0) | "\(.id)|\(.user_obj.name)|\(.type)"')

  [ "$(echo "$response" | jq -r '.data.meta.count')" -lt 15 ] && break || page=$((page+1))
done
echo "Approved: $approved"
```

## TypeScript Client

```typescript
interface TancaConfig {
  baseUrl: string;
  token: string;
  deviceHeader: string;
  shopId: string;
}

interface TancaResponse<T> {
  error_code: number;
  data: { meta: { total: number; count: number }; items: T[] };
}

const headers = (c: TancaConfig) => ({
  'authorization': c.token, 'device': c.deviceHeader, 'is-admin': '1', 'lang': 'vi', 'timezone': 'Asia/Saigon', 'Content-Type': 'application/json'
});

// Employees
export async function fetchEmployees(config: TancaConfig, page = 1) {
  const params = new URLSearchParams({ shop_id: config.shopId, page: String(page), is_quit: '0' });
  const res = await fetch(`${config.baseUrl}/employee-list/get-dynamic-list?${params}`, { headers: headers(config) });
  return res.json() as Promise<TancaResponse<any>>;
}

// Direct reports (uses legacy endpoint)
export async function getDirectReports(config: TancaConfig, managerId: string) {
  const params = new URLSearchParams({ shop_id: config.shopId, limit: '100', is_inactive: '0' });
  const res = await fetch(`${config.baseUrl}/employee/list?${params}`, { headers: headers(config) });
  const json = await res.json() as Promise<TancaResponse<any>>;
  return (await json).data.items.filter((e: any) => e.direct_manager_id === managerId);
}

// Shifts
export async function getEmployeeShifts(config: TancaConfig, userIds: string[], startDate: string, endDate: string) {
  const params = new URLSearchParams({ shop_id: config.shopId, start_date: startDate, end_date: endDate, limit: '10' });
  userIds.forEach((id, i) => params.append(`user_ids[${i}]`, id));
  const res = await fetch(`${config.baseUrl}/shift/summary-employee-shift?${params}`, { headers: headers(config) });
  return res.json();
}

// Check-in/out
export async function checkInOut(config: TancaConfig, shiftId: string, type: 'check_in' | 'check_out', reason = 'API') {
  await fetch(`${config.baseUrl}/shift/check-in-out-shift`, {
    method: 'POST', headers: headers(config),
    body: JSON.stringify({ employee_shift_id: shiftId, type, time: new Date().toISOString(), reason })
  });
}

// Approve/reject request
export async function approveRequest(config: TancaConfig, requestId: string, requestType: string, action: 'approve' | 'reject' = 'approve', reason = '') {
  const status = action === 'approve' ? '1' : '2';
  const params = new URLSearchParams({ type: requestType, id: requestId, status, status_value: status, confirm_reason: reason });
  const res = await fetch(`${config.baseUrl}/request/confirm-request?${params}`, { headers: headers(config) });
  return res.json();
}
```

## Common Workflows

### Auto check-in
1. `GET /shift/summary-employee-shift?user_ids[0]=X&start_date=TODAY&end_date=TODAY`
2. Extract shift `id` from `.data.items[0].shifts[date][0].id`
3. If `checkin_time` is null, `POST /shift/check-in-out-shift` with `type: check_in`

### Get direct reports
1. Get manager ID from JWT `sub` claim
2. `GET /employee/list?limit=100` (legacy endpoint - has `direct_manager_id`)
3. Filter where `direct_manager_id == manager_id`
4. **DO NOT use `/employee-list/get-dynamic-list`** - missing `direct_manager_id`

### Sync all employees
1. `GET /employee-list/get-dynamic-list?page=1`
2. Check `.data.meta.total`
3. Loop until `page * limit >= total`

### Approve pending requests
1. Get manager ID from JWT `sub` claim
2. `GET /request/list-request?from_date=X&to_date=Y` (paginated)
3. Filter where `user_obj.direct_manager_id == manager_id` and `status == 0`
4. For each request: `POST /request/confirm-request?type=<type>&id=<id>&status=1&status_value=1`

## Known IDs

Look up your organization's IDs from the Tanca admin panel or API responses:

| Resource | ID |
|----------|-----|
| Shop | `<TANCA_SHOP_ID>` |
| Branch | `<TANCA_BRANCH_ID>` |
| Department | `<TANCA_DEPT_ID>` |
| Region | `<TANCA_REGION_ID>` |

## Troubleshooting

### "file name too long" error
```bash
# ❌ source fails with 400+ char JWT
source tanca.env
# ✅ Use grep + cut
TANCA_TOKEN=$(grep "^TANCA_TOKEN=" tanca.env | cut -d= -f2-)
```

### jq errors "Cannot index array"
```bash
# ❌ Wrong structure
jq '.data[]'
# ✅ Correct
jq '.data.items[]'
jq '.data.meta.total'
```

### Empty shifts
- User has no shifts assigned
- Use wider date range
- Check `is_quit`/`is_inactive` filters

### Endpoint differences
- `/employee-list/get-dynamic-list` - faster, but no `direct_manager_id`
- `/employee/list` - slower, but has full hierarchy data

### Request approval status not updating
When approving requests (especially `onleave` type), the API may return success but the `status` field remains `0` for some time. This is normal behavior:
- Approval is recorded successfully (`error_code: 0`)
- Status update may be delayed due to caching or async processing
- The request will be processed and status updated internally
- Check the UI after approval to verify the request is approved

**Note:** For `onleave` requests, use the request `id` (not `onleave_id`) with `/request/confirm-request?type=onleave&id={request_id}&status=1&status_value=1`
