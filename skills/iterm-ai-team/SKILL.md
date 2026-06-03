---
name: iterm-ai-team
description: This skill should be used when the user wants to run a "team" of AI CLI agents in visible iTerm split panes (cmd+D style) to work on a task in parallel, watch each agent work live, and have Claude orchestrate + review. Triggers on "iterm team", "split panes team", "run agents in iterm", "watch agents work", "team work in iterm", "fan out to cursor/copilot panes", or wanting to use cheaper CLIs (cursor/copilot) for implementation to save Claude tokens while Claude acts as principal/orchestrator.
---

# iTerm AI Team

Orchestrate a team of AI CLI agents in **visible iTerm split panes** so the user watches each agent
work live, while Claude (this session) acts as **principal engineer**: it splits the work, hands each
pane a tightly-scoped prompt, waits for completion, then reviews the combined result.

**Core idea — Claude orchestrates, cheaper CLIs implement.** Claude is expensive per token. Push
mechanical implementation work (edits, builds, greps, doc updates) to `cursor-agent` or `copilot`
panes; keep Claude for planning, decomposition, conflict-avoidance, and final review. This cuts
Claude token spend substantially on multi-step tasks.

## When to use

- A task splits into 2+ **independent** lanes (e.g. one agent edits Go, another edits docs) and the
  user wants to *see* progress in real terminals, not just summarized messages.
- The user wants to offload implementation to `cursor-agent`/`copilot` to save Claude tokens.
- The user explicitly asks for "iterm team", "split panes", "watch the agents", etc.

Do **not** use for a single trivial change, or when lanes edit the **same file** (edit conflicts).
If lanes share a file, serialize them or give one agent the whole file.

## Hard rules (principal-engineer discipline)

1. **Resolve blockers before fan-out.** If the task has unresolved decisions that change *what code
   gets written* (e.g. an unconfirmed external contract), surface them via AskUserQuestion FIRST.
   Never let an agent guess at the very thing a stakeholder must confirm.
2. **Read before change.** Inspect the repo yourself first — prior work may already exist. Give each
   agent accurate, file-specific context and explicit "do NOT touch X" boundaries.
3. **Non-overlapping lanes only.** Assign each agent disjoint files. Verify with `git diff --stat`
   afterward that no agent strayed outside its lane.
4. **Verify, don't trust.** After agents finish, independently confirm their claims (re-run the
   build, grep the artifacts, read the diff) before declaring done.
5. **Scope tightly.** Each pane prompt = goal + exact files + boundaries + a "print DONE marker when
   finished" instruction so completion is detectable.

## Workflow

### 1. Plan & decompose
Read the task and repo. Identify independent lanes and the right CLI per lane (see CLI routing). If
blockers exist, ask the user first.

### 2. Detect available CLIs
```bash
scripts/detect-clis.sh
```
Prints which of `claude`, `cursor-agent`, `copilot` are installed. Route lanes to whatever is present;
prefer non-Claude CLIs for implementation.

### 3. Write per-lane prompt files
One file per lane under a scratch dir (e.g. `/tmp/<task>-team/laneN.txt`). Each prompt MUST contain:
- Role + team context ("You are Agent N (ROLE) on a team").
- Exact file(s) to edit and explicit files NOT to touch.
- Concrete steps and success criteria.
- A final-line DONE marker instruction (e.g. `print "LANE2 DONE"`).

### 4. Launch panes
```bash
scripts/launch-pane.sh <cli> <prompt-file> <log-file> <repo-dir> [split: vertical|horizontal]
```
This splits the **current** iTerm session and runs the chosen CLI on the prompt, tee'd to a log.
Call once per lane. Keep Claude's own pane as the orchestrator.

### 5. Wait for completion (do NOT poll-burn)
Use a single background wait that exits when all DONE markers / FINISH lines appear:
```bash
until grep -q "PANE FINISHED" log1 && grep -q "PANE FINISHED" log2; do sleep 3; done; echo ALL DONE
```
Run it via Bash `run_in_background: true` so the harness re-invokes Claude on completion — these are
external CLI processes, so a wait-loop is correct (not harness-tracked work).

### 6. Review
Independently verify (re-run build, grep generated artifacts, `git diff --stat`, read diffs). Give a
crisp principal verdict: ✅ what's correct, ⚠️ what's deliberately incomplete/blocked. Optionally run
the `/review` skill on the diff.

## CLI routing (token economy)

| Lane type | Preferred CLI | Why |
|-----------|--------------|-----|
| Orchestration, decomposition, final review | **claude** (this session) | judgment-heavy |
| Code edits / refactors / builds | **cursor-agent** or **copilot** | cheap, capable for mechanical work |
| Doc updates, grep/verify, mechanical edits | **copilot** or **cursor-agent** | cheapest |

CLI invocation cheatsheet (non-interactive, auto-approve, streamed to pane):
- Claude:  `claude --dangerously-skip-permissions --verbose -p "<prompt>"`
- Cursor:  `cursor-agent -p "<prompt>" --force` (headless print mode)
- Copilot: `copilot -p "<prompt>" --allow-all-tools` (flags vary by version; see `copilot --help`)

`--dangerously-skip-permissions` / `--allow-all-tools` run autonomously on the user's machine — only
use when the user has asked for autonomous team execution, and keep each lane scoped to its files.

## iTerm split reference

`scripts/launch-pane.sh` uses AppleScript. The primitives:
```applescript
tell application "iTerm2"
  tell current window
    tell current session
      set newPane to (split vertically with same profile)   -- cmd+D (left/right)
      -- or: split horizontally with same profile            -- cmd+shift+D (top/bottom)
    end tell
    tell newPane to write text "cd <repo> && <cli-command>"
  end tell
end tell
```

## Optional: publish results to a remote

After review, if the user wants the change pushed, confirm the target repo + identity first (a
non-default GitHub account needs its own credentials/remote). Use plain `git` (branch → commit →
push); `gh` only if installed.
