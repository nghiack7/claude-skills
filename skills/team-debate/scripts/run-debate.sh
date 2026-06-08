#!/bin/zsh
# Fan one decision prompt out to every installed AI CLI in parallel, headless, and
# capture each agent's argument to its own file. The orchestrator (Claude) then reads
# all files and judges — this script does NOT pick a winner.
#
# Usage: run-debate.sh <prompt-file> <out-dir>
#   prompt-file : text file with the framed decision (question + options + criteria + output format)
#   out-dir     : directory to write <cli>.md transcripts into (created if missing)
#
# Each agent reasons only — no repo edits expected. Runs are independent and concurrent;
# the script blocks until all finish, then lists what it collected.
set -euo pipefail

prompt_file="${1:?prompt-file required}"
out_dir="${2:?out-dir required}"
[[ -f "$prompt_file" ]] || { echo "prompt file not found: $prompt_file" >&2; exit 1; }
mkdir -p "$out_dir"

prompt="$(cat "$prompt_file")"
pids=()
ran=()

run_one() {
  local name="$1"; shift
  command -v "$name" >/dev/null 2>&1 || { echo "skip $name (MISSING)"; return; }
  ran+=("$name")
  (
    echo "# Debate transcript — $name"
    echo
    case "$name" in
      claude)       claude -p "$prompt" 2>&1 ;;
      cursor-agent) cursor-agent -p "$prompt" --force 2>&1 ;;
      copilot)      copilot -p "$prompt" --allow-all-tools 2>&1 ;;
    esac
    echo
    echo ">>> $name DONE <<<"
  ) > "$out_dir/$name.md" 2>&1 &
  pids+=($!)
}

run_one claude
run_one cursor-agent
run_one copilot

if (( ${#ran[@]} == 0 )); then
  echo "no AI CLIs found — cannot run a debate" >&2
  exit 1
fi

echo "debating with: ${ran[*]}  (waiting for all to finish...)"
wait "${pids[@]}" || true

echo "---- collected transcripts ----"
# Validate each transcript so the orchestrator never synthesizes from a silently-dropped voice:
# a CLI can exit 0 with empty/truncated output, or hang on an auth/confirm prompt (ADR-001 finding).
incomplete=()
for n in "${ran[@]}"; do
  f="$out_dir/$n.md"
  state="ok"
  body_lines=$(awk 'NF{c++} END{print c+0}' "$f" 2>/dev/null)
  if (( body_lines <= 3 )); then
    state="INCOMPLETE (empty/too short)"
    incomplete+=("$n")
  elif ! grep -qi "RECOMMENDATION:" "$f"; then
    state="INCOMPLETE (no RECOMMENDATION footer — may be truncated)"
    incomplete+=("$n")
  fi
  printf "%-14s %-40s %s\n" "$n:" "$f" "$state"
done
(( ${#ran[@]} < 2 )) && echo "WARNING: only 1 voice available — this is a monologue, not a debate."
if (( ${#incomplete[@]} > 0 )); then
  echo "WARNING: ${#incomplete[@]} voice(s) incomplete: ${incomplete[*]} — do NOT synthesize as if all voices spoke; re-run or exclude explicitly."
fi
exit 0
