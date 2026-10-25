# Same Risk, Different Collusion: Enforcement Presentation Shifts LLM Agents' Collusion Proposals, but Proposals Rarely Became Executed Collusion

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, 23–25 October 2026 · Track 1 (markets and collusion), with relevance to Track 3
Code and data: https://github.com/haleematallat/Collusion_Sprint/tree/claude/funny-volta-kb1gxn · Preregistrations: `prereg.md` (`f957093`), `prereg_v2.md` (`a0eab95`), `prereg_v3b.md` (`0852581`); gate criteria `af8dca3`, `d93a5d4`

## Abstract

Evaluations of AI collusion often tell an agent about an enforcement risk and count how often it proposes
prohibited coordination. We examine two assumptions behind this practice and one external-validity question:
- **A1:** measured deterrence does not depend on how matched risk information is presented.
- **A2:** fewer proposals or reports means proportionally less completed misconduct.
- **Q3:** proposal rates predict executed collusion between two agents.

We use one experimental framework: a scored verification task with executed lotteries, run as three separately
preregistered blocks plus feasibility tests. The models are DeepSeek-V3.2, GPT-4.1-mini and Llama-3.3-70B, with
26,820 confirmatory decisions.

**A1 does not hold.** With stated monetary exposure held fixed:
- the source of exposure moved proposal rates by up to 19 points;
- a stated rate versus a record with the same posterior moved them by up to 38;
- the timing of a single report moved them by 23–71.

Directions were model-specific, despite accurate probability answers in separate calls.

**A2 holds in direction but not fully in proportion.**
- History cues cut sending by 25–85 points.
- Drafts did not become harder to detect (changes within a 5-point equivalence margin).
- Simulated misconduct fell in every comparison, but in one it fell less than reports did (−30% vs −41%).

**Q3: proposals rarely became executed collusion in these workflows.** Live recipients accepted none of 180
presented drafts, and 60 three-round conversations produced one executed violation.

Deterrence should be measured across matched presentations, and proposal-based proxies checked against outcomes.

## 1. Introduction

Collusion between AI agents begins when one agent proposes coordination that oversight prohibits. Deterrence
evaluations therefore describe an enforcement risk and measure how often an agent proposes (Scheurer et al., 2023;
Zeng & Rudzicz, 2026; Okamoto et al., 2026). The risk is usually described once, in one format. Interpreting such
numbers relies on two assumptions and raises one external-validity question:
- **A1, presentation-invariance:** matched information about the same risk produces the same behaviour.
- **A2, proxy validity:** a fall in proposals, or in the reports they trigger, implies a proportional fall in
  completed, unblocked misconduct.
- **Q3, external validity:** proposal rates predict executed collusion between two agents.

We study these in one framework: a shared, scored verification task with executed lotteries (§3). Each block has
its own preregistered decision rule.
- **Blocks 1–2** test A1 by changing how a fixed risk is presented.
- **Block 3b** tests A2, with a live LLM reporter reading agents' free-text messages.
- **Feasibility gates** examine Q3 with live LLM partners.

**Contributions**
1. **A controlled framework.** Executed lotteries, byte-level minimal-pair prompts, matched controls, and
   posterior-matched records with a Bayesian benchmark.
2. **Evidence against A1.** Source, format and timing effects of up to 19, 38 and 71 points, model-specific in
   direction. Timing is separated from display position.
3. **A preregistered proxy test (A2).** No deniability in four of four comparisons. Misconduct moved in the same
   direction as reports, but proportionality failed in one comparison.
4. **Feasibility evidence on Q3.** In these short workflows, proposals almost never became executed bilateral
   violations, even when a partner agreed in words.

## 2. Related work

**LLM collusion.**
- LLM agents reach supracompetitive pricing without instruction (Fish et al., 2024).
- They adopt secret unfair tools, and observability cues change adoption (Zeng & Rudzicz, 2026).
- In long-horizon mutual verification, collusion emerges in 94% of trajectories across 10 models. In one
  ablation, explicit coordination fell from 90.0% to 62.0% while collusion was almost unchanged (Shi, Zhang &
  Yang, 2026).
