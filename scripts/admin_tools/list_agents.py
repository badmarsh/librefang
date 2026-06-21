import glob, re, os
tomls = sorted(glob.glob('agents/*/agent.toml'))
for toml in tomls:
    agent = toml.split('/')[1]
    with open(toml) as f:
        m = re.search(r'model\s*=\s*"([^"]+)"', f.read())
        if m:
            print(f"- **{agent}**: `{m.group(1)}`")
