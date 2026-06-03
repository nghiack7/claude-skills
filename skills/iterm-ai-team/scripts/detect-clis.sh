#!/bin/zsh
# Detect which AI CLIs are available. Prints one line per CLI: "<name>: <path|MISSING>".
set -e
for c in claude cursor-agent copilot; do
  if p=$(command -v "$c" 2>/dev/null); then
    printf "%-14s %s\n" "$c:" "$p"
  else
    printf "%-14s %s\n" "$c:" "MISSING"
  fi
done
