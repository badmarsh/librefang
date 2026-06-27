import os, glob

def fix_file(path):
    with open(path, "r") as f:
        content = f.read()
    
    changed = False
    
    # Fix [schedule.cron]
    if "[schedule.cron]" in content:
        content = content.replace("[schedule.cron]", "[schedule.periodic]")
        changed = True
        
    # Fix [schedule] -> [schedule.periodic] in queue-monitor
    if "queue-monitor" in path and "[schedule]" in content:
        content = content.replace("[schedule]", "[schedule.periodic]")
        changed = True
        
    # Fix claim-extractor duplicate model
    if "claim-extractor" in path and "[model]\n[model]" in content:
        content = content.replace("[model]\n[model]", "[model]")
        changed = True
        
    if "predictor-hand" in path and "system_prompt =" not in content and "[Detailed prediction entries" in content:
        parts = content.split("[Detailed prediction entries with reasoning chains]")
        if len(parts) == 2:
            content = parts[0] + "system_prompt = \"\"\"\n[Detailed prediction entries with reasoning chains]" + parts[1]
            # Need to end the string at the end
            content += "\n\"\"\"\n"
            changed = True
            
    if changed:
        with open(path, "w") as f:
            f.write(content)
        print(f"Fixed {path}")

for path in glob.glob("/home/ubuntu/librefang/agents/*/agent.toml"):
    fix_file(path)
