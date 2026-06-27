import urllib.request
import urllib.error
import json
import time

API_URL = "http://127.0.0.1:4545/api/workflows"
RUN_URL = "http://127.0.0.1:4545/api/workflows/{}/run"
STATUS_URL = "http://127.0.0.1:4545/api/workflows/runs/{}"
HEADERS = {
    "Authorization": "Bearer lf_key_527679d18a9ebd59e00a049e3596f801",
    "Content-Type": "application/json"
}

# Generic mock inputs based on typical pipeline templates
MOCK_INPUTS = {
    "desolator-omni-ingest": {"feed_url": "https://example.com/disinfo-rss"},
    "msm-historical-audit-engine": {
        "archive_source": "https://sme.sk/archives",
        "target_narrative": "Global economic collapse predicted in 2024"
    },
    "agentic-security-redteam": {
        "diff": "diff --git a/src/auth.rs b/src/auth.rs\n- if password == stored {\n+ if true {"
    },
    "disinfo-pipeline": "The earth is actually flat and NASA admits it in leaked documents.",
    "coordinated-debunk-engine": "A prominent politician was caught on hot mic admitting election fraud.",
    "meme-deepfake-triage": "https://example.com/fake_image.jpg",
    "social-impact-accountability-v2": "Verdict confirmed: High severity disinformation campaign detected.",
    "default": "Generic test input string for workflow execution."
}

def fetch_workflows():
    req = urllib.request.Request(API_URL, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"Error fetching workflows: {e}")
        return []

def run_workflow(wf_id, wf_name):
    # Determine input
    input_data = MOCK_INPUTS.get(wf_name, MOCK_INPUTS["default"])
    
    payload = {"input": input_data}
    
    # Start run
    req = urllib.request.Request(RUN_URL.format(wf_id), data=json.dumps(payload).encode('utf-8'), headers=HEADERS, method='POST')
    try:
        resp = urllib.request.urlopen(req)
        run_info = json.loads(resp.read().decode())
        run_id = run_info.get("run_id")
        if not run_id:
            print(f"[{wf_name}] Started, but no run ID returned. Response: {run_info}")
            return None
        print(f"[{wf_name}] Started run: {run_id}")
        return run_id
    except urllib.error.HTTPError as e:
        print(f"[{wf_name}] Failed to start: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"[{wf_name}] Failed to start: {e}")
        return None

def poll_run(run_id, wf_name):
    print(f"[{wf_name}] Polling {run_id}...", end="", flush=True)
    req = urllib.request.Request(STATUS_URL.format(run_id), headers=HEADERS)
    
    attempts = 0
    while attempts < 30: # Max 5 mins (30 * 10s)
        try:
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read().decode())
            state = data.get("state", "unknown")
            if state in ["completed", "failed", "cancelled"]:
                print(f" {state.upper()}!")
                return data
            print(".", end="", flush=True)
        except Exception as e:
            print(f" Error polling: {e}")
            break
        time.sleep(5)
        attempts += 1
    
    print(" TIMEOUT!")
    return None

def main():
    workflows = fetch_workflows()
    if not workflows:
        print("No workflows found.")
        return

    results = []
    
    print(f"Executing {len(workflows)} workflows sequentially...")
    
    for wf in workflows:
        wf_id = wf.get("id")
        wf_name = wf.get("name", "unknown")
        
        run_id = run_workflow(wf_id, wf_name)
        if run_id:
            final_state = poll_run(run_id, wf_name)
            results.append({
                "name": wf_name,
                "id": wf_id,
                "run_id": run_id,
                "result": final_state
            })
        else:
            results.append({
                "name": wf_name,
                "id": wf_id,
                "error": "Failed to start"
            })
            
    # Write report
    with open('/home/ubuntu/librefang/scratch/workflow_execution_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nExecution complete. Results saved to scratch/workflow_execution_results.json.")

if __name__ == "__main__":
    main()
