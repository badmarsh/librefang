#!/bin/bash
curl -s -X POST 'http://127.0.0.1:8085/v1/chat/completions' \
  -H 'Authorization: Bearer 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' \
  -H 'Content-Type: application/json' \
  -d '{"model": "nvidia/meta/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": "hello"}]}'