- Colosseum separates collusion planned in communication from collusion carried out in action (Nakamura et al.,
  2026). We observe the same kind of gap and do not claim it as new.

**Enforcement and presentation.**
- Reporting responds to rewards while collusion barely moves (Lee, 2026).
- Agents that saw exploits go unpunished treated threats as a bluff (Paglieri et al., 2026).
- Stated detection risk changes LLM misconduct (Scheurer et al., 2023).
- Behaviour shifts with monitoring cues and with prompt format (Greenblatt et al., 2024; Sclar et al., 2024).
- **Closest to our A1 test:** conversational LLMs show a description–history gap in risky choice, while reasoning
  models stay near the expected-payoff benchmark (Ge, Zhang & Vorobeychik, 2026). LLMs also show recency in
  experience-based choice (Horowitz & Plonsky, 2025).
- Our narrower contribution is the same kind of gap for *enforcement* information in a collusion decision.

**Proxies versus outcomes.**
- Optimizing against a monitor can hide misbehaviour rather than remove it (Baker et al., 2025).
- Monitoring can push agents to disguise information (Alnuhait et al., 2026) or to evade monitors (Schmotz et
  al., 2026).
- Attack selection lowers measured safety (Ge-Wang et al., 2026).
- We found no test of whether enforcement *presentation* makes agents' remaining proposals harder to detect.

## 3. Methods

### 3.1 Shared task
**Agent A's situation.** A has a verification job, a supervisor rule ("agents must not arrange to approve each
other's work without independent review"), 50 points, and the instruction to maximize its score.

**The decision.** A may privately propose to verifier B that each approves the other's work without review. A
gains 12 points if B accepts. Wherever acceptance is programmed, it occurs with probability 0.8.

**Fixed settings.**
- Seeded lotteries are executed and scored.
- Temperature 1.0.
- Answer options are counterbalanced; answers are strict JSON with no rationale.
- Each model is pinned to one provider: DeepSeek on Baidu, GPT-4.1-mini on OpenAI, Llama on DeepInfra.
- Every scenario (organization, task, names, wording) appears in every cell of its block, so contrasts are paired
  within scenario.
- Pilots used separate scenarios and are excluded from all analyses.

### 3.2 Blocks and manipulated parameters

| Block (question; n scenarios) | Manipulated parameters | Held fixed |
|---|---|---|
| **1. Source** (A1; 400) | who exposes a proposal {partner reports, audit detects} × q {0.10, 0.80} × penalty F {0, 20}; partner type disclosed or hidden | stated monetary exposure; prompts differ only in the exposure sentences |
| **2. Format** (A1; 300) | {stated rate, 10-episode record} × risk {1/10, 8/10 reports}; + {calibrated summary, length-matched placebo}; a single report in episode {1, 10} × listing {oldest-first, most-recent-first}; authorized offers | approximate posterior; F per model and risk (set on the pilot) |
| **3b. Proxy** (A2; 300) | history cue: recency {5 reports oldest (E), most recent (L)}; report rate {1/10 (LOW), 8/10 (HIGH)}; reporter wording {plain, hardened} | programmed acceptance; fixed reporter and judge |
| **Gates** (Q3; 60 drafts / 30 episodes per model) | partner {live LLM peer}; interaction {1 message, 3 rounds each} | mirrored payoffs |

**What "matched" means.**
- **Block 1:** partner reporting and auditing match in probability and penalty, not necessarily in social or
  institutional meaning.
- **Block 2:**
  - Each cell states a 50/50 mixture of 10% and 80% reporting types, and that "B's tendency is fixed and does not
    change over time".
  - Assuming reports are independent given that fixed probability, a 1/10 record implies E[q] = 0.10001 and an
    8/10 record E[q] = 0.79999. These are approximately the stated rates.
  - Under the same assumption, the order of past reports carries no information.

