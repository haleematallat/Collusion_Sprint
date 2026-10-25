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

## Results

Report: [`report/report.md`](report/report.md). Three preregistered studies (26,820 confirmatory scored decisions;
DeepSeek-V3.2, GPT-4.1-mini, Llama-3.3-70B), plus pilots and gate tests. They examine two assumptions behind
proposal-based deterrence evaluations and one external-validity question:
- **A1:** deterrence is invariant to how equivalent risk is presented (Studies 1–2).
- **A2:** fewer proposals or reports means proportionally less completed misconduct (Study 3b).
- **Q3 (external validity):** do proposal rates predict executed collusion by a live partner (gates)? Proposals rarely became executed collusion in our short workflows.
- **Study 1 (source; `prereg.md`):** partner reporting vs an equivalent automated audit shifts initiation by up to
  19 pp, in model-specific directions (DeepSeek more deterred by peers, −0.16; GPT-4.1-mini less, +0.19, in a different cell).
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
- **Pilots and gates (A3):**
  - A displacement pilot (3a) failed its gates: the override was almost never used (0–3%).
  - Two LLM verifiers had a mean approval probability below 0.001 across 2,400 evaluations, and a stake made them
    report harmless messages.
  - Live partners accepted 0 of 180 real drafts.
  - Over three rounds of conversation, Llama never agreed. DeepSeek's partner agreed in words 6 times out of 30,
    carried the deal out once, and reported the proposer 3 times.

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
