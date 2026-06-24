import os
import glob
import re

agent_dir = "/home/ubuntu/librefang/agents"
for toml_file in glob.glob(os.path.join(agent_dir, "*", "agent.toml")):
    with open(toml_file, "r") as f:
        content = f.read()
    
    # Replace any model = "nvidia/..." with model = "ovh/Meta-Llama-3_3-70B-Instruct"
    new_content = re.sub(r'model\s*=\s*"nvidia/[^"]+"', 'model = "ovh/Meta-Llama-3_3-70B-Instruct"', content)
    
    if new_content != content:
        with open(toml_file, "w") as f:
            f.write(new_content)
        print(f"Updated {toml_file}")
