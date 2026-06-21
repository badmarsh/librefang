import os
import urllib.request
import json

dashscope_key = os.environ.get("DASHSCOPE_API_KEY")

data = json.dumps({
    "model": "qwen3.7-plus",
    "messages": [{"role": "user", "content": "hi"}]
}).encode('utf-8')

req = urllib.request.Request(
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
    data=data,
    headers={
        "Authorization": f"Bearer {dashscope_key}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        print("Success:")
        print(response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
