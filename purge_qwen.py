import glob, re

modified_files = []
for f in glob.glob('/home/ubuntu/librefang-dedup/agents/*/agent.toml'):
    with open(f, 'r') as fp:
        c = fp.read()
    if 'Qwen' in c or 'qwen' in c:
        parts = c.split('[[fallback_models]]')
        new_parts = [parts[0]]
        for p in parts[1:]:
            if 'Qwen' not in p and 'qwen' not in p:
                new_parts.append('[[fallback_models]]' + p)
        new_c = ''.join(new_parts)
        # Handle cases where the main model is qwen
        # Wait, the prompt says "Audit Qwen fallback models: Identify and purge remaining Qwen models from all agent manifests."
        # If Qwen is the main model, it needs to be replaced.
        # But wait, Qwen3.5-397B-A17B is often the main model!
        # If I remove it without replacement, the agent will have no model!
        # Let's see if the prompt said "Qwen fallback models" specifically.
        # Yes: "Audit Qwen fallback models: Identify and purge remaining Qwen models from all agent manifests."
        # If it meant MAIN models too, I should replace it with llama-3.3-70b-instruct or similar.
        # But let's only purge fallback models first.
        with open(f, 'w') as fp:
            fp.write(new_c)
        modified_files.append(f)
print('Purged from:', len(modified_files), 'files')
