# Science & Literature Dezolator Integration

This implementation plan outlines the structural and methodological upgrades required to embed the requested scientific literature into the Mediálny Dezolator pipeline.

## User Review Required

> [!IMPORTANT]
> - **New Agent Creation**: We will create a brand new agent, `framing-detector`, to handle the 18-class propaganda technique taxonomy. Please review its proposed integration into the broader pipeline.
> - **CIB Threshold Calibration**: The CIB detector currently uses hardcoded temporal windows (2h/12h/72h). We will update its instructions to calibrate these thresholds against labeled campaign data dynamically.
> - **Slovak Defamation Law**: Active learning modifications will need to respect existing hard safety constraints regarding defamation law.

## Open Questions

> [!WARNING]
> - **Pipeline Routing for `framing-detector`**: Should the new `framing-detector` run in parallel with the other scoring agents (`ml-classifier`, `wiki-checker`, etc.) and feed into the `disinfo-orchestrator`, or should it be a post-processing step for the `writer` agent? (Assuming parallel scoring agent for now).
> - **Conformal Prediction Implementation**: Should conformal prediction be handled directly within `ml-classifier`'s Python script/fallback script, or solely described in its `agent.toml` instructions? (Assuming `agent.toml` prompt updates for now).

## Proposed Changes

---

### Documentation & Reference

#### [MODIFY] [ACADEMIC_REFERENCES.md](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\docs\ACADEMIC_REFERENCES.md)
- Append the 10 new academic references in their appropriate thematic sections.
- Create new sections for Conformal Prediction, Multimodal Forensics, and Persuasion Techniques.

#### [MODIFY] [annotation_guidelines.md](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\docs\annotation_guidelines.md)
- Integrate methodology from **Buntain et al. (2023)** for building the Slovak ground truth corpus using existing fact-checker verdicts (Demagog.sk, AFP Slovakia).
- Introduce Active Learning for Borderline Claim Selection (**Settles, 2012**) to resolve annotation breakdown efficiently while maintaining Krippendorff α > 0.65.

---

### ML & Calibration Upgrades

#### [MODIFY] [ml-classifier/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\ml-classifier\agent.toml)
- **Temporal Distribution Shift**: Embed temporal re-calibration strategies (**Luu et al. 2022**) and retrieval-augmented inference (**Lazaridou et al. 2022**) to handle post-2025 narrative shifts.
- **Conformal Prediction**: Replace standard Bayesian UQ with distribution-free conformal prediction (**Angelopoulos & Bates, 2021**) for stronger legal guarantees under Slovak defamation law.
- **Calibration**: Update Platt scaling references to modern deep network calibration (**Guo et al. 2017**).

---

### Detection & Analysis Agents

#### [MODIFY] [cib-detector/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\cib-detector\agent.toml)
- **Calibration**: Update temporal thresholding instructions to calibrate against labeled campaign data (**Sharma et al. 2021**).
- **Network Topology**: Integrate cascade topology analysis (**Pierri et al. 2022**) and continuous graph representation of amplification networks using GraphSAGE (**Hamilton et al. 2017**).

#### [MODIFY] [narrative-tracker/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\narrative-tracker\agent.toml)
- Introduce the SemEval-2023 Task 3 persuasion techniques taxonomy (**Piskorski et al. 2023**) to cluster narratives by framing techniques.

#### [MODIFY] [disarm-hunter/system_prompt.md](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\hands\disarm-hunter\system_prompt.md)
- Incorporate the SemEval-2023 Task 3 taxonomy (**Piskorski et al. 2023**) into the atomic decomposition rules for tracking FIMI techniques.

#### [MODIFY] [visual-analyst/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\visual-analyst\agent.toml)
- Add image provenance verification methodology (**Zlatkova et al. 2019**).
- Introduce evaluation against the FakeSV Multimodal Benchmark for short videos (**Qi et al. 2023**), critical for Telegram vectors.

#### [MODIFY] [triplet-fact-checker/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\triplet-fact-checker\agent.toml)
- Add explicit FEVER-style decomposition methodology (**Thorne et al. 2018**) to the STAGE 1 Claim Decomposition rules.

#### [MODIFY] [wiki-checker/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\wiki-checker\agent.toml)
- Expand to query structured evidence beyond Wikidata SPARQL, referencing the MultiFC framework (**Augenstein et al. 2019**).

---

### New Capabilities

#### [NEW] [framing-detector/agent.toml](file:///\\wsl.localhost\Ubuntu\home\ubuntu\librefang\agents\framing-detector\agent.toml)
- **Purpose**: A dedicated agent to identify propaganda and persuasion framing.
- **Methodology**: Implement the 18-class propaganda technique taxonomy (**Da San Martino et al. 2020** & **Piskorski et al. 2023**) including appeal to fear, loaded language, whataboutism, etc.

## Verification Plan

### Automated Tests
- `cargo test -p librefang-kernel` and `cargo test -p librefang-runtime` to ensure pipeline parsing doesn't break.
- Run `python3 scripts/maintenance/find_valid.py` to ensure `framing-detector` is registered correctly.

### Manual Verification
- Review the generated `framing-detector/agent.toml` to ensure correct integration into the LibreFang pipeline structure.
- Verify `ACADEMIC_REFERENCES.md` renders cleanly with the new citations.
