#!/usr/bin/env bash
# Restart the LibreFang daemon and verify health
set -euo pipefail

echo "=== Stopping LibreFang daemon ==="
pkill -9 -f "librefang start" || echo "No running daemon found"
sleep 2

echo ""
echo "=== Starting LibreFang daemon ==="
set -a
source /home/ubuntu/.librefang/secrets.env
set +a
nohup /home/ubuntu/.librefang/bin/librefang start >> ~/.librefang/daemon.log 2>&1 &
NEW_PID=$!
echo "Started PID $NEW_PID"

echo "Waiting for gateway to come up..."
sleep 4

/home/ubuntu/.librefang/bin/librefang health && echo "" && echo "✓ Gateway restarted successfully with new DashScope key"
