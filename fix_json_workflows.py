import json
import glob
import os

for json_file in glob.glob('workflows/*.json'):
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Failed to parse {json_file}: {e}")
            continue
            
    modified = False
    if 'steps' in data:
        for step in data['steps']:
            if 'agent' in step:
                agent_val = step.pop('agent')
                if isinstance(agent_val, dict) and 'name' in agent_val:
                    step['agent_name'] = agent_val['name']
                elif isinstance(agent_val, str):
                    step['agent_name'] = agent_val
                modified = True
                
    if modified:
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Fixed {json_file}")
