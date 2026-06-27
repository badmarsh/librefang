import glob, json, os

out = ""
files = glob.glob('/home/ubuntu/librefang/workflows/*.json')
for f in sorted(files):
    try:
        with open(f, 'r') as fh:
            data = json.load(fh)
        name = data.get('name', os.path.basename(f))
        desc = data.get('description', '')
        trigger = data.get('trigger', {})
        t_event = trigger.get('event', 'manual') if isinstance(trigger, dict) else trigger
        t_sched = trigger.get('schedule', '') if isinstance(trigger, dict) else ''
        t_sched_dict = trigger.get('cron', '') if isinstance(trigger, dict) else ''
        if trigger and 'cron' in trigger:
            t_sched = trigger['cron']
        if 'schedule' in data and 'cron' in data['schedule']:
            t_sched = data['schedule']['cron']
            t_event = 'scheduled'
        
        steps = data.get('steps', [])
        step_names = [s.get('name', 'unnamed') for s in steps]
        final_output = steps[-1].get('output_var', 'None') if steps else 'None'
        
        out += f"## {name}\n"
        out += f"**Description:** {desc}\n"
        out += f"**Current Trigger:** {t_event} / {t_sched}\n"
        out += f"**Steps ({len(steps)}):** {', '.join(step_names)}\n"
        out += f"**Final Output Var:** {final_output}\n\n"
    except Exception as e:
        out += f"Error on {f}: {e}\n\n"

with open('/home/ubuntu/librefang/scratch/dump.md', 'w') as fh:
    fh.write(out)
