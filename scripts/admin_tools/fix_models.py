import os
import re
import glob
import json

AVAILABLE_MODELS = [
    "qwen3.7-plus",
    "qwen3-vl-plus-2025-09-23",
    "qwen-vl-plus",
    "qwen-plus-2025-09-11",
    "qwen3.7-plus-2026-05-26",
    "qwen3-vl-plus",
    "qwen-mt-plus",
    "qwen-plus-character",
    "qwen3-vl-plus-2025-12-19",
    "qwen-plus-2025-04-28",
    "qwen-plus-2025-07-14",
    "qwq-plus"
]

def get_replacement(model_id):
    if model_id in AVAILABLE_MODELS or model_id == "default":
        return model_id
    
    id_lower = model_id.lower()
    if "vl" in id_lower or "kf2v" in id_lower or "clip" in id_lower or "ocr" in id_lower:
        return "qwen3-vl-plus"
    if "mt" in id_lower or "translation" in id_lower or "aligner" in id_lower:
        return "qwen-mt-plus"
    if "thinking" in id_lower or "reasoning" in id_lower or "qwq" in id_lower or "qvq" in id_lower or "deepseek" in id_lower:
        return "qwq-plus"
    if "character" in id_lower:
        return "qwen-plus-character"
    
    # default fallback
    return "qwen3.7-plus"

# Fix config.toml
config_path = "/home/ubuntu/openfang/config.toml"
with open(config_path, "r") as f:
    config_content = f.read()

config_content = re.sub(r'model\s*=\s*"[^"]+"', lambda m: f'model = "{get_replacement(m.group().split("\"")[1])}"', config_content)
with open(config_path, "w") as f:
    f.write(config_content)

# Fix agents
for agent_path in glob.glob("/home/ubuntu/openfang/agents/*/agent.toml"):
    with open(agent_path, "r") as f:
        content = f.read()
    
    new_content = re.sub(r'model\s*=\s*"([^"]+)"', lambda m: f'model = "{get_replacement(m.group(1))}"', content)
    
    if new_content != content:
        with open(agent_path, "w") as f:
            f.write(new_content)

# Create a slimmed down custom_models.json that ONLY contains valid models
new_custom_models = []
tiers = {
    "qwen3.7-plus": "standard",
    "qwen3-vl-plus-2025-09-23": "vision",
    "qwen-vl-plus": "vision",
    "qwen-plus-2025-09-11": "standard",
    "qwen3.7-plus-2026-05-26": "standard",
    "qwen3-vl-plus": "vision",
    "qwen-mt-plus": "translation",
    "qwen-plus-character": "standard",
    "qwen3-vl-plus-2025-12-19": "vision",
    "qwen-plus-2025-04-28": "standard",
    "qwen-plus-2025-07-14": "standard",
    "qwq-plus": "reasoning"
}

for m in AVAILABLE_MODELS:
    new_custom_models.append({
        "id": m,
        "display_name": m,
        "provider": "qwen",
        "tier": tiers.get(m, "standard"),
        "aliases": [],
        "context_window": 128000,
        "max_output_tokens": 4096,
        "input_cost_per_m": 0.0,
        "output_cost_per_m": 0.0,
        "supports_tools": True,
        "supports_vision": "vl" in m,
        "supports_streaming": True
    })

with open("/home/ubuntu/openfang/custom_models.json", "w") as f:
    json.dump(new_custom_models, f, indent=2)

print("Models patched successfully.")
