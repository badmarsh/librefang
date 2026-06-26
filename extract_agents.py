import os
import toml
import json

agents = [
    "arbiter", "archivist", "browser-hand", "cib-detector", "claim-decomposer",
    "claim-extractor", "coherence-checker", "collector-hand", "compliance-officer",
    "cross-domain-evaluator", "cross-lingual-aligner", "dennikn", "disarm-hunter",
    "disinfo-orchestrator", "gart-synthesizer", "impact-comms", "injection-shield",
    "inquisitor", "investigator", "kg-consistency-checker", "ml-classifier",
    "narrative-tracker", "ontology", "predictor-hand", "queue-monitor",
    "research-analyst", "researcher-hand", "source-rater", "speculative",
    "stance-detector", "temporal-checker", "triplet-fact-checker", "visual-analyst",
    "watchdog", "wiki-checker", "writer", "network-mapper"
]

results = {}

for name in agents:
    path = f"/home/ubuntu/librefang/agents/{name}/agent.toml"
    if not os.path.exists(path):
        # try hands
        path = f"/home/ubuntu/librefang/hands/{name}/HAND.toml"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = toml.load(f)
            
            agent_data = data.get("agent", data.get("hand", {}))
            capabilities = agent_data.get("capabilities", {})
            
            results[name] = {
                "version": agent_data.get("version", ""),
                "tags": agent_data.get("tags", []),
                "reads": capabilities.get("memory_read", []),
                "writes": capabilities.get("memory_write", []),
                "tools": agent_data.get("tools", []),
                "skills": agent_data.get("skills", []),
                "mcp_servers": agent_data.get("mcp_servers", []),
                "system_prompt": agent_data.get("system_prompt", "")[:200] + "..." # just excerpt
            }
        except Exception as e:
            results[name] = {"error": str(e)}

with open("/home/ubuntu/librefang/scratch_agents.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

