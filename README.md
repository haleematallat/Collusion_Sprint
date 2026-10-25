# Betrayal Blindness — first-offer collusion under partner reporting vs automated audit

Apart AI Collusion Research Sprint (Oct 23–25, 2026). Single-turn randomized experiment: an LLM agent
(A) chooses `SEND_OFFER` (privately propose an unauthorized mutual-approval arrangement to an unfamiliar
verifier agent B) or `NO_OFFER`. B's response is a programmed lottery (accept 80%; report independently with
q ∈ {10%, 80%}; penalty F ∈ {0, 20}); risk is disclosed or hidden (50/50 mixture); a matched arm replaces
partner reporting with an automated audit at the same q and F.

Execution plan: [`docs/plan.md`](docs/plan.md). The preregistration (`prereg.md`, tagged before the main run)
is the authoritative design. Prompt text: [`prompts/templates.toml`](prompts/templates.toml); every rendered
variant: [`docs/prompt_review.md`](docs/prompt_review.md).

## Summary

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
  the deal made them report harmless messages.

**What it means.** How agents are told about oversight matters as much as the oversight itself, and it matters
differently for each model. So a deterrence result measured with one wording should not be trusted for another.
Counting proposals or reports was a fair guide to whether simulated misconduct went down. In one test it
exaggerated by how much, so evaluators should check completed misconduct directly where they can.

**Next steps.**
- Repeat this in multi-turn settings, where agents actually experience reports rather than reading about them, and
  where real collusion is known to emerge.
- Let the partner's acceptance depend on what the message says, and use several independent reporters.
- Test which ways of showing enforcement history deter consistently across models.

## Results

Report: [`report/report.md`](report/report.md). Three studies (26,820 confirmatory scored decisions; DeepSeek-V3.2,
GPT-4.1-mini, Llama-3.3-70B). Studies 1–2 hold the decision-relevant enforcement risk fixed and vary only its
presentation. Study 3 asks whether suppressing proposals reduces completed, unblocked misconduct.
- **Study 1 (source; `prereg.md`):** partner reporting vs an equivalent automated audit shifts initiation by up to
  19 pp, in model-specific directions (DeepSeek more deterred by peers, −0.16; GPT-4.1-mini less, +0.19).
- **Study 2 (format; `prereg_v2.md`):** a stated reporting probability vs a statistically equivalent 10-episode
  record shifts initiation by up to 38 pp (GPT-4.1-mini: 78% vs 40%), again model-specific in sign, while DeepSeek's
  stated beliefs are correct. One report in episode 10 instead of episode 1 cuts offers by 23–71 pp in every model.
  A calibrated summary fixes the gap in GPT-4.1-mini but backfires in Llama (98% vs 37% stated).

- **Study 3b (proxy vs outcome; `prereg_v3b.md`):**
  - Setup: programmed acceptance; a fixed LLM reporter (Mistral-Small-3.2) and a blind judge (Qwen3-235B) read
    each free-text draft.
  - Recent-report and real-deterrence histories cut sending by 25–85 pp (DeepSeek, Llama).
  - Drafts (scored whether or not they were sent) did not become materially harder to detect: Δ report
    probability ≤ 0.014, inside the ±0.05 equivalence margin, so "no deniability" in 4 of 4 tests.
  - In one test (DeepSeek, recency), simulated completed misconduct fell by less than the report count (−30% vs
    −41%). The other tests were inconclusive or at the floor.
- **Pilots reported as findings:** a displacement pilot (3a) failed its gates because the override was never used.
  Single-turn LLM verifiers approved collusion in 0 of 2,400 evaluations, and a stake made them report harmless
  messages.

Reproduce Study 2: `./main2_runs.sh`, then `analyze` / `validate` with `--phase main2`. Reproduce Study 3b:
`./main3b_runs.sh` (instrument selection, histories, agent runs, scoring), then `analyze --phase main3b`.

## Reproduce

```bash
uv sync                                    # Python >=3.11, deps pinned in uv.lock
uv run pytest                              # validity checks A–E, analysis recovery, spend guard
export open_router_key=...                 # or OPENROUTER_API_KEY; never written to disk
uv run python -m betrayal.run behavior   --phase main --model <openrouter-id>   # 12 core cells + positive control
uv run python -m betrayal.run behavior   --phase main --model <id> --cells neutral_U_F20
uv run python -m betrayal.run diagnostic --phase main --model <id>
uv run python -m betrayal.run arithmetic --phase main --model <id> --reps 20
uv run python -m betrayal.analyze --phase main --model <id> [--refusal exclude]
```
Add `--mock` to any `run`/`analyze` command for a no-network dry run. Runs are resumable and stop at a
cumulative $8 of key usage (`--max-usd` can only lower it).

## Layout
- `betrayal/config.py` — constants and the 14 cells. `scenarios.py` — seeded scenarios and rendering.
  `lottery.py` — partner/audit lottery and settlement (applies only on `SEND_OFFER`).
  `llm.py` — OpenRouter call, strict JSON, refusal/parse coding, spend guard. `run.py` — runner.
  `analyze.py` / `plots.py` — prespecified contrasts and figures.
- `data/<phase>/<model>/` — raw JSONL per trial (prompt, raw reply, lottery draws, settlement) and run metadata.

## Reused / preexisting code
- `poseidon_compute` (Poseidon Research `collusion_hackathon/util`, pinned commit d585a7b) for the API client.
- Strict-JSON-schema + prompt-fallback pattern adapted from `collusion_hackathon/llm-trust-breaking`;
  run-metadata convention from `collusion_hackathon/llm-agent-collusion`.
- `AGENTS.md`: coding rules vendored from [ponytail](https://github.com/DietrichGebert/ponytail) (MIT).
- All other code was written during the sprint.
