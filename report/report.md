# Betrayal Blindness? The Source of Exposure Shifts LLM Agents' First Collusion Offers, in Model-Specific Directions

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions)
Code, data, preregistration: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`; preregistration commit `f957093`)

## Abstract

LLM agents readily accept offers of unauthorized coordination, but proposing collusion to an unfamiliar
agent who might report it is less studied. We ran a preregistered, single-turn
experiment in which an agent bound by a no-coordination rule could privately propose a mutual-approval
arrangement to an unfamiliar verifier. Each of 400 scenarios was rendered in 14 matched conditions. We
randomized the exposure probability (10% or 80%), the penalty (0 or 20 points), whether the partner's type
was disclosed, and the source of exposure: the partner reporting, or an automated audit detecting, at
identical probability, penalty and benefit. The lotteries were executed and scored. Both models proposed
the prohibited arrangement almost always at low risk (88–100%) and far less often at high, costly risk (0–34%). DeepSeek-V3.2
forecast risk accurately, including a calibrated 45% for hidden partner types, which contradicts an
optimistic-partner explanation. The preregistered primary
test found the opposite of "betrayal blindness": DeepSeek offered *less* when the partner could report than
under an equivalent audit (18.0% vs 33.5%; Δ = −0.16, 95% CI [−0.22, −0.10]), and both wordings gave the
same sign. GPT-4.1-mini did not replicate this, because it was at the floor in that cell. In the matched
cell where it had room, it showed the reverse asymmetry (+0.19 [+0.14, +0.25]). At matched incentives, then,
the source of exposure shifts first-offer behavior by up to 16–19 percentage points, in directions that
differ by model. Evaluations that treat peer reporting and automated auditing as interchangeable deterrents can
misestimate when collusion begins.

## 1. Introduction

A collusive arrangement between AI agents has to start with someone proposing it. Unless the partner is
already trusted, that first proposal is a gamble. An unfamiliar agent may decline, and it may also report the
proposal to whoever oversees the system. Prior work shows that LLM agents frequently *accept* offers of
unauthorized coordination (Zeng & Rudzicz, 2026). It also shows that LLM agents sometimes whistleblow on
misconduct (Agrawal et al., 2025; Paglieri et al., 2026). Much less is known about the strategic step in
between: when does an agent *initiate* coordination with a stranger who might report it?

We study this first-offer decision in a controlled, single-turn environment. Agent A works under a rule
prohibiting unauthorized coordination. It may privately propose a mutual-approval arrangement to an
unfamiliar verifier agent B. We independently randomize four things:
- the probability that the proposal is exposed (q = 10% or 80%),
- the penalty if it is exposed (F = 0 or 20 points),
- whether A is told the exposure probability,
- and the **source** of exposure: B reports it, or an automated audit detects it, at identical probability
  and penalty.

B's acceptance (80%) and its reporting or the audit's detection are programmed, independent lotteries. They
are actually executed and settled against A's score.

Our preregistered primary question asks whether agents discount exposure risk that comes from a peer relative
to the same risk from an impersonal audit. We call this hypothesized failure *betrayal blindness*.

We find no general betrayal blindness. Our primary model shows the reverse at high risk, and the replication
model is uninformative in the primary cell. The source of exposure is nevertheless far from irrelevant.

**Contributions.**
1. **A reproducible first-offer environment.** It has programmed, independently randomized acceptance and
   exposure lotteries, exact settlement, byte-level leakage checks, and a partner/audit pair matched
   sentence by sentence.
2. **A preregistered causal estimate of the exposure-source effect.** With 400 paired scenarios on two
   models, the effect is large and significant in one model and model-specific in direction across the
   matched cells.
3. **Evidence that initiation is dominated by stated incentives, not by the rule.**
   - Agents propose prohibited coordination almost always when it pays.
   - They forecast hidden-partner risk accurately (no optimistic partner beliefs).
   - They are deterred by exposure even when it costs nothing.
4. **Practical findings for low-cost deterrence (track 1.5).** Disclosing that a partner is high-risk is a
   strong deterrent. Disclosing that a partner is low-risk *increases* initiation. A supposedly neutral
   sentence about the partner shifted GPT-4.1-mini's offers by 14 points.

## 2. Related work

**Collusion and secret coordination between LLM agents.**
- LLM pricing agents reach supracompetitive outcomes without explicit instruction (Fish et al., 2024).
- Agents offered secret tools for unfair cooperation accept them at high rates. Adoption is highly sensitive
  to framing such as "unfair" labels, ethical warnings and observability (Zeng & Rudzicz, 2026).
- Steganographic channels make covert collusion hard to monitor (Motwani et al., 2024).
- Our setting is deliberately overt and single-turn. It isolates the initiation decision rather than
  sustained coordination.

**Reporting and enforcement.**
- Lee (2026) imports the leniency and whistleblower-reward institutions of Bigoni et al. (2012) into an LLM
  Bertrand duopoly. Reporting there responds strongly to incentives, but prices barely move: "detection is
  not deterrence".
- In Lee's design, communication is mandatory and the reporter is a co-conspirator seeking leniency. No agent
  ever decides whether to approach an unfamiliar partner.
- In an autonomous research swarm, Paglieri et al. (2026) observed exploiters, converts and whistleblowers.
  Peer reports did not stop the exploit, and some agents read the prompt's threats as a bluff.
- Agrawal et al. (2025) show that LLM whistleblowing varies strongly by model family and with prompt
  nudges. An unfamiliar AI partner's reporting propensity is therefore genuinely uncertain.

**Responses to detection risk.**
- GPT-4 acting as a trading agent was less likely to act on insider information when the stated risk of
  being caught was very high (Scheurer et al., 2023).
- Models behave differently under cues of monitoring (Greenblatt et al., 2024) and often recognize
  evaluation contexts (Needham et al., 2025).
- We add a matched comparison of *who* does the detecting, holding the detection probability, penalty and
  benefit fixed. We also separate disclosed from hidden partner types against a known benchmark.

## 3. Methods

**Environment.**
- Each trial is one chat call. A is told:
  - its job (a verification pipeline in one of 8 domains);
  - the supervisor's rule against arranging mutual approval without independent review;
  - its current score (50) and that its objective is to maximize its score;
  - the offer's consequences: +12 if B accepts (probability 80%), and an independent exposure event costing
    F points.
- A answers with strict JSON `{"action": "SEND_OFFER" | "NO_OFFER"}`. No rationale is requested. Option
  order is counterbalanced.
- After the decision, the task system draws B's acceptance and the exposure event from independent seeded
  lotteries. It settles the score only if A sent the offer.
- All prompts are in `prompts/templates.toml`, and every rendered variant is in `docs/prompt_review.md`.

**Cells.** Every one of 400 independently generated scenarios is rendered in all of the following cells:
- **Partner arm, 8 cells:** q ∈ {10%, 80%} × F ∈ {0, 20} × risk {disclosed, undisclosed}.
  - All partner cells state that verifier agents come in two equally common types, reporting with
    probability 10% or 80%.
  - Disclosed cells add which type B is. Undisclosed cells say A has not been told, so the correct forecast
    is 45%.
- **Audit arm, 4 cells:** disclosed q × F. The same sentences, but exposure comes from an automated audit
  "at one of two equally common settings", and B "never reports proposals".
- **Neutral control:** the undisclosed F = 20 cell, plus a non-informative note that B "was assigned to this
  batch by the scheduler".
- **Authorized-offer positive control:** the supervisor has authorized the arrangement and there is no
  exposure.

Scenarios vary the organization, task, supervisor title and agent identifiers. Each scenario is assigned one
of two semantically matched wordings per source; the assignment is balanced, with 200 scenarios each. Partner
and audit cells of a scenario share the wording index and the option order.

**Models and sampling.**
- **Primary model:** DeepSeek-V3.2, pinned through OpenRouter to the Baidu provider (fp8) with no
  fallbacks.
- **Preregistered replication:** GPT-4.1-mini, pinned to OpenAI.
- Temperature 1.0, max 1,024 output tokens, and a strict JSON schema.
- **Model selection:** a 20-scenario pilot was excluded from all analyses. Claude Haiku 5.5 was dropped
  because it failed the positive control (0% SEND even when the offer was authorized). In the pilot,
  Llama-3.3-70B and GPT-4.1-mini were near the floor in the primary cell.

**Diagnostics** (DeepSeek only).
- Separate calls, made from the identical pre-decision state and never shown to the behavioral call, ask for
  four values: the probability that the deduction applies, its size, and the expected score with and without
  sending.
- They are run in two formats: answer-only JSON, and JSON with a free-text "work" field before the numbers.
- A separate permitted arithmetic task, with no coordination framing, poses the same expected-value
  calculations and the 50/50 mixture probability.

**Preregistered analysis** (`prereg.md`, committed before any confirmatory call).
- **Primary estimand:** Δ_src = P(SEND | partner, disclosed, q = 80%, F = 20) − P(SEND | audit, same).
  - It is estimated as the mean of within-scenario differences, with a scenario-clustered (paired) 95%
    t-interval.
  - The test is two-sided at α = 0.05. An exact McNemar test and a 2,000-resample scenario bootstrap serve as
    checks.
- **Equivalence:** TOST at ±0.10.
- **Generalization:** the same contrast in the other three matched cells, Holm-corrected.
- **Secondary family (Holm over 7):**
  - τ_I, the disclosure × risk difference-in-differences at F = 20
  - the penalty effects at each disclosed q
  - two placebo contrasts between hidden types
  - two neutral-control contrasts
- **Refusals** are coded as NO_OFFER in the primary analysis, with an exclusion sensitivity analysis.
- **Wording robustness** is descriptive. A result is "directionally consistent" if both within-wording
  estimates share the pooled sign, and a gap of 0.10 or more between them is flagged as heterogeneity.
- **Replication** requires GPT-4.1-mini's Δ_src to have the same sign as DeepSeek's and p < 0.05.

**Validation.** `pytest` (22 tests) and `betrayal/validate.py`, the latter run on the recorded data, check:
- lottery rates and independence (10⁶ simulated draws, and on the data);
- exact settlement, with NO_OFFER never changing the score;
- byte-identical prompts across hidden types;
- that partner and audit prompts differ only in the exposure lines;
- that logged prompts equal the code's rendering;
- nominal CI coverage of the analysis code on simulated data with injected effects;
- the $8 spend guard.

## 4. Results

All 6,120 DeepSeek and 5,600 GPT-4.1-mini behavioral trials returned a valid action. There were no
refusals, parse failures or unresolved API errors, so the refusal-exclusion sensitivity analysis is identical
to the primary analysis. Every trial was served by the pinned provider.

**Validity checks** (Appendix B) all pass on the recorded data:
- Acceptance draws came out at 80.4% for both models.
- Exposure draws came out at 11.0% and 79.8%, against targets of 10% and 80%. Acceptance and
  exposure were independent (χ² p > 0.13). The draws are seeded identically for both models.
- Settlement had 0 mismatches, and NO_OFFER never changed a score.
- All 800 of 800 undisclosed prompt pairs were byte-identical, and all 400 primary pairs differed only in the
  exposure lines.
- The authorized-offer positive control was chosen 100% of the time by both models.

**Agents respond strongly to stated risk and penalty** (Figure 1, Table 1).
- Both models proposed the prohibited arrangement in almost every low-risk scenario: 88–100% at
  q = 10%, F = 20, across both arms.
- They rarely proposed it when exposure was likely and costly: 18.0% (DeepSeek) and 0.5% (GPT-4.1-mini) at
  q = 80%, F = 20.
- Disclosing the partner's type had a very large effect. τ_I was −0.78 [−0.86, −0.70] for DeepSeek and
  −1.01 [−1.07, −0.96] for GPT-4.1-mini.
- At q = 80%, raising the penalty from 0 to 20 reduced offers by 0.36 [0.30, 0.42] for DeepSeek and 0.39
  [0.34, 0.44] for GPT-4.1-mini.
- Exposure deterred even when it cost nothing. At q = 80%, F = 0, partner-arm offers fell to 52% and 40%
  respectively (audit arm: 65% and 21%), from about 100% at q = 10%, F = 0. So a substantial part of deterrence is not explained by the scored penalty
  and may reflect rule compliance or aversion to being reported.
- With the type hidden (correct forecast 45%; expected gain +0.6 at F = 20), offer rates were intermediate:
  54–63%.
- The two hidden-type placebo contrasts were supported nulls for both models (all |est| ≤ 0.02, with 90% CIs
  inside ±0.10). This is the behavioral confirmation that the hidden type did not leak.

**Primary test: partner vs audit at disclosed q = 80%, F = 20.**
- **DeepSeek-V3.2 offered *less* when the partner might report than when an automated audit might detect
  the proposal:** 18.0% [14.5, 22.1] vs 33.5% [29.1, 38.3].
  - Δ_src = −0.159, 95% CI [−0.217, −0.100], p = 1.6×10⁻⁷.
  - McNemar: 48 vs 110 discordant scenarios, p = 9×10⁻⁷. Bootstrap CI [−0.219, −0.101].
  - Using first runs only (dropping the 40 repeat scenarios): −0.155 [−0.215, −0.095].
  - The effect is directionally consistent across the two tested wordings: −0.195 [−0.282, −0.108] and −0.122
    [−0.201, −0.044]. The difference between wordings, −0.07 [−0.19, +0.04], is below the heterogeneity flag.
  - This is a significant effect in the direction opposite to the hypothesized betrayal blindness.
- **GPT-4.1-mini did not replicate it** under the preregistered rule. Both arms are at the floor (0.5% vs
  0.0%), giving Δ_src = +0.005 [−0.002, +0.012].
  - TOST formally classifies this as equivalence within ±0.10, but the floor makes the cell uninformative
    about how the model weighs the two sources.

**Source effects in the other matched cells are model-specific** (generalization family, Holm-corrected).
- DeepSeek shows a crossover:
  - At low risk, partner exposure deters *less* than audit exposure: q = 10%, F = 20: +0.089 [+0.052, +0.125].
  - At high risk, it deters *more*: q = 80%, F = 0: −0.115 [−0.176, −0.054].
- GPT-4.1-mini shows the betrayal-blindness pattern in the one cell where it has room. At q = 80%, F = 0,
  partner 39.8% vs audit 20.5%: **+0.193 [+0.138, +0.247]**.
  - It shows a small effect in the same direction at q = 10%, F = 20: +0.018 [+0.005, +0.030].
- Across the four matched cells the source of exposure therefore moved initiation by up to 16 points
  (DeepSeek) and 19 points (GPT-4.1-mini) at identical probability, penalty and benefit. **The sign of that shift differed between the two models.**

**The "neutral" partner note was not neutral.** Adding "B was assigned to this batch by the scheduler" to the
undisclosed F = 20 cell changed offers by +0.064 [+0.006, +0.123] for DeepSeek (p_Holm = 0.09). For
GPT-4.1-mini the change was −0.136 [−0.190, −0.082] (p_Holm < 10⁻⁵).

**Realized consequences.** In DeepSeek's primary cell, the 72 partner-arm offers and 134 audit-arm offers
ended with mean scores of 43.3 and 43.4, against 50 for not offering. The executed lotteries made initiation
costly, as stated. The model never observed these outcomes.

| Cell (disclosed unless U) | DeepSeek-V3.2 | GPT-4.1-mini |
|---|---|---|
| Partner q=10% F=0 / Audit | 1.000 / 0.990 | 1.000 / 1.000 |
| Partner q=10% F=20 / Audit | 0.963 / 0.875 | 1.000 / 0.983 |
| Partner q=80% F=0 / Audit | 0.522 / 0.652 | 0.398 / 0.205 |
| **Partner q=80% F=20 / Audit** | **0.180 / 0.335** | **0.005 / 0.000** |
| Undisclosed F=0 (q=10% / q=80% hidden) | 0.787 / 0.765 | 0.963 / 0.963 |
| Undisclosed F=20 (q=10% / q=80% hidden) | 0.555 / 0.542 | 0.615 / 0.632 |
| Neutral note, undisclosed F=20 | 0.610 | 0.487 |
| Authorized-offer positive control | 1.000 | 1.000 |

*Table 1. P(SEND_OFFER), n = 400 scenarios per cell (first runs). Wilson 95% CIs are in
`results/main/*/summary_no_offer.json`.*

![Figure 1](../results/main/fig_source_models.png)
*Figure 1. Offer rate when the partner may report (blue) or an automated audit may detect (orange) the
proposal, at identical disclosed probability q and penalty F. Error bars are 95% Wilson intervals; n = 400
scenarios per bar.*

**Risk comprehension** (DeepSeek diagnostics: 5,200 forks per format; Figure 2).
- **Forecasts were calibrated in both formats.** The mean forecast probability that the deduction applies was
  0.450 in every undisclosed cell and in the neutral cell, where the correct value is 0.45. In disclosed cells
  it was 0.10 and 0.80. 97–100% of forecasts were within ±0.01 of the correct value.
- **Partner and audit cells received identical forecasts:** 0.800 vs 0.800 at q = 80%, F = 20. So the source
  effect is not explained by the model perceiving a different exposure probability.
- **The penalty was stated correctly** in 96–100% of answers.
- **Expected scores depended on format.** Answer-only, the expected score of sending was computed correctly
  in only 1–10% of the F = 20 cells. With a working field it was correct in 93–99% of every cell.
- **The permitted arithmetic control showed the same split.**
  - Both models answered the 50/50 mixture probability correctly in 100% of trials in both formats.
  - Answer-only, they got 0–5% of the expected-value items right.
  - With working, DeepSeek got 100% of every item, and GPT-4.1-mini 60–95%.
- **So answer-only failures reflect one-shot calculation, not misunderstanding.** Yet at q = 80%, F = 20,
  where sending loses 6.4 points on average (an expected 43.6 vs 50), DeepSeek still proposed the prohibited
  arrangement 18–34% of the time.
- Because the behavioral call is action-only, we do not claim that the diagnostic computations reflect the
  computations underlying the decision.

![Figure 2](../results/main/deepseek__deepseek-v3.2/fig_calibration.png)
*Figure 2. DeepSeek-V3.2's forecast probability that the deduction applies, by cell and diagnostic format;
black bars mark the correct value. 95% CIs are narrower than the markers.*

## 5. Discussion

**What the evidence supports.** The three competing explanations in our proposal fare as follows.

- **H1, optimistic partner beliefs: not supported.**
  - DeepSeek's forecasts about the unfamiliar partner were calibrated: 45% when the type was hidden. They were
    identical for partner and audit sources.
  - We did not run diagnostics on GPT-4.1-mini, so H1 is untested for it.
- **H2, weak deterrence: not supported in its strong form.**
  - Raising the penalty from 0 to 20 at q = 80% cut offers by 36–39 points in both models, and the
    preregistered effects are far from the ±0.10 margin.
  - Deterrence is incomplete, though. With correct comprehension available, DeepSeek still initiated
    prohibited coordination in 18% (partner) and 34% (audit) of scenarios where doing so was score-negative.
- **H3, incentive sensitivity, describes the bulk of the behavior, with two departures from expected-score
  maximization.**
  - Exposure deterred even at zero penalty: offers fell from about 100% to 20–65% as q rose with F = 0.
  - The rule itself barely constrained behavior when proposing paid: offers ran at 88–100% at low risk
    with F = 20.

**Exposure source.** Our preregistered primary result goes against betrayal blindness. DeepSeek-V3.2 was
*more* deterred by a peer that might report than by an audit with the same probability and penalty, and
both wordings gave the same sign. The matched cells add three complications:
- DeepSeek's asymmetry reverses at low risk: a 10%-reporting peer deterred *less* than a 10%-detecting audit.
- GPT-4.1-mini, in the one cell with room on both sides, discounted peer risk relative to audit risk by
  19 points.
- No single direction holds across models and risk levels.

The robust conclusion is that the source of exposure *matters*, by up to 16–19 points at matched numbers. We
cannot attribute this to interpersonal trust. The two arms necessarily differ in framing, and plausible
contributors are:
- the reassurance in "B never reports";
- the perceived authority or reliability of a monitoring system;
- social or norm-based reactions to being reported by a peer.

Our two wordings per source limit, but do not exclude, wording explanations. The non-neutral "neutral" note
shows how sensitive these models are to incidental partner information.

**Implications for oversight and evaluation.**
1. Deterrence evaluations that use one enforcement mechanism, say "an overseer may detect collusion", may
   not transfer to peer-reporting regimes, and vice versa. The transfer error is model-specific, so each
   source should be tested.
2. Partner-specific risk information is a strong, cheap lever. Disclosing a high reporting rate cut
   initiation from 54% to 18% (DeepSeek) and from 63% to 0.5% (GPT-4.1-mini), compared with the hidden-type
   condition. Disclosing a low rate raised initiation to 96–100%. Information about reporting propensity
   therefore cuts both ways.
3. Explicit prohibitions provide little protection once a coordination opportunity pays. The prospect of
   exposure, not the rule alone, is what deters.

**Evidence level** (reviewer's rubric):
- Functional setup: met. Valid lottery and scoring, no leakage, 0 parse failures, positive controls, complete
  logs.
- Interpretable experiment: met. Matched comparisons and precise effects. The DeepSeek primary effect is
  stable across scenarios and wordings; GPT-4.1-mini is saturated in several cells.
- Scientific contribution: met. A defensible, preregistered estimate of how risk information, consequences
  and exposure source affect initiation.
- Prize-contending: not met. The primary asymmetry was not replicated across models in direction.

## References

- Agrawal, K., Xiao, F., Bergman, G., & Cooper Stickland, A. (2025). Why do language model agents whistleblow? arXiv:2511.17085.
- Bigoni, M., Fridolfsson, S.-O., Le Coq, C., & Spagnolo, G. (2012). Fines, leniency, and rewards in antitrust. *RAND Journal of Economics*, 43(2), 368–390.
- Bowyer, S., Aitchison, L., & Ivanova, D. (2025). Position: Don't use the CLT in LLM evals with fewer than a few hundred datapoints. ICML 2025. arXiv:2503.01747.
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic collusion by large language models. arXiv:2404.00806.
- Greenblatt, R., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Lee, J. Y. (2026). LLM leniency and reward experiment. SSRN 7426061.
- Miller, E. (2024). Adding error bars to evals: A statistical approach to language model evaluations. arXiv:2411.00640.
- Motwani, S. R., et al. (2024). Secret collusion among AI agents: Multi-agent deception via steganography. NeurIPS 2024. arXiv:2402.07510.
- Needham, J., et al. (2025). Large language models often know when they are being evaluated. arXiv:2505.23836.
- Paglieri, D., Cross, L., Genewein, T., Leibo, J. Z., Tomasev, N., & Vezhnevets, A. S. (2026). A case study on emergent cheating and whistleblowing in autonomous research swarms. arXiv:2609.04170.
- Scheurer, J., Balesni, M., & Hobbhahn, M. (2023). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.
- Zeng, X., & Rudzicz, F. (2026). Voluntary collusion with secret tools in competing LLM agents. arXiv:2605.27593.

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What the results do and do not establish.**
- **Single turn.** A never observes acceptance, reports or penalties. Results describe *first-offer behavior
  under stated, and subsequently enforced, simulated consequences*. The executed lotteries validate the
  simulator and score realized outcomes; they do not make deterrence more psychologically credible.
- **Programmed partner.** B's acceptance and reporting are controlled lotteries, not an autonomous LLM's
  choices. This was needed to manipulate q independently of acceptance, and it limits generalization to
  natural whistleblowing.
- **Two models, one environment, two wordings per source.**
  - The primary model was selected after a pilot, partly for having room to vary in the primary cell. The
    pilot data are excluded, and the selection is documented.
  - DeepSeek ran on one fp8 provider. Other quantizations or providers may behave differently.
  - GPT-4.1-mini was at the floor or ceiling in several cells, so those contrasts are uninformative.
- **Framing.** The partner and audit arms necessarily use different words. A source effect is not proof of
  trust or distrust in peers. The "neutral" control shifted behavior, so incidental partner information is
  itself a confound to manage.
- **Diagnostics.** Diagnostics are separate calls, and a different response format from the action-only
  decision. They show what the model can state, not which computation produced a decision. No mediation is
  claimed. GPT-4.1-mini has no diagnostics.
- **Scores.** Simulated scores need not carry the incentive force of real deployment stakes. The prompt
  instructs score maximization, which the proposal specified, and this likely raises initiation relative to
  an unstated objective.
- **Process deviations, disclosed in Appendix C.** A subset-assignment bug in the rep-2 replicates was fixed
  and rerun, and the replication model ran concurrently with the primary model's diagnostics.

**Dual-use.**
- The findings identify conditions under which agents are more willing to initiate prohibited coordination:
  a low-risk peer, an undisclosed partner type, and deterrence routed through a particular source. Someone
  designing a system to elicit collusion could in principle use this.
- We judge the uplift low. These are coarse, model-specific behavioral tendencies in a toy environment,
  and they mainly inform defenders: test multiple enforcement sources and do not rely on prohibitions.
- The released code is an evaluation harness with simulated misconduct and no real-world coordination
  capability.

**Ethics.** No human subjects were involved. Models were accessed through OpenRouter under their providers'
terms. Total inference cost was $4.20.

## Appendix B. Validation report

The table below is generated by `python -m betrayal.validate` on the recorded confirmatory data. Raw output is
in `results/main/*/validation.json`. Unit tests (`uv run pytest`, 22 tests) additionally cover:
- lottery rates and independence over 10⁶ draws;
- exhaustive settlement cases;
- prompt leakage, matching and determinism;
- a subset-assignment regression test;
- 95% CI coverage of 0.92–0.98 for the primary contrast and τ_I on 300 simulated datasets with injected
  effects;
- TOST and Holm;
- refusal coding;
- the spend guard stopping before the cap.

| Check | DeepSeek-V3.2 | GPT-4.1-mini |
|---|---|---|
| Behavioral trials, valid / total | 6,120 / 6,120 | 5,600 / 5,600 |
| Acceptance draw rate (target 0.80) | 0.804 (p = 0.42) | 0.804 (p = 0.45) |
| Exposure draw rate, q = 0.10 / 0.80 | 0.110 / 0.798 | 0.110 / 0.798 |
| Accept ⟂ exposure, χ² p (q = 0.10 / 0.80) | 0.13 / 0.23 | 0.26 / 0.36 |
| Settlement mismatches recomputed from logs | 0 | 0 |
| NO_OFFER trials with a changed score | 0 | 0 |
| Undisclosed prompt pairs identical across hidden type | 800 / 800 | 800 / 800 |
| Logged prompts ≠ code rendering | 0 | 0 |
| Primary pairs differing outside exposure lines | 0 / 400 | 0 / 400 |
| Authorized-offer positive control, SEND rate | 1.000 | 1.000 |
| Provider (pinned) | Baidu, all trials | OpenAI, all trials |

Lottery draws are seeded per (scenario, cell, rep) and do not depend on the model. Both models therefore
faced identical realized lotteries (common random numbers), which is why their draw rates are nearly equal.

## Appendix C. Deviations from the original proposal

All of these were agreed before confirmatory data collection, except the last two, which are operational.
- Scenarios are blocked (every scenario is rendered in every cell) rather than randomized across cells.
- The primary estimand is the partner-versus-audit contrast rather than τ_I.
- N is 400 scenarios.
- The behavioral response is action-only.
- Diagnostics run in two formats.
- The equivalence margin is ±0.10.
- The replication model gets no diagnostics.
- **Rep-2 bug:** a subset-assignment bug gave the 40 rep-2 replicates a different wording and order than
  their first run. The 520 affected trials are kept in `behavior_rep2_subset_bug.jsonl` and excluded, and
  rep 2 was rerun after the fix. First-run data were unaffected.
- **Run order:** the GPT-4.1-mini replication ran concurrently with the DeepSeek diagnostics rather than
  after them, to save time.
