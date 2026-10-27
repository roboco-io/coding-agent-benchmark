#!/usr/bin/env python3
"""Codex rollout usage per run: 각 rollout(=iteration 1회 세션)의 마지막 total_token_usage(세션 누계)를 취해 run 내 합산.
사용: python3 usage_codex.py <BASE> <run> [...]  → CSV
input은 캐시 포함 누계, cached는 그중 캐시 히트, reasoning은 output에 포함(재가산 금지).
aggregate_tokens.py(Claude message.id dedup)는 Codex 누계를 거부하므로 Codex는 이 스크립트를 쓴다.
"""
import json, sys
from pathlib import Path
F = ['input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens']
base = Path(sys.argv[1])
print('run,sessions,missing,' + ','.join(F))
for run in sys.argv[2:]:
    tot = dict.fromkeys(F, 0); n = miss = 0
    for p in sorted((base / f'sessions-{run}').rglob('rollout-*.jsonl')):
        last = None
        for line in p.open():
            if '"total_token_usage"' not in line:
                continue
            info = (json.loads(line).get('payload') or {}).get('info') or {}
            last = info.get('total_token_usage') or last
        n += 1
        if last is None:
            miss += 1; continue
        for k in F:
            tot[k] += last.get(k, 0) or 0
    print(f'{run},{n},{miss},' + ','.join(str(tot[k]) for k in F))
