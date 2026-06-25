#!/usr/bin/env bash
# scripts/rotate_keys.sh
# Rotates internal deployment keys and purges any accidentally committed private keys.

set -euo pipefail

echo "Executing key rotation and purge protocol..."

# Ensure the offending key file is removed
if [ -f "privatekey" ]; then
    rm -f privatekey
    echo "[X] Purged 'privatekey' from root directory."
else
    echo "[✓] No 'privatekey' found in root."
fi

# Ensure it's not tracked by git
if git ls-files | grep -q 'privatekey'; then
    git rm --cached privatekey
    echo "[X] Untracked 'privatekey' from git index."
fi

echo "Key rotation procedures initialized."
# In a real environment, this script would interact with AWS KMS or HashiCorp Vault.
echo "New keys should be provisioned externally."
