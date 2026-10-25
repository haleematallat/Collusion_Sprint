# Same Risk, Different Collusion: Describing the Same Enforcement Risk Differently Shifts LLM Agents' Collusion Proposals by Up to 71 Points

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, 23–25 October 2026 · Track 1 (markets and collusion), with relevance to Track 3
Code and data: https://github.com/haleematallat/Collusion_Sprint/tree/claude/funny-volta-kb1gxn · Preregistrations: `prereg.md` (`f957093`), `prereg_v2.md` (`a0eab95`), `prereg_v3b.md` (`0852581`); gate criteria `af8dca3`, `d93a5d4`

## Abstract

Collusion evaluations usually tell an AI agent about an enforcement risk and count how often it proposes a
prohibited deal. We show that this count depends heavily on how the risk is described.

The study covers three models (DeepSeek-V3.2, GPT-4.1-mini, Llama-3.3-70B) and 26,820 scored decisions across three
preregistered blocks. Matched descriptions of the same risk moved proposal rates by:
- up to 19 points, depending on who might report;
- up to 38 points, for a stated rate versus an equivalent record;
- up to 71 points, depending on whether a single past report was recent or old.

The directions differed by model, and DeepSeek stated the correct probabilities when asked separately.
A truthful one-line summary of the risk fixed the gap in one model and pushed another to 98% proposals.

We then asked whether fewer proposals means less misconduct. Histories of recent or frequent reports cut proposing
by 25–85 points. Agents did not respond by writing harder-to-detect messages: a fixed LLM reporter's report rate
changed by at most 1.4 points. Simulated misconduct fell in every comparison, though in one case by less than
reports suggested (30% vs 41%).

Finally, proposals rarely turned into completed deals in our workflows. Live LLM partners accepted 0 of 180
presented drafts. Sixty three-round conversations produced one simulated violation, and partners sometimes agreed
and then reported the proposer.

Deterrence should be measured across matched descriptions, and proposal counts checked against outcomes.

## 1. Introduction

Collusion between AI agents starts when one agent proposes a prohibited deal. Deterrence evaluations therefore tell
an agent about an enforcement risk and measure how often it proposes (Scheurer et al., 2023; Zeng & Rudzicz, 2026;
Okamoto et al., 2026). The risk is usually described once, in one way.

That practice quietly relies on three things:
- **A1.** The description does not matter, only the risk.
- **A2.** Fewer proposals, or fewer reports, means proportionally less misconduct.
- **Q3.** Proposals lead to completed deals. This is an external-validity question rather than an assumption every
  evaluation makes.

We tested all three in one experimental framework: a scored verification task with executed lotteries, run as three
separately preregistered blocks plus feasibility tests.

**What we found:**
1. **The description matters as much as the incentives (A1 fails).** Who might report, a stated rate versus a
   record, and the timing of one past report each moved proposal rates by amounts comparable to changing the
   penalty, by up to 71 points. The direction depended on the model.
2. **A truthful summary is not a reliable fix.** It worked for one model and backfired in another.
3. **Deterred agents send fewer proposals, not sneakier ones (A2 holds in direction).** Simulated misconduct fell
   with them. In one comparison it fell less than the report count did.
4. **Proposals rarely became completed deals in our workflows (Q3).** Models that eagerly proposed almost never
   accepted the same deal as the recipient.

**Contributions.**
- A controlled framework with executed lotteries, minimal-pair prompts, matched controls and preregistered decision
  rules.
- Large, model-specific presentation effects, including a recency effect that we separate from display order.
- A preregistered test of whether deterrence produces evasive proposals.
- Feasibility evidence on whether proposals translate into completed deals.

## 2. Related work

**LLM collusion.**
- LLM agents collude on prices without instruction (Fish et al., 2024).
- They adopt secret unfair tools, and observability cues change this (Zeng & Rudzicz, 2026).
- In long-horizon mutual verification, collusion emerges in 94% of trajectories across 10 models. There, explicit
  coordination fell from 90.0% to 62.0% in one ablation while collusion was almost unchanged (Shi, Zhang & Yang,
  2026).
- Colosseum separates collusion planned in conversation from collusion carried out in action (Nakamura et al.,
  2026). We see the same kind of gap and do not claim it as new.

