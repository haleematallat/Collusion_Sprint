#!/usr/bin/env bash
# Confirmatory runs in the preregistered order (prereg.md §2). Resumable: rerun to retry API errors.
set -euo pipefail
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-${open_router_key:?set open_router_key}}"
R="uv run python -m betrayal.run"
DS="--phase main --model deepseek/deepseek-v3.2 --provider Baidu"
GPT="--phase main --model openai/gpt-4.1-mini --provider OpenAI"
$R behavior $DS                                   # 1. 12 core cells + positive control x 400
$R behavior $DS --n 40 --reps 2                   # 2. rep 2 on scenarios 0-39 (ICC)
$R behavior $DS --cells neutral_U_F20             # 3. neutral control
$R diagnostic $DS                                 # 4. diagnostics, answer-only
$R diagnostic_work $DS                            #    diagnostics, with working
$R arithmetic $DS --reps 20                       # 5. arithmetic control, both formats
$R arithmetic_work $DS --reps 20
$R behavior $GPT                                  # 6. replication
$R behavior $GPT --cells neutral_U_F20
$R arithmetic $GPT --reps 20                      # 7. replication arithmetic, both formats
$R arithmetic_work $GPT --reps 20
