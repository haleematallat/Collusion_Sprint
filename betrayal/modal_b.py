"""Ephemeral Modal vLLM server for the fixed verifier B (Study 3b). Modelled on poseidon_compute/modal_serve.py,
but the endpoint is protected by a per-run API key and the weights are cached in a Modal volume.

  with served("Qwen/Qwen2.5-32B-Instruct") as (base_url, key): ...   # torn down on exit
"""
import contextlib
import os
import secrets
import subprocess
import time
import urllib.request

import modal

MODEL = os.environ.get("B_MODEL", "Qwen/Qwen2.5-32B-Instruct")
KEY = os.environ.get("B_KEY") or secrets.token_hex(16)
os.environ["B_KEY"] = KEY  # same key in the container (via the secret) and the client

app = modal.App("collusion-verifier")
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("vllm==0.6.6", "huggingface_hub[hf_transfer]==0.26.2")
         .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"}))
cache = modal.Volume.from_name("collusion-hf-cache", create_if_missing=True)


@app.function(image=image, gpu=os.environ.get("B_GPU", "A100-80GB"), timeout=6 * 3600, scaledown_window=300,
              volumes={"/root/.cache/huggingface": cache},
              secrets=[modal.Secret.from_dict({"B_KEY": KEY, "B_MODEL": MODEL})])
@modal.concurrent(max_inputs=64)
@modal.web_server(port=8000, startup_timeout=1500)
def serve():
    subprocess.Popen(f"python -m vllm.entrypoints.openai.api_server --model {os.environ['B_MODEL']} --host 0.0.0.0 "
                     f"--port 8000 --api-key {os.environ['B_KEY']} --max-model-len 8192 --max-logprobs 20", shell=True)


@contextlib.contextmanager
def served(timeout=1800):
    with modal.enable_output(), app.run():
        url = serve.get_web_url().rstrip("/")
        req = urllib.request.Request(url + "/v1/models", headers={"Authorization": f"Bearer {KEY}"})
        t0 = time.time()
        while True:
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    if r.status == 200:
                        break
            except Exception as e:  # cold start: connection errors / 503 until vLLM has loaded the weights
                if time.time() - t0 > timeout:
                    raise TimeoutError(f"verifier endpoint not ready after {timeout}s: {e}")
            time.sleep(10)
        print(f"[modal_b] {MODEL} ready after {time.time() - t0:.0f}s", flush=True)
        yield url + "/v1", KEY
