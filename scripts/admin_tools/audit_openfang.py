import os
import json
import urllib.request
import urllib.error
import glob
import re

def check_daemon_health():
    try:
        req = urllib.request.Request("http://127.0.0.1:4200/api/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print("✅ Daemon is healthy")
            else:
                print(f"❌ Daemon health check failed with status: {response.status}")
    except Exception as e:
        print(f"❌ Daemon health check failed: {e}")

def check_providers_api():
    try:
        req = urllib.request.Request("http://127.0.0.1:4200/api/providers")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            providers = data if isinstance(data, list) else data.get('providers', data.get('data', []))
            if not isinstance(providers, list):
                if isinstance(providers, dict):
                    providers = list(providers.values())
                else:
                    providers = []
            
            for p in providers:
                if not isinstance(p, dict): continue
                if p.get('auth_status') == 'configured' or p.get('auth_status') == 'not_required':
                    print(f"✅ Provider '{p.get('id')}' is {p.get('auth_status')}")
                elif p.get('auth_status') == 'missing' and p.get('id') in ['qwen', 'openrouter', 'gemini', 'huggingface']:
                    print(f"❌ IMPORTANT Provider '{p.get('id')}' is missing auth!")
    except Exception as e:
        print(f"❌ Failed to fetch providers from API: {e}")

def verify_api_keys():
    # Sourced from secrets.env (we'll run this script after sourcing)
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    brave_key = os.environ.get("BRAVE_API_KEY")
    
    # Check DashScope
    if dashscope_key:
        req = urllib.request.Request("https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models", headers={"Authorization": f"Bearer {dashscope_key}"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                print("✅ DashScope API Key is valid")
        except urllib.error.HTTPError as e:
            print(f"❌ DashScope API Key error: {e.code}")
    else:
        print("❌ DASHSCOPE_API_KEY not found in environment")

    # Check OpenRouter
    if openrouter_key:
        req = urllib.request.Request("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {openrouter_key}"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                print("✅ OpenRouter API Key is valid")
        except urllib.error.HTTPError as e:
            print(f"❌ OpenRouter API Key error: {e.code}")
    else:
        print("❌ OPENROUTER_API_KEY not found in environment")

    # Check Brave
    if brave_key:
        req = urllib.request.Request("https://api.search.brave.com/res/v1/web/search?q=test", headers={"Accept": "application/json", "X-Subscription-Token": brave_key})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                print("✅ Brave Search API Key is valid")
        except urllib.error.HTTPError as e:
            print(f"❌ Brave Search API Key error: {e.code}")
    else:
        print("❌ BRAVE_API_KEY not found in environment")

def verify_agents():
    # Load custom models
    custom_models = []
    try:
        with open("/home/ubuntu/openfang/custom_models.json", "r") as f:
            custom_models_json = json.load(f)
            custom_models = [m["id"] for m in custom_models_json]
    except Exception as e:
        print(f"❌ Failed to load custom_models.json: {e}")
        return

    agent_files = glob.glob("/home/ubuntu/openfang/agents/*/agent.toml")
    errors = 0
    for agent_file in agent_files:
        agent_name = os.path.basename(os.path.dirname(agent_file))
        with open(agent_file, "r") as f:
            content = f.read()
        
        provider_match = re.search(r'provider\s*=\s*"([^"]+)"', content)
        model_match = re.search(r'model\s*=\s*"([^"]+)"', content)
        
        if not provider_match:
            print(f"❌ Agent '{agent_name}' is missing a provider")
            errors += 1
            continue
        if not model_match:
            print(f"❌ Agent '{agent_name}' is missing a model")
            errors += 1
            continue
            
        provider = provider_match.group(1)
        model = model_match.group(1)
        
        if model not in custom_models:
            print(f"❌ Agent '{agent_name}' uses unknown model: {model}")
            errors += 1
            
        if provider not in ['qwen', 'openrouter', 'gemini', 'ollama']:
            print(f"⚠️ Agent '{agent_name}' uses unconventional provider: {provider}")

    if errors == 0:
        print(f"✅ All {len(agent_files)} agents have valid provider/model configurations.")

if __name__ == "__main__":
    print("--- OpenFang Audit ---")
    print("\n1. Checking Daemon Health")
    check_daemon_health()
    
    print("\n2. Checking Configured Providers")
    check_providers_api()
    
    print("\n3. Validating API Keys")
    verify_api_keys()
    
    print("\n4. Verifying Agent Configurations")
    verify_agents()
    print("----------------------")
