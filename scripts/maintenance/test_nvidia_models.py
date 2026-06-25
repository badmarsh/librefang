import os
import requests

api_key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

models_to_test = [
    "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "nvidia/nemotron-mini-4b-instruct",
    "nvidia/nemotron-4-340b-instruct"
]

for model in models_to_test:
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 10
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"{model}: {response.status_code}")
