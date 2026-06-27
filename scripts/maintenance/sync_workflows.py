import urllib.request, urllib.error, json, os, glob

API_URL = 'http://127.0.0.1:4545/api/workflows'
HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer lf_key_527679d18a9ebd59e00a049e3596f801'}

def sync():
    # 1. Fetch all existing workflows
    print("Fetching current workflows...")
    req = urllib.request.Request(API_URL, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req)
        existing = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Failed to fetch workflows: {e}")
        return

    print(f"Found {len(existing.get('items', existing))} existing workflows. Deleting...")
    
    workflows_to_delete = existing.get('items', existing) if isinstance(existing, dict) else existing
    for wf in workflows_to_delete:
        wf_id = wf if isinstance(wf, str) else wf.get('id')
        if wf_id:
            del_req = urllib.request.Request(f"{API_URL}/{wf_id}", headers=HEADERS, method='DELETE')
            try:
                urllib.request.urlopen(del_req)
                print(f"Deleted {wf_id}")
            except Exception as e:
                print(f"Failed to delete {wf_id}: {e}")

    # 2. Upload correct workflows
    print("Uploading correct workflows from repository...")
    repo_workflows = glob.glob('/home/ubuntu/librefang/workflows/*.json')
    print(f"Found {len(repo_workflows)} workflows to upload.")
    
    for f in repo_workflows:
        try:
            with open(f, 'rb') as file:
                data = json.load(file)
            
            # Fix up agent strings for the API
            if 'steps' in data and isinstance(data['steps'], list):
                for step in data['steps']:
                    if 'agent' in step:
                        if isinstance(step['agent'], str):
                            step['agent_name'] = step['agent']
                        elif isinstance(step['agent'], dict) and 'name' in step['agent']:
                            step['agent_name'] = step['agent']['name']
                        del step['agent']

            req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'), headers=HEADERS)
            resp = urllib.request.urlopen(req)
            print(f'Uploaded {os.path.basename(f)}')
        except urllib.error.HTTPError as e:
            print(f'Failed to upload {f}: {e.code} {e.read().decode()}')
        except Exception as e:
            print(f'Error uploading {f}: {e}')

if __name__ == '__main__':
    sync()
