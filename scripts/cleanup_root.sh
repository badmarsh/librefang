#!/usr/bin/env bash
# scripts/cleanup_root.sh
# Forces the deletion of any rogue patch or fix scripts in the repository root.
# Ensures operational cleanliness by enforcing that structural repairs happen
# via standard Rust crate lifecycles, not root-level ad-hoc scripts.

set -euo pipefail

echo "Executing root cleanup..."

# Find and remove any python scripts in the root starting with patch_, fix_, or edit
find . -maxdepth 1 -type f -name "patch_*.py" -exec rm -f {} +
find . -maxdepth 1 -type f -name "fix_*.py" -exec rm -f {} +
find . -maxdepth 1 -type f -name "edit*.py" -exec rm -f {} +

echo "Root cleaned of ad-hoc python scripts."
