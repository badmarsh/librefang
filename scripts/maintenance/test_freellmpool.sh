#!/bin/bash
curl -s -X POST 'http://127.0.0.1:8085/v1/chat/completions' \
  -H 'Authorization: Bearer flp-local-token-librefang-dev-1234' \
  -H 'Content-Type: application/json' \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "hello"}]}'
