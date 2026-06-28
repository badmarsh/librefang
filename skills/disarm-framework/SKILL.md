---
name: disarm-framework
description: >
  DISARM v1.5 Tactics, Techniques, Procedures (TTP) taxonomy for FIMI investigation.
  Use when classifying disinformation verdicts against the DISARM framework, mapping
  narrative clusters to TTP IDs, constructing TTP hypotheses for the DISARM-hunter
  hunting loop, or querying the four-phase FIMI kill-chain (Plan/Prepare/Execute/Assess).
  Do not use for generic fact-checking tasks — use this only when DISARM TTP classification
  or FIMI campaign attribution is required.
---

# DISARM Framework v1.5 — Skill Context

A structured adversary behaviour vocabulary for describing Foreign Information Manipulation
and Interference (FIMI) operations. Analogous to MITRE ATT&CK for cyber threats.

**Source**: DISARMFoundation/DISARMframeworks
**Version**: v1.5 (2024)
**Full JSON taxonomy**: https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/DISARM_STIX/DISARM.json
**DISARM Navigator**: https://disarm.foundation/navigator

---

## Four-Phase Kill Chain

```
Phase 1: PLAN      TA01  Assess vulnerabilities, identify target audience, develop strategy
Phase 2: PREPARE   TA02–TA08  Create/acquire assets: personas, content, infrastructure
Phase 3: EXECUTE   TA09–TA15  Deploy: microtarget, post, engage, amplify, legitimise
Phase 4: ASSESS    TA16  Measure effect, adapt, iterate
```

---

## Tactic–Technique Map (curated subset for Slovak/CEE FIMI context)

### Phase 1: PLAN

| TTP ID | Name | Signal |
|--------|------|--------|
| T0003 | Develop Competing Narratives | Parallel counter-narratives seeded across outlets |
| T0065 | Leverage Conspiracy Theory Narratives | Existing conspiracy templates adapted |
| T0066 | Identify Wedge Issues | Exploit cultural/political fault lines |

### Phase 2: PREPARE

| TTP ID | Name | Signal |
|--------|------|--------|
| T0010 | Create Fake Experts | Sockpuppet academics, fake NGO spokespeople |
| T0014 | Acquire Social Media Accounts | Account farm acquisition, aged accounts |
| T0017 | Promote Newsletters | Obscure newsletter seeding into media ecosystem |
| T0020 | Establish Legitimising Narratives | Building credibility infrastructure |
| T0021 | Establish Social Media Groups/Pages | Facebook groups, Telegram channels |
| T0061 | Develop AI-Generated Text | LLM-produced content at scale |

### Phase 3: EXECUTE

| TTP ID | Name | Signal |
|--------|------|--------|
| T0007 | Coordinate Inauthentic Accounts | Cross-account amplification with temporal sync |
| T0019 | Generate Information Pollution | High-volume low-quality content flooding |
| T0023 | Distort Facts | Selective framing, cherry-picking, misleading context |
| T0029 | Messaging Bombing | Sustained high-frequency repeat of single message |
| T0046 | Search Engine Optimisation Manipulation | Keyword stuffing, SEO farms |
| T0049 | Flooding | Overwhelming discourse with volume (alias of T0029 in v1.5) |
| T0057 | Organise Events | Real-world events to generate media amplification |
| T0073 | Use AI-Generated Content for Amplification | AIGC replacing repetitive human posts |

### Phase 4: ASSESS

| TTP ID | Name | Signal |
|--------|------|--------|
| T0083 | Measure Effectiveness of Messaging | Engagement tracking, A/B narrative testing |
| T0084 | Adapt Messaging Based on Feedback | Content pivot when narrative fails |

---

## DISARM Entity Types (ontology vocabulary)

When creating DISARM-linked knowledge graph entities, use these types:

```
DisarmTTP {
  id:           string  -- internal UUID
  ttp_id:       string  -- DISARM ID e.g. "T0007"
  name:         string  -- human-readable TTP name
  phase:        enum    -- PLAN | PREPARE | EXECUTE | ASSESS
  tactic_id:    string  -- parent tactic e.g. "TA09"
  first_detected: datetime
  last_seen:    datetime
  confidence:   float   -- 0.0–1.0, based on Fisher OR
  status:       enum    -- ACTIVE | DORMANT | HISTORICAL
}

FIMICampaign {
  id:           string
  label:        string  -- descriptive campaign name
  attributed_to: string -- actor or state if attributed
  ttps:         array   -- list of DisarmTTP IDs
  first_seen:   datetime
  last_seen:    datetime
  target_country: string -- ISO 3166-1 alpha-2
}

EvidenceAtom {
  id:           string
  claim_text:   string  -- the atomic SQL-testable assertion
  ttp_id:       string  -- linked DISARM TTP
  verdict:      enum    -- PASS | INSUFFICIENT_EVIDENCE
  odds_ratio:   float
  p_value:      float
  supporting_count: int
  created_at:   datetime
}
```

---

## Statistical Gate Reference

Before marking any TTP as PASS (per Tseng et al. arXiv:2601.15109):

```
Contingency table (2×2):
                    | Confirmed DISINFO | Not disinfo |
  Matches TTP hyp. |       a           |      b      |
  No TTP match     |       c           |      d      |

Odds Ratio:  OR = (a·d) / (b·c)
Requirement: OR ≥ 3.0  AND  p < 0.05  AND  a ≥ 5

Chi-squared approximation: χ² = N·(ad-bc)² / ((a+b)(c+d)(a+c)(b+d))
Use Fisher's exact test when any expected cell < 5.
```

---

## Integration with Pipeline

- **DISARM-hunter Hand** runs nightly, queries `orchestrator.verdicts` and `cib_detector.*`
  to test TTP hypotheses. Results written to `disarm_hunter.session_summary` and
  `output/disarm_audit.jsonl`.
- **disinfo-orchestrator** reads `disarm_hunter.*` and appends `disarm_ttp_ids` to
  each verdict in the audit log.
- **Ontology skill** stores `DisarmTTP`, `FIMICampaign`, `EvidenceAtom` entities in
  `memory/ontology/graph.jsonl`.

## Ontology Skill Contract

```yaml
ontology:
  reads:  [NarrativeCluster, Claim, Actor]
  writes: [DisarmTTP, FIMICampaign, EvidenceAtom]
  preconditions:
    - "EvidenceAtom.odds_ratio must be >= 3.0 before writing DisarmTTP with status=ACTIVE"
  postconditions:
    - "Each PASS DisarmTTP is linked to at least 1 EvidenceAtom"
    - "Each EvidenceAtom is linked to at least 1 Claim via SUPPORTS_TTP_CLAIM"
```
