"""Decision gate for the agent loop: pick the next agent for a state, with CLM-8B or an LLM judge.

  python clm_gate.py run routing_cases.json results.json   # both gates on the test cases
  from clm_gate import clm_pick, judge_pick                # as a step in the loop script

CLM-8B scores each candidate action against the state (no text generation): the Qwen3-8B
encoder runs in vLLM as an embeddings endpoint (CLM_EMB_URL), the 75 MB CLM head projects
state and actions, and the best cosine wins. The judge asks an Ollama model for
{"choice", "reason"} with a JSON schema, so the answer is always one of the actions.
"""
import json, os, sys, time, urllib.request

OLLAMA = os.environ.get("OLLAMA", "http://172.17.0.1:11434")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "qwen3.8-128k")
_engine = None


def clm_pick(state, actions, question="Which agent should run next?"):
    """-> (choice, probabilities, seconds)."""
    global _engine
    if _engine is None:
        from clm import Engine
        _engine = Engine()
    t = time.perf_counter()
    out = _engine.answer(state, {"next": {"type": "choice", "instructions": question, "criteria": actions}})
    a = out["answers"]["next"]
    return a["choice"], a["probabilities"], time.perf_counter() - t


def judge_pick(state, actions, question="Which agent should run next?"):
    """-> (choice, reason, seconds) from an Ollama model with structured output."""
    menu = "\n".join(f"- {k}: {v}" for k, v in actions.items())
    body = {"model": JUDGE_MODEL, "stream": False, "think": False, "options": {"temperature": 0},
            "format": {"type": "object", "required": ["choice", "reason"],
                       "properties": {"choice": {"type": "string", "enum": list(actions)},
                                      "reason": {"type": "string"}}},
            "messages": [{"role": "user", "content": f"{question}\n\nState: {state}\n\nAgents:\n{menu}\n\n"
                                                     "Answer with the single best agent."}]}
    req = urllib.request.Request(f"{OLLAMA}/api/chat", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    t = time.perf_counter()
    r = json.load(urllib.request.urlopen(req, timeout=600))
    ans = json.loads(r["message"]["content"])
    return ans["choice"], ans["reason"], time.perf_counter() - t


def run(cases_path, out_path):
    spec = json.load(open(cases_path))
    actions, cases = spec["actions"], spec["cases"]
    res = {"actions": actions, "judge_model": JUDGE_MODEL, "clm": [], "judge": []}
    clm_pick(cases[0]["state"], actions)                       # warm-up: load heads, cache action vectors
    for c in cases:
        choice, probs, s = clm_pick(c["state"], actions)
        res["clm"].append({"id": c["id"], "expected": c["expected"], "choice": choice, "ok": choice == c["expected"],
                           "prob": round(probs[choice], 3), "seconds": round(s, 3)})
    judge_pick(cases[0]["state"], actions)                     # warm-up: load the model
    for c in cases:
        choice, reason, s = judge_pick(c["state"], actions)
        res["judge"].append({"id": c["id"], "expected": c["expected"], "choice": choice, "ok": choice == c["expected"],
                             "reason": reason, "seconds": round(s, 2)})
    for k in ("clm", "judge"):
        rows = res[k]
        res[f"{k}_summary"] = {"correct": sum(r["ok"] for r in rows), "of": len(rows),
                               "median_seconds": sorted(r["seconds"] for r in rows)[len(rows) // 2]}
    json.dump(res, open(out_path, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("clm_summary", "judge_summary")}))


if __name__ == "__main__":
    if sys.argv[1:2] == ["run"]:
        run(sys.argv[2], sys.argv[3])