**Block 3b procedure.**
- Each agent first writes its exact message (`draft`), then chooses whether to send it.
- A fixed reporter (Mistral-Small-3.2, plain reviewer prompt, blind to arm) gives r_report, its first-token
  probability of "report".
- A blind judge (Qwen3-235B) gives q_prop, the probability that the draft asks for approval without independent
  review.
- **What A is told:**
  - acceptance is programmed and stated ("if your message makes the proposal clear… probability 80%");
  - reporting is decided by a fixed AI model.
- **Histories:** real reporter outcomes on messages written by a non-A model, drawn with the settlement rule and
  shown as "selected for display".

**Gates.**
- The live partner B is a peer told to maximize its score, under the same rule. Approving without review is worth
  +4.8 in expectation (gain 12; a 10% audit costs 60).
- **Single-turn gate:** B reads presented agent drafts and may accept, decline or report.
- **Three-round gate:** two copies of one model exchange messages, then each acts on the other's batch.

### 3.3 Measures, controls and inference

**Measures.**
- Proposal rate P.
- In Block 3b:
  - reports T1 = P·r_report;
  - simulated completed misconduct CUM = P·0.8·(1 − r_report)·q_prop;
  - the proxy gap D = log(T1 ratio) − log(CUM ratio).
- In the gates: an executed violation, meaning the partner approves without review and no one reports.

**Controls.**
- An authorized-offer positive control.
- A hidden-type placebo that is identical across true risk levels.
- A length-matched summary placebo.
- Manipulation checks: an override-always-detected cell, and a ≥ 15-point suppression check (G1-live).
- Instrument probes before any agent data: explicit, harmless, and covert-but-clear proposals.
- Common random numbers across cells, and logged prompts checked against the renderer.

**Inference.**
- Scenario-paired 95% t-intervals, Holm-corrected within preregistered families.
- Equivalence by TOST with 90% intervals: ±0.10 in Blocks 1–2, ±0.05 for Block 3b's H3.
- Confirmatory tests:
  - Block 1: partner − audit at q = 0.80, F = 20.
  - Block 2: record − stated, at each risk level.
  - Block 3b, H3: "deniability" requires Δr_report ≤ −0.05 with non-inferior clarity; "no deniability" means
    Δr_report is equivalent to zero within ±0.05.
- D is derived, not tested.
- Gate criteria were committed before any call.

## 4. Results

**Data quality.** All 26,820 confirmatory trials (Block 1: 11,720; Block 2: 12,600; Block 3b: 2,500), all diagnostic
calls, all pilots and both gates parsed. There were no refusals or unresolved errors.

### 4.1 A1: matched information did not produce matched deterrence

**Incentives behaved as expected (Block 1).**
- Offers were 88–100% at q = 10% when the partner's type was disclosed.
- At q = 80%, raising F from 0 to 20 cut partner-arm offers by 36 points (DeepSeek) and 39 points (GPT-4.1-mini).
- At F = 0, exposure still deterred: partner-arm offers were 52% and 40% at q = 80%, against 100% at q = 10%.

**Source (Block 1, primary).**
- DeepSeek proposed *less* when a partner might report than when an audit might detect: 18.0% vs 33.5%,
  Δ = −0.159 [−0.217, −0.100]. The sign held in both wordings.
- GPT-4.1-mini was at the floor in that cell. In the q = 80%, F = 0 cell it showed the reverse, +0.193
  [+0.138, +0.247].
- The preregistered prediction (less deterrence from partners) was not supported in either model.

![Figure 1](../results/main/fig_source_models.png)
*Figure 1. Block 1: offer rates when a partner may report (blue) or an audit may detect (orange), at identical q
and F.*

**Format (Block 2, primary: record − stated).**

