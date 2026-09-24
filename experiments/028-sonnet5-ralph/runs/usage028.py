#!/usr/bin/env python3
"""EXP-028 usage: message.id dedup, 메인 세션과 서브에이전트 세션을 분리 집계. 모델·도구 호출도 기록."""
import json, sys, glob, os
from collections import Counter
BASE = os.path.expanduser(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser("~/ralph-exp028")
RUNS = sys.argv[2:] or [f"sonnet5-{l}-{n}" for n in (1, 2, 3) for l in ("en", "ko")]
F = ["input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"]

def agg(files):
    seen, tot, models, tools = {}, Counter(), Counter(), Counter()
    for f in files:
        for line in open(f):
            try: d = json.loads(line)
            except Exception: continue
            m = d.get("message") or {}
            if d.get("type") != "assistant" or not isinstance(m, dict): continue
            mid = m.get("id"); u = m.get("usage")
            if not mid or not u: continue
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools[(mid, c.get("id"))] = c.get("name")
            seen[mid] = (u, m.get("model"))
    for u, model in seen.values():
        for k in F: tot[k] += u.get(k) or 0
        models[model] += 1
    return tot, len(seen), models, Counter(tools.values())

print("run,part,sessions,messages," + ",".join(F) + ",models,tools")
for r in RUNS:
    d = f"{BASE}/sessions-{r}"
    for part, files in (("main", glob.glob(f"{d}/*.jsonl")), ("subagent", glob.glob(f"{d}/*/subagents/*.jsonl"))):
        if not files: continue
        tot, n, models, tools = agg(files)
        print(f"{r},{part},{len(files)},{n}," + ",".join(str(tot[k]) for k in F) + ","
              + ";".join(f"{k}={v}" for k, v in models.items()) + ","
              + ";".join(f"{k}={v}" for k, v in sorted(tools.items(), key=lambda x: -x[1])))