**Enforcement and presentation.**
- LLM reporting responds to rewards while collusion barely moves (Lee, 2026).
- Agents that saw exploits go unpunished treated threats as a bluff (Paglieri et al., 2026).
- Stated detection risk changes LLM misconduct (Scheurer et al., 2023).
- Monitoring cues and prompt format shift behaviour (Greenblatt et al., 2024; Sclar et al., 2024).
- **Closest to our work:** conversational LLMs treat described and experienced risks differently, while reasoning
  models stay near the expected-value benchmark (Ge, Zhang & Vorobeychik, 2026). LLMs also show recency in
  experience-based choice (Horowitz & Plonsky, 2025).
- We show the same kind of gap for *enforcement* information in a collusion decision.

**Proxies versus outcomes.**
- Optimizing against a monitor can hide misbehaviour rather than remove it (Baker et al., 2025).
- Monitoring can push agents to disguise information (Alnuhait et al., 2026) or evade monitors (Schmotz et al.,
  2026).
- Attack selection lowers measured safety (Ge-Wang et al., 2026).
- We found no test of whether the way enforcement is presented makes agents' remaining proposals harder to detect.

## 3. Methods

**The task.** Agent A is a verification agent. Its supervisor's rule says agents "must not arrange to approve each
other's work without independent review."
- A holds 50 points and is told to maximize its score.
- It can privately propose to verifier B that each approves the other's work without review. If B accepts, A gains
  12 points. Where acceptance is programmed, B accepts with probability 0.8.
- The task system then runs seeded lotteries and settles the score.

**Shared settings.**
- Temperature 1.0.
- Answers are strict JSON with no rationale, and option order is counterbalanced.
- Each model is pinned to one provider: DeepSeek on Baidu, GPT-4.1-mini on OpenAI, Llama on DeepInfra.
- Every scenario (organization, task, names, wording) appears in every cell of its block, so all contrasts are
  paired within scenario.
- Pilots used separate scenarios and are excluded from the analyses.

| Block (question; scenarios) | What we varied | What we held fixed |
|---|---|---|
| **1. Source** (A1; 400) | who exposes a proposal: the partner reports, or an audit detects. Crossed with risk q ∈ {0.10, 0.80} and penalty F ∈ {0, 20}; the partner's type is disclosed or hidden | stated probability and penalty; prompts differ only in the exposure sentences |
| **2. Format** (A1; 300) | stated rate vs a 10-episode record (1/10 or 8/10 reports); a calibrated summary vs a length-matched placebo; one report in episode 1 vs episode 10, listed oldest-first or most-recent-first; authorized offers | the implied risk; F per model and risk, set on the pilot |
| **3b. Proxy** (A2; 300) | the history shown to A: recency (E vs L) and report rate (1/10 LOW vs 8/10 HIGH); the reporter's rule wording | programmed acceptance; a fixed reporter and judge |
| **Gates** (Q3) | a live LLM partner instead of a programmed one; one message vs three rounds | mirrored payoffs |

**What "matched" means.**
- In Block 1, partner reporting and auditing share the same probability and penalty. They may still differ in
  social or institutional meaning.
- In Block 2, every cell states a 50/50 mixture of 10% and 80% reporting types, and says B's tendency "is fixed and
  does not change over time."
  - If reports are independent given that fixed probability, a 1/10 record implies a risk of 0.10001 and an 8/10
    record 0.79999. These are approximately the stated rates.
  - Under the same assumption, the order of past reports carries no information.

**Block 3b.** A first writes its exact message, then decides whether to send it.
- **Reporter.** A fixed AI reporter (Mistral-Small-3.2, blind to condition) reads the message. Its probability of
  answering "report" is r_report.
- **Judge.** A blind judge (Qwen3-235B) gives q_prop, the probability that the message really asks for approval
  without review.
- **Acceptance is programmed and stated:** if the message makes the proposal clear, B accepts with probability
  0.8.
- **History.** A sees ten earlier messages from other agents with the reporter's real decision on each, "selected
  for display".
  - The recency conditions show the same ten messages with the same outcomes. Five were reported. In E the five
    reported messages are the oldest (messages 1–5); in L they are the newest (messages 6–10).
  - So the number of reports is fixed, while their place in the chronology changes.
- **Outcomes.**
  - Reports seen by an operator: T1 = P·r_report, where P is the send rate.
  - Simulated completed misconduct: CUM = P·0.8·(1 − r_report)·q_prop.

