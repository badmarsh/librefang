#!/usr/bin/env bash
# Restart the OpenFang daemon and verify health
set -euo pipefail

echo "=== Stopping OpenFang daemon ==="
OLD_PID=$(pgrep -f 'openfang start' 2>/dev/null || true)
if [ -n "$OLD_PID" ]; then
    kill "$OLD_PID"
    echo "Killed PID $OLD_PID"
    sleep 2
else
    echo "No running daemon found (may have already exited)"
fi

echo ""
echo "=== Starting OpenFang daemon ==="
set -a
source /home/ubuntu/.openfang/secrets.env
set +a
nohup /home/ubuntu/.openfang/bin/openfang start >> ~/.openfang/daemon.log 2>&1 &
NEW_PID=$!
echo "Started PID $NEW_PID"

echo "Waiting for gateway to come up..."
sleep 4

/home/ubuntu/.openfang/bin/openfang health && echo "" && echo "✓ Gateway restarted successfully with new DashScope key"
