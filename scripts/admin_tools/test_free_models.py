import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

openrouter_key = os.environ.get('OPENROUTER_API_KEY', '')
nvidia_key = os.environ.get('NVIDIA_API_KEY', '')

def test_endpoint(name, url, key, model):
    if not key:
        print(f"[{name}] SKIP: No API key found.")
        return

    payload = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': 'Respond with OK'}],
        'max_tokens': 10
    }).encode()
    
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    req = Request(url, data=payload, headers=headers, method='POST')
    
    print(f"[{name}] Testing model '{model}'...")
    try:
        resp = urlopen(req, timeout=15)
        body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        print(f"[{name}] HTTP 200 OK — response: {content}")
    except HTTPError as e:
        body = e.read().decode()
        print(f"[{name}] HTTP {e.code} ERROR — {body[:300]}")
    except Exception as e:
        print(f"[{name}] ERROR — {str(e)}")

# Test OpenRouter free models
test_endpoint('OpenRouter', 'https://openrouter.ai/api/v1/chat/completions', openrouter_key, 'nvidia/llama-3.1-nemotron-70b-instruct:free')
test_endpoint('OpenRouter', 'https://openrouter.ai/api/v1/chat/completions', openrouter_key, 'meta-llama/llama-3.1-8b-instruct:free')
test_endpoint('OpenRouter', 'https://openrouter.ai/api/v1/chat/completions', openrouter_key, 'google/gemma-2-9b-it:free')

# Test Nvidia NIM endpoint directly (if key exists)
test_endpoint('Nvidia NIM', 'https://integrate.api.nvidia.com/v1/chat/completions', nvidia_key, 'meta/llama-3.1-70b-instruct')
