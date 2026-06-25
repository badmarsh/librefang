import json
import tomllib
import tomli_w
import os
import glob

workflow_files = glob.glob('workflows/*.json') + glob.glob('workflows/*.toml')

valid_step_fields = {
    'name', 'agent', 'prompt_template', 'mode', 'timeout_secs',
    'error_mode', 'output_var', 'inherit_context', 'depends_on', 'session_mode'
}

for f in workflow_files:
    print(f"Refactoring {f}...")
    is_json = f.endswith('.json')
    try:
        if is_json:
            with open(f, 'r') as fp:
                data = json.load(fp)
        else:
            with open(f, 'rb') as fp:
                data = tomllib.load(fp)
    except Exception as e:
        print(f"Failed to read {f}: {e}")
        continue

    steps = data.get('steps', [])
    new_steps = []
    
    for step in steps:
        new_step = {}
        # retain valid keys that are present
        for k in valid_step_fields:
            if k in step:
                new_step[k] = step[k]
        
        # fix missing agent
        if 'agent' not in new_step:
            new_step['agent'] = 'orchestrator'
            
        # check mode overrides
        mode_set = False
        if 'condition' in step:
            new_step['mode'] = {'conditional': {'condition': step['condition']}}
            mode_set = True
        elif 'parallel' in step and step['parallel'] is True:
            new_step['mode'] = 'fan_out'
            mode_set = True
        elif 'wait' in step:
            # legacy wait -> collect, if not using depends_on
            if 'depends_on' not in step:
                new_step['mode'] = 'collect'
                mode_set = True
        
        new_steps.append(new_step)
        
    data['steps'] = new_steps
    
    # write back
    if is_json:
        with open(f, 'w') as fp:
            json.dump(data, fp, indent=2)
    else:
        with open(f, 'wb') as fp:
            tomli_w.dump(data, fp)

print("Done refactoring.")
