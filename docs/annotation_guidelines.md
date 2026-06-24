# Annotation Guidelines — Mediálny Dezolator

These guidelines are designed to ensure high inter-annotator agreement (Krippendorff's α ≥ 0.65) for human reviewers confirming or refuting disinformation verdicts.

> **Wave 3.5 — IMPROVE-2**: Guidelines expanded to include explicit Krippendorff alpha requirement explanation, enhanced Slovak defamation law handling, and multi-annotator workflow for borderline cases.
>
> Reference: Krippendorff, K. (2011). *Agreement on Agreement in Content Analysis*. Journal of Communication, 61(3), 486–493.

---

## Why These Guidelines Matter

When `feedback.krippendorff_alpha` drops below 0.65, the **Bayesian weight update loop is automatically paused** and a Telegram alert is sent. Consistent, principled annotation is therefore critical to the pipeline's self-improvement mechanism. Individual annotator bias accumulates — these guidelines are the safeguard.

---

## 1. Satire Identification

* **Definition**: Content that uses humor, irony, exaggeration, or ridicule to expose and criticize stupidity or vices, particularly in politics.
* **Slovak satire markers**: Portals like *Zomri* (zomri.sk), *Denník Satiry*, or articles explicitly labeled *„Satirický komentár"* / *„Paródia"*.
* **Reviewer Action**:
  * Check for satire markers (portal name, tone, satirical columns).
  * Satire should **never** be labeled as `DISINFORMATION` unless it is framed as a serious news story by a third-party amplifier to deceive the public.
  * Classify genuine satire as `CREDIBLE` with the note `"satire"`.
  * If the claim is from a satire portal but has been republished without satirical framing on a non-satire outlet, label as `UNCERTAIN` and flag for HITL review.
* **Common error**: Mislabeling hyperbolic political commentary as disinformation because it contains factual inaccuracies. Political hyperbole ≠ coordinated disinformation.

---

## 2. Opinion vs. Factual Claim

* **Definition**: Opinions are value judgments, predictions, or non-verifiable beliefs (e.g. *"Our foreign policy is a disaster"*). Factual claims assert statements about reality that can be checked (e.g. *"Slovakia sent fighter jets to Ukraine"*).
* **Reviewer Action**:
  * If a claim is purely opinion or a future prediction, it is **out of scope** for a disinformation verdict. Mark as `UNCERTAIN` or filter it out.
  * Only confirm verdicts for claims with clear factual assertions that can be proved true or false.
  * **Borderline case**: "Slovakia's government is corrupt." → Opinion. "The Slovak Prime Minister was convicted of corruption." → Factual (verifiable).
* **Common error**: Treating politically controversial but factually accurate reporting as disinformation because the framing is biased. Bias ≠ disinformation.

---

## 3. Partial Truths

* **Definition**: A statement that contains some element of truth but is mixed with false context, exaggeration, or omission of critical facts.
* **Reviewer Action**:
  * Determine the **primary narrative impact**.
  * If the false context alters the core message to mislead, label as `SUSPICIOUS` or `DISINFORMATION`.
  * If the inaccuracy is minor and non-deliberate, label as `UNCERTAIN` or `CREDIBLE` with a clarification note.
  * **Example**: "NATO has 1,000 troops in Slovakia" (true, per agreement) framed as "NATO occupies Slovak territory with 1,000 troops" (misleading framing). → Label: `SUSPICIOUS`, not `DISINFORMATION` (no outright falsehood).
* **Common error**: Treating any technically inaccurate statement as disinformation. Disinformation requires **deliberate intent to mislead**.

---

## 4. Slovak Legal Context & Defamation Law

Under Slovak law (Criminal Code, Act No. 300/2005 Coll., Section 373 — Defamation / *Ohováranie*) and Civil Code (protection of personality rights — *právo na ochranu osobnosti*):

* Publicly accusing a named individual or news organization of **deliberate lying** or **spreading hostile propaganda** can trigger defamation lawsuits if not backed by absolute factual proof.
* The system can result in legal liability for the operating organization if false `DISINFORMATION` verdicts are published.

**Reviewer Action for named individuals/outlets**:
1. For claims involving named politicians or journalists: require at least **two independent, reputable wire service corroborations** (e.g. TASR, SITA, Reuters SK) or official government/regulatory statements before confirming a `DISINFORMATION` verdict.
2. For claims involving named media outlets: require corroboration from at least **two external credibility registries** (NewsGuard, MBFC, EUvsDisinfo, or Konšpirátori.sk).
3. If evidence is conflicting, you **must** label the claim as `UNCERTAIN` or `SUSPICIOUS` to avoid legal liabilities.
4. Verdicts involving named individuals must be reviewed by **two independent annotators** regardless of P_fake score.

**Public vs. restricted verdicts**:
* Verdicts with P_fake in [0.65, 0.80] and named individuals/outlets: restricted to authenticated reviewer access only (not auto-published to Telegram).
* Only verdicts with P_fake ≥ 0.80 AND full evidence trail AND two annotator confirmations may be auto-published.

---

## 5. Information Laundering Context

If `laundering_risk_score > 0.60` is flagged in the review queue entry:
* The immediate source may be high-credibility (e.g. sme.sk) but the claim's narrative originated from a known-bad source within 72h.
* Do NOT base your verdict solely on the immediate source's credibility.
* Review the `claim_extractor.provenance_chain` field for the originating source.
* If provenance chain shows a known-bad source as origin: weight your verdict toward `SUSPICIOUS` or `DISINFORMATION` even if the immediate source is credible.
* Annotate with: `"Information laundering risk acknowledged"`.

---

## 6. Uncertainty Field Interpretation

Each review queue entry includes `u_ale` (aleatory) and `u_epi` (epistemic) uncertainty scores:

| Field | Value | Meaning | Annotator Action |
|---|---|---|---|
| `u_ale` | > 0.30 | Agents fundamentally disagree (ambiguous claim) | Extra caution; 2 annotators mandatory |
| `u_ale` | ≤ 0.30 | Good agent consensus | Standard review |
| `u_epi` | > 0.35 | Insufficient evidence found | Note evidence gaps; mark `UNCERTAIN` if unresolvable |
| `u_epi` | ≤ 0.35 | Sufficient evidence coverage | Standard review |

---

## 7. Multiple Annotator Workflow (IMPROVE-2)

* For **borderline claims** (P_fake ∈ [0.45, 0.75]), at least **two independent annotators** must record a verdict before the label is added to the Bayesian training loop.
* If annotators disagree (one says `DISINFORMATION`, other says `CREDIBLE`):
  1. The claim is flagged as `CONFLATED`.
  2. Sent to the chief editor for final arbitration.
  3. The arbitrated verdict is annotated with both original verdicts and the arbitration rationale.
* Annotators must not communicate before both have submitted their independent verdict.
* Annotation sessions should be conducted using separate logins to ensure independence tracking.

### Krippendorff's Alpha Requirement
* α ≥ 0.65: Acceptable annotation quality — Bayesian weight loop runs normally.
* α ∈ [0.50, 0.65): Warning zone — team lead must review annotation disagreements.
* α < 0.50: Critical — pipeline weight updates **automatically paused**; annotation session suspended pending calibration review.
* α is recomputed every 50 verdicts and logged to `output/annotation_quality.log`.

---

## 8. Annotation Scope Checklist

Before confirming any verdict, verify:

- [ ] The claim contains a verifiable factual assertion (not opinion/prediction)
- [ ] The claim is not satire or parody
- [ ] Source corroboration requirements are met (2+ for named individuals)
- [ ] Defamation law constraints are satisfied (see Section 4)
- [ ] Uncertainty fields have been reviewed (u_ale, u_epi)
- [ ] Laundering risk has been considered if flagged
- [ ] For P_fake in [0.45, 0.75]: a second independent annotator has been assigned
