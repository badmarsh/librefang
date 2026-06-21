import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

key = os.environ.get('OPENROUTER_API_KEY', '')

def test_model(model):
    payload = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': 'Say OK'}],
        'max_tokens': 10
    }).encode()
    
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    req = Request('https://openrouter.ai/api/v1/chat/completions', data=payload, headers=headers, method='POST')
    
    try:
        resp = urlopen(req, timeout=15)
        body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        print(f"[OK] {model}: {content}")
    except HTTPError as e:
        print(f"[ERROR] {model}: {e.read().decode()}")

test_model('nvidia/nemotron-3-ultra-550b-a55b:free')
test_model('nvidia/nemotron-3.5-content-safety:free')
test_model('nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free')
test_model('nvidia/nemotron-nano-12b-v2-vl:free')