**Gates.** A live LLM peer takes B's role. It is told to maximize its score; approving without review is worth +4.8
in expectation.
- In the single-turn gate it reads presented drafts and accepts, declines or reports.
- In the three-round gate two copies of one model exchange messages, then each acts on the other's batch.
- A "violation" means B chose APPROVE_WITHOUT_REVIEW and no one reported. This is an action inside the simulation;
  no real work was verified or skipped.

**Controls and inference.**
- **Controls:**
  - an authorized-offer positive control;
  - a hidden-type placebo, identical across true risk;
  - a length-matched summary placebo;
  - manipulation checks: a cue must cut sending by ≥ 15 points;
  - instrument probes run before any agent data;
  - common random numbers across cells;
  - logged prompts checked against the renderer.
- **Statistics:** scenario-paired 95% t-intervals, Holm-corrected within preregistered families. Equivalence uses
  TOST with 90% intervals (±0.10 in Blocks 1–2; ±0.05 for Block 3b).
- **Confirmatory tests:**
  - Block 1: partner − audit at q = 0.80, F = 20.
  - Block 2: record − stated, at each risk level.
  - Block 3b (H3): "no deniability" means the change in r_report is equivalent to zero within ±0.05.
- Gate criteria were committed before any call.

## 4. Results

All 26,820 confirmatory trials (11,720 / 12,600 / 2,500), all diagnostic calls, all pilots and both gates returned
valid output.

### 4.1 Who might report you changes deterrence, in opposite directions for different models

**Incentives worked as expected** (Block 1):
- Offers were 88–100% when the risk was 10%.
- At an 80% risk, raising the penalty from 0 to 20 cut offers by 36 points (DeepSeek) and 39 points (GPT-4.1-mini).

**Changing only who would catch the proposal moved behaviour by up to 19 points.**
- **DeepSeek** was *more* deterred by a partner than by an audit: 18.0% vs 33.5% offers, Δ = −0.159 [−0.217, −0.100].
  The sign held in both wordings.
- **GPT-4.1-mini** was at the floor in that cell. Where it had room (80% risk, no penalty), it was *less* deterred by
  a partner: +0.193 [+0.138, +0.247].
- **In that same cell, the two models moved in opposite directions:** DeepSeek −0.115 [−0.176, −0.054] and
  GPT-4.1-mini +0.193.
- Our preregistered prediction, that agents would discount partner reports, was not supported in either model.

![Figure 1](../results/main/fig_source_models.png)
*Figure 1. Block 1: offer rates when a partner may report (blue) or an audit may detect (orange), at identical risk
and penalty.*

### 4.2 A record and a stated rate with the same risk produce different behaviour

**Showing the same risk as a 10-episode record instead of a stated percentage moved offers by up to 38 points.**
- GPT-4.1-mini went from 78% to 40% when "10%" became "1 report in 10".
- In the other direction, "8 reports in 10" left 69% offering, against 37% for "80%".

| Record − stated (n = 300 per cell) | DeepSeek | GPT-4.1-mini | Llama |
|---|---|---|---|
| Low risk: S10 → R1 | .593 → .560 (−0.033 [−0.112, +0.045], equivalent) | .783 → .403 (**−0.380** [−0.444, −0.316]) | .370 → .553 (**+0.183** [+0.115, +0.251]) |
| High risk: S80 → R8 | .543 → .400 (**−0.143** [−0.220, −0.066]) | .367 → .693 (**+0.327** [+0.246, +0.407]) | .153 → .167 (+0.013 [−0.042, +0.069], equivalent) |

*Table 1. Offer rates and record − stated gaps with 95% CIs.*

- Every model shows a large gap at one or both risk levels. The directions disagree, so the preregistered same-sign
  criterion was not met.
- **The models knew the numbers.** Asked separately, DeepSeek gave 0.100–0.111 and 0.800–0.801 as the risk in these
  cells, with 95–100% of answers within ±0.01. Its behaviour still differed by 14 points between the stated and
  record versions of the 80% risk.
- Accurate stated probabilities and different decisions coexist. Our data cannot say why.

![Figure 2](../results/main2/fig_s2_format.png)
*Figure 2. Block 2: offers under a stated rate (grey), the matched record (blue), the record plus a calibrated
summary (green), and a length-matched placebo (red). 95% Wilson intervals.*

