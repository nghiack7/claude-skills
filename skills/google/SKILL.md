---
name: google
description: Manages Google Calendar and Gmail. Use when the user asks to "check Google Calendar", "find free time", "search Gmail", "read email", "reply email", "send email", "create calendar event", "manage Gmail labels", "tìm lịch", "xem Gmail", or mentions Google Calendar or Gmail operations (not Google Chat).
---

## Related Skills

- **google-chat** — Gửi messages qua Google Chat (trong cùng plugin)
- **incident-response** — Gửi incident notification
- **tanca** — Attendance tracking (complement với Calendar)

# Google Services (Calendar & Gmail)

Quản lý Google Calendar và Gmail.

## CLI

**Install:** `go install github.com/nguyenvanduocit/google-mcp/cmd/google-cli@latest`

```bash
CREDENTIALS="<TOKEN_PATH>/google-credentials.json"
TOKEN="<TOKEN_PATH>/google-token.json"
```

## Calendar Commands

| Command | Mô tả |
|---------|-------|
| `calendar-event` | Tạo/update/list/respond calendar events |
| `calendar-find-time-slot` | Tìm time slot available |
| `calendar-get-busy-times` | Lấy busy times của users |

```bash
# List events
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli calendar-event --action list

# Create event
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli calendar-event --action create \
  --title "Sprint Planning" \
  --start "2026-03-20T09:00:00+07:00" \
  --end "2026-03-20T10:00:00+07:00"

# Find free time slot
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli calendar-find-time-slot \
  --attendees "user1@your-domain.com,user2@your-domain.com" \
  --duration 60

# Get busy times
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli calendar-get-busy-times \
  --emails "you@your-domain.com" \
  --start "2026-03-20" --end "2026-03-21"
```

## Gmail Commands

| Command | Mô tả |
|---------|-------|
| `gmail-search` | Tìm emails |
| `gmail-read-email` | Đọc nội dung email |
| `gmail-reply-email` | Reply email |
| `gmail-move-to-spam` | Chuyển email vào spam |
| `gmail-filter` | Quản lý Gmail filters |
| `gmail-label` | Quản lý Gmail labels |

```bash
# Tìm email
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli gmail-search --query "from:shopify subject:order" --max-results 10

# Đọc email
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli gmail-read-email --message-id MESSAGE_ID

# Reply email
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli gmail-reply-email \
  --message-id MESSAGE_ID \
  --body "Cảm ơn, đã nhận được."

# List labels
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-cli gmail-label --action list
```
