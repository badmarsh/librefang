import json
import glob
import tomllib
import os

for toml_file in glob.glob('workflows/*.toml'):
    json_file = toml_file.replace('.toml', '.json')
    with open(toml_file, 'rb') as f:
        try:
            data = tomllib.load(f)
        except Exception as e:
            print(f"Failed to parse {toml_file}: {e}")
            continue
            
    if 'steps' in data:
        for step in data['steps']:
            if 'agent' in step:
                agent_val = step.pop('agent')
                if isinstance(agent_val, dict) and 'name' in agent_val:
                    step['agent_name'] = agent_val['name']
                elif isinstance(agent_val, str):
                    step['agent_name'] = agent_val
                    
    with open(json_file, 'w') as f:
        json.dump(data, f)
