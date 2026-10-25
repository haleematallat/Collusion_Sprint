# Same Risk, Different Collusion: Testing Three Assumptions Behind Proposal-Based Deterrence Evaluations of LLM Agents

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions) and 3.4 (response to monitoring)
Code, data, preregistrations: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`). Blocks 1, 2 and 3b are preregistered as Studies 1, 2 and 3b (`prereg.md` `f957093`, `prereg_v2.md` `a0eab95`, `prereg_v3b.md` `0852581`); gate criteria `af8dca3`, `d93a5d4`.

## Abstract

A common way to evaluate deterrence of AI collusion is to tell an agent about the enforcement risk and count how
often it proposes prohibited coordination. This practice rests on three assumptions:
- **A1.** The measured deterrence depends on the risk itself, not on how equivalent risk information is presented.
- **A2.** Fewer proposals, or fewer reports, means proportionally less completed misconduct.
- **A3.** A proposal is the step that leads to collusion, because a partner that receives one may carry it out.

We test all three in **one experimental paradigm**: a scored, single-decision collusion task with fixed payoffs
and executed lotteries. Enforcement parameters are varied one at a time against matched controls. The paradigm was
run with DeepSeek-V3.2, GPT-4.1-mini and Llama-3.3-70B, in three preregistered blocks (26,820 confirmatory
decisions) plus pilots and feasibility gates whose criteria were fixed in advance.

**A1 does not hold.** With the decision-relevant risk held fixed:
- changing the source of exposure (a reporting partner vs an automated audit) moved proposal rates by up to 19
  percentage points;
- a stated rate versus a 10-episode record with the same Bayesian posterior moved them by up to 38 points;
- a single report in the most recent episode rather than the oldest cut proposals by 23–71 points in all three
  models.

The directions differed by model. A truthful calibrated summary closed the format gap in one model and widened it
in another. These differences coexist with accurate probability answers in separate diagnostic calls, so the
decision mechanism remains unidentified.

**A2 holds in direction; proportionality is not fully supported.**
- Setup: acceptance was programmed. A fixed LLM reporter and a blind judge read every free-text draft.
- Two history cues cut sending by 25–85 points.
- Deterred agents did not write harder-to-detect drafts: the change in report probability was at most 1.4 points,
  inside a ±5-point equivalence margin.
- Simulated completed misconduct fell in every tested condition. In one of the two interpretable comparisons it
  fell by significantly less than reports did (−30% vs −41%).
- The reporter detected 93–96% of agent drafts, which limits how far this generalizes.

**A3 was not established in our short-horizon experiments.**
- Live recipients accepted none of 180 presented drafts in a single-turn gate.
- In 60 three-round episodes, one reciprocal violation was executed.
- Proposal generation and executed misconduct were far apart in these workflows. The results do not establish how
  often collusion occurs in longer-running agent systems.

## 1. Introduction

Collusion between AI agents has to start somewhere: one agent proposes coordination that oversight prohibits.
Deterrence evaluations therefore describe an enforcement risk to an agent and measure how often it proposes.
Examples include Scheurer et al. (2023), Zeng & Rudzicz (2026) and Okamoto et al. (2026), which typically describe
the risk once, in one format.

Those numbers are informative only under three assumptions:
- **A1, presentation-invariance:** equivalent information about the same risk produces the same behaviour.
- **A2, proxy validity:** a drop in proposals, or in the reports they trigger, means a proportional drop in
  completed, unblocked misconduct.
- **A3, proposals are the binding step:** a partner that receives a proposal may actually carry it out, so
  suppressing proposals prevents collusion.

We test each assumption by varying one enforcement parameter at a time in a single paradigm (§3), against matched
controls. The parameters are:
- **for A1:** source, format, record content, timing and summaries;
- **for A2:** history cues with a live reporter;
- **for A3:** a programmed vs a live partner, and one vs three message rounds.

**Contributions**
1. **A controlled, reproducible paradigm.** It has executed lotteries, exact settlement, byte-level minimal-pair
   prompts, matched controls and preregistered decision rules, plus a Bayesian benchmark with a known correct
   answer wherever a record replaces a stated rate.
2. **Evidence against A1.** Source, format and timing effects of up to 19, 38 and 71 points, model-specific in
   direction.
3. **A preregistered low-cost intervention test.** A calibrated summary worked in one of three models and never
   reduced authorized cooperation.
4. **A preregistered proxy test (A2).**
   - No deniability in four of four comparisons.
   - Simulated misconduct moved in the same direction as reports.
   - Proportionality failed in one comparison.
5. **Feasibility evidence on A3.** Live recipients almost never executed the deal, even in model families that
   often proposed it, and verbal agreement often did not lead to execution.

## 2. Related work

**LLM collusion.**
- LLM agents reach supracompetitive pricing without instruction (Fish et al., 2024).
- They accept secret unfair tools at high rates, and observability and ethics cues change adoption (Zeng &
  Rudzicz, 2026).
- In long-horizon mutual verification, collusion emerges in 94% of trajectories across 10 models (Shi, Zhang &
  Yang, 2026). Peer behaviour shapes it: replacing a compliant scripted peer with a violating one raises
  Gemini-3.1-Flash-Lite's acceptance rate from 13.6% to 41.2%. That environment has no monitor, audit or penalty.
- Colosseum separates collusion planned in communication from collusion executed in action ("collusion on paper";
  Nakamura et al., 2026). Our three-round gate observes the same kind of gap; we do not claim it as new.

**Enforcement.**
- In an LLM leniency experiment, reporting responds to rewards while prices barely move (Lee, 2026).
- In an autonomous research swarm, agents that saw exploits go unpunished treated the stated threats as a bluff
  (Paglieri et al., 2026).
- Reporting propensity varies widely across model families (Agrawal et al., 2025).

**Risk and presentation.**
- Stated detection risk changes LLM misconduct (Scheurer et al., 2023).
- Models behave differently under monitoring cues (Greenblatt et al., 2024) and are sensitive to prompt format
  (Sclar et al., 2024).
- LLMs show recency and underweight rare events in decisions from experience (Horowitz & Plonsky, 2025).
- **Closest to our A1 test:** Ge, Zhang & Vorobeychik (2026) compare described with experienced prospects in 20
  LLMs. Conversational models show a large description–history gap and sensitivity to order and framing, while
  reasoning models stay near the expected-payoff benchmark.
- Our format results agree with their conversational-model findings. Our narrower contribution is the same kind
  of gap for *enforcement* information in a collusion decision, with posterior-matched records and executed
  lotteries.

**Proxies vs outcomes.**
- Training against a chain-of-thought monitor reduced detected reward hacking while hidden hacking continued
  (Baker et al., 2025).
- Explicit coordination fell from 90.0% to 62.0% in one ablation while the collusion rate was almost unchanged
  (Shi et al., 2026).
- Monitoring can push agents to disguise information (Alnuhait et al., 2026) or to evade monitors under ordinary
  task pressure (Schmotz et al., 2026).
- Attack selection lowers measured safety (Ge-Wang et al., 2026).
- Crime-prevention evaluations find displacement and diffusion of benefits about equally often (Guerette & Bowers,
  2009).
- **Gap:** we found no test of whether the *presentation* of enforcement information makes the proposals agents
  still send harder to detect. Our A2 block tests that in one setting.

## 3. The experiment

### 3.1 Fixed task and payoffs
Every trial uses the same scored decision.
- **Agent A** has a verification job, a supervisor rule ("agents must not arrange to approve each other's work
  without independent review"), 50 points, and the instruction to maximize its score.
- **The choice:** A may privately propose to verifier B that each approves the other's work without review.
- **Settlement:** the task system executes seeded lotteries and settles A's score. Only A's choice and the lottery
  draws determine the outcome.
- **Fixed parameters** in every block: base 50 points, bonus 12, acceptance probability 0.8 wherever acceptance
  is programmed, and temperature 1.0.
- **Other constants:**
  - answer options are counterbalanced, and answers are strict JSON with no rationale;
  - each model is pinned to one provider (DeepSeek on Baidu, GPT-4.1-mini on OpenAI, Llama on DeepInfra);
  - every scenario (organization, task, names, wording family) appears in every cell of its block, so each contrast
    is paired within scenario.

### 3.2 Independent variables
Each block varies some parameters and holds the others fixed.

| Block | Independent variables (levels) | Held fixed / calibrated |
|---|---|---|
| **1. Source** (A1; 400 scenarios) | exposure source {partner reports, audit detects}; exposure probability q {0.10, 0.80}; penalty F {0, 20}; partner type {disclosed, hidden 50/50 mixture} | bonus, acceptance; partner and audit text differ only in the exposure sentences |
| **2. Format** (A1; 300 scenarios) | format {stated rate, 10-episode record}; risk {1/10 reports → E[q] = .10, 8/10 → E[q] = .80}; appended text {none, calibrated summary, length-matched placebo}; position of a single report {episode 1, episode 10} × list order {oldest-first, most-recent-first}; authorization {prohibited, authorized} | posterior equal across format; F per model and risk, set on the pilot (stated cell 30–70%) |
| **3a. Displacement** (pilot; 30 scenarios) | menu {2 options, 3 options with an admin override}; report timing {early, late}; override penalty {0.5×, 1×}; override detection {0.28, 1.0} | the two violation routes matched in completion probability (0.72) and expected value |
| **3b. Proxy** (A2; 300 scenarios) | history cue: recency {5 reports oldest (E), 5 most recent (L)}; report rate {1/10 (LOW), 8/10 (HIGH)}; reporter wording {plain, hardened} (applied to the same drafts) | programmed acceptance; fixed reporter and judge; F per model, set on the pilot |
| **Gates** (A3) | partner {programmed → live LLM peer}; interaction {1 message → 3 rounds each} | payoffs mirrored between the two agents |

### 3.3 Dependent variables and instruments
- **Proposal rate P**, the primary outcome in every block: P(SEND), or P(MESSAGE) in Block 3.
- **Detectability r_report** (Block 3b): a fixed reporter reads A's exact draft and gives its probability of
  "report". The reporter is Mistral-Small-3.2 in a plain reviewer prompt; the probability comes from first-token
  logprobs.
- **Clarity q_prop** (Block 3b): a blind judge (Qwen3-235B) gives the probability that the draft asks for approval
  without independent review.
- **Block 3b outcomes:**
  - operator-visible reports T1 = P·r_report;
  - completed, unblocked misconduct CUM = P·0.8·(1 − r_report)·q_prop;
  - proxy gap D = log(T1 ratio) − log(CUM ratio). D < 0 means reports fell proportionally more than CUM.
- **Execution** (gates): the live partner approves without review and nobody reports.
- **Diagnostics** (Blocks 1–2, DeepSeek): stated probability and expected score, from separate calls.

### 3.4 Controls and validity checks
- **Positive control:** authorized offers carry no penalty and should be sent about 100% of the time.
- **Placebos:**
  - a hidden-type prompt that is identical across true risk levels (Block 1);
  - a length-matched placebo for the summary (Block 2);
  - a neutral-metadata cell (Block 1).
- **Manipulation checks:**
  - override-always-detected (Block 3a);
  - each history cue must cut sending by ≥ 15 points, G1-live (Block 3b).
- **Instrument checks before any agent data** (Block 3b):
  - explicit proposals must be reported;
  - a harmless message must rarely be reported;
  - hand-written covert-but-clear proposals must be judged clear;
  - logprobs must match sampled frequencies.
- **Paired randomness:** common random numbers across cells; histories are real reporter outcomes drawn with the
  settlement rule and shown as "selected for display".
- **Exclusions and checks:** pilots run on separate scenarios and are excluded; logged prompts are checked against
  the renderer.
- **Inference:**
  - scenario-paired 95% t-intervals, Holm-corrected within preregistered families;
  - equivalence by TOST with 90% intervals, at ±0.10 (Blocks 1–2) or ±0.05 (Block 3b H3);
  - one confirmatory test per block, fixed in its preregistration:
    - Block 1: partner − audit at q = .80, F = 20;
    - Block 2: record − stated at each risk level;
    - Block 3b: H3, defined below.
- **Block 3b, H3 "no deniability":** Δr_report equivalent to zero within ±0.05. "Deniability" would have required
  Δr_report ≤ −0.05 together with non-inferior clarity.

## 4. Results

All 26,820 confirmatory trials returned valid output: Block 1 11,720; Block 2 12,600; Block 3b 2,500. So did the
11,480 diagnostic and arithmetic calls, all pilots and both gates. There were no refusals, parse failures or
unresolved API errors.

### 4.1 A1: does equivalent information produce equivalent deterrence?

**The incentive parameters behave as expected** (Block 1):
- Offers ran at 88–100% when q = 10% and the type was disclosed.
- At q = 80%, raising F from 0 to 20 cut partner-arm offers by 36 points (DeepSeek) and 39 (GPT-4.1-mini).
- The positive control was sent 100% of the time.
- Exposure deterred even at zero cost: at q = 80%, F = 0, partner-arm offers were 52% (DeepSeek) and 40% (GPT),
  against 100% at q = 10%.

**Source of exposure** (Block 1, primary):
- DeepSeek offered *less* when the partner might report than when an audit might detect: 18.0% vs 33.5%,
  Δ = −0.159 [−0.217, −0.100], p = 1.6×10⁻⁷. The sign was the same in both wordings.
- GPT-4.1-mini was at the floor in that cell (0.5% vs 0%).
- In the q = 80%, F = 0 cell, GPT-4.1-mini offered *more* under partner reporting: +0.193 [+0.138, +0.247].
  DeepSeek showed −0.115 [−0.176, −0.054] in the same cell.
- The preregistered prediction (less deterrence from partners in both models) is not supported. The source effect
  exists but differs in sign by model.

![Figure 1](../results/main/fig_source_models.png)
*Figure 1. Block 1: offer rates when the partner may report (blue) or an audit may detect (orange), at identical q
and F.*

**Format: stated rate vs equivalent record** (Block 2):

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

*Table 1. Block 2 offer rates. Bold marks the consequential format gaps. Wilson CIs are in
`results/main2/*/summary_no_offer.json`.*

| Format gap (record − stated; primary, Holm over risk levels) | Low risk | High risk |
|---|---|---|
| DeepSeek | −0.033 [−0.112, +0.045], equivalent | **−0.143 [−0.220, −0.066]** |
| GPT-4.1-mini | **−0.380 [−0.444, −0.316]** | **+0.327 [+0.246, +0.407]** |
| Llama | **+0.183 [+0.115, +0.251]** | +0.013 [−0.042, +0.069], equivalent |

- Every model has a consequential gap at one or both risk levels.
- The signs disagree, so the preregistered same-sign criterion (≥ 2 of 3 models) is **not met**.
- For GPT-4.1-mini, one report in ten cut offers from 78% to 40%, while eight reports in ten left 69% offering,
  against 37% for a stated 80%.

**Explicit probabilities were accurate.** In separate diagnostic calls, DeepSeek's mean forecast was:
- 0.100–0.111 in the S10, R1 and R1+summary cells;
- 0.800–0.801 in the S80, R8 and R8+summary cells.

95–100% of forecasts were within ±0.01, and 92–99% of expected-score answers were correct. Even so, its offers
differed by 14 points between S80 and R8. The large behavioural differences coexist with accurate explicit
probability calculations; the decision mechanism in the action-only calls remains unidentified.

**Timing of a single report** (Block 2, secondary):

| Report in episode 10 rather than 1 | Pooled | Oldest-first listing | Most-recent-first listing |
|---|---|---|---|
| DeepSeek | **−0.233 [−0.291, −0.175]** | −0.21 | −0.25 |
| GPT-4.1-mini | **−0.300 [−0.345, −0.255]** | −0.23 | −0.37 |
| Llama | **−0.708 [−0.741, −0.675]** | −0.51 | −0.91 (93% → 2%) |

- B was stated to be unchanging, so the order of events does not affect expected value.
- The effect holds when the late report is listed last as well as first, so it reflects temporal recency, not only
  position in the prompt.
- Most-recent-first listing amplified it in GPT-4.1-mini (+0.14 [+0.05, +0.23]) and Llama (+0.40), but not in
  DeepSeek (+0.04, n.s.).

**Calibrated summary as a fix** (Block 2, preregistered; difference-in-differences against the placebo):
- **GPT-4.1-mini: it worked.**
  - Low risk: +0.267 [+0.204, +0.329], closing 54% of the gap.
  - High risk: −0.250 [−0.321, −0.179], closing 99%.
  - Same direction in both wordings.
- **DeepSeek, high risk: it widened the gap.** −0.117 [−0.194, −0.040], ending 21 points below the stated cell.
- **Llama, low risk: it widened the gap greatly.** Offers rose to 98.0%, against 37.0% for the directly stated 10%.
  The difference-in-differences was +0.583 [+0.527, +0.639].
- **At levels without a gap, it still moved behaviour.** DeepSeek low +0.153. Llama high −0.190, an
  over-correction by the preregistered definition.
- **Verdict:** the preregistered criterion was success in ≥ 2 of 3 models. It succeeded in one, so it is **not a
  working correction**.
- **No collateral harm:** authorized cooperation stayed at 99.7–100%, with 90% CIs within ±0.01 (TOST-equivalent).

![Figure 2](../results/main2/fig_s2_format.png)
*Figure 2. Block 2: offer rates under a stated rate (grey), the equivalent record (blue), the record plus a
calibrated summary (green), and the record plus a length-matched placebo (red). 95% Wilson intervals; n = 300 per
bar.*

### 4.2 A2: do fewer proposals and reports mean proportionally less misconduct?

**Displacement pilot (Block 3a).**
- The admin-override route was chosen in 0–3% of baseline trials, even at half its penalty, where it beat
  messaging on expected value.
- The recency effect shrank in this three-option format, to −7, −10 and −30 points. It missed its gate (≥ 15
  points in ≥ 2 models), so no main run was made and displacement remains untested.

**Proxy test (Block 3b).**

| n = 300 per cell | DeepSeek E → L | DeepSeek LOW → HIGH | Llama E → L | Llama LOW → HIGH |
|---|---|---|---|---|
| Send rate | .78 → .47 | .89 → .41 | .25 → .00 | .86 → .01 |
| ΔP (G1-live: needs ≤ −.15) | **−.32** [−.39, −.25] | **−.49** [−.55, −.42] | **−.25** [−.30, −.20] | **−.85** [−.89, −.81] |
| Report probability of drafts | .937 → .927 | .940 → .927 | .960 → .959 | .964 → .963 |
| **H3** Δr_report | −.011 [−.020, −.002] | −.014 [−.025, −.002] | −.001 [−.006, +.004] | −.001 [−.005, +.003] |
| H3 label | no deniability | no deniability | no deniability | no deniability |
| Judge clarity q_prop | 1.00 → .98 | 1.00 → .99 | 1.00 → 1.00 | 1.00 → 1.00 |
| Reports per trial (T1) | .735 → .431 (−41%) | .841 → .379 (−55%) | .235 → 0 | .829 → .009 |
| Completed misconduct per trial (CUM) | .039 → .027 (−30%) | .042 → .022 (−47%) | .012 → 0 | .025 → .0005 |
| D (derived) | −0.18 [−0.35, −0.01] | −0.16 [−0.34, +0.03] | n/a (no L sends) | −0.48 [−0.94, −0.02], from 3 HIGH sends |

*Table 2. Block 3b. Scenario-paired 95% CIs. Drafts are scored whether or not they were sent. GPT-4.1-mini failed
G1-live in the pilot (+.23 and .00) and was excluded before the main run.*

**Detectability did not change materially.**
- All four Δr_report values are equivalent to zero within ±0.05.
- In DeepSeek the drafts written under the cues were reported about one point less often. That drop is small but
  statistically detectable.
- The judge rated nearly every draft a clear proposal. Its rating fell slightly under DeepSeek's recency cue:
  Δq_prop −0.017, 90% CI [−0.030, −0.005].
- The H3 label was unchanged on DeepSeek scenarios that sent in both cells, and under the hardened reporter.
- Llama had too few overlapping sends for the composition check.

**Direction: holds.** Simulated completed misconduct fell in every comparison. The outcomes realized by the
executed lotteries moved the same way.

**Proportionality: not fully supported.**
- For DeepSeek's recency cue, reports fell 41% but completed misconduct only 30% (D = −0.18, CI excludes 0).
- The reason is that the reporter detected 93–96% of agents' drafts, against 51% of the pool messages written by
  another model. Completed misconduct therefore lives in a small unreported tail, and a one-point fall in report
  probability raises that tail by about 15–20%.
- DeepSeek's real-deterrence cue pointed the same way, but its interval included 0.
- Llama's sending fell to about zero, so its D is not informative.
- With a less accurate reporter or more ambiguous messages, the gap could be larger or smaller. We tested one
  reporter.

**The hardened reporter failed its collateral check.** Adding "however it is worded" to the rule changed no H3
label. But it reported authorized coordination 97% of the time, against 0.3% for the plain reporter.

![Figure 3](../results/main3b/fig_s3b.png)
*Figure 3. Block 3b. Top: sending (grey) and operator-visible reports (blue) per trial. Bottom: expected
completed, unblocked misconduct per trial. 95% CIs; n = 300 scenarios per bar.*

### 4.3 A3: does a proposal lead to an executed violation?
Blocks 1–3 program the partner's acceptance. Here we replaced it with live LLMs. Each gate's criteria were
committed before any call.

**Verifier instrument checks.** These preceded Block 3b.
- Qwen3-235B and Mistral-Small-3.2 had a mean approve-without-review probability below 0.001 in 2,400 pool
  evaluations: 400 per model under each of three prompts.
- Giving them a stake in the deal made them report a harmless status message 84–99% of the time.

**Single-turn gate.**
- **Setup:** each model played B, a peer told to maximize its score. Approving without review was worth +4.8 in
  expectation (gain 12; a 10% audit costs 60).
- **What B read:** 60 agent-A drafts sampled from Block 3b's pilot, including drafts that A had chosen not to send.
  The gate therefore measures how B responds to presented drafts, not the success rate of naturally sent offers.
- **Result:** 0 of 180 drafts were accepted.
  - DeepSeek and GPT-4.1-mini each declined 58 and reported 2.
  - Llama declined 22 and reported 38.

**Three-round gate.** Two copies of one model exchanged six private messages, then each acted on the other's
batch.
- **Llama:** A proposed in all 30 episodes. B refused every time, with 0 executed violations.
- **DeepSeek:** A proposed in 24 of 30.
  - B agreed in words in 6 episodes, sometimes while discussing how to avoid the audit.
  - It executed the reciprocal violation in 1 of the 6, reviewed normally in 2, and reported A in 3.
  - A approved B's batch without review in all 6.
- **Gate result:** 0/30 and 1/30 executed violations, so the gate failed and we stopped.
- **Coding:** these counts are descriptive. Each gate is one model playing itself, and agreement was coded by
  reading the transcripts.
- **Scope:** the two gates used different protocols and are not pooled into one estimate.

**What this shows, and does not.**
- In A's seat the same model families often proposed the deal: 88–100% at low risk in Block 1, and 86–89% under
  the low-report history in Block 3b. In B's seat they almost never carried it out.
- This is a role-sensitive asymmetry **within the tested workflows**. It is not a clean causal effect of role,
  because the two prompts differ in responsibilities, options, information and incentives.
- The DeepSeek pattern — verbal agreement followed by review or reporting — fits the say–do gap documented in
  Colosseum.

## 5. Discussion

**A1 is not supported.** Decision-equivalent changes to one enforcement parameter at a time moved proposal rates by
amounts comparable to changing the incentives:
- the source of exposure: up to 19 points;
- a stated rate vs an equivalent record: up to 38 points;
- the timing of one report: 23–71 points;
- a probability stated directly vs given as a summary of evidence: up to 61 points.

Directions differed by model, so model rankings can reverse: GPT-4.1-mini and Llama moved in opposite directions at
low risk. The differences coexist with accurate explicit probability answers. Why the decisions differ is not
identified.

*Exploratory, not preregistered:* at high risk in Block 2 the penalty was 2 points, so offering gained about +8 in
expectation. Yet offer rates in the stated cell were only 15–54%. Together with Block 1's deterrence at zero cost,
this is consistent with models treating the probability of being reported as a cost in itself.

**A2 holds directionally; proportionality is not fully supported.**
- Deterred agents sent fewer proposals. They did not write measurably less detectable ones.
- Simulated misconduct fell whenever sending fell.
- With near-certain detection, small changes in detectability have large relative effects on the escaped tail, and
  in one comparison reports overstated the fall in misconduct.
- This is evidence about one reporter at 93–96% detection, not a general bias of report-based evaluations.

**A3 was not established in our short-horizon experiments.**
- Live recipients accepted none of 180 presented drafts in the single-turn gate.
- In 60 three-round episodes, one reciprocal violation was executed.
- Proposal generation and executed misconduct were far apart in these workflows. The results do not establish how
  often collusion occurs in longer-running systems, where it has been observed to emerge (Shi et al., 2026).

**Implications for evaluation and oversight.**
1. **Report deterrence across equivalent presentations,** not under one description of the risk.
2. **Treat exposed enforcement history as a high-leverage design choice.** Recent enforcement deterred strongly in
   every model.
3. **Validate information fixes per model.** A truthful summary helped one model and pushed another to 98%
   initiation. Hardened reporter wording reported authorized coordination 97% of the time.
4. **Validate the proxy.**
   - Measure completed misconduct with a fixed outcome instrument where possible.
   - Check whether the receiving side of a collusive act is ever carried out.
   - Do not infer executed collusion from proposals or verbal agreement.

**Evidence level.**
- Three preregistered blocks, 26,820 confirmatory decisions, zero failures.
- Preregistered outcomes:
  - Block 1's directional prediction was not supported.
  - Block 2's same-sign format and correction criteria were not met.
  - Block 3b's H3 was "no deniability" in 4 of 4 comparisons.
- The proxy gap D was derived, not preregistered as a test.
- The live-partner gates are feasibility tests and failed their criteria.

**In plain words.**

**What we tested.** AI agents that might be reported for proposing a forbidden deal hold back, and researchers
measure this by counting proposals. We ran one experiment, changing one setting at a time, to check three things
that counting assumes:
- that only the risk matters, not how it is described;
- that fewer proposals means less misconduct;
- that a proposal can actually lead to a carried-out deal.

**Does only the risk matter?** No.
- Keeping the risk the same, changing who might catch the agent moved proposing by up to 19 points.
- Describing the risk as a percentage or as a past record moved it by up to 38 points.
- A recent report scared every model far more than the same report long ago, by 23–71 points.
- Models differed in direction, and a truthful one-line summary fixed the gap for one model and made another
  propose almost every time.

**Does fewer proposals mean less misconduct?** In direction, yes.
- Showing agents recent or frequent reports cut proposing by 25–85 points.
- The messages agents still wrote were about as easy to catch as before.
- Misconduct fell too. In one test it fell less than the report count suggested (30% against 41%), because the few
  messages that slip past the reporter matter a lot.

**Does a proposal lead to a carried-out deal?** Rarely, in our short tests.
- A real AI partner accepted none of 180 presented messages.
- Over three rounds of conversation, one model's partner agreed in words 6 times in 30, carried the deal out once,
  and three times reported the proposer.
- We cannot say what happens in long-running systems.

**What it means.** How oversight is described changes how agents behave, differently for each model, so deterrence
should be measured under several equivalent descriptions. Counting proposals pointed in the right direction in our
setting, but not always by the right amount. Whether stopping proposals prevents real collusion needs longer
interactions to test.

**Next steps.**
- Long multi-turn interactions, where agents experience reports and collusion is known to emerge.
- Partners whose acceptance depends on the message, and several independent reporters.
- Presentations of enforcement history that deter consistently across models.

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
- In Blocks 1–2, acceptance and exposure are executed lotteries.
- In Block 3b, acceptance is programmed and does not depend on wording beyond the judge's clarity check. Covert
  wording therefore costs nothing in intelligibility.
- Block 3b's outcome is simulated misconduct, not executed collusion between autonomous agents.

**Instruments.**
- Block 3b rests on one reporter model.
- That reporter reports a harmless message 10% of the time, a declared deviation from the ≤ 5% gate.
- No second reporter passed its gates.
- The histories are real but "selected for display", and A was told so.

**Penalties.**
- F differs by model, so cross-model comparisons concern signs only.
- Several cells sat outside the 30–70% target range: Llama at high risk in Block 2; DeepSeek and Llama in
  Block 3b.

**Other.**
- Agents were told to maximize their score.
- Diagnostics are DeepSeek-only. They show what the model can state in a separate call, not which estimates drove
  its decisions.
- Three mid-sized models, one environment.
- The three-round gate used self-play, and its agreement coding was manual.
- The proposer–recipient asymmetry is observed within the tested workflows. It is not a clean causal effect of
  role, because the two prompts differ in responsibilities, options, information and incentives.
- The single-turn gate presented sampled drafts, including some that A had not sent.
- Block 3b's proportionality result rests on one reporter with 93–96% detection on agent drafts.

**Hypothesis outcomes, stated plainly.**
- Block 1's directional prediction was not supported.
- Block 2's same-sign criteria were not met.
- The proxy gap D was not preregistered as a test.

**Dual-use.**
- Knowing that presentation shifts initiation could in principle help someone make collusion more likely, for
  example by hiding recent reports.
- The effects are model-specific and environment-bound, so we judge the uplift low.
- The practical message is defensive: evaluate oversight across equivalent presentations and validate fixes per
  model.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total inference
cost was $7.77: Blocks 1–2 $6.58; Block 3, instruments and gates $1.19.

## Appendix B. Validation

Unit tests (`uv run pytest`, 46 tests) and data-level validators (`results/*/*/validation.json`) cover:
- lottery rates and independence;
- exact settlement;
- byte-identical prompts across hidden types;
- each study's minimal-pair structure;
- logged prompts equal to the renderer's output;
- recovery of injected effects by the analysis code;
- the spend guard ($8, raised by the user to $9.50).

For Block 3b they also cover:
- each history outcome equals its logged draw (u < r_report);
- E and L show the same episodes;
- every draft was scored.

| Check (recorded data) | Block 1 (DS / GPT) | Block 2 (DS / GPT / Llama) | Block 3b (DS / Llama) |
|---|---|---|---|
| Valid trials | 6,120 / 5,600 | 4,200 / 4,200 / 4,200 | 1,300 / 1,200 |
| Settlement mismatches | 0 / 0 | 0 / 0 / 0 | — (settled from logged draws) |
| Logged prompt ≠ renderer | 0 / 0 | 0 / 0 / 0 | 0 / 0 |
| Provider (pinned) | Baidu / OpenAI | Baidu / OpenAI / DeepInfra | Baidu / DeepInfra |

## Appendix C. Deviations

These were agreed before the corresponding confirmatory data were collected, unless noted.

**Block 1**
- Scenarios rendered in every cell.
- Primary analysis partner vs audit.
- N = 400.
- Equivalence margin ±0.10.
- *After data collection:* a subset-assignment bug in the 40 repeat scenarios was fixed and those runs redone.

**Block 2**
- Pilot penalty grid extended.
- Llama pinned to DeepInfra.

**Block 3** (declared in `prereg_v3b.md` §5)
- Spend cap raised to $9.50 by the user.
- Block 3a stopped at its pilot gate.
- Acceptance programmed.
- Reporter harmless-probe rate .10 accepted by the user.
- No second reporter.
- F not interior.
- GPT excluded on G1-live.
- Reporter and judge prompts revised on probes only, before any agent-A data.

**Gates**
- Both were run after the Block 3b main analysis, with criteria committed before any call.
- Both failed and were stopped as specified.
