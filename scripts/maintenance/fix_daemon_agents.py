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
        
        # Replace the problematic models with ovh/Meta-Llama-3_3-70B-Instruct
        new_content = re.sub(r'model\s*=\s*\"[^\"]*llama-3\.1-8b-instruct[^\"]*\"', 'model = \"ovh/Meta-Llama-3_3-70B-Instruct\"', content)
        new_content = re.sub(r'model\s*=\s*\"[^\"]*nemotron[^\"]*\"', 'model = \"ovh/Meta-Llama-3_3-70B-Instruct\"', new_content)
        new_content = re.sub(r'model\s*=\s*\"nvidia[^\"]*\"', 'model = \"ovh/Meta-Llama-3_3-70B-Instruct\"', new_content)
        
        # Also ensure provider is freellmpool
        new_content = re.sub(r'provider\s*=\s*\"[^\"]*\"', 'provider = \"freellmpool\"', new_content)
        
        if content != new_content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f'Updated {file_path}')
