import os
import json
import urllib.request

req = urllib.request.Request("https://openrouter.ai/api/v1/models")
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        free_models = []
        for m in data.get("data", []):
            try:
                if float(m.get("pricing", {}).get("prompt", 1.0)) == 0.0:
                    free_models.append(m["id"])
            except:
                pass
        
        print("--- OpenRouter Free Models ---")
        for m in free_models[:20]:
            print(m)
except Exception as e:
    print(f"Error: {e}")
