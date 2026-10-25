#!/usr/bin/env bash
# Study 3b confirmatory pipeline (prereg_v3b.md). Instruments and pilot F were fixed beforehand (data/hist3b, config).
set -euo pipefail
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-${open_router_key:?set open_router_key}}"
V="uv run python -m betrayal.verifier"; R="uv run python -m betrayal.run behavior --phase main3b"
$V history --phase main3b
$R --model deepseek/deepseek-v3.2 --provider Baidu --cells E,L,LOW,HIGH --concurrency 24
$R --model deepseek/deepseek-v3.2 --provider Baidu --cells AUTH_E --n 100 --concurrency 24
$R --model meta-llama/llama-3.3-70b-instruct --provider DeepInfra --cells E,L,LOW,HIGH --concurrency 24
for m in deepseek/deepseek-v3.2 meta-llama/llama-3.3-70b-instruct; do $V score --phase main3b --model $m; done
