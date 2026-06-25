import os
import glob
import re

directories = [
    '/home/ubuntu/.librefang/registry/agents/*/agent.toml',
    '/home/ubuntu/.librefang/workspaces/agents/*/agent.toml'
]

for directory in directories:
    for file_path in glob.glob(directory):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Change model from ovh/Meta... to nvidia/llama-3.3-nemotron-super-49b-v1.5
        new_content = re.sub(r'model\s*=\s*"[^"]*"', 'model = "nvidia/llama-3.3-nemotron-super-49b-v1.5"', content)
        
        # Change provider to nvidia-nim
        new_content = re.sub(r'provider\s*=\s*"[^"]*"', 'provider = "nvidia-nim"', new_content)
        
        if content != new_content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f'Updated {file_path}')
