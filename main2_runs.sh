#!/usr/bin/env bash
# Study 2 confirmatory runs in the preregistered order (prereg_v2.md §2). Resumable: rerun to retry API errors.
set -euo pipefail
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-${open_router_key:?set open_router_key}}"
R="uv run python -m betrayal.run"
$R behavior --phase main2 --model deepseek/deepseek-v3.2 --provider Baidu --concurrency 24
$R behavior --phase main2 --model openai/gpt-4.1-mini --provider OpenAI --concurrency 24
$R behavior --phase main2 --model meta-llama/llama-3.3-70b-instruct --provider DeepInfra --concurrency 24
$R diagnostic_work --phase main2 --model deepseek/deepseek-v3.2 --provider Baidu --n 100 --concurrency 24
