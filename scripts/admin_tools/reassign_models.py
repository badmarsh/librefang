import os
import re
import glob

# Mappings for specific agents to retain high intelligence Qwen
KEEP_QWEN = ['disinfo-orchestrator', 'cross-lingual-aligner', 'arbiter']

# Mappings for logic models
LOGIC_AGENTS = ['coherence-checker', 'inquisitor', 'ml-classifier']

# Mappings for vision models
VISION_AGENTS = ['visual-analyst', 'clip-hand']

for agent_file in glob.glob('/home/ubuntu/openfang/agents/*/agent.toml'):
    agent_dir = os.path.dirname(agent_file)
    agent_name = os.path.basename(agent_dir)
    
    with open(agent_file, 'r') as f:
        content = f.read()
        
    if agent_name in KEEP_QWEN:
        # keep it as it is (it was already patched to qwen3.7-plus or similar)
        continue
    elif agent_name in LOGIC_AGENTS:
        new_model = 'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free'
    elif agent_name in VISION_AGENTS:
        new_model = 'nvidia/nemotron-nano-12b-v2-vl:free'
    else:
        new_model = 'nvidia/nemotron-3-super-120b-a12b:free'

    # Regex to replace model = "..."
    content = re.sub(r'model\s*=\s*"[^"]+"', f'model = "{new_model}"', content)
    
    with open(agent_file, 'w') as f:
        f.write(content)
        
print("Agent models updated successfully.")
