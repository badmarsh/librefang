import os
import re
import glob

KEEP_QWEN = ['disinfo-orchestrator', 'cross-lingual-aligner', 'arbiter']
LOGIC_AGENTS = ['coherence-checker', 'inquisitor', 'ml-classifier']
VISION_AGENTS = ['visual-analyst', 'clip-hand']

for agent_file in glob.glob('/home/ubuntu/librefang/agents/*/agent.toml'):
    agent_dir = os.path.dirname(agent_file)
    agent_name = os.path.basename(agent_dir)
    
    with open(agent_file, 'r') as f:
        content = f.read()
        
    if agent_name in KEEP_QWEN:
        # We need to ensure provider is qwen
        content = re.sub(r'provider\s*=\s*"[^"]+"', 'provider = "qwen"', content)
    else:
        # All other agents are on openrouter now
        content = re.sub(r'provider\s*=\s*"[^"]+"', 'provider = "openrouter"', content)

    with open(agent_file, 'w') as f:
        f.write(content)
        
print("Agent providers patched successfully.")