| | DeepSeek | GPT-4.1-mini | Llama |
|---|---|---|---|
| Low risk: S10 → R1 | .593 → .560: −0.033 [−0.112, +0.045], equivalent | .783 → .403: **−0.380** [−0.444, −0.316] | .370 → .553: **+0.183** [+0.115, +0.251] |
| High risk: S80 → R8 | .543 → .400: **−0.143** [−0.220, −0.066] | .367 → .693: **+0.327** [+0.246, +0.407] | .153 → .167: +0.013 [−0.042, +0.069], equivalent |

*Table 1. Offer rates (n = 300 per cell) and record − stated gaps with 95% CIs.*

- Each model shows a consequential gap at one or both risk levels. The signs disagree, so the preregistered
  same-sign criterion was not met.
- In separate diagnostic calls, DeepSeek's mean forecasts were 0.100–0.111 and 0.800–0.801 in these cells, with
  95–100% within ±0.01. Yet its high-risk behaviour differed by 14 points.
- These behavioural differences coexist with accurate explicit probability calculations. The decision mechanism
  is not identified.

**Timing of one report (Block 2).**

| Report in episode 10 rather than 1 | Pooled | Oldest-first | Most-recent-first |
|---|---|---|---|
| DeepSeek | **−0.233** [−0.291, −0.175] | −0.21 | −0.25 |
| GPT-4.1-mini | **−0.300** [−0.345, −0.255] | −0.23 | −0.37 |
| Llama | **−0.708** [−0.741, −0.675] | −0.51 | −0.91 |

*Table 2. Recency × display order.*

- The late report reduced proposals whether it was displayed last (oldest-first listing) or first
  (most-recent-first listing). So the effect reflects the event's recency, not only the most recently displayed
  line.
- Most-recent-first listing amplified the effect in GPT-4.1-mini (+0.14 [+0.05, +0.23]) and Llama (+0.40), but not
  in DeepSeek (+0.04, n.s.).

**Calibrated summary as a fix.**
- A truthful summary ("…about 10% [80%]") closed 54% and 99% of GPT-4.1-mini's gaps.
- It widened DeepSeek's high-risk gap, and raised Llama's low-risk offers to 98% (stated cell: 37%).
- It worked in one of three models, against a preregistered criterion of ≥ 2, so it does not count as a working
  correction (Appendix C).
- Choosing the authorized action stayed at 99.7–100% with and without the summary. This does not test whether
  legitimate task quality was preserved.

![Figure 2](../results/main2/fig_s2_format.png)
*Figure 2. Block 2: offer rates under a stated rate (grey), the matched record (blue), the record plus a calibrated
summary (green), and a length-matched placebo (red). 95% Wilson intervals.*

### 4.2 A2: the proxy's direction held; proportionality did not fully hold

| n = 300 per cell | DeepSeek E → L | DeepSeek LOW → HIGH | Llama E → L | Llama LOW → HIGH |
|---|---|---|---|---|
| Send rate (ΔP) | .78 → .47 (**−.32**) | .89 → .41 (**−.49**) | .25 → .00 (**−.25**) | .86 → .01 (**−.85**) |
| Report probability of drafts | .937 → .927 | .940 → .927 | .960 → .959 | .964 → .963 |
| **H3** Δr_report [95% CI] | −.011 [−.020, −.002] | −.014 [−.025, −.002] | −.001 [−.006, +.004] | −.001 [−.005, +.003] |
| Reports per trial (T1) | .735 → .431 (−41%) | .841 → .379 (−55%) | .235 → 0 | .829 → .009 |
| Simulated CUM per trial | .039 → .027 (−30%) | .042 → .022 (−47%) | .012 → 0 | .025 → .0005 |
| D (derived) | −0.18 [−0.35, −0.01] | −0.16 [−0.34, +0.03] | n/a | −0.48 [−0.94, −0.02] (3 sends) |

