#!/bin/zsh
# Launch one AI-agent lane in a new iTerm split pane.
#
# Usage: launch-pane.sh <cli> <prompt-file> <log-file> <repo-dir> [vertical|horizontal]
#   cli         : claude | cursor-agent | copilot
#   prompt-file : path to a text file containing the agent's scoped prompt
#   log-file    : where to tee the pane's output (so the orchestrator can detect completion)
#   repo-dir    : working directory for the agent
#   split       : iTerm split direction (default: vertical = cmd+D left/right)
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

# Per-pane launcher script (keeps AppleScript quoting clean).
launcher="$(mktemp -t iterm-ai-pane).sh"
cat > "$launcher" <<EOF
#!/bin/zsh
cd "$repo_dir"
echo "==================== AGENT: $cli ($(basename "$prompt_file")) ===================="
$run 2>&1 | tee "$log_file"
echo "EXIT:\$?  >>> PANE FINISHED <<<"
exec zsh
EOF
chmod +x "$launcher"

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

echo "launched $cli in new $split pane; log -> $log_file"
