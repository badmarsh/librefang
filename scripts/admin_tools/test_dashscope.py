#!/usr/bin/env python3
"""Validate new DashScope key against the actual models used by the 57 agents."""
import urllib.request
import urllib.error
import json
import os

KEY = "sk-ws-H.IRMLYE.kWPQ.MEUCIQCyysRaStOHxFEO4sO_cbGi_ZjXab66QcPvGsf2cyAm_wIgdkFYeWKKbuI4FNao6T60U2oI9BLzj74q4PgdK8VrSA8"
URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

# All distinct models actually used by agents (post-patch)
AGENT_MODELS = [
    "qwen-plus-2025-07-28",
    "qwen-plus-2025-07-28",
    "qwen-plus-2025-07-28",
    "qwen3.5-plus-2026-02-15",
    "qwen3-max",
    "qwen3.7-plus",
    "qwen3.7-plus",
    "qwen3.7-plus",
    "qwen3-vl-235b-a22b-thinking",
]

def test(key, model):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply: OK"}],
        "max_tokens": 5
    }).encode()
    req = urllib.request.Request(
        URL, data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        body = json.loads(resp.read())
        return "✓", body["choices"][0]["message"]["content"].strip()[:20]
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:120]
        code = e.code
        if "exhausted" in err or "free tier" in err:
            return "⚠", f"HTTP {code} FREE TIER EXHAUSTED"
        return "✗", f"HTTP {code}: {err}"
    except Exception as ex:
        return "✗", str(ex)[:80]

print("=== DashScope Model Validation (new key) ===\n")
ok_count = 0
fail_count = 0
for model in AGENT_MODELS:
    status, msg = test(KEY, model)
    if status == "✓":
        ok_count += 1
    else:
        fail_count += 1
    print(f"  {status}  {model:<40} {msg}")

print(f"\nSummary: {ok_count} OK, {fail_count} FAILED")
if fail_count == 0:
    print("→ All agent models are accessible. Ready to restart gateway.")
else:
    print("→ Some models still failing. Check the DashScope console quota list.")
