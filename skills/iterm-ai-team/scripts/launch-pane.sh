#!/bin/zsh
# Launch one AI-agent lane in a new split pane — terminal-agnostic.
#
# Usage: launch-pane.sh <cli> <prompt-file> <log-file> <repo-dir> [vertical|horizontal]
#   cli         : claude | cursor-agent | copilot
#   prompt-file : path to a text file containing the agent's scoped prompt
#   log-file    : where to tee the pane's output (so the orchestrator can detect completion)
#   repo-dir    : working directory for the agent
#   split       : split direction (default: vertical = side-by-side)
#
# Pane backend is auto-selected so this works in ANY terminal (iTerm2, Ghostty,
# Kitty, Terminal.app, plain SSH), not just iTerm2:
#   1. tmux        — used whenever tmux is available (universal; works in every host
#                    terminal). If already inside tmux ($TMUX) it splits the current
#                    window; otherwise it creates/extends a detached session you attach to.
#   2. iTerm2      — native AppleScript fast-path when running in iTerm2 without tmux.
#   3. otherwise   — error with guidance (install tmux for cross-terminal panes).
#
# Override the backend explicitly with AI_TEAM_PANE=tmux|iterm.
# tmux session name is AI_TEAM_SESSION (default: ai-team).
#
# The pane prints ">>> PANE FINISHED <<<" on exit so a wait-loop can detect completion.
set -euo pipefail

cli="${1:?cli required}"
prompt_file="${2:?prompt-file required}"
log_file="${3:?log-file required}"
repo_dir="${4:?repo-dir required}"
split="${5:-vertical}"

[[ -f "$prompt_file" ]] || { echo "prompt file not found: $prompt_file" >&2; exit 1; }

# Build the CLI invocation. All run non-interactive, autonomous, streamed.
case "$cli" in
  claude)        run='claude --dangerously-skip-permissions --verbose -p "$(cat '"$prompt_file"')"' ;;
  cursor-agent)  run='cursor-agent -p "$(cat '"$prompt_file"')" --force' ;;
  copilot)       run='copilot -p "$(cat '"$prompt_file"')" --allow-all-tools' ;;
  *) echo "unknown cli: $cli" >&2; exit 1 ;;
esac

# Per-pane launcher script (keeps quoting clean across backends).
launcher="$(mktemp -t iterm-ai-pane).sh"
cat > "$launcher" <<EOF
#!/bin/zsh
cd "$repo_dir"
echo "==================== AGENT: $cli ($(basename "$prompt_file")) ===================="
$run 2>&1 | tee "$log_file"
# \${pipestatus[1]} is the agent's exit code (not tee's). Append the completion
# marker to the log too (| tee -a) so an orchestrator polling the log file can
# detect completion — echoing to the pane alone is invisible to the watcher.
echo "EXIT:\${pipestatus[1]}  >>> PANE FINISHED <<<" | tee -a "$log_file"
exec zsh
EOF
chmod +x "$launcher"

# --- Pick a backend -----------------------------------------------------------
backend="${AI_TEAM_PANE:-}"
if [[ -z "$backend" ]]; then
  if command -v tmux >/dev/null 2>&1; then
    backend="tmux"
  elif [[ "${TERM_PROGRAM:-}" == "iTerm.app" ]]; then
    backend="iterm"
  else
    echo "no pane backend available in this terminal (${TERM_PROGRAM:-unknown})." >&2
    echo "install tmux for cross-terminal split panes:  brew install tmux" >&2
    exit 1
  fi
fi

case "$backend" in
  tmux)
    # tmux flags: -h = left/right (vertical visual split), -v = top/bottom.
    case "$split" in
      horizontal) tmux_dir="-v" ;;
      *)          tmux_dir="-h" ;;
    esac
    if [[ -n "${TMUX:-}" ]]; then
      # Inside tmux already — split the current window so the user watches it live.
      tmux split-window $tmux_dir -c "$repo_dir" "$launcher"
      tmux select-layout tiled >/dev/null 2>&1 || true
      echo "launched $cli in tmux pane (current window); log -> $log_file"
    else
      # Not in tmux — build a detached session the user attaches to once.
      session="${AI_TEAM_SESSION:-ai-team}"
      if tmux has-session -t "$session" 2>/dev/null; then
        tmux split-window $tmux_dir -t "$session" -c "$repo_dir" "$launcher"
        tmux select-layout -t "$session" tiled >/dev/null 2>&1 || true
      else
        tmux new-session -d -s "$session" -c "$repo_dir" "$launcher"
      fi
      echo "launched $cli in tmux session '$session'; log -> $log_file"
      echo "  watch live:  tmux attach -t $session"
    fi
    ;;

  iterm)
    case "$split" in
      horizontal) direction="split horizontally" ;;
      *)          direction="split vertically" ;;
    esac
    osascript <<APPLESCRIPT
tell application "iTerm2"
  tell current window
    tell current session
      set newPane to ($direction with same profile)
    end tell
    tell newPane to write text "$launcher"
  end tell
end tell
APPLESCRIPT
    echo "launched $cli in new iTerm2 $split pane; log -> $log_file"
    ;;

  *)
    echo "unknown backend: $backend (use tmux|iterm)" >&2
    exit 1
    ;;
esac
