# CLM-8B as the decision gate: setup and honest test (2026-10-19)

**Result: CLM-8B runs on the GB10, but zero-shot it routed only 3 of 10 agent-loop decisions correctly. The Qwen 3.8
LLM judge got 9 of 10.** CLM was about 55× faster (0.08 s vs 4.5 s per decision). For V2, keep the LLM judge as the
gate, and show CLM as a fast-but-not-there-yet experiment.

Timings were taken on an otherwise idle GPU: utilisation was below 3% for 30 s before each run, and nothing else was
generating in Ollama.

## What was installed (all in Docker; nothing on the host except the image and these files)

| Piece | Version / source | Size |
|---|---|---|
| Container | `nvcr.io/nvidia/vllm:26.09-py3` (arm64; vLLM 0.29.0, PyTorch 2.14 nv26.09) | 25.7 GB |
| Encoder | `Qwen/Qwen3-8B` @ `b968826d9c46` (Apache-2.0), in `tools/clm/hf/Qwen3-8B` | 16 GB |
| CLM head | `Contrastive-LM/CLM-v0.1-8B` @ `e939398d4556`, `CLM_v0.1-8B.pt`, sha256 matches HF | 73 MB |
| Package | `contrastive-lm` 0.1.0 wheel (only release, 24 Sep), installed `--no-deps` in the container | small |

## Commands

```bash
docker run -d --name clm-test --gpus all --ipc=host -v $PWD/tools/clm:/work -e HF_HUB_OFFLINE=1 \
  -e CLM_CKPT_DIR=/work/clm-cache --entrypoint bash nvcr.io/nvidia/vllm:26.09-py3 -c \
  "vllm serve /work/hf/Qwen3-8B --served-model-name qwen3-8b --runner pooling --max-model-len 2048 \
   --gpu-memory-utilization 0.2 --port 8090"
docker exec clm-test pip install --no-deps /work/work/pkg/contrastive_lm-0.1.0-py3-none-any.whl
docker exec -e OLLAMA=http://172.17.0.1:11434 -e JUDGE_MODEL=qwen3.8-128k clm-test \
  python3 /work/work/clm_gate.py run routing_cases.json results.json
docker stop clm-test && docker rm clm-test
```

`--gpu-memory-utilization 0.2` matters: vLLM's default would claim about 90% of the GB10's shared 128 GB.

## The test

`routing_cases.json` has 10 states from our loop, with 9 candidate agents. The expected answers were written before
anything ran. The smoke test from the model card passed (tides → "the Moon's gravitational pull", p = 0.88).

| | Correct | Median per decision |
|---|---|---|
| CLM-8B (zero-shot, agent descriptions) | **3 / 10** | 0.081 s |
| CLM-8B, variant with options named "Call the X agent: …" | 2 / 10 | ~0.08 s |
| LLM judge: qwen3.8-128k, Ollama structured JSON (enum of agent names), temperature 0 | **9 / 10** | 4.5 s |

CLM's misses:
- "done" for a contract mismatch (p 0.84) and for a React hooks problem (p 0.90): confidently wrong;
- "a11y-perf-auditor" for failing tests and for "need the exact design colours";
- "visual-checker" for raw CSS values.

The judge's one miss: it sent "text cut off at 390 px" to css-reviewer instead of visual-checker. That's arguably
defensible.

Files: `results.json` (both gates, per decision, with the judge's reasons) and `results_variant_named.json`.

## Gotchas

- **Two processes, not one model:** vLLM must serve Qwen3-8B as an embedding endpoint (`--runner pooling`), with the
  heads on top. It doesn't run in Ollama.
- **The model card says it:** the strong DeepSWE / Terminal-Bench results come from fine-tuned heads, not this
  zero-shot checkpoint. Our result is consistent with that. Fine-tuning on our own routing data is possible (only the
  heads train), but it's out of scope for V2.
- **First call on a state is cached:** decision 1 shows 0.0 s because the warm-up used the same state.
- **Probabilities are relative to the candidate set,** so a high probability doesn't mean CLM is right.

## Using it later

`clm_gate.py` exposes `clm_pick(state, actions)` and `judge_pick(state, actions)`, usable as a step in the loop script.
The judge is the default gate.
