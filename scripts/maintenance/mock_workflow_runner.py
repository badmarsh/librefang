import json
import sys
import re

def expand_variables(template, input_val, vars_dict):
    res = template.replace("{{input}}", str(input_val))
    # Replace input.property
    for m in re.finditer(r'\{\{input\.([a-zA-Z0-9_]+)\}\}', res):
        prop = m.group(1)
        if isinstance(input_val, dict) and prop in input_val:
            res = res.replace(m.group(0), str(input_val[prop]))
        else:
            res = res.replace(m.group(0), f"<input.{prop}>")

    for k, v in vars_dict.items():
        res = res.replace(f"{{{{{k}}}}}", str(v))
        # Handle dict property access like {{cached_asset.local_path}}
        pattern = r'\{\{' + k + r'\.([a-zA-Z0-9_]+)\}\}'
        for m in re.finditer(pattern, res):
            prop = m.group(1)
            if isinstance(v, dict) and prop in v:
                res = res.replace(m.group(0), str(v[prop]))
            else:
                res = res.replace(m.group(0), f"<{k}.{prop}>")
    return res

def get_mock_output(workflow_name, step_name):
    # Deterministic mock outputs for observability
    mocks = {
        "meme-deepfake-triage": {
            "fetch-asset": {"asset_hash": "a1b2c3d4", "local_path": "/tmp/meme.jpg"},
            "metadata-parsing": "C2PA missing. SynthID absent.",
            "vlm-forensics": "MANIPULATED: Forensic indicators show frequency domain anomalies in the facial region.",
            "generate-overlay": {"overlay_path": "/output/visual/overlays/a1b2c3d4.png"},
            "escalate-to-inquisitor": "DEBUNKED: Deepfake detected.",
            "deliver-visual-debunk": "Published post ID 12345"
        },
        "consensus-vote-protocol-v1": {
            "provenance-init": "node_789",
            "complexity-router": "COMPLEX",
            "vote-deep-reasoning": "{'verdict': 'FALSE', 'confidence': 0.9}",
            "vote-large-model": "{'verdict': 'FALSE', 'confidence': 0.85}",
            "debate-reflection": "CONSENSUS_REACHED",
            "arbiter-rubric-decision": "FALSE_DEBUNK",
            "route-decision": "Accountability workflow triggered"
        },
        "gart-evaluation-cart": {
            "synthesize-adversarial-articles": ["article1", "article2", "article3"],
            "evaluate-bypass-rate": "BYPASS_DETECTED (Rate: 5%)",
            "diagnostic-root-cause": "Missing ontology term mapping for novel slang.",
            "log-gart-results": "Logged successfully."
        },
        "desolator-omni-ingest": {
            "dynamic-osint-ingestion": ["claim_raw_1", "claim_raw_2"],
            "collect-raw-claims": ["claim_raw_1", "claim_raw_2"],
            "cross-lingual-translation": "{'claim_raw_1': 'translated_1', 'claim_raw_2': 'translated_2'}",
            "disinfo-triage-vlm": "['translated_1']",
            "wikidata-graph-enrichment": "{'translated_1': 'Entity: Politician X, Status: Active'}",
            "orchestrator-handover": "HANDOVER_SUCCESS"
        },
        "msm-historical-audit-engine": {
            "agentic-archive-retrieval": ["Prediction: 2024 collapse", "Prediction: Market boom"],
            "collect-extractions": ["Prediction: 2024 collapse", "Prediction: Market boom"],
            "historical-outcome-alignment": "Deviation found: Market did not boom.",
            "moe-debate-audit": "DEBATE_CONCLUDED",
            "ontological-narrative-mapping": "Mapped to Taxonomy: False Prognosis."
        },
        "agentic-security-redteam": {
            "codebase-surface-mapping": "Surface mapped: Auth controller.",
            "automated-exploit-generation": ["exploit_payload_1.py", "exploit_payload_2.py"],
            "collect-exploits": ["exploit_payload_1.py", "exploit_payload_2.py"],
            "dynamic-sandbox-execution": "Exploit payload 2 successful.",
            "zero-day-vulnerability-reasoning": "HIGH_SEVERITY: Privilege escalation in Auth controller."
        }
    }
    return mocks.get(workflow_name, {}).get(step_name, "MOCK_SUCCESS")

def run_workflow(filepath, initial_input):
    with open(filepath, 'r') as f:
        wf = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"🚀 STARTING WORKFLOW: {wf.get('name')} [{filepath}]")
    print(f"{'='*60}")
    
    vars_dict = {}
    current_input = initial_input
    
    for step in wf.get('steps', []):
        s_name = step.get('name', 'unnamed')
        s_mode = step.get('mode', 'sequential')
        s_agent = step.get('agent', 'system')
        
        print(f"\n🔹 STEP: {s_name} | Agent: {s_agent}")
        print(f"   [Mode]: {s_mode}")
        
        # Check conditionals
        if isinstance(s_mode, dict) and 'conditional' in s_mode:
            cond = s_mode['conditional'].get('condition', '')
            if cond.lower() not in str(current_input).lower():
                print(f"   ⏭️ SKIPPED: Condition '{cond}' not found in previous output.")
                continue
            else:
                print(f"   ✅ CONDITION MET: Found '{cond}' in previous output.")
        
        # Resolve prompt
        prompt = step.get('prompt_template', '')
        resolved_prompt = expand_variables(prompt, current_input, vars_dict)
        print(f"   [Prompt Resolved]:\n      {resolved_prompt.strip()}")
        
        # Execute mock
        mock_output = get_mock_output(wf.get('name'), s_name)
        print(f"   [Mock Output generated]: {mock_output}")
        
        # Save variables and cascade input
        current_input = mock_output
        if 'output_var' in step:
            vars_dict[step['output_var']] = mock_output
            print(f"   💾 Saved to variable '{step['output_var']}'")
            
    print(f"\n🏁 WORKFLOW COMPLETE. Final output: {current_input}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    run_workflow('workflows/c1a4f7d2-meme-deepfake-triage.json', {"asset_url": "http://evil.com/meme.jpg", "source_url": "http://twitter.com/bad"})
    run_workflow('workflows/consensus-vote.json', {"claim_id": "c_999", "claim_text": "Aliens landed in NY."})
    run_workflow('workflows/gart-evaluation.json', {"last_log": "bypass_rate: 10%"})
    run_workflow('workflows/desolator-omni-ingest.json', {"feed_url": "http://telegram.me/bad_actors"})
    run_workflow('workflows/b609beef-5d94-4fb8-8211-38f280874983.json', {"archive_source": "Dennik N", "target_narrative": "Election fraud claims 2024"})
    run_workflow('workflows/security-scan.json', {"diff": "+os.system('rm -rf /')"})
