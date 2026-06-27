import os, glob, re

for path in glob.glob("/home/ubuntu/librefang/agents/*/agent.toml"):
    with open(path, "r") as f:
        content = f.read()
    
    changed = False
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if re.match(r'^\s*task\s*=', line):
            lines[i] = '# ' + line
            changed = True
        elif re.match(r'^\s*session_mode\s*=', line):
            lines[i] = '# ' + line
            changed = True
            
    if changed:
        with open(path, "w") as f:
            f.write('\n'.join(lines))
        print(f"Fixed {path}")