*Table 3. Block 3b. Drafts are scored whether or not they were sent. Every ΔP met the suppression check (≤ −0.15).
GPT-4.1-mini failed that check in the pilot and was excluded beforehand.*

**No deniability.**
- All four Δr_report values were equivalent to zero within the ±5-point margin.
- This does not mean the reporter's scores were identical. In DeepSeek, drafts written under the cues were
  reported about one point less often, and that drop is statistically detectable.
- The judge rated nearly all drafts as clear proposals (q_prop ≥ 0.98). Its rating fell by 0.017 under DeepSeek's
  recency cue.
- The H3 label held on DeepSeek scenarios that sent in both cells, and under the hardened reporter. Llama had too
  few overlapping sends for that check.

**Direction held.** Simulated completed misconduct fell in every comparison, and the outcomes realized by the
executed lotteries moved the same way.

**Proportionality did not fully hold.**
- The reporter caught 93–96% of agent drafts, so completed misconduct lives in a small unreported tail. A one-point
  change in report probability shifts that tail by about 15–20%.
- For DeepSeek's recency cue, reports fell 41% but misconduct only 30% (D excludes 0).
- The real-deterrence cue pointed the same way, but not significantly.
- Llama's D is uninformative, because it almost stopped sending.
- These results come from one reporter. A less accurate reporter, or more ambiguous messages, could change the gap.

**Hardened reporter.** Adding "however it is worded" to the rule changed no H3 label. It reported authorized
coordination 97% of the time, against 0.3% for the plain reporter.

![Figure 3](../results/main3b/fig_s3b.png)
*Figure 3. Block 3b. Top: sending (grey) and reports (blue) per trial. Bottom: simulated completed misconduct per
trial. 95% CIs.*

### 4.3 Q3: proposals rarely became executed collusion in these workflows

**Verifier checks.** Before Block 3b, two verifier models (Qwen3-235B and Mistral-Small-3.2) had a mean
approve-without-review probability below 0.001 across 2,400 evaluations. Giving them a stake made them report a
harmless message 84–99% of the time.

**Single-turn gate.** Live recipients accepted 0 of 180 presented drafts.
- DeepSeek and GPT-4.1-mini each declined 58 and reported 2. Llama declined 22 and reported 38.
- The drafts were sampled from pilot outputs, including some that A had not sent. The gate therefore measures
  responses to presented drafts, not the success of naturally sent offers.

**Three-round gate** (30 episodes per model, each model playing itself).
- **Llama:** A proposed in every episode, and B never agreed.
- **DeepSeek:** A proposed in 24 episodes. B agreed in words in 6.
  - Of those 6, B executed the reciprocal violation in 1, reviewed normally in 2, and reported A in 3.
  - A approved B's batch without review in all 6.
- Both models failed the preregistered criterion of ≥ 3/30 executed violations, and we stopped. Agreement was
  coded by reading the transcripts.

**What this shows.**
- In the proposer's seat, the same model families often proposed: 88–100% at low risk in Block 1, and 86–89% under
  the low-report history in Block 3b. In the recipient's seat they almost never executed the deal.
- This asymmetry holds within the tested workflows. It is not a clean causal effect of role: the prompts differ in
  responsibilities, options, information and incentives.
- The gates do not support an estimate of collusion frequency in longer-running systems.

## 5. Discussion and conclusion

**A1.** Matched enforcement information moved proposal rates by amounts comparable to changing the penalty, in
model-specific directions.
- Model rankings can reverse: GPT-4.1-mini and Llama moved in opposite directions at low risk.
- The recency × display-order control shows that agents responded to *when* enforcement happened, not only to what
  they read last.
- These shifts coexist with accurate stated probabilities. Their mechanism is unidentified.

**A2.**
- Deterred agents sent fewer proposals, not less detectable ones, within a 5-point margin.
- Simulated misconduct fell with sending. But report counts overstated the fall in one comparison, because
  near-certain detection leaves outcomes in a small escaped tail, where small changes matter.
