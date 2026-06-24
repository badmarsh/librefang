import os
import requests

api_key = "lf_key_527679d18a9ebd59e00a049e3596f801"
url = "http://localhost:8085/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "messages": [{"role": "user", "content": "hello"}],
    "max_tokens": 10
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.text)
except Exception as e:
    print(e)
