---
name: confluence
description: This skill should be used when the user asks to "search Confluence", "find spec on Confluence", "read Confluence page", "create Confluence page", "update Confluence", "publish ADR to Confluence", "post release notes", "write runbook on Confluence", "tìm tài liệu Confluence", or mentions Confluence knowledge base or Confluence documentation.
---

## Related Skills

- **adr** — Publish ADRs to Confluence
- **release-notes** — Publish release notes to Confluence
- **incident-response** — Write runbooks/postmortems to Confluence
- **collect-docs** — Collect codebase docs (Confluence là nguồn bổ sung)
- **technical-analysis** — Reference Confluence specs khi phân tích

# Confluence Knowledge Base

Tương tác với Confluence workspace tại `your-org.atlassian.net`.

## CLI

**Install:** `go install github.com/nguyenvanduocit/confluence-mcp/cmd/confluence-cli@latest`

```bash
ENV_FILE="<PATH_TO_CONFLUENCE_ENV_FILE>"
```

| Command | Mô tả |
|---------|-------|
| `search-page` | Tìm pages bằng CQL query |
| `get-page` | Lấy nội dung và metadata của page |
| `create-page` | Tạo page mới trong space |
| `update-page` | Cập nhật nội dung page hiện có |
| `get-comments` | Lấy comments của một page |
| `list-spaces` | Liệt kê các Confluence spaces |

## Workspace

- **Host:** `https://your-org.atlassian.net`

## Tìm Kiếm (search-page)

```bash
# Tìm theo title/content
confluence-cli --env $ENV_FILE search-page --query "order sync"

# Tìm trong space cụ thể
confluence-cli --env $ENV_FILE search-page --query "space = '<SPACE_KEY>' AND title ~ 'ADR'"

# Tìm tài liệu gần đây
confluence-cli --env $ENV_FILE search-page --query "lastModified > '2024-01-01' ORDER BY lastModified DESC"

# Tìm theo label
confluence-cli --env $ENV_FILE search-page --query "label = 'runbook' AND space = '<SPACE_KEY>'"
```

## Đọc Nội Dung (get-page)

```bash
confluence-cli --env $ENV_FILE get-page --page-id 123456789
```

Page ID lấy từ kết quả `search-page` hoặc từ URL Confluence: `.../pages/123456789/...`

## Tạo Page Mới (create-page)

```bash
confluence-cli --env $ENV_FILE create-page \
  --space-key <SPACE_KEY> \
  --title "ADR-042: Tên quyết định kỹ thuật" \
  --content "<h1>Context</h1><p>...</p>" \
  --parent-id "optional-parent-page-id"
```

## Cập Nhật Page (update-page)

```bash
confluence-cli --env $ENV_FILE update-page \
  --page-id 123456789 \
  --title "Tiêu đề mới" \
  --content "<p>Nội dung cập nhật</p>" \
  --version 2
```

## Publish ADR

1. Viết ADR theo skill `adr`
2. Tìm ADR index: `search-page --query "space = '<SPACE_KEY>' AND title = 'Architecture Decision Records'"`
3. `create-page` với `--parent-id` là ADR index page

## Publish Release Notes

1. Tạo nội dung từ skill `release-notes`
2. Tìm Release Notes space/parent
3. `create-page` hoặc `update-page` nếu page đã tồn tại

## Publish Runbook / Postmortem

1. Tạo nội dung từ skill `incident-response`
2. Tìm Runbooks space: `search-page --query "space = '<SPACE_KEY>' AND label = 'runbooks'"`
3. `create-page` với `--parent-id` phù hợp

## CQL Reference

```
# Operators
space = '<SPACE_KEY>'         # exact space
title = "Exact Title"        # exact title match
title ~ "Partial"            # partial title match
label = "runbook"            # has label
creator = currentUser()      # created by me
lastModified > "2024-01-01"  # modified after date

# Combine
space = '<SPACE_KEY>' AND label = 'adr' ORDER BY created DESC
space = '<SPACE_KEY>' AND title ~ 'sync' AND type = page
```

## Content Format

Confluence dùng **HTML** (Storage Format). Khi tạo/update page:

```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<p>Paragraph với <strong>bold</strong> và <em>italic</em></p>

<ul>
  <li>Unordered item</li>
</ul>

<ol>
  <li>Ordered item</li>
</ol>

<!-- Code block -->
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">javascript</ac:parameter>
  <ac:plain-text-body>const x = 1;</ac:plain-text-body>
</ac:structured-macro>

<!-- Info panel -->
<ac:structured-macro ac:name="info">
  <ac:rich-text-body><p>Info message</p></ac:rich-text-body>
</ac:structured-macro>
```
