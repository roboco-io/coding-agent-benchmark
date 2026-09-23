#!/usr/bin/env python3
"""Codex rollout: token_count events carry info.total_token_usage (session-cumulative) and info.last_token_usage (per-request).
Verify: sum of distinct last_token_usage increments == final total (to detect duplicate token_count emissions)."""
import json,sys,glob,os
K=['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
def sess(p):
    evs=[]; model=set()
    for l in open(p):
        try:e=json.loads(l)
        except:continue
        pl=e.get('payload',e)
        if isinstance(pl,dict) and pl.get('model'): model.add(pl.get('model'))
        if isinstance(pl,dict) and pl.get('type')=='token_count' and pl.get('info'):
            evs.append(pl['info'])
    final=evs[-1]['total_token_usage'] if evs else None
    # sum increments only when total changes (repeated token_count with same total = duplicate emission)
    s=dict((k,0) for k in K); prev=None; n=0; dup=0; mono=True
    for i in evs:
        t=i['total_token_usage']
        if prev is not None and t==prev: dup+=1; continue
        if prev is not None and any(t.get(k,0)<prev.get(k,0) for k in K): mono=False
        n+=1
        for k in K: s[k]+=i['last_token_usage'].get(k,0)
        prev=t
    return dict(final=final,sum_last=s,requests=n,dup_events=dup,monotonic=mono,events=len(evs),models=sorted(model))
for d in sys.argv[1:]:
    for p in sorted(glob.glob(d+'/**/rollout-*.jsonl',recursive=True)):
        r=sess(p); print(d, os.path.basename(p)[:40], json.dumps(r))
