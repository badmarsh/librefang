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
        
        # Replace api_key_env
        new_content = re.sub(r'api_key_env\s*=\s*"[^"]*"', 'api_key_env = "NVIDIA_API_KEY"', content)
        
        if content != new_content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f'Updated api_key_env in {file_path}')