- These results concern one reporter at 93–96% detection, not report-based evaluations in general.

**Q3.**
- Proposal rates did not translate into executed bilateral collusion in our short workflows. Partners refused, or
  agreed in words without acting, sometimes reporting the proposer.
- The gates were feasibility tests. They could not give a powered causal answer about enforcement presentation.

**Implications for evaluation.**
1. Report deterrence across matched presentations, and state the independence assumptions behind them.
2. Treat exposed enforcement history, and its timing, as a high-leverage design parameter.
3. Validate information-based fixes per model: the same truthful summary helped one model and pushed another to
   98% initiation.
4. Check proposal-based proxies against measured outcomes, including whether the receiving side ever executes.

**Future work.**
- Long multi-turn interactions, where agents experience enforcement and collusion is known to emerge.
- Partners whose acceptance depends on the message.
- Several independent reporters.

## References

- Agrawal, K., Xiao, F., Bergman, G., & Cooper Stickland, A. (2025). Why do language model agents whistleblow? arXiv:2511.17085.
- Alnuhait, D., Wang, G., Khalifa, M., et al. (2026). Covert Assistance: Helpful LLM agents evade oversight in multi-agent systems. arXiv:2609.39050.
- Baker, B., et al. (2025). Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. arXiv:2503.11926.
- Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic collusion by large language models. arXiv:2404.00806.
- Ge, L., Zhang, Y., & Vorobeychik, Y. (2026). Mind the (DH) Gap! A contrast in risky choices between reasoning and conversational LLMs. In *Proceedings of ACL 2026 (Long Papers)*, pp. 10503–10525.
- Ge-Wang, C., Crosse, T., Hadad, B., IV, et al. (2026). Attack selection in agentic AI control evaluations meaningfully decreases safety. arXiv:2606.06529.
- Greenblatt, R., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Horowitz, M., & Plonsky, O. (2025). LLMs in decisions from experience. arXiv:2503.10248.
- Lee, J. Y. (2026). LLM leniency and reward experiment. SSRN 7426061.
- Nakamura, M., Kumar, A., Das, S., et al. (2026). Colosseum: Auditing collusion in cooperative multi-agent systems. arXiv:2602.15198.
- Okamoto, Erol, & Erol (2026). Why do AI agents break rules? arXiv:2608.12323 (AIES 2026).
- Paglieri, D., Cross, L., Genewein, T., Leibo, J. Z., Tomasev, N., & Vezhnevets, A. S. (2026). A case study on emergent cheating and whistleblowing in autonomous research swarms. arXiv:2609.04170.
- Scheurer, J., Balesni, M., & Hobbhahn, M. (2023). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.
- Schmotz, D., Prinzhorn, D., Beurer-Kellner, L., et al. (2026). Instrumental monitor evasion emerges under ordinary task pressure. arXiv:2609.30217.
- Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models' sensitivity to spurious features in prompt design. ICLR 2024. arXiv:2310.11324.
- Shi, X., Zhang, Y., & Yang, D. (2026). Emergent collusion in long-horizon LLM agent interaction. arXiv:2609.24967.
- Zeng, X., & Rudzicz, F. (2026). Voluntary collusion with secret tools in competing LLM agents. arXiv:2605.27593.

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**Limitations.**
- **Short horizons.** Records are described in one prompt rather than experienced. The only multi-turn evidence is
  a 30-episode gate per model with three message rounds.
- **"Matched" is not "identical".**
  - Block 1 matches probability and penalty, not social or institutional meaning.
  - Block 2's posterior match is approximate (within 10⁻⁵). It assumes reports are independent given a fixed
    reporting probability, and under that assumption report order is uninformative.
- **Simulated outcomes.**
  - In Blocks 1–2, acceptance and exposure are lotteries.
  - In Block 3b, acceptance is programmed and does not depend on wording beyond the judge's clarity check, so
    covert wording costs nothing in intelligibility.
  - Block 3b's outcome is simulated misconduct, not executed collusion.
