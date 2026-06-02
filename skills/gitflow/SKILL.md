---
name: gitflow
description: This skill should be used when the user asks to "start feature", "create hotfix", "finish feature", "start release", "start bugfix", "merge to develop", "merge to master", "git flow init", "accept MR", "finish MR", "git flow finish from GitLab", "pull and finish branch", or mentions Git Flow branching, feature/bugfix/hotfix/release workflow.
---

## Related Skills

- **deploy-sls** - Deploy after feature finish
- **ship-it** - Full deployment pipeline
- **conventional-commit** - Commit message format
- **incident-response** - Hotfix workflow for production issues

> Note: Set `WORKSPACE_ROOT` env var to your workspace path (default: `/path/to/workspace`)

## Preferred: Use jira-cli for Jira Operations

Use the `jira-cli` binary instead of raw curl — cleaner, no manual auth header construction.

**Install:** `go install github.com/nguyenvanduocit/jira-mcp/cmd/jira-cli@latest`

```bash
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"

# Create issue
jira-cli --env "$JIRA_ENV" create-issue --project PROJ --summary "<description>" --type Bug --output json | jq -r '.key'

# Get available transitions
jira-cli --env "$JIRA_ENV" get-transitions --issue-key PROJ-XXXX

# Transition to In Progress
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 21

# Transition to Fixed
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 4

# Get issue details
jira-cli --env "$JIRA_ENV" get-issue --issue-key PROJ-XXXX --output json
```

> Transition IDs remain the same — see the Transition IDs table below.

# Git Flow (via git-flow CLI extension)

**ALWAYS use the `git flow` CLI extension** — NEVER manually checkout/merge/tag by hand.

The extension ensures correct source branch, merge targets, and tag conventions automatically. Manual git commands are error-prone (e.g. creating a hotfix from develop instead of master).

## Prerequisite

```bash
# Check installed
git flow version
# Expected: 1.12.3 (AVH Edition) or later

# Init in new repo (only once, accept defaults)
git flow init -d
```

## Branch Model

| Branch | Prefix | Source | Merge Into | Purpose |
|--------|--------|--------|------------|---------|
| **master** | — | — | — | Production-ready code |
| **develop** | — | — | — | Integration branch |
| **Feature** | `feature/` | develop | develop | New features |
| **Bugfix** | `bugfix/` | develop | develop | Bug fixes on develop |
| **Release** | `release/` | develop | master + develop | Release preparation |
| **Hotfix** | `hotfix/` | **master** | master + develop | Production fixes |

## Jira Issue Requirement (MANDATORY)

**Every codebase change MUST have a Jira issue before starting** — no issue = no code.

### 1. Create Issue & Self-assign (before `git flow start`)

```bash
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"

# Create issue (replace type: Story/Bug/Task)
ISSUE_KEY=$(jira-cli --env "$JIRA_ENV" create-issue --project PROJ --summary "<short description>" --type Bug --output json | jq -r '.key')
echo "Created: $ISSUE_KEY"
# → e.g. PROJ-123
```

### 2. Transition to In Progress

```bash
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key "$ISSUE_KEY" --transition-id 21
```

### 3. Start git flow with issue key as branch name

```bash
# Use issue key as branch name: feature/PROJ-123-short-desc
git flow feature start PROJ-123-short-desc
# or
git flow hotfix start PROJ-123-short-desc
```

### 4. Close Issue after merge

```bash
# Transition → Fixed
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 4
```

### Transition IDs
| ID | Status |
|----|--------|
| 11 | To Do |
| 21 | In Progress |
| 41 | Ready Testing |
| 61 | Testing |
| 4  | Fixed |
| 62 | Closed |

---

## Workflows

### Feature

```bash
# 0. Create Jira issue (see Jira Issue Requirement above)
#    → Note ISSUE_KEY (e.g. PROJ-123)

# 1. Start (branches from develop automatically)
git flow feature start PROJ-123-user-authentication

# 2. Work, commit (issue key right after type/scope)...
git add . && git commit -m "feat(auth): PROJ-123 add OAuth2 login"

# 3. Push branch + create MR for review before finish
git push --no-verify origin feature/PROJ-123-user-authentication
glab mr create --source-branch feature/PROJ-123-user-authentication --target-branch develop \
  --title "feat(auth): PROJ-123 add OAuth2 login" --no-editor

# 4. After MR is approved, finish (merges to develop, deletes branch)
git flow feature finish PROJ-123-user-authentication
git push origin develop

# 5. Close Jira issue
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-123 --transition-id 4
```

### Bugfix

