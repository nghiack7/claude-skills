---
name: jira
description: This skill should be used when the user asks to "get Jira issue", "search Jira", "create Jira ticket", "update issue", "list sprints", "get active sprint", "transition issue", "add comment", "check Jira status", "lấy Jira issue", "tìm Jira", or mentions Jira issue management.
patterns: []
---

## Related Skills

- **sprint-retro** — Fetch sprint data từ Jira cho retrospective
- **adr** — Link ADRs với Jira stories
- **workflow** — Development workflow với Jira tracking
- **gitlab-deep-review** — Map Jira issues với GitLab MRs/commits

# Jira Issue Management

Tương tác với Jira workspace tại `your-org.atlassian.net`.

## CLI

```bash
JIRA_ENV="<PATH_TO_JIRA_ENV_FILE>"
```

**Install (nếu chưa có binary):**
```bash
go install github.com/nguyenvanduocit/jira-mcp/cmd/jira-cli@latest
```

**Note:** Dùng flag `--env` (double dash).

## Commands

| Command | Mô tả |
|---------|-------|
| `get-issue` | Lấy chi tiết issue theo key |
| `search-issues` | Tìm issues bằng JQL |
| `create-issue` | Tạo issue mới |
| `create-child-issue` | Tạo subtask/child issue |
| `update-issue` | Cập nhật issue |
| `list-issue-types` | Liệt kê issue types của project |
| `list-sprints` | Liệt kê sprints của board |
| `get-sprint` | Lấy sprint theo ID |
| `get-active-sprint` | Lấy active sprint |
| `search-sprint` | Tìm sprint theo tên |
| `add-comment` | Thêm comment vào issue |
| `get-comments` | Lấy comments của issue |
| `get-transitions` | Lấy các transitions available |
| `transition-issue` | Chuyển trạng thái issue |
| `list-statuses` | Liệt kê statuses của project |
| `get-issue-history` | Lịch sử thay đổi issue |
| `get-related-issues` | Issues liên quan/linked |
| `link-issues` | Tạo link giữa 2 issues |
| `get-development-info` | Branches, PRs, commits của issue |
| `download-attachment` | Download attachment |

## Projects

Configure your Jira project keys and board IDs:

| Project | Key | Board ID |
|---------|-----|----------|
| Main project | `<PROJECT_KEY>` | `<BOARD_ID>` |

## Sprint Management

```bash
# Active sprint
jira-cli get-active-sprint --env $JIRA_ENV -project-key <PROJECT_KEY>

# List all sprints
jira-cli list-sprints --env $JIRA_ENV -project-key <PROJECT_KEY>

# Tìm sprint theo tên
jira-cli search-sprint --env $JIRA_ENV -project-key <PROJECT_KEY> -name "Sprint 1"

# Get sprint by ID
jira-cli get-sprint --env $JIRA_ENV -sprint-id <SPRINT_ID>
```

## Tìm Issues (search-issues)

```bash
# Active sprint
jira-cli search-issues --env $JIRA_ENV\
  -jql "project = <PROJECT_KEY> AND sprint in openSprints() ORDER BY status ASC"

# Issues của sprint cụ thể
jira-cli search-issues --env $JIRA_ENV\
  -jql "sprint = <SPRINT_ID> ORDER BY status ASC, assignee ASC" \
  -output json

# Issues của 1 người
jira-cli search-issues --env $JIRA_ENV\
  -jql "project = <PROJECT_KEY> AND assignee = currentUser() AND status != Done"

# Bugs chưa xử lý
jira-cli search-issues --env $JIRA_ENV\
  -jql "project = <PROJECT_KEY> AND issuetype = Bug AND status not in (Done, Closed)"

# Issues gần đây
jira-cli search-issues --env $JIRA_ENV\
  -jql "project = <PROJECT_KEY> AND updated >= -7d ORDER BY updated DESC"
```

## Lấy Issue (get-issue)

```bash
jira-cli get-issue --env $JIRA_ENV -issue-key <PROJECT_KEY>-123
jira-cli get-issue --env $JIRA_ENV -issue-key <PROJECT_KEY>-123 -output json
```

## Tạo Issue (create-issue)

```bash
jira-cli create-issue --env $JIRA_ENV\
  -project <PROJECT_KEY> \
  -type Story \
  -summary "Tên issue" \
  -description "Mô tả chi tiết"

# Tạo bug
jira-cli create-issue --env $JIRA_ENV\
  -project <PROJECT_KEY> \
  -type Bug \
  -summary "[Bug] Payment gateway timeout" \
  -priority High
```

## Transition Issue

```bash
# Xem transitions available
jira-cli get-transitions --env $JIRA_ENV -issue-key <PROJECT_KEY>-123

# Chuyển sang In Progress
jira-cli transition-issue --env $JIRA_ENV -issue-key <PROJECT_KEY>-123 -transition "In Progress"

# Chuyển sang Done
jira-cli transition-issue --env $JIRA_ENV -issue-key <PROJECT_KEY>-123 -transition Done
```

## Comment

```bash
# Thêm comment
jira-cli add-comment --env $JIRA_ENV\
  -issue-key <PROJECT_KEY>-123 \
  -body "Fixed in MR !456. Ready for testing."

# Đọc comments
jira-cli get-comments --env $JIRA_ENV -issue-key <PROJECT_KEY>-123
```

## Development Info (branches, MRs, commits)

```bash
jira-cli get-development-info --env $JIRA_ENV -issue-key <PROJECT_KEY>-123 -output json
```

## JQL Reference

```
# Status
status = "In Progress"
status in ("To Do", "In Progress")
status not in (Done, Closed)

# Sprint
sprint in openSprints()
sprint = <SPRINT_ID>

# Assignee
assignee = currentUser()
assignee = "john.doe"

# Time
created >= -7d
updated >= "2026-03-01"
resolved >= startOfMonth()

# Type
issuetype = Bug
issuetype in (Story, Task)

# Combine
project = <PROJECT_KEY> AND sprint in openSprints() AND assignee = currentUser()
project = <PROJECT_KEY> AND issuetype = Bug AND priority = High AND status != Done
```
