---
name: google-chat
description: Manages Google Chat messages and spaces. Use when the user asks to "send Google Chat", "post to Chat", "notify team on Chat", "delete Chat message", "gửi Google Chat", "thông báo Google Chat", "list Chat spaces", "read Chat messages", or mentions Google Chat messaging or space management (not Gmail or Google Calendar).
---

## Related Skills

- **incident-response** — Gửi incident notification/update qua Google Chat
- **monitoring-observability** — Alert routing đến Google Chat spaces
- **google** — Calendar, Gmail (trong cùng plugin)

# Google Chat

Gửi messages và quản lý Google Chat spaces.

## CLI

**Install:** `go install github.com/nguyenvanduocit/google-chat-mcp/cmd/google-chat-cli@latest`

```bash
CREDENTIALS="<TOKEN_PATH>/google-credentials.json"
TOKEN="<TOKEN_PATH>/google-token.json"
```

| Command | Mô tả |
|---------|-------|
| `list-spaces` | Liệt kê tất cả spaces accessible |
| `get-space` | Lấy chi tiết một space cụ thể |
| `list-messages` | Đọc messages trong space |
| `get-message` | Lấy một message cụ thể |
| `send-message` | Gửi message đến space hoặc DM |
| `delete-message` | Xóa message |
| `list-members` | Liệt kê members của space |
| `get-member` | Lấy thông tin member |

## Tìm Space

```bash
# Liệt kê tất cả spaces
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli list-spaces

# Lấy chi tiết space
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli get-space --space spaces/SPACE_ID
```

Space name format: `spaces/AAA...` (lấy từ kết quả list-spaces)

## Gửi Message

```bash
# Gửi text đơn giản
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli send-message \
  --space spaces/SPACE_ID \
  --text "🔴 [P0 Incident] Payment gateway down — đang điều tra"

# Gửi message có format
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli send-message \
  --space spaces/SPACE_ID \
  --text "*Deploy completed* ✅\nVersion: v2.3.1\nEnv: production"
```

## Đọc Messages

```bash
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli list-messages --space spaces/SPACE_ID --page-size 20
```

## Use Case: Incident Notification

Khi có incident (từ skill `incident-response`):

1. Tìm space phù hợp: `list-spaces` → chọn `#incidents` hoặc `#engineering`
2. Gửi initial alert:
   ```
   🔴 [P0] {service} down
   - Time: {timestamp}
   - Impact: {description}
   - IC: {on-call engineer}
   ```
3. Update tiến độ mỗi 15-30 phút
4. Gửi resolution message khi resolved

## Use Case: Deploy Notification

```bash
GOOGLE_CREDENTIALS_FILE=$CREDENTIALS GOOGLE_TOKEN_FILE=$TOKEN \
  google-chat-cli send-message \
  --space spaces/DEPLOY_SPACE \
  --text "🚀 *{service}* deployed to *{env}*\nVersion: {version}\nBy: {deployer}"
```

## Message Formatting

Google Chat hỗ trợ basic markdown:

```
*bold*
_italic_
~strikethrough~
`code`
```multi-line code```

Mention: <users/USER_ID>
Link: <https://example.com|Link text>
```
