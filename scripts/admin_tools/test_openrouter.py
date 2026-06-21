#!/usr/bin/env python3
"""Test OpenRouter key and list available Qwen-equivalent models."""
import urllib.request
import urllib.error
import json

OR_KEY = None
# Load from secrets.env
import os
with open(os.path.expanduser("~/.librefang/secrets.env")) as f:
    for line in f:
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY="):
            OR_KEY = line.split("=", 1)[1]
            break

print(f"OpenRouter key found: {bool(OR_KEY)}, length: {len(OR_KEY) if OR_KEY else 0}")

def test_openrouter(key, model):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with one word: OK"}],
        "max_tokens": 10
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://librefang.ai",
            "X-Title": "LibreFang"
        },
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=25)
        body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"]
        return True, f"'{content}'"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} - {e.read().decode()[:200]}"
    except Exception as e:
        return False, f"Exception: {e}"

print("\n=== OpenRouter Connectivity Test ===")
models_to_test = [
    "qwen/qwen3-235b-a22b",
    "qwen/qwen3-30b-a3b",
    "google/gemini-2.5-flash",
    "anthropic/claude-3.5-haiku",
]
for m in models_to_test:
    ok, msg = test_openrouter(OR_KEY, m)
    print(f"  {'✓' if ok else '✗'} {m:<45} {msg}")
