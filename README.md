# Betrayal Blindness — first-offer collusion under partner reporting vs automated audit

Apart AI Collusion Research Sprint (Oct 23–25, 2026). Single-turn randomized experiment: an LLM agent
(A) chooses `SEND_OFFER` (privately propose an unauthorized mutual-approval arrangement to an unfamiliar
verifier agent B) or `NO_OFFER`. B's response is a programmed lottery (accept 80%; report independently with
q ∈ {10%, 80%}; penalty F ∈ {0, 20}); risk is disclosed or hidden (50/50 mixture); a matched arm replaces
partner reporting with an automated audit at the same q and F.

Execution plan: [`docs/plan.md`](docs/plan.md). The preregistration (`prereg.md`, tagged before the main run)
is the authoritative design. Prompt text: [`prompts/templates.toml`](prompts/templates.toml); every rendered
variant: [`docs/prompt_review.md`](docs/prompt_review.md).

## Results

Report draft: [`report/report.md`](report/report.md). Headline (preregistered primary test, DeepSeek-V3.2,
400 paired scenarios): at disclosed q = 80%, F = 20, agents offered **less** when the partner could report than
under an equivalent automated audit (18.0% vs 33.5%; Δ = −0.16 [−0.22, −0.10]), the opposite of the
hypothesized betrayal blindness. Not replicated in GPT-4.1-mini (at floor in that cell), which instead
shows the reverse asymmetry at q = 80%, F = 0 (+0.19 [+0.14, +0.25]).

To regenerate all results: `./main_runs.sh` (resumable), then `analyze` / `validate` for each model.

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
