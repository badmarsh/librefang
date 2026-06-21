#!/usr/bin/env python3
"""
Patch all agent TOMLs:
1. Replace model IDs not in the DashScope quota list with valid equivalents
2. Update DASHSCOPE_API_KEY env var references
"""
import os
import re
import glob

AGENTS_DIR = "/home/ubuntu/librefang/agents"

# Models in use → replacement (only for models NOT in quota list)
MODEL_REMAP = {
    # plain "qwen-plus" → "qwen-plus-2025-07-28" (has 1M quota)
    '"qwen-plus"': '"qwen-plus-2025-07-28"',
    '"qwen-plus-latest"': '"qwen-plus-2025-07-28"',
    # exhausted flagship reasoning → use qwen3.7-plus (has 1M quota)
    '"qwen3.5-397b-a17b"': '"qwen3.7-plus"',
    # model with enable_thinking restriction → use qwen3.7-plus
    '"qwen3-235b-a22b"': '"qwen3.7-plus"',
    # old coder date suffix not in list → use base name (has 1M quota)
    '"qwen3-coder-plus-2025-07-22"': '"qwen3-coder-plus"',
    '"qwen3-coder-plus"': '"qwen3-max"',
}

patched = []
skipped = []

for toml_path in sorted(glob.glob(f"{AGENTS_DIR}/*/agent.toml")):
    with open(toml_path, "r") as f:
        content = f.read()

    original = content
    for old, new in MODEL_REMAP.items():
        content = content.replace(f"model = {old}", f"model = {new}")

    if content != original:
        with open(toml_path, "w") as f:
            f.write(content)
        agent = toml_path.split("/")[-2]
        # show what changed
        for old, new in MODEL_REMAP.items():
            if old in original and new.replace('"','') in content:
                patched.append(f"  {agent}: {old} → {new}")
    else:
        skipped.append(toml_path.split("/")[-2])

print("=== Agent Model Patch Report ===")
print(f"\nPatched ({len(patched)} changes):")
for p in patched:
    print(p)
print(f"\nNo change needed ({len(skipped)} agents):")
print("  " + ", ".join(skipped))

# Also verify the full model inventory after patching
print("\n=== Post-patch Model Distribution ===")
from collections import Counter
counter = Counter()
for toml_path in glob.glob(f"{AGENTS_DIR}/*/agent.toml"):
    with open(toml_path) as f:
        for line in f:
            m = re.match(r'^model\s*=\s*"([^"]+)"', line.strip())
            if m:
                counter[m.group(1)] += 1
for model, count in sorted(counter.items(), key=lambda x: -x[1]):
    print(f"  {count:3d}  {model}")
