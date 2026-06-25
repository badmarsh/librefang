import tomllib, json, sys, os, subprocess

workflows = ['health-check-critical', 'security-scan', 'visual-debunk-pipeline-v1']
for wf in workflows:
    path = f'/home/ubuntu/librefang/workflows/{wf}.toml'
    if not os.path.exists(path):
        print(f'Missing {path}')
        continue
    with open(path, 'rb') as f:
        data = tomllib.load(f)
    json_data = json.dumps(data)
    
    process = subprocess.Popen(
        ['/home/ubuntu/.librefang/bin/librefang', 'workflow', 'create'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=json_data.encode())
    print(f'Workflow {wf}: stdout={stdout.decode()} stderr={stderr.decode()}')
