#!/usr/bin/env bash
set -euo pipefail

source ~/.librefang/secrets.env

echo "=== Testing DashScope (qwen provider) ==="
RESPONSE=$(python3 -c "
import os, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

key = os.environ.get('DASHSCOPE_API_KEY', '')
print(f'Key present: {bool(key)}, length: {len(key)}')

payload = json.dumps({
    'model': 'qwen-plus',
    'messages': [{'role': 'user', 'content': 'Say OK'}],
    'max_tokens': 5
}).encode()

req = Request(
    'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    method='POST'
)
try:
    resp = urlopen(req, timeout=15)
    body = json.loads(resp.read())
    print(f'HTTP 200 OK — response: {body[\"choices\"][0][\"message\"][\"content\"]}')
except HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code} ERROR — {body[:300]}')
")
echo "$RESPONSE"

echo ""
echo "=== Testing OpenRouter ==="
python3 -c "
import os, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

key = os.environ.get('OPENROUTER_API_KEY', '')
print(f'Key present: {bool(key)}, length: {len(key)}')

payload = json.dumps({
    'model': 'google/gemini-2.5-flash',
    'messages': [{'role': 'user', 'content': 'Say OK'}],
    'max_tokens': 5
}).encode()

req = Request(
    'https://openrouter.ai/api/v1/chat/completions',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    method='POST'
)
try:
    resp = urlopen(req, timeout=15)
    body = json.loads(resp.read())
    print(f'HTTP 200 OK — response: {body[\"choices\"][0][\"message\"][\"content\"]}')
except HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code} ERROR — {body[:300]}')
"

echo ""
echo "=== Testing Pydantic AI Gateway ==="
python3 -c "
import os, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

key = os.environ.get('PYDANTIC_AI_GATEWAY_API_KEY', '')
print(f'Key present: {bool(key)}, length: {len(key)}')

payload = json.dumps({
    'model': 'openai:gpt-4o-mini',
    'messages': [{'role': 'user', 'content': 'Say OK'}],
    'max_tokens': 5
}).encode()

req = Request(
    'https://gateway.pydantic.dev/v1/chat/completions',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    method='POST'
)
try:
    resp = urlopen(req, timeout=15)
    body = json.loads(resp.read())
    print(f'HTTP 200 OK — response: {body[\"choices\"][0][\"message\"][\"content\"]}')
except HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code} ERROR — {body[:300]}')
"
