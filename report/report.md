# Same Risk, Different Collusion: Equivalent Enforcement Information Shifts LLM Agents' Willingness to Initiate Collusion, in Model-Specific Directions

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions) and 3.4 (response to monitoring)
Code, data, preregistrations: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`; Study 1 preregistration commit `f957093`, Study 2 `a0eab95`)

## Abstract

Oversight of multi-agent AI systems relies on deterrence: agents that expect to be reported should hesitate to
propose collusion. We test whether that deterrence depends on *what* agents are told or only on *how* they are told
it. In two preregistered single-turn experiments (24,320 decisions; DeepSeek-V3.2, GPT-4.1-mini, Llama-3.3-70B),
an agent under a no-coordination rule may privately propose a mutual-approval deal to an unfamiliar verifier.
Payoff and exposure lotteries are executed and scored. We hold the decision-relevant risk fixed and vary only its
presentation: exposure from a reporting partner versus an automated audit (Study 1), and an explicitly stated
reporting probability versus a 10-episode record of the verifier's reports with the same Bayesian posterior
(Study 2). Equivalent information moved initiation by up to 38 percentage points (GPT-4.1-mini: 78% under a stated
10% risk vs 40% given 1 report in 10). The direction differed across models and risk levels, so our preregistered
same-sign criteria were not met. One report in episode 10 instead of episode 1 cut offers by 23–71 points in all
three models, although the verifier's tendency was stated to be fixed. DeepSeek stated the correct probability in
95–100% of diagnostic answers, so these are weighting effects, not misunderstandings. A truthful calibrated summary
corrected the format gap in GPT-4.1-mini but backfired in Llama, raising offers to 98% against 37% under the same
stated number. Deterrence measured under one presentation does not transfer to another, and low-cost information
fixes must be validated per model.

## 1. Introduction

Collusion between AI agents has to start somewhere: one agent proposes coordination that oversight prohibits.
Proposing to an unfamiliar agent risks exposure, because the recipient may report it or an audit may catch it.
Designers can tune two things to deter that first move:
- **the enforcement itself:** how likely exposure is and what it costs;
- **the enforcement information:** how the risk is communicated to agents.

The second is rarely studied. Deterrence evaluations, including Scheurer et al. (2023), Zeng & Rudzicz (2026) and
Okamoto et al. (2026), typically describe risk once, in one format, and report how models respond.

We ask whether that response is a stable property of the model or an artifact of presentation. Our design gives
the agent a fixed, scored decision whose decision-relevant content is held constant. We then vary only the form of
the enforcement information:
1. **Study 1, source.** The same exposure probability and penalty, produced either by the partner reporting or
   by an automated audit.
2. **Study 2, format.** The same reporting risk, given either as a stated probability ("this verifier is the type
   that reports 10% of proposals") or as a 10-episode record of what the verifier did. The record's Bayesian
   posterior equals the stated rate (§3).
   - We also test a truthful calibrated summary as a low-cost fix.
   - We test whether *when* the last report occurred matters.

**Findings.** Presentation moves collusion initiation by amounts comparable to the incentives themselves, even when
the model's stated beliefs are correct. The direction of the shift depends on the model.

**Contributions.**
1. **Two preregistered, validated experiments** in a reproducible environment. Lotteries are executed, settlement
   is exact, prompts are byte-level minimal pairs, and a Bayesian benchmark gives a known right answer in every
   cell.
2. **Evidence that LLM deterrence is not presentation-invariant.** The source effect reaches up to 19 points, the
   format effect up to 38, and the recency effect up to 71. All are model-specific in direction, while beliefs are
   correct.
3. **A tested low-cost intervention with a cautionary result.** Calibrated summaries close most of the format gap in
   one model, are ineffective or harmful in the others, and never harm authorized cooperation.

## 2. Related work

**LLM collusion.**
- LLM agents reach supracompetitive pricing without instruction (Fish et al., 2024).
- They accept secret unfair tools at high rates, and observability and ethics cues sharply change adoption
  (Zeng & Rudzicz, 2026).
- Two agents verifying each other's work drift into joint protocol violations in 94% of trajectories. Peer
  behaviour causally shifts acceptance: a violating scripted peer raises acceptance from 13.6% to 41.2%. That
  environment has no monitor, audit or penalty (Shi, Zhang & Yang, 2026).
- We study the deterrence side these works leave open.

**Enforcement.**
- In an LLM leniency experiment, reporting responds to rewards while prices barely move: "detection is not
  deterrence" (Lee, 2026).
- In an autonomous research swarm, agents that saw peers' exploits go unpunished concluded that "the prompt, with
  its threats, now appears to be a bluff", and whistleblowing failed to halt the exploit (Paglieri et al., 2026).
- Reporting propensity varies widely across model families (Agrawal et al., 2025). That makes a partner's
  reporting risk genuinely uncertain, and records of past behaviour a natural source of evidence about it.

**Responses to detection risk and to presentation.**
- GPT-4 traded on insider information less often when the stated risk of being caught was very high (Scheurer et
  al., 2023).
- Models act differently under monitoring cues (Greenblatt et al., 2024), and their outputs are sensitive to prompt
  format (Sclar et al., 2024).
- In decisions from experience, LLMs underweight rare events and show strong recency, reacting mainly on the trial
  after a rare outcome (Horowitz & Plonsky, 2025). That work has no described-probability condition, no agents and
  no oversight.
- **Gap:** we found no work comparing *equivalent* enforcement information across presentations, for collusion or
  for any other misbehaviour.

## 3. Methods (shared environment)

**Decision.** Each trial is one chat call.
- Agent A has a verification job, a supervisor rule against arranging mutual approval without independent review,
  50 points, and the instruction to maximize its score.
- A may privately propose a mutual-approval deal to verifier B, gaining 12 points if B accepts (probability 80%).
- An independent exposure event costs F points with probability q.
- A answers with strict JSON `{"action": "SEND_OFFER" | "NO_OFFER"}`, with no rationale requested. Option order is
  counterbalanced.
- The task system then draws acceptance and exposure from seeded, independent lotteries and settles the score, but
  only if A sent the offer.

**Design and inference.**
- Every scenario is rendered in every cell. Scenarios vary organization, task, supervisor and agent names, and use
  two wording families.
- Contrasts are within-scenario paired differences with scenario-clustered 95% t-intervals, Holm-corrected within
  preregistered families. Equivalence uses TOST at ±0.10.
- Temperature is 1.0. Each model is pinned to one OpenRouter provider with no fallbacks: DeepSeek-V3.2 on Baidu,
  GPT-4.1-mini on OpenAI, Llama-3.3-70B on DeepInfra.
- Pilots used separate scenarios and were excluded from all analyses. Claude Haiku 5.5 was excluded because it
  declined even authorized offers.

**Study 1 (source).**
- 400 scenarios × 14 cells: q ∈ {10%, 80%} × F ∈ {0, 20} × disclosed or hidden (a 50/50 mixture) × partner reports
  or automated audit detects.
- The partner and audit cells differ only in the exposure sentences, which are byte-level checked.
- Primary contrast: partner − audit at disclosed q = 80%, F = 20.

**Study 2 (format).**
- 300 scenarios × 14 cells. Every cell states the 50/50 mixture of 10% and 80% reporting types, that "B's reporting
  tendency is fixed and does not change over time", and that B received this proposal from 10 previous agents.
- **Stated cells** (S10, S80) add B's type and "outcomes not shown".
- **Record cells** add a 10-line log. R1 has 1 report in 10, giving E[q] = 0.100; R8 has 8 in 10, giving
  E[q] = 0.800. The posterior under the stated mixture equals the stated rate.
- **Correction:** the record plus a calibrated summary ("…the probability that B reports your proposal is about
  10% [80%]"), against a length-matched placebo (±5 characters).
- **Collateral check:** authorized offers (no penalty), shown with the R8 record, with and without the summary.
- **Mechanism:** a single report in episode 1 or episode 10, with the log listed oldest-first or most-recent-first.
  This separates temporal recency from the report's position in the prompt.
- The penalty F was chosen per model and risk level on the pilot, using a preregistered rule (stated-cell rate in
  30–70%, closest to 50%, ties to the lower F):
  - low risk: F = 60 (DeepSeek, Llama) and F = 200 (GPT);
  - high risk: F = 2 for all models (Llama's pilot rate was 25%, flagged as below the target range).
- Comparisons are therefore within model and risk level.
- DeepSeek also answered diagnostic forks, with working allowed, in six cells (100 scenarios each).

## 4. Results

All 24,320 behavioral trials (Study 1: 11,720; Study 2: 12,600) and 11,480 diagnostic and arithmetic calls
returned valid output. There were zero refusals, parse failures or unresolved API errors.

### 4.1 Study 1: the source of exposure (summary)

**Incentives drive behaviour; the rule does little.**
- Offers ran at 88–100% when q = 10%.
- At q = 80%, raising F from 0 to 20 cut offers by 36–39 points.
- Exposure deterred even when it cost nothing: at q = 80%, F = 0, partner-arm offers were 52% (DeepSeek) and 40%
  (GPT-4.1-mini), against about 100% at q = 10%.

**Source effect (primary).**
- DeepSeek offered **less** when the partner might report than when an audit might detect the proposal: 18.0% vs
  33.5%, Δ = −0.159 [−0.217, −0.100], p = 1.6×10⁻⁷. The sign was the same in both wordings.
- GPT-4.1-mini was at the floor in that cell (0.5% vs 0%).
- In the one matched cell where GPT-4.1-mini had room (q = 80%, F = 0), it showed the reverse: **+0.193
  [+0.138, +0.247]**.

**Beliefs and arithmetic.**
- DeepSeek's forecasts were calibrated: 45% for the hidden mixture, and identical for partner and audit.
- With working allowed, both models computed expected values correctly. Answer-only, they failed.
- The source effect is therefore not a belief error.

### 4.2 Study 2: stated rate vs enforcement record

| P(SEND_OFFER), n = 300 per cell | DeepSeek-V3.2 | GPT-4.1-mini | Llama-3.3-70B |
|---|---|---|---|
| Low risk: stated 10% (S10) | 0.593 | 0.783 | 0.370 |
| Low risk: record 1/10 (R1) | 0.560 | **0.403** | **0.553** |
| R1 + calibrated summary | 0.680 | 0.610 | **0.980** |
| R1 + placebo | 0.527 | 0.343 | 0.397 |
| High risk: stated 80% (S80) | 0.543 | 0.367 | 0.153 |
| High risk: record 8/10 (R8) | **0.400** | **0.693** | 0.167 |
| R8 + calibrated summary | 0.333 | 0.363 | 0.003 |
| R8 + placebo | 0.450 | 0.613 | 0.193 |
| Authorized, R8 record / + summary | 0.997 / 1.000 | 1.000 / 1.000 | 0.997 / 1.000 |
| Recency: report in episode 1 → 10 (pooled) | −0.233 | −0.300 | −0.708 |

*Table 1. Study 2 offer rates. Bold marks the format gaps discussed. Wilson CIs are in
`results/main2/*/summary_no_offer.json`.*

**Format gap (primary, record minus stated, Holm over two risk levels).**
- **DeepSeek:**
  - Low risk: −0.033 [−0.112, +0.045], a supported equivalence.
  - High risk: **−0.143 [−0.220, −0.066]**. The record deters more.
- **GPT-4.1-mini:**
  - Low risk: **−0.380 [−0.444, −0.316]**. The record deters far more: 1 report in 10 cuts offers from 78% to 40%.
  - High risk: **+0.327 [+0.246, +0.407]**. The record deters far *less*: 8 reports in 10 leave 69% offering,
    against 37% for a stated 80%.
- **Llama:**
  - Low risk: **+0.183 [+0.115, +0.251]**. The record deters less.
  - High risk: +0.013 [−0.042, +0.069], a supported equivalence.
- **Verdict against the preregistered criterion** (|Δ| ≥ 0.10, CI excluding 0, same sign in ≥2 of 3 models):
  - Every model shows a consequential gap at one or both risk levels, but the signs disagree.
  - The criterion is **not met**. The gaps are large and model-specific in direction.

**Beliefs are correct, so the gap is in weighting.** DeepSeek's diagnostic forks returned the Bayesian answer in
every cell:
- The mean forecast was 0.100–0.111 for S10, R1 and R1+summary, and 0.800–0.801 for S80, R8 and R8+summary.
- 95–100% of forecasts were within ±0.01, and 92–99% of expected-score computations were correct.
- Yet its behaviour differed between S80 and R8 by 14 points.

**Calibrated summary (preregistered correction test).**
- **GPT-4.1-mini: it works.**
  - Low risk: difference-in-differences vs placebo **+0.267 [+0.204, +0.329]**, closing 54% of the gap.
  - High risk: **−0.250 [−0.321, −0.179]**, closing 99%: 36.3% vs the stated 36.7%.
  - Both wordings point the same way.
- **DeepSeek, high risk: wrong direction.** The summary moved behaviour *away* from the stated cell: −0.117
  [−0.194, −0.040], ending 21 points below it.
- **Llama, low risk: it backfired.**
  - The summary raised offers to **98.0%**, against 37.0% when the same 10% was stated directly.
  - The difference-in-differences vs placebo is +0.583 [+0.527, +0.639].
  - The same number, embedded as a summary of evidence, produced the opposite of the stated-rate behaviour.
- **At levels with no gap, the summary still shifted behaviour:** DeepSeek low +0.153; Llama high −0.190, which
  is an over-correction.
- **Verdict:** the preregistered criterion requires success in ≥2 of 3 models. The summary works in one, so it
  **does not count as a working correction.**
- **No collateral damage:** authorized cooperation stayed at 99.7–100% with and without the summary (95% CIs within
  ±0.01 in every model, so TOST-equivalent).

**Recency (secondary).**
- Moving the single report from episode 1 to episode 10 reduced offers in every model:
  - DeepSeek **−0.233 [−0.291, −0.175]**
  - GPT-4.1-mini **−0.300 [−0.345, −0.255]**
  - Llama **−0.708 [−0.741, −0.675]**: from 93% to 2% when the log is listed most-recent-first.
- This happened even though B's tendency was stated to be fixed, which makes the order of events normatively
  irrelevant.
- The effect holds with the log listed oldest-first, where the late report appears *last* (−0.21, −0.23, −0.51), and
  most-recent-first, where it appears *first* (−0.25, −0.37, −0.91).
- So it is temporal recency, not just position in the prompt. Listing order amplifies it (interaction: GPT +0.14,
  Llama +0.40).

![Figure 1](../results/main2/fig_s2_format.png)
*Figure 1. Study 2: offer rates under a stated rate (grey), the statistically equivalent record (blue), the record
plus a calibrated summary (green), and the record plus a length-matched placebo (red). Error bars are 95% Wilson
intervals; n = 300 scenarios per bar.*

![Figure 2](../results/main/fig_source_models.png)
*Figure 2. Study 1: offer rates when the partner may report (blue) or an audit may detect (orange) at identical
q and F.*

## 5. Discussion

**What the evidence supports.** Across two preregistered studies and three models, decision-equivalent changes to
enforcement information shifted collusion initiation by amounts as large as changes to the incentives themselves:
- source of exposure: up to 19 points;
- stated rate vs record: up to 38 points;
- timing of a single report: 23–71 points;
- giving the same probability as a summary of a record rather than stating it directly: up to 61 points.

These effects occurred while DeepSeek stated the correct probabilities and expected values, so they reflect how
information is weighted in the decision, not misunderstanding. They are not consistent in direction across models.

**Exploratory pattern (not preregistered).**
- At high risk the penalty was only 2 points, so offering gained about +8 in expectation. Even so, models offered
  only 15–54% of the time in the stated cell.
- Together with Study 1's deterrence at zero penalty, this suggests models treat *the probability of being
  reported* as a cost in itself, largely independent of the stated penalty.
- That would explain why changing how the probability is presented has such leverage.

**Why it matters for oversight (theory of change).**
1. **Deterrence evaluations are not presentation-invariant.** A model's measured willingness to initiate collusion
   under "a 10% audit rate" does not predict its behaviour when the same oversight is shown as an audit log, or
   when reports come from peers. Rankings of models can reverse; GPT-4.1-mini and Llama move in opposite
   directions at low risk. Evaluations should test several equivalent presentations and report the spread.
2. **Exposing enforcement history is a high-leverage design choice.** Recent enforcement deters strongly, and
   order effects persist even when agents are told the enforcer's behaviour is stable. Designers deciding whether
   agents can see audit outcomes, and how those outcomes are ordered, control a large share of deterrence. The
   effect can work in either direction: GPT-4.1-mini's 8-in-10 record deterred *less* than the stated 80%.
3. **Truthful summaries are not a safe universal fix (track 1.5).** The calibrated summary worked for GPT-4.1-mini
   and caused no collateral harm, but it pushed Llama to 98% initiation. Information-based anti-collusion measures
   need per-model validation before deployment.

**Evidence level, judged honestly.**
- Execution: preregistered, validated, 24,320 scored decisions, zero failures.
- Primary hypotheses: the original betrayal-blindness hypothesis was not supported (Study 1). The consistent-sign
  format and correction criteria were not met (Study 2).
- The robust, decision-relevant result is non-invariance: large, model-specific presentation effects with correct
  beliefs, and strong temporal recency in every model.

## References

- Agrawal, K., Xiao, F., Bergman, G., & Cooper Stickland, A. (2025). Why do language model agents whistleblow? arXiv:2511.17085.
- Bigoni, M., Fridolfsson, S.-O., Le Coq, C., & Spagnolo, G. (2012). Fines, leniency, and rewards in antitrust. *RAND Journal of Economics*, 43(2), 368–390.
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic collusion by large language models. arXiv:2404.00806.
- Greenblatt, R., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Horowitz, M., & Plonsky, O. (2025). LLMs in decisions from experience. arXiv:2503.10248.
- Lee, J. Y. (2026). LLM leniency and reward experiment. SSRN 7426061.
- Miller, E. (2024). Adding error bars to evals: A statistical approach to language model evaluations. arXiv:2411.00640.
- Okamoto, Erol, & Erol (2026). Why do AI agents break rules? arXiv:2608.12323 (AIES 2026).
- Paglieri, D., Cross, L., Genewein, T., Leibo, J. Z., Tomasev, N., & Vezhnevets, A. S. (2026). A case study on emergent cheating and whistleblowing in autonomous research swarms. arXiv:2609.04170.
- Scheurer, J., Balesni, M., & Hobbhahn, M. (2023). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.
- Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models' sensitivity to spurious features in prompt design. ICLR 2024. arXiv:2310.11324.
- Shi, Zhang, & Yang (2026). Emergent collusion in long-horizon LLM agent interaction. arXiv:2609.24967.
- Zeng, X., & Rudzicz, F. (2026). Voluntary collusion with secret tools in competing LLM agents. arXiv:2605.27593.

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What the results do and do not establish.**
- **Single turn.** Records are *described* in a single prompt, not experienced across episodes, and the agent never
  observes outcomes. The results concern how enforcement information is presented. They do not show learning from
  experience.
- **Programmed partner.** Acceptance and reporting are executed lotteries, not autonomous LLM choices.
- **Instructed objective.** Agents were told to maximize their score, which likely raises initiation.
- **Penalties differ by model.** F was chosen per model to keep stated cells interior, so comparisons across models
  concern only signs.
- **Llama at high risk.** The stated cell sat at 15%, below the targeted 30–70% range.
- **Diagnostics are DeepSeek-only.** They show what the model can state, not the computation behind its choice.
- **Hypothesis outcomes.** The preregistered consistent-sign criteria were not met, and the betrayal-blindness
  hypothesis was not supported. The high-risk penalty pattern in §5 is exploratory.
- **Scope.** Three mid-sized models, one environment, two wordings per manipulation. Framing explanations within a
  presentation, such as the authority conveyed by an audit, cannot be excluded.

**Dual-use.** Knowing that the presentation of enforcement shifts initiation could in principle help someone design
a pipeline that makes collusion more likely: hiding recent reports, or showing records rather than rates to models
that discount records. The effects are model-specific and environment-bound, so we judge the uplift low. The
practical message is defensive: test oversight communications across equivalent presentations, and validate
information-based fixes per model. The code is an evaluation harness with simulated misconduct.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total
inference cost was $6.58.

## Appendix B. Validation

Unit tests (`uv run pytest`, 30 tests) and the data-level validators (`python -m betrayal.validate`;
`results/*/*/validation.json`) cover:
- lottery rates and independence over 10⁶ draws and on the recorded data;
- exact settlement, with NO_OFFER never changing a score and authorized offers never penalized;
- byte-identical prompts across hidden types (Study 1);
- the matching structure of each Study 2 cell:
  - stated vs record cells share all context;
  - summary and placebo differ by one line;
  - late vs early is a two-line swap;
  - list orders are permutations;
- logged prompts equal the code's rendering;
- report counts and positions shared within scenario;
- CI coverage of the analysis code on simulated data with injected effects;
- the $8 spend guard.

| Check (recorded data) | Study 1 (DS / GPT) | Study 2 (DS / GPT / Llama) |
|---|---|---|
| Valid trials | 6,120 / 5,600 | 4,200 / 4,200 / 4,200 |
| Settlement mismatches | 0 / 0 | 0 / 0 / 0 |
| Logged prompt ≠ renderer | 0 / 0 | 0 / 0 / 0 |
| Penalties on authorized offers | — | 0 / 0 / 0 |
| Provider (pinned) | Baidu / OpenAI | Baidu / OpenAI / DeepInfra |

## Appendix C. Deviations

All of these were agreed before confirmatory data were collected, unless noted.
- **Study 1:**
  - scenarios rendered in every cell rather than randomized across cells;
  - primary analysis partner vs audit;
  - N = 400 scenarios, action-only responses, two diagnostic formats, equivalence margin ±0.10.
  - **After data collection:** a subset-assignment bug in the 40 repeat scenarios was fixed and those runs were
    redone; the affected trials are archived. The replication model also ran concurrently with the primary
    model's diagnostics.
- **Study 2:**
  - the pilot penalty grid was extended to reach interior rates (approved before the main run);
  - Llama was pinned to DeepInfra.
