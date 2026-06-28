# LibreFang Workflows: Theoretical Research & Architectural Proposals

Based on the initial analysis of the broken workflows in the `workflows/` directory, here is the theoretical research and proposed modernization architecture for each workflow.

## 1. Meme & Deepfake Triage (`c1a4f7d2-meme-deepfake-triage.json`)

### **Current State & Intended Function**
A sequential visual disinformation pipeline that fetches an asset, runs OCR, reasons about authenticity (manipulation, out-of-context, deepfakes) using a single Vision-Language Model (VLM), generates an overlay, and escalates to a human/inquisitor if confidence is low.

### **State-of-the-Art (SOTA) Forensics Methodologies**
* **Cross-Modal Consistency Checking**: Modern VLM forensics rely on separating the visual content from the textual content and evaluating their semantic alignment. A mismatch often indicates "cheap fakes" (out-of-context misattribution).
* **Ensemble Artifact Detection**: Relying on a single prompt for both OCR layout anomalies and pixel-level deepfake artifacts is sub-optimal. SOTA approaches use specialized models (e.g., frequency-domain analysis for GAN/Diffusion artifacts, spatial layout analysis for text tampering).
* **Multi-Turn Visual Q&A**: Iteratively querying the image based on initial findings rather than a single zero-shot prompt.

### **Proposed Architectural Improvements**
1. **Parallelized Expert Analysis (Branching)**: Split the `visual-reason` step into a `Branch` mode that concurrently runs:
   * **Deepfake/Pixel Forensics**: Focuses strictly on synthetic generation artifacts.
   * **Semantic/Contextual Analysis**: Compares OCR text against the visual context for misattribution.
2. **Dynamic Escalation Routing**: Instead of purely sequential escalation based on `< 0.85` confidence, route the workflow dynamically. If the pixel forensics score is highly anomalous but semantic score is normal, route to a specialized deepfake inquisitor rather than a generic fact-checker.

---

## 2. Consensus Vote Protocol (`consensus-vote.json`)

### **Current State & Intended Function**
A fan-out MoE (Mixture-of-Experts) pattern where a claim is evaluated blindly and independently by a deep-reasoning agent, a large model agent, a retrieval agent, and a visual agent. An arbiter then aggregates these votes using a weighted Bayesian merge to make a final routing decision.

### **State-of-the-Art (SOTA) Mixture-of-Experts (MoE) Routing**
* **Multi-Agent Debate & Reflection**: Isolated voting is good for preventing bias, but SOTA multi-agent systems often introduce a secondary "debate" phase. If experts strongly disagree (high variance), they are allowed to see each other's reasoning and refine their vote before the arbiter decides.
* **Programmatic Reward Models (PRMs)**: The arbiter evaluates the step-by-step logic of the experts rather than just their final confidence scores.
* **Dynamic Expert Selection**: Instead of always calling the same three models, a router first analyzes the claim's domain (e.g., medical, political, visual) and dynamically selects the most relevant expert nodes.

### **Proposed Architectural Improvements**
1. **Two-Phase Consensus (Vote -> Debate -> Arbiter)**: Introduce a conditional `Sequential` step after the `FanOut`. If the arbiter detects high divergence (e.g., retrieval says False, deep-reasoning says True), trigger a "Debate" step where experts critique the opposing reasoning chain.
2. **Refined Arbiter Node**: Update the arbiter to output not just a weighted decision, but a structured "Controversy Score" that determines the routing path.

---

## 3. GART Evaluation (`gart-evaluation.toml`)

### **Current State & Intended Function**
A weekly scheduled Red Teaming workflow that generates 20 adversarial articles to test the pipeline's bypass rate. It uses a static 30% threshold to trigger an alert and strictly segregates adversarial data from the Bayesian training loop.

### **State-of-the-Art (SOTA) Agentic CI/CD Red-Teaming**
* **Adaptive/Reinforcement Red Teaming**: Instead of blindly generating 20 articles using static strategies (A-E), modern red-teaming agents use previous successful bypasses as few-shot examples for the next iteration (Adaptive Attack).
* **Multi-Turn Sandbox Generation**: The synthesizer acts interactively against a sandbox version of the detector, tweaking the article until it successfully bypasses detection, *then* submits the hardest examples to the main evaluation pipeline.
* **Continuous vs. Batch**: Transitioning from a weekly cron job to a continuous background process that tests edge cases on every major model or ontology update.

### **Proposed Architectural Improvements**
1. **Feedback-Driven Synthesis**: Update the `synthesize-adversarial-articles` step to ingest the results of the *previous* week's run. If Strategy B (Negation Framing) was successful, the agent should dynamically weight Strategy B higher this week.
2. **Iterative Refinement Loop**: Structure the workflow to allow a `StepMode` loop where the synthesizer can test its output against a mock-detector, refine it, and then output the final "hardened" adversarial batch.

---

### **Next Steps**
Please review these theoretical improvements. Once validated and approved, I will proceed to **STEP 2**: searching the LibreFang documentation (`firecrawl.dev.significa.sk`) for the exact `WorkflowStep` schema and constraint rules.