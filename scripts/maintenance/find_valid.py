import json, glob
running = ["academic-researcher", "analyst-subagent", "arbiter", "architect", "archivist", "browser-subagent", "cib-detector", "claim-decomposer", "claim-extractor", "clip-hand", "coherence-checker", "dennikn", "disinfo-orchestrator", "framing-detector", "impact-comms", "inquisitor", "investigator", "kg-consistency-checker", "ml-classifier", "narrative-tracker", "predictor-hand", "qsvm-classifier", "research-analyst", "research-lead", "researcher", "researcher-hand", "source-rater", "stance-detector", "temporal-checker", "triplet-fact-checker", "visual-analyst", "watchdog", "wiki-checker"]
valid = []
for f in glob.glob("workflows/*.json"):
    with open(f) as fp:
        try:
            d = json.load(fp)
            agents = {s.get("agent_name") for s in d.get("steps", []) if "agent_name" in s}
            if all(a in running for a in agents):
                valid.append(f)
        except:
            pass
print("VALID WORKFLOWS:", valid)
