import os, glob

for path in glob.glob("/home/ubuntu/librefang/agents/*/agent.toml"):
    with open(path, "r") as f:
        content = f.read()
    
    changed = False
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('task =') or line.strip().startswith('task='):
            lines[i] = '# ' + line
            changed = True
        elif line.strip().startswith('session_mode =') or line.strip().startswith('session_mode='):
            lines[i] = '# ' + line
            changed = True
            
    if changed:
        with open(path, "w") as f:
            f.write('\n'.join(lines))
        print(f"Fixed {path}")