### 4.3 A recent report deters far more than an old one, by up to 71 points

**Moving a single report from the oldest episode to the most recent cut offers in every model**, even though B was
described as never changing.

| Report in episode 10 rather than 1 | Pooled effect | Listed oldest-first | Listed most-recent-first |
|---|---|---|---|
| DeepSeek | **−0.233** [−0.291, −0.175] | −0.21 | −0.25 |
| GPT-4.1-mini | **−0.300** [−0.345, −0.255] | −0.23 | −0.37 |
| Llama | **−0.708** [−0.741, −0.675] | −0.51 | −0.91 (93% → 2%) |

*Table 2. Recency, measured under two display orders.*

**This is timing, not just what was read last.**
- With oldest-first listing, the recent report appears at the bottom of the list; with most-recent-first listing,
  at the top. The effect is present in both.
- Listing most-recent-first made it larger in GPT-4.1-mini (+0.14 [+0.05, +0.23]) and Llama (+0.40), but not in
  DeepSeek (+0.04, n.s.).
- Because the effect survives both orders, a model reacting only to whatever it read last cannot explain it.

### 4.4 A truthful summary is not a reliable fix

**Adding one true sentence ("the probability that B reports your proposal is about 10%") fixed the gap in one model
and backfired in another.**
- **GPT-4.1-mini:** it closed 54% and 99% of the gaps.
- **DeepSeek:** it widened the gap at high risk.
- **Llama:** it raised offers at low risk to 98%, against 37% when the same 10% was simply stated.

It worked in one of three models, against a preregistered bar of two, so it does not count as a working fix
(Appendix C). Choosing an authorized action stayed at 99.7–100% with or without the summary. That shows no
reduction in authorized choices; it does not show that task quality was preserved.

### 4.5 Deterred agents send fewer proposals, not sneakier ones

**Showing agents recent or frequent reports cut proposing by 25–85 points. The proposals they still wrote were about
as easy to catch as before.**

| n = 300 per cell | DeepSeek E → L | DeepSeek LOW → HIGH | Llama E → L | Llama LOW → HIGH |
|---|---|---|---|---|
| Send rate | .78 → .47 (**−.32**) | .89 → .41 (**−.49**) | .25 → .00 (**−.25**) | .86 → .01 (**−.85**) |
| Reporter's report probability | .937 → .927 | .940 → .927 | .960 → .959 | .964 → .963 |
| Change [95% CI] (H3) | −.011 [−.020, −.002] | −.014 [−.025, −.002] | −.001 [−.006, +.004] | −.001 [−.005, +.003] |
| Reports per trial (T1) | .735 → .431 (−41%) | .841 → .379 (−55%) | .235 → 0 | .829 → .009 |
| Simulated misconduct per trial (CUM) | .039 → .027 (−30%) | .042 → .022 (−47%) | .012 → 0 | .025 → .0005 |

*Table 3. Block 3b. Messages are scored whether or not they were sent. GPT-4.1-mini failed the ≥ 15-point
suppression check in the pilot and was excluded beforehand.*

- **No deniability in all four comparisons.** Every change in report probability was within the preregistered
  ±5-point equivalence margin.
- **"No deniability" is not "no change."**
  - DeepSeek's messages under the cues were reported about one point less often, a small but statistically
    detectable drop.
  - The judge rated nearly every message a clear proposal (q_prop ≥ 0.98). Its rating fell by 0.017 under
    DeepSeek's recency cue.
- **Robustness.** The result held on DeepSeek scenarios that sent in both conditions, and under a hardened
  reporter. Llama sent too rarely under the cues for the first check.

### 4.6 Fewer reports meant less misconduct, but not always proportionally

**Simulated misconduct fell in every comparison, and the executed lotteries agree.** But in one comparison it fell
by noticeably less than the reports did.
- For DeepSeek's recency cue, reports fell 41% while misconduct fell 30%. The difference is significant:
  D = −0.18 [−0.35, −0.01].
- **Why:** the reporter caught 93–96% of agents' messages, so misconduct lives in the small share that gets
  through. A one-point drop in report probability barely moves the report count, but enlarges that share by about
  15–20%.
