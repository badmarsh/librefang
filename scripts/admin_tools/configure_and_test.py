import os
import glob
import re
import urllib.request
import json
from urllib.error import HTTPError

models = [
    "qwen-vl-ocr-2025-11-20", "qwen3.7-plus", "qwen3-vl-235b-a22b-thinking", "qwen-mt-flash",
    "qwen3-vl-30b-a3b-thinking", "qwen3.7-max-2026-06-08", "glm-5.1", "qwen3.7-max-preview",
    "qwen3-32b", "qwen3-vl-plus-2025-09-23", "qwen-vl-plus", "deepseek-v4-flash",
    "qwen3.5-35b-a3b", "qwen3-30b-a3b-thinking-2507", "qwen3-vl-8b-thinking", "wan2.2-kf2v-flash",
    "qwen-plus-2025-09-11", "qwen3-vl-flash-2026-01-22", "qwen3.5-flash-2026-02-23",
    "qwen3-vl-flash-2025-10-15", "qwen3.7-max-2026-05-20", "qwen-vl-max", "qwen3.7-plus-2026-05-26",
    "qwen3-vl-30b-a3b-instruct", "qwen3-vl-235b-a22b-instruct", "qwen3-8b", "qwen3-coder-30b-a3b-instruct",
    "qwen3.6-27b", "qwen3-235b-a22b", "qwen-mt-lite", "qwen3.6-flash-2026-04-16", "qvq-max",
    "qwen3-vl-plus", "qwen3-next-80b-a3b-thinking", "qwen3.5-27b", "qwen3.7-max-2026-05-17",
    "qwen3-30b-a3b", "qwen3-vl-flash", "qwen-mt-plus", "qwen3-14b", "qwen3-vl-8b-instruct",
    "qwen-plus-character", "deepseek-v4-pro", "qwen3-coder-flash-2025-07-28", "qwen-flash-character",
    "qwen3-vl-plus-2025-12-19", "qwen-plus-2025-04-28", "qwen-mt-turbo", "qwen3-30b-a3b-instruct-2507",
    "qwen3.6-35b-a3b", "qwen-flash-2025-07-28", "qwen-plus-2025-07-14", "qwen3-235b-a22b-instruct-2507",
    "qwq-plus", "qwen3.7-max", "qwen-vl-ocr", "qwen3-next-80b-a3b-instruct"
]

def update_agents():
    agents_dir = "/home/ubuntu/openfang/agents"
    tomls = sorted(glob.glob(os.path.join(agents_dir, "*", "agent.toml")))
    
    for i, toml_path in enumerate(tomls):
        model = models[i % len(models)]
        with open(toml_path, "r") as f:
            content = f.read()
        
        # Replace the model line
        new_content = re.sub(r'model\s*=\s*"[^"]+"', f'model = "{model}"', content)
        
        if content != new_content:
            with open(toml_path, "w") as f:
                f.write(new_content)
            print(f"Updated {toml_path.split('/')[-2]} -> {model}")

def test_models():
    import os, json
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    
    # Let's source the secrets.env manually if possible, or just expect DASHSCOPE_API_KEY
    key = os.environ.get('DASHSCOPE_API_KEY', '')
    if not key:
        secrets_path = os.path.expanduser("~/.openfang/secrets.env")
        if os.path.exists(secrets_path):
            with open(secrets_path) as f:
                for line in f:
                    if line.startswith("export DASHSCOPE_API_KEY="):
                        key = line.strip().split("=")[1].strip('"\'')
                    elif line.startswith("DASHSCOPE_API_KEY="):
                        key = line.strip().split("=")[1].strip('"\'')
    
    print(f"Testing models. Key present: {bool(key)}")
    
    results = {"success": [], "failed": []}
    for model in models:
        payload = json.dumps({
            'model': model,
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
            print(f"[{model}] OK")
            results["success"].append(model)
        except HTTPError as e:
            body = e.read().decode()
            print(f"[{model}] ERROR {e.code}: {body[:200]}")
            results["failed"].append((model, e.code, body[:200]))
        except Exception as e:
            print(f"[{model}] EXCEPTION: {e}")
            results["failed"].append((model, type(e).__name__, str(e)))
    
    print(f"\\nTest summary: {len(results['success'])} success, {len(results['failed'])} failed")

if __name__ == '__main__':
    update_agents()
    test_models()
