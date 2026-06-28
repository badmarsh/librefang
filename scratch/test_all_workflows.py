import urllib.request
import urllib.error
import json

base_url = 'http://127.0.0.1:4545/api'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer lf_key_527679d18a9ebd59e00a049e3596f801'
}

def test_workflows():
    try:
        req = urllib.request.Request(f'{base_url}/workflows', headers=headers)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        workflows = data.get('items', [])
        
        print(f"Found {len(workflows)} workflows. Testing...")
        
        for wf in workflows:
            wid = wf['id']
            name = wf['name']
            print(f"\n--- Running {name} ({wid}) ---")
            run_req = urllib.request.Request(
                f'{base_url}/workflows/{wid}/run?wait=true',
                data=b'{"input":"test payload"}',
                headers=headers
            )
            try:
                run_resp = urllib.request.urlopen(run_req, timeout=30)
                run_data = json.loads(run_resp.read())
                print(f"Success. State: {run_data.get('state')}")
                if 'error' in run_data and run_data['error']:
                    print(f"Error payload: {run_data['error']}")
                else:
                    print(f"Result length: {len(str(run_data))}")
            except urllib.error.HTTPError as e:
                print(f"HTTP {e.code}: {e.read().decode('utf-8')}")
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Failed to fetch workflows: {e}")

if __name__ == '__main__':
    test_workflows()