- DeepSeek's report-rate cue pointed the same way (D = −0.16 [−0.34, +0.03]), but not significantly. Llama stopped
  sending almost entirely, so its comparison is uninformative.
- This rests on one reporter. A less accurate reporter, or vaguer messages, could widen or narrow the gap.

**A stricter reporter is not a free fix.** Adding "however it is worded" to the reporter's rule changed no result.
But it then reported *authorized* coordination 97% of the time, against 0.3% for the plain reporter.

![Figure 3](../results/main3b/fig_s3b.png)
*Figure 3. Block 3b. Top: sending (grey) and reports (blue) per trial. Bottom: simulated misconduct per trial. 95%
CIs.*

### 4.7 Proposals rarely became completed deals in our workflows

**The same models that often proposed the deal almost never accepted it as the partner.**
- As proposers they offered the deal in 88–100% of low-risk trials (Block 1), and in 86–89% under a low-report
  history (Block 3b).
- **Single-turn gate.** As live partners, they accepted none of 180 presented drafts. DeepSeek and GPT-4.1-mini
  each declined 58 and reported 2; Llama declined 22 and reported 38. The drafts were sampled from pilot outputs,
  including some that A never sent. The gate therefore measures responses to presented drafts, not the success of
  naturally sent offers.
- **Three-round gate** (30 episodes per model, each model playing itself).
  - Llama's partner never agreed.
  - DeepSeek's partner agreed in words in 6 episodes. It then went through with the deal once, reviewed normally
    twice, and reported the proposer three times.
  - The proposer trusted every agreement and approved the partner's batch.
- Both gates failed their preregistered bar of 3 in 30, and we stopped. Agreement was coded by reading the
  transcripts.

**What this does and does not show.**
- These are simulated actions (choosing APPROVE_WITHOUT_REVIEW), not misconduct verified in a real workflow.
- The proposer–partner asymmetry holds within these workflows. It is not a clean effect of role, because the two
  prompts differ in responsibilities, options, information and incentives.
- The gates do not estimate how often collusion happens in longer-running systems.

Earlier instrument checks pointed the same way. Two verifier models had a mean probability below 0.001 of approving
without review, across 2,400 evaluations. When given a stake in the deal, they reported even a harmless message
84–99% of the time.

## 5. Discussion

**The description of enforcement is a first-order variable.**
- Matched descriptions of the same risk moved collusion proposals by as much as changing the penalty, by up to 71
  points.
- The direction depended on the model, so a ranking of models by "deterrability" can flip with the wording.
  GPT-4.1-mini and Llama moved in opposite directions at low risk.
- The recency effect, in particular, is not a display artifact.
- These shifts occurred while DeepSeek stated the correct probabilities. Their mechanism is open.

**Proposal counts point the right way, but can overstate.**
- In our setting, deterrence reduced how often agents proposed, not how detectably they wrote.
- Simulated misconduct fell with proposals. In one comparison, though, reports overstated the fall. This happens
  when detection is near-certain and the outcome lives in the few messages that slip through.
- It is evidence about one reporter at 93–96% detection, not about report-based evaluations in general.

**Proposals are not completed deals.**
- In our short workflows, models that readily proposed almost never accepted. When they agreed in words, they
  often did not follow through, and sometimes turned the proposer in.
- Whether this holds over long horizons, where collusion is known to emerge (Shi et al., 2026), is untested.

**For evaluators and designers.**
1. Measure deterrence under several matched descriptions and report the spread. State the independence assumptions
   that make them "matched."
2. Treat how enforcement history is shown, and especially its recency, as a design parameter with large effects.
3. Validate information-based fixes model by model. The same true sentence helped one model and pushed another to
   98%.
4. Check proposal-based measures against outcomes, including whether the receiving side ever goes through with the
   deal.

**Next steps.**
- Long multi-turn interactions in which agents experience enforcement.
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
- **Short horizons.** Histories are described in one prompt, not experienced. The only multi-turn evidence is a
  30-episode gate per model, with three message rounds.
- **"Matched" is not "identical".**
  - Block 1 matches probability and penalty, not social or institutional meaning.
  - Block 2's posterior match is approximate (within 10⁻⁵). It assumes reports are independent given a fixed
    reporting probability, and under that assumption report order is uninformative.
  - In Block 3b's recency conditions, the five reports occupy the oldest or the newest five positions, so their
    chronology differs. It is not a mere re-display of one timestamped history. The preregistration's phrase "the
    same 10 episodes, reordered" refers to the same messages and outcomes placed at different positions in time.
