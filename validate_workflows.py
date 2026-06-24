import json
import tomllib
import os
import glob

workflow_files = glob.glob('workflows/*.json') + glob.glob('workflows/*.toml')

valid_step_fields = {
    'name', 'agent', 'prompt_template', 'mode', 'timeout_secs',
    'error_mode', 'output_var', 'inherit_context', 'depends_on', 'session_mode'
}

print('=== WORKFLOW VALIDATION REPORT ===')
for f in sorted(workflow_files):
    print(f'\nChecking {f}...')
    try:
        if f.endswith('.json'):
            with open(f, 'r') as fp:
                data = json.load(fp)
        else:
            with open(f, 'rb') as fp:
                data = tomllib.load(fp)
        
        steps = data.get('steps', [])
        if not steps:
            print('  - NO STEPS FOUND')
            continue
            
        errors = []
        for i, step in enumerate(steps):
            keys = set(step.keys())
            invalid_keys = keys - valid_step_fields
            if invalid_keys:
                errors.append(f'Step {i} ({step.get("name", "unnamed")}): invalid fields {invalid_keys}')
        if errors:
            print('  - FAILED SCHEMA VALIDATION:')
            for e in errors:
                print('      ' + e)
        else:
            print('  - PASSED')
    except Exception as e:
        print(f'  - PARSE ERROR: {e}')
