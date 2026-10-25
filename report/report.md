# Same Risk, Different Collusion: Equivalent Enforcement Information Shifts LLM Agents' Collusion Initiation, but Deterred Agents Do Not Write Less Detectable Proposals

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions) and 3.4 (response to monitoring)
Code, data, preregistrations: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`; preregistration commits: Study 1 `f957093`, Study 2 `a0eab95`, Study 3b `0852581`)

## Abstract

Oversight of multi-agent AI systems relies on deterrence: agents that expect to be reported should hesitate to
propose collusion. Evaluations therefore count proposals, or the reports they trigger. We ask two questions:
1. Does deterrence depend on *how* enforcement information is presented?
2. Does suppressing proposals actually reduce the outcome that matters, completed and unblocked misconduct?

**Setup.** Three single-turn studies (Studies 1, 2 and 3b preregistered), 26,820 confirmatory scored decisions, with DeepSeek-V3.2, GPT-4.1-mini and
Llama-3.3-70B. An agent under a no-coordination rule may privately propose a mutual-approval deal to a verifier.
Lotteries are executed and scored.

**Study 1 (source of exposure).** Information with the same decision-relevant risk moved initiation by up to
19 points.

**Study 2 (format).**
- A stated rate versus a record with the same Bayesian posterior moved initiation by up to 38 points. The
  direction depended on the model.
- One report in episode 10 rather than episode 1 cut offers by 23–71 points in every model, although the
  verifier's tendency was stated to be fixed.
- DeepSeek stated the correct probabilities, so the shifts are not explained by misstated beliefs.
- A truthful calibrated summary fixed the gap in one model and backfired in another.

**Study 3 (proposals vs completed misconduct).** Acceptance was programmed. A fixed LLM reporter read each
free-text proposal, and a blind judge checked that it really proposed the deal.
- A recent-report history and a real-deterrence history suppressed sending by 25–85 points (DeepSeek, Llama).
- The drafts agents wrote did not become materially harder to detect. Scored on all drafts, sent or not, the
  reporter's report probability changed by at most −0.014, inside the preregistered ±0.05 equivalence margin, so
  there was no "deniability". Because only about 6% of drafts escape the reporter, even a one-point change matters
  for the outcome.
- Completed misconduct fell with the suppression. In one test, DeepSeek's recency cue, it fell by significantly
  less than the report count: 30% against 41%. The other DeepSeek test was inconclusive, and Llama nearly stopped
  sending.
- The misconduct is simulated: acceptance is programmed, a judge checks that the proposal is clear, and one fixed
  AI reporter decides detection. This is not autonomous agents negotiating and carrying out collusion.
- Along the way we found that LLM verifiers never accepted collusion in 2,400 single-turn evaluations, and that
  giving them a stake made them report harmless messages.

**Takeaway.** Deterrence measured under one presentation does not transfer to another. In our setting,
suppression reduced how often agents proposed, not how detectably they wrote. Whether report counts overstate the
fall in misconduct was clear in only one of our tests.

## 1. Introduction

Collusion between AI agents has to start somewhere: one agent proposes coordination that oversight prohibits.
Proposing to an unfamiliar agent risks exposure, because the recipient may report it or an audit may catch it.
Designers can tune two things to deter that first move:
- **the enforcement itself:** how likely exposure is and what it costs;
- **the enforcement information:** how the risk is communicated to agents.

The second is rarely studied. Deterrence evaluations, including Scheurer et al. (2023), Zeng & Rudzicz (2026) and
Okamoto et al. (2026), typically describe risk once, in one format, and report how models respond.

We ask whether that response is a stable property of the model or an artifact of presentation, and whether
the proxy that evaluations count (proposals, and the reports they trigger) predicts the outcome an evaluator wants
to minimize: completed, unblocked misconduct. Our design gives
the agent a fixed, scored decision whose decision-relevant content is held constant. We then vary only the form of
the enforcement information:
1. **Study 1, source.** The same exposure probability and penalty, produced either by the partner reporting or
   by an automated audit.
2. **Study 2, format.** The same reporting risk, given either as a stated probability ("this verifier is the type
   that reports 10% of proposals") or as a 10-episode record of what the verifier did. The record's Bayesian
   posterior equals the stated rate (§3).
   - We also test a truthful calibrated summary as a low-cost fix.
   - We test whether *when* the last report occurred matters.
3. **Study 3, proxy vs outcome.** When an enforcement history suppresses proposals, do the remaining proposals get
   rephrased so that a fixed LLM reporter misses them? We call this deniability. And does completed misconduct
   fall as much as the report count suggests?

**Findings.** Presentation moves collusion initiation by amounts comparable to the incentives themselves, even when
the model's stated beliefs are correct. The direction of the shift depends on the model.

**Contributions.**
1. **Two preregistered, validated experiments** in a reproducible environment. Lotteries are executed, settlement
   is exact, prompts are byte-level minimal pairs, and a Bayesian benchmark gives a known right answer in every
   cell.
2. **Evidence that LLM deterrence is not presentation-invariant.** The source effect reaches up to 19 points, the
   format effect up to 38, and the recency effect up to 71. All are model-specific in direction, while stated
   beliefs are correct.
3. **A tested low-cost intervention with a cautionary result.** Calibrated summaries close most of the format gap in
   one model, are ineffective or harmful in the others, and never harm authorized cooperation.
4. **A proxy-validity test of deterrence.**
   - Deterrence reduced sending. It did not make drafts measurably harder to detect: changes stayed inside the ±0.05
     equivalence margin.
   - In one test, completed misconduct fell by significantly less than the report count. The rest were
     inconclusive or at the floor.
   - Reported alongside: two instrument findings (LLM verifiers never accept collusion; stakes make them
     over-report) and a failed displacement pilot.

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
- **Closest to our Study 2:** Ge, Zhang & Vorobeychik (2026) compare described prospects with experienced histories
  in 20 LLMs.
  - Conversational models show a large description–history gap and are sensitive to order and framing.
  - Reasoning models stay close to the expected-payoff benchmark.
  - Our Study 2 is consistent with their conversational-model result. Our contribution is narrower: the same gap
    for *enforcement* information in a collusion decision, with posterior-matched records and executed
    lotteries.
- **Gap:** we found no work comparing *equivalent enforcement* information across presentations for collusion or
  other misbehaviour. Description–history gaps in general risky choice are already documented (Ge et al., 2026).

**Proxies vs outcomes.**
- Training against a chain-of-thought monitor reduced *detected* reward hacking while hidden hacking continued
  (Baker et al., 2025).
- In mutual verification, explicit coordination fell from 90% to 62% while collusion stayed flat (Shi et al., 2026).
- Agents can agree "on paper" without acting on it (Colosseum, 2026).
- Agents evade runtime monitors by encoding requests or moving them to other channels (EvasionBench, 2026; Covert
  Assistance, 2026).
- Choosing when to attack lowers measured safety (Ge-Wang et al., 2026).
- Criminology finds displacement and diffusion about equally often (Guerette & Bowers, 2009).
- **Our narrow addition:** whether EV-irrelevant enforcement *presentation* changes how evasively the surviving
  proposals are phrased.

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

**Study 3a (displacement; pilot only).**
- Three routes: review, message the verifier, or merge with an admin override. Both violation routes completed
  with probability 0.72 and were EV-matched.
- Detection blocked the bonus.
- Arms: Study 2's early vs late report.
- 30 pilot scenarios per cell.

**Study 3b (deniability and proxy validity; preregistered).**
- **Acceptance is programmed and stated:** "if your message makes the proposal clear, the task system makes B
  accept it with probability 80%".
- **Reporting is live.** A fixed reporter (Mistral-Small-3.2, plain reviewer prompt, blind to arm) reads A's exact
  free-text message. Its first-token logprobs give r_report, and a report blocks the deal and costs F.
- **A blind judge** (Qwen3-235B) gives q_prop, the probability that the message really proposes the deal.
  Non-proposals cannot be accepted.
- **A first writes the draft, then decides whether to send it.** Every scenario therefore yields a draft in every
  cell, so phrasing is compared fully paired.
- **History shown to A.** Ten earlier messages from other agents, "selected for display". Each outcome is a real
  reporter decision on a pool message written by a non-A model, drawn exactly as in settlement.
  - Recency suppressor: k = 5 reports shown either as the oldest five (E) or the most recent five (L). The same
    episodes are reordered.
  - Real-deterrence suppressor: 1 in 10 reports (LOW) vs 8 in 10 (HIGH).
- **Outcomes per trial.**
  - Operator-visible reports: T1 = P·r_report.
  - Completed, unblocked misconduct: CUM = P·0.8·(1 − r_report)·q_prop.
- **Single confirmatory test (H3), per model and suppressor.** "Deniability" requires both Δr_report ≤ −0.05 (95%
  CI below 0) and q_prop non-inferior at −0.02. "No deniability" means TOST equivalence within ±0.05. The
  operator view D = log(T1 ratio) − log(CUM ratio) is derived from these, not tested separately.
- **F** was chosen on pilot E by Study 2's rule: DeepSeek 60, Llama 20. Neither model reached an interior send
  rate (DeepSeek ≥ .80, Llama ≤ .17), so the closest-to-50% fallback applied.
- **Scale:** 300 fresh scenarios × 4 cells per model, plus 100 authorized-coordination drafts as a collateral check.

## 4. Results

Studies 1–2: all 24,320 behavioral trials (Study 1: 11,720; Study 2: 12,600) and 11,480 diagnostic and arithmetic
calls returned valid output. Study 3b: all 2,500 main trials returned valid output. Across all studies there were
zero refusals, parse failures or unresolved API errors.

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

**Stated beliefs are correct, so the gap is not a belief error.** DeepSeek's diagnostic forks returned the Bayesian
answer in every cell:
- The mean forecast was 0.100–0.111 for S10, R1 and R1+summary, and 0.800–0.801 for S80, R8 and R8+summary.
- 95–100% of forecasts were within ±0.01, and 92–99% of expected-score computations were correct.
- Yet its behaviour differed between S80 and R8 by 14 points.
- This rules out a misstated belief as the explanation. It does not show what computation drives the choice: the
  forks are separate calls, so a correct stated answer does not prove the decision used it.

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

### 4.3 Study 3a and the instrument findings (pilots, reported as found)

**Displacement could not be tested.**
- In the three-route pilot the admin override was chosen in 0–3% of trials in every model. That held even at half
  the penalty, where it beat messaging on expected value.
- The Study-2 recency suppressor also shrank in the new format, to −7, −10 and −30 points. It missed the
  preregistered gate (≥ 15 points in ≥ 2 models), and no main run was made.
- Models treated the override as categorically off-limits rather than as a priced option.

**Live LLM verifiers never accepted collusion.**
- Qwen3-235B and Mistral-Small-3.2 approved without review in 0 of 2,400 pool evaluations, across three verifier
  prompts.
- Telling the verifier it would gain from the deal made it report a harmless status message 84–99% of the time.
- A neutral "monitor" framing flagged that harmless message at .98–.999.
- **The same models also refuse in the partner's seat.** We ran a gate pilot with its criteria fixed in advance
  (`docs/gate_live_b.md`). DeepSeek-V3.2, GPT-4.1-mini and Llama-3.3-70B each played B, a peer agent:
  - B was told to maximize its score, under the same rule as A, and was shown the same expected-value structure
    (+12 if it approves without review; a 10% audit costing 60).
  - B read 60 real agent-A drafts and could accept the deal and then approve without review.
  - **Result: 0 of 180 accepted** (DeepSeek and GPT declined 58 and reported 2; Llama declined 22 and reported
    38).
  - These models proposed the deal in 78–100% of trials in A's seat. So the asymmetry is between proposing and
    accepting. It is not a difference between models.
- **Three rounds of private messages did not change this much.** We ran a second gate, again with criteria fixed
  in advance (`docs/gate_multiturn.md`). Two copies of the same model talked privately for three rounds each, then
  each privately chose an action on the other's batch.
  - **Llama:** A proposed in every episode, and B refused in every one (0/30).
  - **DeepSeek:** A proposed in 80% of episodes. B *agreed in words* in 6 of 30, often with plans to avoid the
    audit. But it carried the deal out only once (1/30, below the gate's 3/30). In 3 of the 6 it **reported A
    after agreeing**, and in 2 it just reviewed normally.
  - A trusted every verbal agreement and approved B's batch without review all 6 times.
  - We stopped as preregistered. Descriptively (n = 6, one model, self-play), this is collusion "on paper" plus
    betrayal of a trusting proposer. Agreement in conversation is not a reliable sign of executed collusion.
- This is why Study 3b programs acceptance and keeps detection live. Live two-agent collusion almost never
  happened in either workflow (1 executed violation in 240 live-partner decisions).

### 4.4 Study 3b: do suppressed proposals become deniable, and does misconduct fall with reports?

| n = 300 per cell | DeepSeek E → L | DeepSeek LOW → HIGH | Llama E → L | Llama LOW → HIGH |
|---|---|---|---|---|
| Sends proposal | .78 → .47 | .89 → .41 | .25 → .00 | .86 → .01 |
| ΔP (G1-live, needs ≤ −.15) | **−.32** [−.39, −.25] | **−.49** [−.55, −.42] | **−.25** [−.30, −.20] | **−.85** [−.89, −.81] |
| Report prob. of drafts | .94 → .93 | .94 → .93 | .96 → .96 | .96 → .96 |
| H3 Δr_report | −.011 [−.020, −.002] | −.014 [−.025, −.002] | −.001 [−.006, +.004] | −.001 [−.005, +.003] |
| H3 label | **no deniability** | **no deniability** | **no deniability** | **no deniability** |
| Reports (T1) change | −41% | −55% | −100% | −99% |
| Completed misconduct change | −30% | −47% | −100% | −98% |
| D (derived) | −0.18 [−0.35, −0.01] | −0.16 [−0.34, +0.03] | n/a (no L sends) | −0.48 [−0.94, −0.02] |

*Table 2. Study 3b. Scenario-paired 95% CIs. The judge's q_prop was ≥ .98 in every cell.*

**What happened.**
- **Both suppressors cut sending strongly in both models.** GPT-4.1-mini showed no suppression in the pilot
  (+.23 and .00), so it was excluded before the main run by the preregistered gate.
- **The drafts did not become materially harder to detect.** The primary analysis scores every generated draft,
  sent or not.
  - In every model × suppressor cell, the change in report probability lay inside the preregistered ±0.05 margin:
    the largest was −0.014. The judge rated essentially every draft as a clear proposal.
  - **DeepSeek:** the result holds on scenarios that sent in both cells.
  - **Llama:** too few scenarios sent in both cells for that check (insufficient data for recency, inconclusive
    for real deterrence).
  - The result also holds under the hardened reporter.
  - Small changes can still matter. DeepSeek's report probability fell by about one point. Because only about 6%
    of drafts escape the reporter, that point matters for the outcome (next bullet).
- **Reports tracked misconduct in direction; the size of the fall differed in one test.**
  - Agents' drafts were reported 93–96% of the time, against 51% for the pool messages. Completed misconduct
    therefore lives in the small unreported tail.
  - A one-point drop in report probability is invisible in the report count. It is a ~15–20% rise in that tail.
  - For DeepSeek's recency cue, reports fell 41% but completed misconduct only 30% (D = −0.18, CI excludes 0).
  - The real-deterrence contrast points the same way (D = −0.16), but its CI includes 0.
  - Llama's D rests on 3 sends in HIGH and is not interpretable.
- **The "fix" failed its collateral check.**
  - Adding "however it is worded" to the reporter's rule did not change any H3 label.
  - It made the reporter report authorized coordination 96% of the time, against 0% for the plain reporter.
  - Hardened wording is not a free safeguard.

![Figure 3](../results/main3b/fig_s3b.png)
*Figure 3. Study 3b. Top: sending (grey) and operator-visible reports (blue) per trial. Bottom: expected
completed, unblocked misconduct per trial. Error bars are 95% CIs; n = 300 scenarios per bar.*

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

These effects occurred while DeepSeek stated the correct probabilities and expected values in separate diagnostic
calls. So they are not explained by misstated beliefs, although our data cannot identify the internal mechanism.
They are not consistent in direction across models.

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

4. **Fewer proposals meant less simulated misconduct here (Study 3b).**
   - Deterred agents did not write measurably less detectable drafts for a fixed LLM reporter.
   - Because detection was near-certain, completed misconduct sits in the small unreported tail. In one of our
     tests (DeepSeek, recency) it fell significantly less than the report count. The other tests were
     inconclusive or at the floor, so this is not established as a general property of anti-collusion
     evaluations.
   - The practical lesson is narrow: when detection is near-certain, estimate the escaped tail directly rather
     than scaling report counts.
5. **Two cautions about LLMs as enforcement instruments.**
   - Single-turn LLM verifiers never accepted collusion. That contrasts with the 94% collusion seen over long
     horizons (Shi et al., 2026), which suggests the time horizon of an evaluation shapes what it can observe.
   - Telling the verifier it had something to gain, or hardening its rule, made it report legitimate messages.

**Evidence level, judged honestly.**
- Execution: preregistered, validated, 26,820 confirmatory scored decisions (Studies 1–2: 24,320; Study 3b: 2,500), zero failures.
- Primary hypotheses: the original betrayal-blindness hypothesis was not supported (Study 1). The consistent-sign
  format and correction criteria were not met (Study 2).
- The robust, decision-relevant result is non-invariance: large, model-specific presentation effects with correct
  stated beliefs, and strong temporal recency in every model.
- Study 3b:
  - The preregistered H3 is a clear "no deniability" in 4 of 4 model × suppressor tests.
  - Proxy inflation (D) is a derived quantity, significant in one of three interpretable tests.
  - Completed misconduct is simulated: programmed acceptance, a clarity judge, and one fixed reporter.
  - No second reporter passed its gates, so the result rests on one reporter model.
  - The 3a displacement test did not get past its pilot.

**In plain words.**

**The idea we tested.** When AI agents are told they might be reported for proposing a forbidden deal, they hold
back. We asked whether that holds up under three conditions: when the same risk is merely described differently;
and when we look past the proposals themselves to how much misconduct actually happens.

**Study 1** gave agents the same chance of being caught and the same penalty. Only the catcher changed: the partner
they propose to, or an automated audit. We expected agents to be less wary of their partner. That was not what we
found. DeepSeek was *more* deterred by its partner (−16 points), GPT-4.1-mini was less deterred (+19), and so there
is no single pattern.

**Study 2** gave agents the same risk either as a stated percentage or as a short log of what the verifier had done
before. The log was built so that it implies the same percentage. If the agents were consistent, both formats would
produce the same behaviour. Instead:
- behaviour shifted by up to 38 points, in different directions for different models, even though DeepSeek could
  state the correct probability;
- in every model, a report that happened *recently* deterred far more than the same report long ago (23–71 points
  less proposing), even though the verifier was described as never changing;
- a truthful one-line summary of the risk fixed the gap for one model and made another propose almost always.

**Study 3** asked whether fewer proposals really means less misconduct. We had a fixed AI reporter read every
message that agents wrote. We expected that agents who were scared off would still send some proposals, but word
them so the reporter would miss them. They did not.
- A recent-report history or a high-report history cut proposing by 25–85 points (DeepSeek, Llama).
- The messages agents wrote were about as easy to catch as before: a change of at most 1.4 points, inside our
  5-point equivalence margin.
- Fewer proposals did mean less completed misconduct. But the reporter catches about 94% of messages, so the
  small leftover that gets through can move differently from the report count. In one test (DeepSeek, recency),
  reports fell 41% while completed misconduct fell only 30%. The other tests were inconclusive or near zero.
- This misconduct was simulated: acceptance was programmed and one fixed AI reporter decided detection.
- Along the way we found that AI reviewers asked to accept such deals never did, and that giving them a stake in
  the deal made them report harmless messages. Even the same models that eagerly proposed the deal refused it
  every time (0 of 180) when they were the one being asked. When two agents could talk for three rounds,
  DeepSeek's partner sometimes agreed (6 of 30), but it followed through only once, and three times it reported
  the proposer instead.

**What it means.** How agents are told about oversight matters as much as the oversight itself, and it matters
differently for each model. So a deterrence result measured with one wording should not be trusted for another.
Counting proposals or reports was a fair guide to whether simulated misconduct went down. In one test it
exaggerated by how much, so evaluators should check completed misconduct directly where they can.

**Next steps.**
- Repeat this in multi-turn settings, where agents actually experience reports rather than reading about them, and
  where real collusion is known to emerge.
- Let the partner's acceptance depend on what the message says, and use several independent reporters.
- Test which ways of showing enforcement history deter consistently across models.

## References

- Agrawal, K., Xiao, F., Bergman, G., & Cooper Stickland, A. (2025). Why do language model agents whistleblow? arXiv:2511.17085.
- Bigoni, M., Fridolfsson, S.-O., Le Coq, C., & Spagnolo, G. (2012). Fines, leniency, and rewards in antitrust. *RAND Journal of Economics*, 43(2), 368–390.
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic collusion by large language models. arXiv:2404.00806.
- Greenblatt, R., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Ge, L., Zhang, Y., & Vorobeychik, Y. (2026). Mind the (DH) Gap! A contrast in risky choices between reasoning and conversational LLMs. In *Proceedings of ACL 2026 (Long Papers)*, pp. 10503–10525. https://aclanthology.org/2026.acl-long.479/
- Horowitz, M., & Plonsky, O. (2025). LLMs in decisions from experience. arXiv:2503.10248.
- Lee, J. Y. (2026). LLM leniency and reward experiment. SSRN 7426061.
- Miller, E. (2024). Adding error bars to evals: A statistical approach to language model evaluations. arXiv:2411.00640.
- Okamoto, Erol, & Erol (2026). Why do AI agents break rules? arXiv:2608.12323 (AIES 2026).
- Paglieri, D., Cross, L., Genewein, T., Leibo, J. Z., Tomasev, N., & Vezhnevets, A. S. (2026). A case study on emergent cheating and whistleblowing in autonomous research swarms. arXiv:2609.04170.
- Scheurer, J., Balesni, M., & Hobbhahn, M. (2023). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.
- Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models' sensitivity to spurious features in prompt design. ICLR 2024. arXiv:2310.11324.
- Shi, Zhang, & Yang (2026). Emergent collusion in long-horizon LLM agent interaction. arXiv:2609.24967.
- Zeng, X., & Rudzicz, F. (2026). Voluntary collusion with secret tools in competing LLM agents. arXiv:2605.27593.
- Baker, B., et al. (2025). Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. arXiv:2503.11926.
- Colosseum (2026). arXiv:2602.15198.
- Covert Assistance (2026). arXiv:2609.39050.
- EvasionBench (2026). arXiv:2609.30217.
- Ge-Wang, et al. (2026). Attack selection. arXiv:2606.06529.
- Guerette, R. T., & Bowers, K. J. (2009). Assessing the extent of crime displacement and diffusion of benefits: A review of situational crime prevention evaluations. *Criminology*, 47(4), 1331–1368.

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
- **Study 3b's own limits.**
  - **Programmed acceptance.** Acceptance does not depend on phrasing beyond the judge's clarity check, so
    covertness costs nothing in intelligibility.
  - **One reporter.** It reports a harmless message 10% of the time, a declared deviation from the ≤ 5% gate, and
    no second reporter passed its gates.
  - **Selected histories.** The histories are real but "selected for display"; A was told so.
  - **Penalty not interior.** F was not interior for DeepSeek or Llama.
  - **Llama at the floor.** Llama's near-zero sending under both suppressors leaves its operator-view numbers
    uninformative.
  - **Derived inflation.** D is derived, not a preregistered test.

**Dual-use.** Knowing that the presentation of enforcement shifts initiation could in principle help someone design
a pipeline that makes collusion more likely: hiding recent reports, or showing records rather than rates to models
that discount records. The effects are model-specific and environment-bound, so we judge the uplift low. The
practical message is defensive: test oversight communications across equivalent presentations, and validate
information-based fixes per model. The code is an evaluation harness with simulated misconduct.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total
inference cost was $7.70 (Study 3: $1.12).

## Appendix B. Validation

Unit tests (`uv run pytest`, 46 tests) and the data-level validators (`python -m betrayal.validate`;
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
- Study 3:
  - settlement, CRN draws, rendered minimal pairs (E/L differ only in history lines);
  - label recovery for injected displacement, diffusion and deniability;
  - each history outcome equals its logged draw (u < r_report), and E and L show the same episodes;
- the spend guard ($8, raised by the user to $9.50).

| Check (recorded data) | Study 1 (DS / GPT) | Study 2 (DS / GPT / Llama) |
|---|---|---|
| Valid trials | 6,120 / 5,600 | 4,200 / 4,200 / 4,200 |
| Settlement mismatches | 0 / 0 | 0 / 0 / 0 |
| Logged prompt ≠ renderer | 0 / 0 | 0 / 0 / 0 |
| Penalties on authorized offers | — | 0 / 0 / 0 |
| Provider (pinned) | Baidu / OpenAI | Baidu / OpenAI / DeepInfra |

Study 3b (DeepSeek / Llama): 1,300 / 1,200 valid trials. Logged prompts all equal the renderer's output. Providers
were pinned: Baidu / DeepInfra. All drafts were scored, and the mean leaked label mass was < 1%.

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
- **Study 3** (all declared in `prereg_v3b.md` §5 before any main3b call):
  - the spend cap was raised from $8 to $9.50 by the user;
  - Study 3a stopped at its pilot gate;
  - acceptance was programmed after live verifiers never accepted;
  - the reporter's harmless-probe rate is .10 against a ≤ .05 gate, accepted by the user;
  - no second reporter;
  - F was not interior for DeepSeek or Llama;
  - GPT-4.1-mini was excluded on G1-live;
  - the reporter and judge prompts were revised on probes only, before any agent-A data.