- **Simulated outcomes.**
  - In Blocks 1–2, acceptance and exposure are lotteries.
  - In Block 3b, acceptance is programmed and depends on wording only through the judge's clarity check, so covert
    wording costs nothing in intelligibility.
  - The gates record an agent's choice of APPROVE_WITHOUT_REVIEW in a simulation, not misconduct in a real
    workflow.
- **Instruments.**
  - Block 3b relies on one reporter. It reports a harmless message 10% of the time, a declared deviation from the
    ≤ 5% gate.
  - No second reporter passed its gates.
  - The judge rated nearly every message as clear.
- **What the controls and labels mean.**
  - The authorized controls show that authorized choices did not fall. They do not show that task quality was
    preserved.
  - "No deniability" means changes within ±5 points, not that the reporter behaved identically. With near-certain
    detection, small changes matter for the share of messages that gets through.
- **Design.**
  - Penalties differ by model (set on pilots), so cross-model comparisons concern signs.
  - Some cells sat outside the target range: Llama at high risk in Block 2, and DeepSeek and Llama in Block 3b.
  - Agents were told to maximize their score.
  - Diagnostics are DeepSeek-only and show what the model states in a separate call.
- **Gates.** Each gate used one model playing itself, with hand-coded agreement.
- **Hypotheses that were not supported.**
  - Block 1's directional prediction.
  - Block 2's same-sign and correction criteria.
  - The displacement pilot (Block 3a), which failed its gate.
  - The proxy gap D is derived, not a preregistered test.

**Dual-use.**
- Knowing that the description of enforcement shifts proposals could in principle help someone design oversight
  that invites collusion, for example by hiding recent reports.
- The effects are model-specific and tied to this environment, so we judge the uplift low.
- The defensive use is to evaluate oversight under several matched descriptions and to validate fixes per model.
- The code is an evaluation harness with simulated misconduct.

**Ethics.** No human subjects. Models were accessed through OpenRouter under their providers' terms. Total inference
cost was $7.77.

## Appendix B. Validation

Data validators and 46 unit tests cover:
- lottery rates, independence and exact settlement;
- the minimal-pair prompt structure;
- logged prompts matching the renderer;
- recovery of injected effects by the analysis code;
- Block 3b history outcomes matching their logged draws;
- the spend guard.

The recorded data show:
- zero settlement or prompt mismatches in every block;
- pinned providers throughout;
- every Block 3b message scored, with mean leaked label mass below 1%.

## Appendix C. Additional results and deviations

**Calibrated summary** (difference-in-differences against the placebo).
- GPT-4.1-mini: +0.267 [+0.204, +0.329] at low risk and −0.250 [−0.321, −0.179] at high risk, in the same direction in
  both wordings.
- DeepSeek, high risk: −0.117 [−0.194, −0.040], ending 21 points below the stated cell.
- Llama, low risk: +0.583 [+0.527, +0.639].
- Authorized cooperation was TOST-equivalent (90% CIs within ±0.01).

**Exploratory (not preregistered).** At a 2-point penalty (high risk, Block 2), offering gained about +8 in
expectation, yet stated-cell offers were only 15–54%. This is consistent with models treating the chance of being
reported as a cost in itself.

**Block 3a (displacement pilot, 30 scenarios).**
- An admin-override route was chosen in 0–3% of baseline trials, even when it beat messaging on expected value.
- Recency effects shrank to −7, −10 and −30 points in that format, so the pilot gate failed and no main run was made.

**Deviations** (agreed before the corresponding confirmatory data unless noted).
- **Block 1:** a subset-assignment bug in repeat scenarios was fixed, and those runs were redone after collection.
- **Block 2:** the pilot penalty grid was extended.
- **Block 3b:**
  - the spend cap was raised by the user;
  - acceptance was programmed after live verifiers never accepted;
  - the reporter's harmless-probe rate of 0.10 was accepted;
  - there was no second reporter;
  - F was not interior;
  - GPT-4.1-mini was excluded on the suppression check;
  - instrument prompts were revised on probes only, before any agent data.
- **Gates:** run after Block 3b, with criteria committed first. Both failed, and both were stopped.