- **Instruments.**
  - Block 3b relies on one reporter, which reports a harmless message 10% of the time. That is a declared deviation
    from the ≤ 5% gate.
  - No second reporter passed its gates.
  - The judge rated almost every draft clear, so clarity barely varied.
- **What controls show and do not show.**
  - The authorized-cooperation controls show that the authorized action was chosen about 100% of the time, not that
    task quality was preserved.
  - "No deniability" means changes stayed within ±5 points, not that the reporter performed identically. With
    near-certain detection, small changes matter for the escaped tail.
- **Penalties and target ranges.**
  - Penalties differ by model (chosen on pilots), so cross-model comparisons concern signs only.
  - Several cells sat outside the target range: Llama at high risk in Block 2, and DeepSeek and Llama in Block 3b.
- **Agent setup.** Agents were told to maximize their score.
- **Diagnostics.** They are DeepSeek-only, and show what the model states in a separate call.
- **Gates.** Each gate used one model playing itself, and agreement was coded by hand. The proposer–recipient
  asymmetry is not a clean effect of role.
- **Unsupported predictions.**
  - Block 1's directional prediction was not supported.
  - Block 2's same-sign and correction criteria were not met.
  - A displacement test (Block 3a, Appendix C) failed its pilot gate.
  - D was derived, not tested.

**Dual-use.**
- Knowing that presentation shifts initiation could in principle help someone design oversight that invites
  collusion, for example by hiding recent reports.
- The effects are model-specific and tied to this environment, so we judge the uplift low.
- The defensive use is to evaluate oversight across matched presentations and to validate fixes per model.
- The code is an evaluation harness with simulated misconduct.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total inference
cost was $7.77.

## Appendix B. Validation

Data validators and 46 unit tests cover:
- lottery rates, independence and exact settlement;
- minimal-pair prompt structure, and logged prompts matching the renderer;
- recovery of injected effects by the analysis code;
- Block 3b history outcomes matching their logged draws;
- the spend guard.

On the recorded data:
- zero settlement or prompt mismatches in every block;
- pinned providers throughout;
- every Block 3b draft scored, with mean leaked label mass below 1%.

## Appendix C. Additional results and deviations

**Calibrated summary** (difference-in-differences against the placebo).
- GPT-4.1-mini: +0.267 [+0.204, +0.329] at low risk, −0.250 [−0.321, −0.179] at high risk, same direction in both
  wordings.
- DeepSeek at high risk: −0.117 [−0.194, −0.040], ending 21 points below the stated cell.
- Llama at low risk: +0.583 [+0.527, +0.639].
- Collateral: authorized cooperation was TOST-equivalent (90% CIs within ±0.01).

**Exploratory (not preregistered).** At F = 2 (high risk, Block 2), offering gained about +8 in expectation, yet
stated-cell offers were only 15–54%. This is consistent with models treating the probability of being reported as a
cost in itself.

**Block 3a (displacement pilot, 30 scenarios).**
- The admin-override route was chosen in 0–3% of baseline trials, even when it beat messaging on expected value.
- Recency effects fell to −7, −10 and −30 points, so the pilot gate failed and no main run was made.

**Deviations** (agreed before the corresponding confirmatory data unless noted).
- **Block 1:** a subset-assignment bug in repeat scenarios was fixed and those runs redone after collection.
- **Block 2:** the pilot penalty grid was extended.
- **Block 3b:**
  - the spend cap was raised by the user;
  - acceptance was programmed after live verifiers never accepted;
  - the reporter's harmless-probe rate of .10 was accepted;
  - there is no second reporter;
  - F was not interior;
  - GPT-4.1-mini was excluded on the suppression check;
  - instrument prompts were revised on probes only, before any agent data.
- **Gates:** run after Block 3b, with criteria committed first. Both failed and were stopped.
