#!/usr/bin/env python3
# EXP-026 usage 집계: run별 세션 jsonl, assistant message.id dedup (같은 ID usage 불일치 시 오류)
import json, glob, os, re, sys, collections, subprocess
from datetime import datetime as D
BASE = os.path.expanduser("~/ralph-exp026")
PROJ = os.path.expanduser("~/.claude/projects/-Users-dohyunjung-ralph-exp026-app-{}")
RUNS = ["en-1", "ko-1", "en-2", "ko-2", "en-3", "ko-3"]
KEYS = ["input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"]

def stats(run):
    ids, rows, models, tools, think, conflicts = {}, 0, collections.Counter(), collections.Counter(), 0, 0
    for p in glob.glob(PROJ.format(run) + "/**/*.jsonl", recursive=True):
        for line in open(p):
            try: d = json.loads(line)
            except Exception: continue
            m = d.get("message") or {}
            if d.get("type") != "assistant" or not m.get("id") or not m.get("usage"): continue
            rows += 1
            u = {k: m["usage"].get(k) or 0 for k in KEYS}
            if m["id"] in ids and ids[m["id"]] != u: conflicts += 1
            ids[m["id"]] = u
            models[m.get("model")] += 1
            for c in m.get("content", []):
                if isinstance(c, dict):
                    if c.get("type") == "tool_use": tools[c["name"]] += 1
                    if c.get("type") == "thinking": think += 1
    if conflicts: sys.exit(f"{run}: usage conflict on {conflicts} ids")
    tot = {k: sum(x[k] for x in ids.values()) for k in KEYS}
    return len(ids), rows - len(ids), tot, models, tools, think

def secs(run):
    t = open(f"{BASE}/ralph-run-{run}.log").read()
    s = re.findall(r"iteration \d+ start: (\S+ \S+)", t); e = re.findall(r"iteration \d+ end \(exit \d+\): (\S+ \S+)", t)
    return sum((D.fromisoformat(b) - D.fromisoformat(a)).total_seconds() for a, b in zip(s, e)), len(e)

print("run,iters,sec,api,dups,input,cache_create,cache_read,output,thinking_blocks,models,commits,tools")
for r in RUNS:
    if not os.path.exists(f"{BASE}/done-{r}"): continue
    api, dups, u, models, tools, think = stats(r)
    sec, it = secs(r)
    commits = subprocess.run(["git", "-C", f"{BASE}/app-{r}", "rev-list", "--count", "HEAD"], capture_output=True, text=True).stdout.strip()
    top = " · ".join(f"{k} {v}" for k, v in tools.most_common(4))
    print(f"{r},{it},{sec:.0f},{api},{dups},{u['input_tokens']},{u['cache_creation_input_tokens']},{u['cache_read_input_tokens']},{u['output_tokens']},{think},{'|'.join(models)},{commits},{top}")
