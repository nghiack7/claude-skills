---
name: release-notes
description: This skill should be used when the user asks to generate "release notes", "changelog", "what changed", "generate changelog", "create changelog", "write release notes", "version notes", or needs to create release notes from git log with Conventional Commits categorization.
---

## Related Skills

- **workflow** - Commit convention (Conventional Commits + Jira keys)
- **gitflow** - Release branches and versioning

## Auto-detected Git Context

- **Latest tag:** !`git describe --tags --abbrev=0 2>/dev/null || echo "no tags found"`
- **Current branch:** !`git branch --show-current 2>/dev/null || echo "unknown"`
- **Commits since last tag:**

!`git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD --oneline --no-merges 2>/dev/null | head -30 || echo "Could not determine commit range — specify manually"`

> Use the auto-detected context above to skip Step 1 (scope detection) when data is available. If no tags found, ask user for range.

# Release Notes Skill

Automatically generate release notes from git history. When the team uses Conventional Commits with Jira keys (per `/workflow`), the git log contains enough information to produce high-quality release notes.

## Workflow

### Step 1: Determine scope

Ask the user or auto-detect:

```bash
# Between 2 tags
git log v1.2.0..v1.3.0 --oneline

# Between 2 branches
git log main..release/1.3.0 --oneline

# From tag to HEAD
git log v1.2.0..HEAD --oneline
```

If the user doesn't specify, find the nearest tag:
```bash
git describe --tags --abbrev=0
```

### Step 2: Parse commits

Read git log and categorize by Conventional Commit type:

```bash
git log <range> --pretty=format:"%s" --no-merges
```

Each commit has the format: `<type>(<scope>): <message> <STORY-KEY> <TASK-KEY>`

Categories:
- `feat` -> New Features
- `fix` -> Bug Fixes
- `perf` -> Performance Improvements
- `refactor` -> Refactoring (internal notes only)
- `docs` -> Documentation
- `chore`/`test`/`style` -> Other (usually omitted from user-facing notes)

### Step 3: Gather Jira context (if available)

From story keys in commits, use `jira-cli` to fetch story context:
- Story title
- Story description (summary)

```bash
# Fetch story details for context enrichment
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" get-issue --issue-key PROJ-XXXX --output json | jq '{summary: .fields.summary, description: .fields.description}'

# Search all issues from a commit range
jira-cli --env "$JIRA_ENV" search-issues --jql "project = PROJ AND key in (PROJ-100, PROJ-101, PROJ-102)" --output json
```

This gives the release notes business context, not just technical details.

### Step 4: Generate release notes

Create 2 versions:

#### Internal Release Notes (for the team)

Full technical detail, includes all commit types:

```markdown
# Release v1.3.0 — YYYY-MM-DD

## New Features
- **orders**: Add order validation API ([PROJ-123](link))
- **dashboard**: Real-time revenue chart ([PROJ-130](link))

## Bug Fixes
- **auth**: Fix expired token refresh ([PROJ-125](link))
- **sync**: Handle partial order sync failure ([PROJ-128](link))

## Performance
- **queries**: Optimize aggregation pipeline for large datasets ([PROJ-132](link))

## Refactoring
- **sync**: Extract retry logic to shared util ([PROJ-200](link))

## Documentation
- Added implementation docs for order validation

## Stats
- Commits: X
- Stories completed: Y
- Contributors: [list]
```

#### User-Facing Release Notes (for end users)

Business language, feat + fix only, no technical jargon:

```markdown
# What's New in v1.3.0

## New
- Order validation now checks data before processing
- Real-time revenue chart on dashboard

## Improved
- Faster page load for accounts with large order history

## Fixed
- Login session no longer expires unexpectedly
- Order sync now handles partial data correctly
```

### Step 5: Place the file

```
repository/
├── docs/
│   ├── releases/
│   │   ├── v1.3.0.md
│   │   └── v1.2.0.md
│   ├── stories/
│   └── adr/
```

## Breaking Changes

If a commit uses `!` (breaking change), highlight it at the top:

```markdown
## Breaking Changes
- **api**: Response format for /api/v1/orders changed ([PROJ-140](link))
  - Migration guide: [link or description]
```

## Tips

- If commit messages don't follow convention, parse best-effort and warn the user
- Group by scope when there are many changes in the same area
- If Jira access is available, enrich with story title instead of relying solely on commit message
