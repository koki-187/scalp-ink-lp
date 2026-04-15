#!/bin/bash
set -euo pipefail

# Only run in remote environments (Claude Code on the web / iOS)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Install npm dependencies (uses cache when available)
npm install --prefer-offline 2>&1 | tail -5
