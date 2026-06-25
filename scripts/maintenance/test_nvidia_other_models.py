import os
import requests

api_key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

models_to_test = [
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.3-70b-instruct",
    "mistralai/mistral-7b-instruct-v0.3"
]

for model in models_to_test:
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 10
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"{model}: {response.status_code}")