```bash
# 0. Create Jira issue → PROJ-XXXX

# 1. Start (branches from develop)
git flow bugfix start PROJ-XXXX-fix-null-check

# 2. Work, commit...
git add . && git commit -m "fix(orders): PROJ-XXXX handle null transaction_fees"

# 3. Push branch + create MR for review
git push --no-verify origin bugfix/PROJ-XXXX-fix-null-check
glab mr create --source-branch bugfix/PROJ-XXXX-fix-null-check --target-branch develop \
  --title "fix(orders): PROJ-XXXX handle null transaction_fees" --no-editor

# 4. After MR approved, finish
git flow bugfix finish PROJ-XXXX-fix-null-check
git push origin develop

# 5. Close Jira issue
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 4
```

### Hotfix

**Two options for finishing a hotfix:**
- **Option A: GitLab MR flow** (recommended) — merge via GitLab, skip `git flow finish`
- **Option B: Local git flow finish** — merge locally then push

#### Option A: GitLab MR flow (recommended)

```bash
# 0. Create Jira issue → PROJ-XXXX

# 1. Start (branches from master automatically)
git flow hotfix start PROJ-XXXX-fix-nil-pointer

# 2. Work, commit...
git add . && git commit -m "fix(orders): PROJ-XXXX add nil check for transaction_fees"

# 3. Push branch + create 2 MRs: master + develop (simultaneously)
git push origin hotfix/PROJ-XXXX-fix-nil-pointer
glab mr create --source-branch hotfix/PROJ-XXXX-fix-nil-pointer --target-branch master \
  --title "fix(orders): PROJ-XXXX add nil check for transaction_fees" --no-editor
glab mr create --source-branch hotfix/PROJ-XXXX-fix-nil-pointer --target-branch develop \
  --title "fix(orders): PROJ-XXXX add nil check for transaction_fees (merge to develop)" --no-editor

# 4. After both MRs are approved → merge MR to master first (do NOT delete source branch yet)
glab mr merge <MASTER_MR_ID> --yes --remove-source-branch=false
# Then merge MR to develop
glab mr merge <DEVELOP_MR_ID> --yes --remove-source-branch=true

# 5. Close Jira issue
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 4
```

#### Option B: Local git flow finish

```bash
# 0-2. Same as Option A

# 3. Push branch + create 2 MRs: master + develop (simultaneously)
git push origin hotfix/PROJ-XXXX-fix-nil-pointer
glab mr create --source-branch hotfix/PROJ-XXXX-fix-nil-pointer --target-branch master \
  --title "fix(orders): PROJ-XXXX add nil check for transaction_fees" --no-editor
glab mr create --source-branch hotfix/PROJ-XXXX-fix-nil-pointer --target-branch develop \
  --title "fix(orders): PROJ-XXXX add nil check for transaction_fees (merge to develop)" --no-editor

# 4. After MR approved, finish locally (merges to master + develop, deletes branch)
git fetch origin
git checkout master && git pull origin master
git checkout develop && git pull origin develop
git checkout hotfix/PROJ-XXXX-fix-nil-pointer
git flow hotfix finish PROJ-XXXX-fix-nil-pointer -m "Hotfix: nil pointer in transaction fees"

# Push master, develop, and tags
git push origin master && git push origin develop && git push origin --tags

# 5. Close Jira issue
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key PROJ-XXXX --transition-id 4
```

### Release

```bash
# Start (branches from develop)
git flow release start 1.2.0

# Bump version, changelog, final fixes...
git commit -m "chore: bump version to 1.2.0"

# Push branch + create MR targeting master for review
git push --no-verify origin release/1.2.0
glab mr create --source-branch release/1.2.0 --target-branch master \
  --title "chore: release 1.2.0" --no-editor

# After MR approved, finish (merges to master + develop, deletes branch)
# ⚠️ git flow tags by BRANCH NAME (e.g., "1.2.0"), does not auto-add "v" prefix
git flow release finish 1.2.0 -m "Release 1.2.0"

# Manually bump version tag if "v" prefix is needed
git checkout master
git tag -a v1.2.0 -m "Release v1.2.0"

# Push everything
git push origin master && git push origin develop && git push origin --tags
```

## Accept MR from GitLab (Review & Finish)

When a teammate creates a MR on GitLab and it's been reviewed/approved, use this flow to finish it locally via git flow. This ensures proper merge to both master and develop (for hotfix/release) or develop (for feature/bugfix).

### Detect branch type from MR

Extract the source branch from the MR URL to determine the git flow type:

| Source branch prefix | Git flow type | Merges into |
|---------------------|---------------|-------------|
| `feature/` | feature | develop |
| `bugfix/` | bugfix | develop |
| `hotfix/` | hotfix | master + develop |
| `release/` | release | master + develop |

### Flow

