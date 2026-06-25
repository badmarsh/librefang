#!/bin/bash
curl -s -X POST 'http://127.0.0.1:8085/v1/chat/completions' \
  -H 'Authorization: Bearer dummy' \
  -H 'Content-Type: application/json' \
  -d '{"model": "ovh/Meta-Llama-3_3-70B-Instruct", "messages": [{"role": "user", "content": "hello"}]}'
