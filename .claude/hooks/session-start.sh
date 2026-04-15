#!/bin/bash
set -euo pipefail

# Only run in remote environments (Claude Code on the web / iOS)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

echo "Remote session ready — static site (no dependencies to install)"
