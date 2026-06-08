#!/bin/zsh
# Detect which AI CLIs are available for a debate. Prints one line per CLI:
# "<name>: <path|MISSING>". Exit 0 always; caller decides whether enough voices exist.
set -e
for c in claude cursor-agent copilot; do
  if p=$(command -v "$c" 2>/dev/null); then
    printf "%-14s %s\n" "$c:" "$p"
  else
    printf "%-14s %s\n" "$c:" "MISSING"
  fi
done