```bash
# 1. Fetch MR info via GitLab API (extract source_branch, target_branch)
GITLAB_TOKEN=$(cat "${WORKSPACE_ROOT:-/path/to/workspace}/secret/devops/gitlab-token")
PROJECT_PATH="group%2Frepo-name"  # URL-encoded
MR_ID=268

MR_INFO=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_PATH/merge_requests/$MR_ID")
SOURCE_BRANCH=$(echo "$MR_INFO" | jq -r '.source_branch')
# e.g. hotfix/PROJ-38

# 2. cd into repo
cd /path/to/your/repo

# 3. Fetch + sync master and develop (MANDATORY before any git flow op)
git fetch origin
git checkout master && git pull origin master
git checkout develop && git pull origin develop
# ⚠️ If develop diverged: git reset --hard origin/develop
#    (only when local develop has no commits to keep)

# 4. Init git flow if not already done
git flow config 2>/dev/null || git flow init -d

# 5. Checkout remote branch
#    Strip prefix to get the flow name (e.g. hotfix/PROJ-38 → PROJ-38)
git checkout "$SOURCE_BRANCH" && git pull origin "$SOURCE_BRANCH"

# 6. Finish via git flow (auto-detects type from branch prefix)
#    For hotfix:
FLOW_NAME="${SOURCE_BRANCH#hotfix/}"   # strip prefix
git flow hotfix finish "$FLOW_NAME" -m "Hotfix: <description>"

#    For feature:
FLOW_NAME="${SOURCE_BRANCH#feature/}"
git flow feature finish "$FLOW_NAME"

#    For bugfix:
FLOW_NAME="${SOURCE_BRANCH#bugfix/}"
git flow bugfix finish "$FLOW_NAME"

#    For release:
FLOW_NAME="${SOURCE_BRANCH#release/}"
git flow release finish "$FLOW_NAME" -m "Release $FLOW_NAME"

# 7. Bump version tag (hotfix/release only)
git tag --sort=-v:refname | head -5    # check latest
git checkout master
git tag -a v<X.Y.Z> -m "v<X.Y.Z>: <description>"

# 8. Push master, develop, and tags
git push origin master && git push origin develop && git push origin --tags

# 9. Close Jira issue
JIRA_ENV="${WORKSPACE_ROOT:-/path/to/workspace}/secret/atlassian/jira.env"
jira-cli --env "$JIRA_ENV" transition-issue --issue-key <ISSUE-KEY> --transition-id 4
```

### Common pitfalls

- **Develop diverged** — local develop has old commits from a previous hotfix merge that remote already rebased. Use `git reset --hard origin/develop` if local has no uncommitted work.
- **Git flow not initialized** — `git flow config` fails → run `git flow init -d` first.
- **MR auto-close** — GitLab automatically closes MRs when the source branch is deleted (git flow finish deletes branch). No need to close MR manually.
- **Duplicate tags** — git flow tags by branch name (e.g. `PROJ-38`). Always create an additional version tag `v<X.Y.Z>` on master.

---

## Publish & Pull (remote collaboration)

```bash
# Publish branch to remote (for collaboration)
git flow feature publish user-authentication
git flow hotfix publish critical-fix

# Pull someone else's branch
git flow feature pull origin user-authentication
```

## ⚠️ Important Rules

1. **ALWAYS fetch/pull before ANY git flow operation** — Before `start`, `finish`, or any git flow command, MUST pull both master and develop to sync local with remote. Skipping this creates unnecessary merge commits or conflicts.
   ```bash
   # Always run before any git flow operation
   git fetch origin
   git checkout master && git pull origin master
   git checkout develop && git pull origin develop
   ```
2. **NEVER manually create hotfix/release branches** — `git flow` ensures correct source branch
3. **NEVER skip `finish`** — it handles merge to both master AND develop
4. **Always push after finish** — `git flow finish` only works locally
5. **Hotfix from master, bugfix from develop** — `git flow` enforces this automatically
6. **Use `-m` on finish** for tag messages on hotfix/release
7. **Version tag must be bumped manually** — `git flow` only tags by branch name, does not auto-create version tags. After `finish`, check the latest version tag then create a new tag on master

## Quick Reference

```bash
# Feature
git flow feature start <name>
git flow feature finish <name>
git flow feature publish <name>

# Bugfix
git flow bugfix start <name>
git flow bugfix finish <name>

# Hotfix (from master → merges to master + develop)
git flow hotfix start <name>
git flow hotfix finish <name> -m "tag message"
git checkout master && git tag -a v<X.Y.Z> -m "description"  # bump version manually

# Release (from develop → merges to master + develop)
git flow release start <version>
git flow release finish <version> -m "tag message"
git checkout master && git tag -a v<X.Y.Z> -m "description"  # if need "v" prefix

# Check config
git flow config

# Init (first time per repo)
git flow init -d
```

## Commit Message Conventions

Follow **Conventional Commits**:

```
<type>(<scope>): <JIRA-TICKET> <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`

## Related Skills

- `/conventional-commit` — Commit message format
- `/worktree` — Parallel development with git worktrees
- `/incident-response` — Hotfix workflow for production issues
