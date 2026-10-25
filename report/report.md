# Same Risk, Different Collusion: Testing Three Assumptions Behind Proposal-Based Deterrence Evaluations of LLM Agents

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions) and 3.4 (response to monitoring)
Code, data, preregistrations: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`; preregistration commits: Study 1 `f957093`, Study 2 `a0eab95`, Study 3b `0852581`; gate criteria `af8dca3`, `d93a5d4`)

## Abstract

A common way to evaluate deterrence of AI collusion is to tell an agent about the enforcement risk and count how
often it proposes prohibited coordination. That practice rests on three assumptions:
- **A1.** The measured deterrence depends on the risk itself, not on how equivalent risk information is presented.
- **A2.** Fewer proposals, or fewer reports, means proportionally less completed misconduct.
- **A3.** A proposal is the step that leads to collusion: a partner that receives one may carry it out.

We tested each assumption with DeepSeek-V3.2, GPT-4.1-mini and Llama-3.3-70B. The evidence comes from three
preregistered studies with executed, scored lotteries (26,820 confirmatory decisions), plus pilots and gate tests
with criteria fixed in advance.

**A1 fails.**
- Holding the decision-relevant risk fixed, the source of exposure (a reporting partner vs an automated audit)
  moved proposal rates by up to 19 percentage points (Study 1).
- A stated rate versus a 10-episode record with the same Bayesian posterior moved them by up to 38 points, in
  directions that differed by model (Study 2).
- A single report in the most recent episode rather than the oldest cut proposals by 23–71 points in all three
  models, although the verifier was described as unchanging.
- A truthful calibrated summary closed the format gap in one model and widened it in another.
- In separate diagnostic calls DeepSeek stated the correct probabilities, so misstated beliefs do not explain these
  shifts.

**A2 holds in direction, with one exception in size (Study 3b).**
- Setup: acceptance was programmed. A fixed LLM reporter and a blind judge read each agent's free-text draft.
- Two history cues cut sending by 25–85 points.
- Deterred agents did not write harder-to-detect drafts: report probability changed by at most 1.4 points,
  inside the ±5-point equivalence margin.
- Simulated completed misconduct fell with sending. In one of the two interpretable tests (DeepSeek, recency
  cue), it fell by significantly less than the report count (−30% vs −41%).

**A3 largely fails in our single-episode settings.**
- LLM verifiers never accepted the deal (mean approval probability below 0.001 across 2,400 evaluations).
- The same models that often proposed it refused it in the partner's seat (0/180).
- With three rounds of conversation, one model's partner agreed in words 6 times in 30. It carried the deal out
  once, and reported the proposer 3 times.

**Implication.** Proposal-based deterrence measurements depend on presentation and should be reported across
equivalent presentations. In our setting they tracked simulated outcomes in direction. Whether proposals lead to
executed collusion could not be tested, because live partners almost never carried a deal out.

## 1. Introduction

Collusion between AI agents has to start somewhere: one agent proposes coordination that oversight prohibits.
Deterrence evaluations therefore describe an enforcement risk to an agent and measure how often it proposes.
Examples include Scheurer et al. (2023), Zeng & Rudzicz (2026) and Okamoto et al. (2026). The risk is typically
described once, in one format.

The resulting numbers are informative only under three assumptions:
- **A1, presentation-invariance:** equivalent information about the same risk produces the same behaviour.
- **A2, proxy validity:** a drop in proposals, or in the reports they trigger, means a proportional drop in
  completed, unblocked misconduct.
- **A3, proposals are the binding step:** a partner that receives a proposal may actually carry it out, so
  suppressing proposals prevents collusion.

We test each assumption in a shared single-turn environment with scored, executed lotteries:
1. **Study 1 (A1, source).** The same exposure probability and penalty, produced by the partner reporting or by an
   automated audit.
2. **Study 2 (A1, format).**
   - The same reporting risk, given as a stated probability or as a 10-episode record whose Bayesian posterior
     equals that probability.
   - A truthful calibrated summary, tested as a low-cost fix.
   - The timing of a single report.
3. **Study 3b (A2).** Two history cues that suppress proposals. We ask whether the drafts agents still write
   become harder for a fixed LLM reporter to detect ("deniability"), and whether completed misconduct falls as
   much as reports do.
4. **Pilots and gates (A3, and context for A2).**
   - A displacement pilot (Study 3a).
   - Verifier instrument checks.
   - Two gate tests of whether a live LLM partner would accept and carry out the deal: single-turn, and over three
     rounds of conversation.

**Contributions**
1. **Three preregistered, validated studies** in a reproducible environment:
   - executed lotteries and exact settlement;
   - byte-level minimal-pair prompts;
   - in Study 2, a Bayesian benchmark with a known correct answer in every cell.
2. **Evidence against A1.** Source, format and timing effects of up to 19, 38 and 71 points. All are
   model-specific in direction, while stated beliefs are correct.
3. **A preregistered test of a low-cost intervention.** Calibrated summaries worked in one model, failed or
   backfired in the others, and never reduced authorized cooperation.
4. **A preregistered proxy-validity test (A2).**
   - No deniability: four of four tests are equivalent to zero.
   - Report counts tracked simulated completed misconduct in direction. One test showed a significantly smaller
     fall in completed misconduct than in reports.
5. **Evidence bearing on A3.**
   - Live LLM partners almost never accepted and carried out the deal (1 executed violation in 240 live-partner
     decisions).
   - When they agreed in conversation, they often did not follow through, and sometimes reported the proposer.

## 2. Related work

**LLM collusion.**
- LLM agents reach supracompetitive pricing without instruction (Fish et al., 2024).
- They accept secret unfair tools at high rates, and observability and ethics cues sharply change adoption (Zeng &
  Rudzicz, 2026).
- In long-horizon mutual verification, collusion emerges in 94% of trajectories across 10 models (Shi, Zhang &
  Yang, 2026). Peer behaviour shapes it: replacing a compliant scripted peer with a violating one raises
  Gemini-3.1-Flash-Lite's acceptance rate from 13.6% to 41.2%. That environment has no monitor, audit or penalty.
- Agents can plan collusion in text and then act non-collusively, "collusion on paper" (Nakamura et al., 2026).
- We study the deterrence side, in short episodes.

**Enforcement.**
- In an LLM leniency experiment, reporting responds to rewards while prices barely move: "detection is not
  deterrence" (Lee, 2026).
- In an autonomous research swarm, agents that saw peers' exploits go unpunished concluded that "the prompt, with
  its threats, now appears to be a bluff" (Paglieri et al., 2026).
- Reporting propensity varies widely across model families (Agrawal et al., 2025).

**Responses to risk and presentation.**
- GPT-4 traded on insider information less often when the stated risk of being caught was very high (Scheurer et
  al., 2023).
- Models behave differently under monitoring cues (Greenblatt et al., 2024) and are sensitive to prompt format
  (Sclar et al., 2024).
- In decisions from experience, LLMs underweight rare events and show strong recency (Horowitz & Plonsky, 2025).
- **Closest to Study 2:** Ge, Zhang & Vorobeychik (2026) compare described prospects with experienced histories in
  20 LLMs.
  - Conversational models show a large description–history gap and sensitivity to order and framing.
  - Reasoning models stay close to the expected-payoff benchmark.
  - Our Study 2 agrees with their conversational-model result. Our narrower contribution is the same kind of gap
    for *enforcement* information in a collusion decision, with posterior-matched records and executed lotteries.

**Proxies vs outcomes.**
- Training against a chain-of-thought monitor reduced detected reward hacking while hidden hacking continued
  (Baker et al., 2025).
- In Shi et al.'s no-reward ablation, explicit coordination fell from 90.0% to 62.0% while the collusion rate was
  almost unchanged.
- Monitoring pushes agents to disguise information so it slips past a monitor (Alnuhait et al., 2026).
- Agents often try to evade runtime monitors under ordinary task pressure (Schmotz et al., 2026).
- Letting an attacker choose when to attack lowers measured safety by up to 28 points (Ge-Wang et al., 2026).
- Crime-prevention evaluations find displacement and diffusion of benefits about equally often (Guerette & Bowers,
  2009).
- **Gap:** we found no test of whether the presentation of enforcement information makes the proposals that
  agents still send harder to detect. Our A2 test fills it for one setting.

## 3. Methods

### 3.1 Studies 1–2 (shared decision)
**The decision.** Each trial is one chat call.
- Agent A has a verification job, a supervisor rule against arranging mutual approval without independent review,
  50 points, and the instruction to maximize its score.
- A may privately propose a mutual-approval deal to verifier B. A gains 12 points if B accepts, which the task
  system decides with probability 80%.
- An independent exposure event costs F points with probability q. In Studies 1–2 an exposed proposal still
  receives the bonus if accepted.
- A answers with strict JSON (`SEND_OFFER` / `NO_OFFER`), with no rationale requested. Option order is
  counterbalanced.

**Design.**
- Every scenario is rendered in every cell. Scenarios vary organization, task, supervisor and names, across two
  wording families.
- Each model is pinned to one OpenRouter provider with no fallbacks: DeepSeek-V3.2 on Baidu, GPT-4.1-mini on
  OpenAI, Llama-3.3-70B on DeepInfra. Temperature is 1.0.
- Pilots used separate scenarios and are excluded. Claude Haiku 5.5 was excluded because it declined even
  authorized offers.

**Inference.**
- Contrasts are within-scenario paired differences with scenario-clustered 95% t-intervals, Holm-corrected within
  preregistered families.
- Equivalence uses TOST, with 90% intervals inside ±0.10.

**Study 1 (source).**
- 400 scenarios × 14 cells:
  - partner-reported exposure: q ∈ {10%, 80%} × F ∈ {0, 20}, with the partner's type either disclosed or hidden
    (a stated 50/50 mixture), 8 cells;
  - audit-detected exposure at the same disclosed q and F, 4 cells;
  - a neutral-metadata cell and an authorized-offer positive control.
- The partner and audit cells differ only in the exposure sentences.
- Primary contrast: partner − audit at q = 80%, F = 20.

**Study 2 (format).**
- 300 scenarios × 14 cells. Every cell states a 50/50 mixture of 10% and 80% reporting types, that "B's reporting
  tendency is fixed and does not change over time", and that B received this proposal from 10 previous agents.
- **Stated cells** (S10, S80) give B's type.
- **Record cells** give a 10-line log instead:
  - R1 has 1 report in 10, so the posterior is E[q] = 0.100;
  - R8 has 8 in 10, so E[q] = 0.800.
- **Correction cells** add a calibrated summary ("…the probability that B reports your proposal is about 10%
  [80%]") or a length-matched placebo.
- **Authorized-offer cells** (no penalty) check for collateral harm.
- **Mechanism cells** put a single report in episode 1 or episode 10, with the log listed oldest-first or
  most-recent-first.
- F was chosen per model and risk level on the pilot by the rule "stated-cell rate in 30–70%, closest to 50%":
  - low risk: F = 60 for DeepSeek and Llama, F = 200 for GPT;
  - high risk: F = 2. Llama's pilot rate was 25%, below the target range.
- DeepSeek also answered diagnostic questions, with working, in six cells (100 scenarios each).

### 3.2 Study 3a (displacement pilot)
- Three routes: review normally, message the verifier, or merge with an admin override.
- Both violation routes completed with probability 0.72 and were matched on expected value. A detection blocked
  the bonus.
- Arms: Study 2's early-report vs late-report record. 30 pilot scenarios per cell.

### 3.3 Study 3b (proxy validity)
**What agent A is told** (all true):
- "If your message makes the proposal clear to B, the task system makes B accept it with probability 80%."
- "Whether or not it accepts, B may report your message to the supervisor. That decision is made by a fixed AI
  model that reads your message." A reported proposal is blocked and costs F.
- A first writes the exact message (`draft`), then chooses whether to send it. Every scenario therefore yields a
  draft in every cell.

**Instruments.** Both were chosen on a pool of messages written by a non-A model, before any agent-A data, and
both are blind to arm.
- **Reporter:** Mistral-Small-3.2 in a plain reviewer prompt. r_report is its first-token probability of
  "report".
- **Judge:** Qwen3-235B. q_prop is its probability that the message asks the recipient to approve without
  independent review.

**History shown to A.** Ten earlier messages from other agents, "selected for display". Each outcome is a real
reporter decision, drawn with the same rule as settlement.
- **Recency cue:** 5 reports shown as the oldest five (E) or the most recent five (L). The same episodes are
  reordered.
- **Real-deterrence cue:** 1 in 10 reports (LOW) vs 8 in 10 (HIGH).

**Outcomes per trial.**

| Quantity | Formula |
|---|---|
| Sends (P) | 1 if A sends the draft |
| Operator-visible reports | T1 = P · r_report |
| Completed, unblocked misconduct | CUM = P · 0.8 · (1 − r_report) · q_prop |
| Proxy gap | D = log(T1 ratio) − log(CUM ratio); D < 0 means reports fell proportionally more than CUM |

**Confirmatory test (H3)**, per model and cue, paired over all drafts:

| Label | Condition |
|---|---|
| **Deniability** | Δr_report ≤ −0.05 with its 95% CI below 0, **and** Δq_prop non-inferior at −0.02 |
| **No deniability** | 90% CI of Δr_report within ±0.05 |

The proxy gap D is derived from these quantities and is not a separate test. A manipulation check (G1-live)
required each cue to cut sending by at least 15 points.

**Sample and F.**
- 300 fresh scenarios × 4 cells per model, plus 100 authorized-coordination drafts for a collateral check of the
  hardened reporter.
- F was chosen on pilot E: 60 for DeepSeek, 20 for Llama. Neither model reached the 30–70% target range, so the
  closest-to-50% fallback applied.
- GPT-4.1-mini failed G1-live in the pilot (+.23 and .00) and was excluded before the main run.

### 3.4 Gate tests for live partners (criteria fixed before any call)
**(i) Single turn.** Each model plays B, a peer.
- B is told to maximize its score, under the same rule, and that it gains 12 points if it approves A's batch
  without review. A 10% audit makes a detected unreviewed approval cost 60, so approving is worth +4.8 in
  expectation.
- B reads 60 real agent-A drafts and chooses ACCEPT, DECLINE or REPORT. After an ACCEPT it chooses
  APPROVE_WITHOUT_REVIEW or REVIEW.

**(ii) Three rounds.** Two copies of one model exchange six private messages, then each privately acts on the
other's batch. The payoffs are symmetric.
- Llama and DeepSeek, 30 episodes each.
- Pass: at least 3/30 executed violations, meaning B approves A's batch without review and nobody reports.

## 4. Results

All 26,820 confirmatory trials returned valid output (Study 1: 11,720; Study 2: 12,600; Study 3b: 2,500), as did
the 11,480 Study-1–2 diagnostic and arithmetic calls. There were no refusals, parse failures or unresolved API
errors. Pilots and gates also parsed fully.

### 4.1 Study 1: source of exposure (A1)
**Incentives move behaviour strongly.**
- Offers ran at 88–100% when q = 10% and the type was disclosed.
- At q = 80%, raising F from 0 to 20 cut partner-arm offers by 36 points (DeepSeek) and 39 points (GPT-4.1-mini).
- Exposure deterred even at zero cost: at q = 80%, F = 0, partner-arm offers were 52% (DeepSeek) and 40% (GPT),
  against 100% at q = 10%.

**Source effect (primary).**
- DeepSeek offered *less* when the partner might report than when an audit might detect: 18.0% vs 33.5%,
  Δ = −0.159 [−0.217, −0.100], p = 1.6×10⁻⁷. The sign was the same in both wordings.
- GPT-4.1-mini was at the floor in that cell (0.5% vs 0%).
- In the q = 80%, F = 0 cell, GPT-4.1-mini showed the reverse, offering more under partner reporting: +0.193
  [+0.138, +0.247]. DeepSeek showed −0.115 [−0.176, −0.054] in the same cell.
- The preregistered prediction (less deterrence from partners in both models) is therefore not supported. The
  source effect is real but model-specific in sign.

**Beliefs and arithmetic.**
- DeepSeek's forecasts were calibrated, including 0.45 for the hidden 50/50 mixture.
- Asked for answers only, both models mostly failed expected-value arithmetic.
- With working shown, DeepSeek was correct in at least 95% of items and GPT-4.1-mini in 60–95%.

![Figure 1](../results/main/fig_source_models.png)
*Figure 1. Study 1: offer rates when the partner may report (blue) or an audit may detect (orange), at identical q
and F.*

### 4.2 Study 2: stated rate vs record (A1)

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
| Recency: report in episode 10 − episode 1 (pooled over list order) | −0.233 | −0.300 | −0.708 |

*Table 1. Study 2 offer rates. Bold marks the consequential format gaps. Wilson CIs are in
`results/main2/*/summary_no_offer.json`.*

**Format gap** (primary: record − stated, Holm over the two risk levels).

| Model | Low risk | High risk |
|---|---|---|
| DeepSeek | −0.033 [−0.112, +0.045], equivalent | **−0.143 [−0.220, −0.066]** |
| GPT-4.1-mini | **−0.380 [−0.444, −0.316]** | **+0.327 [+0.246, +0.407]** |
| Llama | **+0.183 [+0.115, +0.251]** | +0.013 [−0.042, +0.069], equivalent |

- Every model has a consequential gap at one or both risk levels.
- The signs disagree, so the preregistered same-sign criterion (≥ 2 of 3 models) is **not met**.
- For GPT-4.1-mini, one report in ten cut offers from 78% to 40%, while eight reports in ten left 69% offering,
  against 37% for a stated 80%.

**Stated beliefs were correct.** In separate diagnostic calls, DeepSeek's mean forecast was:
- 0.100–0.111 in the S10, R1 and R1+summary cells;
- 0.800–0.801 in the S80, R8 and R8+summary cells.

Between 95% and 100% of forecasts were within ±0.01, and 92–99% of expected-score answers were correct. Its offers
still differed by 14 points between S80 and R8. This rules out a misstated belief as the explanation. It does not
identify the computation behind the choice.

**Calibrated summary** (preregistered; difference-in-differences against the placebo):
- **GPT-4.1-mini: it worked.**
  - Low risk: +0.267 [+0.204, +0.329], closing 54% of the gap.
  - High risk: −0.250 [−0.321, −0.179], closing 99% (36.3% vs the stated 36.7%).
  - Same direction in both wordings.
- **DeepSeek, high risk: it widened the gap.** −0.117 [−0.194, −0.040], ending 21 points below the stated cell.
- **Llama, low risk: it widened the gap greatly.** Offers rose to 98.0%, against 37.0% when the same 10% was stated
  directly. The difference-in-differences was +0.583 [+0.527, +0.639].
- **At levels without a gap, it still moved behaviour.** DeepSeek low risk +0.153. Llama high risk −0.190, which
  is an over-correction by the preregistered definition.
- **Verdict:** the criterion required success in ≥ 2 of 3 models. The summary succeeded in one, so it **is not a
  working correction**.
- **No collateral harm:** authorized cooperation stayed at 99.7–100%, with 90% CIs of the change within ±0.01
  (TOST-equivalent).

**Recency (secondary).** Moving the single report from episode 1 to episode 10 cut offers in every model:

| Model | Pooled effect | Oldest-first listing | Most-recent-first listing |
|---|---|---|---|
| DeepSeek | **−0.233 [−0.291, −0.175]** | −0.21 | −0.25 |
| GPT-4.1-mini | **−0.300 [−0.345, −0.255]** | −0.23 | −0.37 |
| Llama | **−0.708 [−0.741, −0.675]** | −0.51 | −0.91 (93% → 2%) |

- B was stated to be unchanging, which makes the order of events irrelevant to the expected value.
- The effect appears when the late report is listed last as well as first, so it reflects temporal recency, not
  only position in the prompt.
- Listing most-recent-first amplified it in GPT-4.1-mini (+0.14 [+0.05, +0.23]) and Llama (+0.40), but not in
  DeepSeek (+0.04, n.s.).

![Figure 2](../results/main2/fig_s2_format.png)
*Figure 2. Study 2: offer rates under a stated rate (grey), the equivalent record (blue), the record plus a
calibrated summary (green), and the record plus a length-matched placebo (red). 95% Wilson intervals; n = 300 per
bar.*

### 4.3 Study 3b: do deterred agents write deniable proposals, and does misconduct fall with reports? (A2)

| n = 300 per cell | DeepSeek E → L | DeepSeek LOW → HIGH | Llama E → L | Llama LOW → HIGH |
|---|---|---|---|---|
| Send rate | .78 → .47 | .89 → .41 | .25 → .00 | .86 → .01 |
| ΔP (G1-live: needs ≤ −.15) | **−.32** [−.39, −.25] | **−.49** [−.55, −.42] | **−.25** [−.30, −.20] | **−.85** [−.89, −.81] |
| Report probability of drafts | .937 → .927 | .940 → .927 | .960 → .959 | .964 → .963 |
| **H3** Δr_report | −.011 [−.020, −.002] | −.014 [−.025, −.002] | −.001 [−.006, +.004] | −.001 [−.005, +.003] |
| H3 label | no deniability | no deniability | no deniability | no deniability |
| Judge q_prop | 1.00 → .98 | 1.00 → .99 | 1.00 → 1.00 | 1.00 → 1.00 |
| Reports per trial (T1) | .735 → .431 (−41%) | .841 → .379 (−55%) | .235 → 0 | .829 → .009 |
| Completed misconduct per trial (CUM) | .039 → .027 (−30%) | .042 → .022 (−47%) | .012 → 0 | .025 → .0005 |
| D (derived) | −0.18 [−0.35, −0.01] | −0.16 [−0.34, +0.03] | n/a (no L sends) | −0.48 [−0.94, −0.02], from 3 HIGH sends |

*Table 2. Study 3b. Scenario-paired 95% CIs. Drafts are scored whether or not they were sent.*

**Both cues suppressed sending strongly in both models.**

**Drafts did not become materially harder to detect.**
- All four Δr_report values lie inside the ±0.05 equivalence margin.
- In DeepSeek the drafts written under the cues were reported about one point less often. That drop is small but
  statistically detectable.
- The judge rated nearly all drafts as clear proposals. Its rating fell slightly under DeepSeek's recency cue:
  Δq_prop −0.017, 90% CI [−0.030, −0.005].
- The H3 label was unchanged on DeepSeek scenarios that sent in both cells, and under the hardened reporter.
- Llama had too few overlapping sends for the composition check.

**Reports tracked simulated misconduct in direction. The size of the fall differed in one test.**
- The reporter caught agents' drafts 93–96% of the time, against 51% of pool messages written by another model.
  Completed misconduct therefore lives in a small unreported tail.
- A one-point drop in report probability barely changes the report count. It raises that tail by about 15–20%.
- For DeepSeek's recency cue, reports fell 41% and completed misconduct 30% (D = −0.18, CI excludes 0).
- For DeepSeek's real-deterrence cue, the gap pointed the same way but was not significant.
- For Llama, sending fell to about zero, so D is not informative. Its real-deterrence D rests on 3 sends.
- Realized outcomes from the executed lotteries moved in the same direction as expected CUM in every comparison.

**The hardened reporter failed its collateral check.**
- Adding "however it is worded" to the reporter's rule changed no H3 label.
- It reported authorized coordination 97% of the time, against 0.3% for the plain reporter.

![Figure 3](../results/main3b/fig_s3b.png)
*Figure 3. Study 3b. Top: sending (grey) and operator-visible reports (blue) per trial. Bottom: expected
completed, unblocked misconduct per trial. Error bars are 95% CIs; n = 300 scenarios per bar.*

### 4.4 Pilots and gates (context for A2; evidence on A3)

**Displacement could not be tested (Study 3a).**
- In the baseline cell the admin override was chosen in 0–3% of trials. That held even at half its penalty, where
  it beat messaging on expected value.
- The recency suppressor shrank in that three-option format, to −7, −10 and −30 points. It missed its gate of
  ≥ 15 points in ≥ 2 models, so no main run was made.

**LLM verifiers did not accept collusion.**
- **The two verifier models:** Qwen3-235B and Mistral-Small-3.2 had a mean approve-without-review probability
  below 0.001 in all 2,400 pool evaluations: 400 per model under each of three prompts.
- **Giving them a stake** in the deal made them report a harmless status message 84–99% of the time.
- **A "monitor" framing** flagged that harmless message 98–99.9% of the time.

**Single-turn live partner (gate i).**
- 0 of 180 drafts were accepted:
  - DeepSeek and GPT-4.1-mini each declined 58 and reported 2;
  - Llama declined 22 and reported 38.
- In A's seat, the same models often proposed: 88–100% at low risk in Study 1, and 86–89% under the low-report
  history in Study 3b.
- B's prompt framed it as the verifier. So the refusal goes with the role and its framing; it is not specific to a
  model.

**Three rounds of conversation (gate ii).**
- **Llama:** A proposed in all 30 episodes; B refused every time.
- **DeepSeek:** A proposed in 24 of 30.
  - B agreed in words in 6 episodes, sometimes while discussing how to avoid the audit.
  - B carried the deal out in 1 of those 6, reviewed normally in 2, and reported A in 3.
  - A approved B's batch without review in all 6.
- Executed violations: 0/30 and 1/30, so the gate failed and we stopped.
- These counts are descriptive: one model playing itself, and agreement coded by reading the transcripts.
- Across both gates: 1 executed violation in 240 live-partner decisions.

## 5. Discussion

**A1 (presentation-invariance) does not hold.** Decision-equivalent changes to enforcement information moved
proposal rates by amounts comparable to changing the incentives:
- the source of exposure: up to 19 points;
- a stated rate vs an equivalent record: up to 38 points;
- the timing of one report: 23–71 points;
- a probability stated directly vs given as a summary of evidence: up to 61 points.

The directions differed by model. In separate calls DeepSeek stated the correct probabilities, so misstated beliefs
do not explain the shifts. Our data cannot identify the internal mechanism.

**Exploratory, not preregistered.** At high risk in Study 2 the penalty was 2 points, so offering gained about +8
in expectation. Yet stated-cell offer rates were only 15–54%. Together with Study 1's deterrence at zero penalty,
this is consistent with models treating the probability of being reported as a cost in itself.

**A2 (proxy validity) holds in direction in our setting.**
- Deterred agents sent fewer proposals. They did not write measurably less detectable ones for a fixed reporter.
- Because detection was near-certain, small changes in detectability have a large relative effect on completed
  misconduct. In one of two interpretable tests, reports overstated the fall in completed misconduct.
- This is not evidence of a general bias in report-based evaluations. It does suggest that, when detection is
  near-certain, the escaped tail should be estimated directly rather than inferred by scaling report counts.

**A3 (proposals are the binding step) could not be confirmed.**
- Live partners almost never carried a deal out, even when the same models eagerly proposed it.
- When a partner agreed in conversation, its words did not predict its action, which echoes "collusion on paper"
  (Nakamura et al., 2026). In half of the agreements it reported the proposer.
- In our short episodes, suppressing proposals removes little *executed* collusion, because there was almost none
  to remove.
- This may differ over long horizons, where collusion has been observed to emerge (Shi et al., 2026). We did not
  test that.

**Implications for oversight.**
1. **Report deterrence across equivalent presentations.** A model's proposal rate under "a 10% audit rate" does not
   predict its rate when the same oversight is shown as an audit log or attributed to a peer. Model rankings can
   reverse: GPT-4.1-mini and Llama moved in opposite directions at low risk.
2. **Exposed enforcement history is a high-leverage design choice.** Recent enforcement deterred strongly in every
   model, even when the enforcer was described as unchanging.
3. **Information fixes need per-model validation.** A truthful summary worked for GPT-4.1-mini and pushed Llama to
   98% initiation. Hardened reporter wording reported authorized coordination 97% of the time.
4. **Validate the proxy before relying on it.** Measure completed misconduct with a fixed outcome instrument where
   possible, and check whether the partner side of a collusive act is ever carried out.

**Evidence level.**
- Three preregistered studies; 26,820 confirmatory decisions; zero failures.
- Preregistered hypotheses:
  - Study 1's partner-vs-audit prediction was not supported.
  - Study 2's same-sign format and correction criteria were not met.
  - Study 3b's H3 was "no deniability" in 4 of 4 tests.
- The robust findings:
  - large, model-specific presentation effects while stated beliefs are correct;
  - strong recency in every model;
  - no deniability;
  - near-zero execution by live partners.
- The proxy gap D is derived, and significant in one test.
- Study 3b's outcome is simulated, with programmed acceptance and one fixed reporter.

**In plain words.**

**What we tested.** AI agents that might be reported for proposing a forbidden deal hold back. Researchers measure
this by counting proposals. We checked three things that counting assumes:
- that only the risk matters, not how it is described;
- that fewer proposals means less misconduct;
- that a proposal can actually lead to a carried-out deal.

**Study 1** kept the chance of being caught and the penalty the same, and changed only who would do the catching:
the partner, or an automated audit. We expected agents to be less wary of their partner. Instead, DeepSeek was
*more* deterred by its partner (−16 points). GPT-4.1-mini was at the floor in that test, and less deterred by its
partner in another (+19). There is no single pattern.

**Study 2** gave the same risk either as a percentage or as a short log of what the verifier had done before, built
to imply the same percentage. Consistent agents would behave the same way. They did not.
- Behaviour shifted by up to 38 points, in different directions for different models.
- A recent report scared every model far more than the same report long ago, by 23–71 points.
- A truthful one-line summary fixed the gap for one model and made another propose almost every time.

**Study 3** asked whether fewer proposals means less misconduct. A fixed AI reporter read every message the agents
wrote, and acceptance followed fixed odds.
- Showing agents recent or frequent reports cut proposing by 25–85 points.
- The messages agents wrote were about as easy to catch as before: at most a 1.4-point change.
- Misconduct fell along with proposals. In one test it fell less than the report count suggested (30% against
  41%), because the few messages that slip past the reporter matter a lot.

**Tests with a real AI partner.** When a real AI partner received the proposal, it almost never went along with it:
0 of 180 times in one round. Over three rounds of conversation it agreed in words 6 of 30 times, carried the deal
out once, and three times reported the proposer instead.

**What it means.** How oversight is described changes how agents behave, differently for each model, so deterrence
should be measured under several equivalent descriptions. Counting proposals pointed in the right direction for
misconduct in our setting. But in short interactions, real collusion between two AI agents almost never happened,
so stopping proposals prevented little executed collusion here.

**Next steps.**
- Long multi-turn interactions, where agents experience reports and where collusion is known to emerge.
- Partners whose acceptance depends on the message, and several independent reporters.
- Ways of presenting enforcement history that deter consistently across models.

## References

- Agrawal, K., Xiao, F., Bergman, G., & Cooper Stickland, A. (2025). Why do language model agents whistleblow? arXiv:2511.17085.
- Alnuhait, D., Wang, G., Khalifa, M., et al. (2026). Covert Assistance: Helpful LLM agents evade oversight in multi-agent systems. arXiv:2609.39050.
- Baker, B., et al. (2025). Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. arXiv:2503.11926.
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic collusion by large language models. arXiv:2404.00806.
- Ge, L., Zhang, Y., & Vorobeychik, Y. (2026). Mind the (DH) Gap! A contrast in risky choices between reasoning and conversational LLMs. In *Proceedings of ACL 2026 (Long Papers)*, pp. 10503–10525.
- Ge-Wang, C., Crosse, T., Hadad, B., IV, et al. (2026). Attack selection in agentic AI control evaluations meaningfully decreases safety. arXiv:2606.06529.
- Greenblatt, R., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Guerette, R. T., & Bowers, K. J. (2009). Assessing the extent of crime displacement and diffusion of benefits: A review of situational crime prevention evaluations. *Criminology*, 47(4), 1331–1368.
- Horowitz, M., & Plonsky, O. (2025). LLMs in decisions from experience. arXiv:2503.10248.
- Lee, J. Y. (2026). LLM leniency and reward experiment. SSRN 7426061.
- Nakamura, M., Kumar, A., Das, S., et al. (2026). Colosseum: Auditing collusion in cooperative multi-agent systems. arXiv:2602.15198.
- Okamoto, Erol, & Erol (2026). Why do AI agents break rules? arXiv:2608.12323 (AIES 2026).
- Paglieri, D., Cross, L., Genewein, T., Leibo, J. Z., Tomasev, N., & Vezhnevets, A. S. (2026). A case study on emergent cheating and whistleblowing in autonomous research swarms. arXiv:2609.04170.
- Scheurer, J., Balesni, M., & Hobbhahn, M. (2023). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.
- Schmotz, D., Prinzhorn, D., Beurer-Kellner, L., et al. (2026). Instrumental monitor evasion emerges under ordinary task pressure (EvasionBench). arXiv:2609.30217.
- Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models' sensitivity to spurious features in prompt design. ICLR 2024. arXiv:2310.11324.
- Shi, X., Zhang, Y., & Yang, D. (2026). Emergent collusion in long-horizon LLM agent interaction. arXiv:2609.24967.
- Zeng, X., & Rudzicz, F. (2026). Voluntary collusion with secret tools in competing LLM agents. arXiv:2605.27593.

## Appendix A. Limitations and dual-use / ethical considerations

**Single-episode settings.**
- Records are described in one prompt, not experienced.
- The only multi-turn evidence is a 30-episode gate per model, with three message rounds each.

**Programmed elements.**
- In Studies 1–2, acceptance and exposure are executed lotteries.
- In Study 3b, acceptance is programmed and does not depend on wording beyond the judge's clarity check. Covert
  wording therefore costs nothing in intelligibility.
- Study 3b's outcome is simulated misconduct, not executed collusion between autonomous agents.

**Instruments.**
- Study 3b rests on one reporter model.
- That reporter reports a harmless message 10% of the time, a declared deviation from the ≤ 5% gate.
- No second reporter passed its gates.
- The histories are real but "selected for display", and A was told so.

**Penalties.**
- F differs by model, so cross-model comparisons concern signs only.
- Several cells sat outside the 30–70% target range: Llama at high risk in Study 2; DeepSeek and Llama in
  Study 3b.

**Other.**
- Agents were told to maximize their score.
- Diagnostics are DeepSeek-only.
- Three mid-sized models, one environment.
- Gate (ii) used self-play, and its agreement coding was manual.

**Hypothesis outcomes, stated plainly.**
- Study 1's directional prediction was not supported.
- Study 2's same-sign criteria were not met.
- The proxy gap D was not preregistered as a test.

**Dual-use.**
- Knowing that presentation shifts initiation could in principle help someone make collusion more likely, for
  example by hiding recent reports.
- The effects are model-specific and environment-bound, so we judge the uplift low.
- The practical message is defensive: evaluate oversight across equivalent presentations and validate fixes per
  model.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total inference
cost was $7.77: Studies 1–2 $6.58; Study 3, instruments and gates $1.19.

## Appendix B. Validation

Unit tests (`uv run pytest`, 46 tests) and data-level validators (`results/*/*/validation.json`) cover:
- lottery rates and independence;
- exact settlement;
- byte-identical prompts across hidden types;
- each study's minimal-pair structure;
- logged prompts equal to the renderer's output;
- recovery of injected effects by the analysis code;
- the spend guard ($8, raised by the user to $9.50).

For Study 3b they also cover:
- each history outcome equals its logged draw (u < r_report);
- E and L show the same episodes;
- every draft was scored.

| Check (recorded data) | Study 1 (DS / GPT) | Study 2 (DS / GPT / Llama) | Study 3b (DS / Llama) |
|---|---|---|---|
| Valid trials | 6,120 / 5,600 | 4,200 / 4,200 / 4,200 | 1,300 / 1,200 |
| Settlement mismatches | 0 / 0 | 0 / 0 / 0 | — (settled from logged draws) |
| Logged prompt ≠ renderer | 0 / 0 | 0 / 0 / 0 | 0 / 0 |
| Provider (pinned) | Baidu / OpenAI | Baidu / OpenAI / DeepInfra | Baidu / DeepInfra |

## Appendix C. Deviations

These were agreed before the corresponding confirmatory data were collected, unless noted.

**Study 1**
- Scenarios rendered in every cell.
- Primary analysis partner vs audit.
- N = 400.
- Equivalence margin ±0.10.
- *After data collection:* a subset-assignment bug in the 40 repeat scenarios was fixed and those runs redone.

**Study 2**
- Pilot penalty grid extended.
- Llama pinned to DeepInfra.

**Study 3** (declared in `prereg_v3b.md` §5)
- Spend cap raised to $9.50 by the user.
- 3a stopped at its pilot gate.
- Acceptance programmed.
- Reporter harmless-probe rate .10 accepted by the user.
- No second reporter.
- F not interior.
- GPT excluded on G1-live.
- Reporter and judge prompts revised on probes only, before any agent-A data.

**Gates**
- Both were run after the Study 3b main analysis, with criteria committed before any call.
- Both failed and were stopped as specified.
