#!/usr/bin/env bash
set -euo pipefail

# This script verifies that the number of crates in the workspace (excluding xtask)
# matches the count declared in the READMEs.

WORKSPACE_CRATES=$(grep -E '^\s*"crates/|^\s*"conformance/' Cargo.toml | wc -l | xargs)
README_COUNT=$(grep -oP '(\d+) crates\.' README.md | grep -oP '\d+' | head -n 1)

if [ "$WORKSPACE_CRATES" != "$README_COUNT" ]; then
  echo "Error: Cargo.toml has $WORKSPACE_CRATES crates, but README.md claims $README_COUNT crates."
  exit 1
fi

echo "Crate count ($WORKSPACE_CRATES) matches README."
exit 0
