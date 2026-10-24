# Peers Deter More Than Audits: Exposure Source and the First Unauthorized Coordination Offer Between LLM Agents

**[Author names and affiliations — to be filled in by the team]**

Apart AI Collusion Research Sprint, October 2026 · Track 1.1 (conditions for collusion), secondary 1.5 (low-cost interventions)
Code, data, preregistration: `github.com/haleematallat/collusion_sprint` (branch `claude/funny-volta-kb1gxn`; preregistration commit `f957093`)

## Abstract

<!-- RESULTS-DEPENDENT: written last, 150–250 words -->

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

<!-- RESULTS-DEPENDENT: one-paragraph summary of findings + contribution bullets -->

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
  Peer reports did not stop the exploit, and stated threats were discounted as bluffs.
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

<!-- RESULTS-DEPENDENT -->

## 5. Discussion

<!-- RESULTS-DEPENDENT -->

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

<!-- RESULTS-DEPENDENT -->

## Appendix B. Validation report

<!-- filled from results/main/*/validation.json -->

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
