#!/bin/bash
curl -s -X POST 'https://integrate.api.nvidia.com/v1/chat/completions' \
  -H 'Authorization: Bearer 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' \
  -H 'Content-Type: application/json' \
  -d '{"model": "meta/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": "hello"}]}'
