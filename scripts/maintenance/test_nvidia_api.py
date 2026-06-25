import os
import requests

api_key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "messages": [{"role": "user", "content": "hello"}],
    "max_tokens": 10
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
