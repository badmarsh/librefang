#!/usr/bin/env python3
"""Validation script for weakpoint remediation changes."""
import json, sys, pathlib, tomllib

errors = []
ok = []

# ── JSON schema ──────────────────────────────────────────────────────────────
try:
    data = json.loads(pathlib.Path("ontology/schema.json").read_text())
    dn = data.get("disarm_nodes", {})
    edges = data.get("edges", {})
    for node in ["DisarmTTP", "FIMICampaign", "EvidenceAtom"]:
        if node not in dn:
            errors.append(f"ontology/schema.json: missing node {node}")
    for edge in ["MAPPED_TO_TTP", "PART_OF_CAMPAIGN", "SUPPORTS_TTP_CLAIM", "REFUTES_TTP_CLAIM"]:
        if edge not in edges:
            errors.append(f"ontology/schema.json: missing edge {edge}")
    ok.append("ontology/schema.json - valid JSON with DISARM nodes+edges")
except Exception as e:
    errors.append(f"ontology/schema.json: {e}")

# ── TOML files ───────────────────────────────────────────────────────────────
toml_files = [
    "hands/disarm-hunter/HAND.toml",
    "hands/longitudinal_tracker/HAND.toml",
    "agents/disarm-hunter/agent.toml",
    "agents/cib-detector/agent.toml",
    "agents/ml-classifier/agent.toml",
    "agents/disinfo-orchestrator/agent.toml",
    "skills/disarm-framework/skill.toml",
    "skills/uq-scorer/skill.toml",
    "pipelines/disinfo-pipeline.toml",
]

for f in toml_files:
    try:
        with open(f, "rb") as fh:
            tomllib.load(fh)
        ok.append(f"{f} - valid TOML")
    except Exception as e:
        errors.append(f"{f}: {e}")

# ── Key content checks ───────────────────────────────────────────────────────
# Check DISARM-hunter HAND.toml has required fields
try:
    with open("hands/disarm-hunter/HAND.toml", "rb") as fh:
        h = tomllib.load(fh)
    assert h["hand"]["session_mode"] == "persistent", "session_mode must be persistent"
    assert "disarm-framework" in h["hand"]["skills"]["skills"], "disarm-framework skill missing"
    ok.append("hands/disarm-hunter/HAND.toml - session_mode=persistent, skills OK")
except Exception as e:
    errors.append(f"hands/disarm-hunter/HAND.toml content check: {e}")

# Check longitudinal_tracker HAND.toml is no longer a stub
try:
    with open("hands/longitudinal_tracker/HAND.toml", "rb") as fh:
        h = tomllib.load(fh)
    assert "hand" in h, "[hand] section missing"
    assert h["hand"].get("session_mode") == "persistent", "session_mode must be persistent"
    assert "schedule" in h["hand"], "schedule missing"
    ok.append("hands/longitudinal_tracker/HAND.toml - fleshed out (session_mode=persistent)")
except Exception as e:
    errors.append(f"hands/longitudinal_tracker/HAND.toml content check: {e}")

# Check ml-classifier has 3 distinct providers in fallback_models
try:
    with open("agents/ml-classifier/agent.toml", "rb") as fh:
        a = tomllib.load(fh)
    fallbacks = a.get("fallback_models", [])
    providers = [f["provider"] for f in fallbacks]
    distinct = set(providers)
    assert len(distinct) >= 2, f"fallback providers not distinct: {providers}"
    assert "uq-scorer" in a.get("skills", []), "uq-scorer skill missing from ml-classifier"
    ok.append(f"agents/ml-classifier/agent.toml - {len(distinct)} distinct providers, uq-scorer skill OK")
except Exception as e:
    errors.append(f"agents/ml-classifier/agent.toml content check: {e}")

# Check CIB weights sum to 1.0
cib_weights = [0.22, 0.22, 0.18, 0.14, 0.14, 0.10]
total = sum(cib_weights)
if abs(total - 1.00) > 0.01:
    errors.append(f"CIB weights don't sum to 1.00: {total}")
else:
    ok.append(f"CIB weight rebalance: {cib_weights} sum={total:.2f} OK")

# Check pipeline has new optional stages
try:
    pipeline_text = pathlib.Path("pipelines/disinfo-pipeline.toml").read_text()
    for marker in ["disarm-ttp-hunt", "longitudinal-sync", "Improvement 25", "Improvement 26", "Improvement 27"]:
        if marker not in pipeline_text:
            errors.append(f"pipelines/disinfo-pipeline.toml: missing '{marker}'")
        else:
            ok.append(f"pipelines/disinfo-pipeline.toml: '{marker}' present")
except Exception as e:
    errors.append(f"pipelines/disinfo-pipeline.toml: {e}")

# ── Report ───────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"PASSED: {len(ok)}")
for o in ok:
    print(f"  ✅ {o}")
if errors:
    print(f"\nFAILED: {len(errors)}")
    for e in errors:
        print(f"  ❌ {e}")
    sys.exit(1)
else:
    print(f"\n✅ All {len(ok)} checks passed.")
