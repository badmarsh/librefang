import json
import sys

file_path = "/home/ubuntu/openfang/custom_models.json"
try:
    with open(file_path, "r") as f:
        models = json.load(f)
except Exception as e:
    print(f"Error loading {file_path}: {e}")
    sys.exit(1)

new_models = [
    {
        "id": "nvidia/nemotron-3-super-120b-a12b:free",
        "display_name": "nvidia/nemotron-3-super-120b-a12b:free",
        "provider": "openrouter",
        "tier": "standard",
        "aliases": [],
        "context_window": 128000,
        "max_output_tokens": 4096,
        "input_cost_per_m": 0.0,
        "output_cost_per_m": 0.0,
        "supports_tools": True,
        "supports_vision": False,
        "supports_streaming": True
    },
    {
        "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "display_name": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "provider": "openrouter",
        "tier": "reasoning",
        "aliases": [],
        "context_window": 128000,
        "max_output_tokens": 4096,
        "input_cost_per_m": 0.0,
        "output_cost_per_m": 0.0,
        "supports_tools": True,
        "supports_vision": False,
        "supports_streaming": True
    },
    {
        "id": "nvidia/nemotron-nano-12b-v2-vl:free",
        "display_name": "nvidia/nemotron-nano-12b-v2-vl:free",
        "provider": "openrouter",
        "tier": "vision",
        "aliases": [],
        "context_window": 128000,
        "max_output_tokens": 4096,
        "input_cost_per_m": 0.0,
        "output_cost_per_m": 0.0,
        "supports_tools": True,
        "supports_vision": True,
        "supports_streaming": True
    }
]

# Avoid duplicates
existing_ids = {m["id"] for m in models}
for nm in new_models:
    if nm["id"] not in existing_ids:
        models.append(nm)

with open(file_path, "w") as f:
    json.dump(models, f, indent=2)

print("Updated custom_models.json successfully.")
