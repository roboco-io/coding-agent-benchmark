#!/usr/bin/env python3
"""pi 세션 jsonl usage 집계 (EXP-029).
사용: python3 usage_pi.py <BASE> <run>...   → <BASE>/sessions-<run>/*.jsonl
- assistant message: responseId로 중복 제거(같은 ID·다른 usage면 오류 중단), responseId 없으면 entry id.
- type:"usage" 엔트리(cache_warm·compaction 등)는 entry id로 포함 (pi 문서상 세션 합계에 포함).
- pi usage 의미: input=비캐시 입력, cacheRead/cacheWrite 별도, reasoning은 output에 포함(totalTokens 검산).
- proxy = input + output + cacheWrite → 토큰 대리지표. 청구 비용 아님.
"""
import glob, json, os, sys
F = ("input", "output", "cacheRead", "cacheWrite", "reasoning")
base, runs = sys.argv[1], sys.argv[2:]
print("run,files,assistant_msgs,usage_entries,dup_skipped,missing_usage," + ",".join(F) + ",proxy")
for run in runs:
    seen, tot = {}, dict.fromkeys(F, 0)
    files = sorted(glob.glob(os.path.join(base, f"sessions-{run}", "**", "*.jsonl"), recursive=True))
    n_msg = n_use = dup = miss = 0
    for fp in files:
        for line in open(fp):
            e = json.loads(line)
            if e.get("type") == "message" and e["message"].get("role") == "assistant":
                m = e["message"]; u = m.get("usage")
                key = ("r", m.get("responseId") or f"{fp}:{e.get('id')}")
            elif e.get("type") == "usage":
                u = e.get("usage"); key = ("u", f"{fp}:{e.get('id')}")
            else:
                continue
            if u is None:
                miss += 1; continue
            v = tuple(u.get(k, 0) or 0 for k in F)
            if key in seen:
                if seen[key] != v:
                    sys.exit(f"usage 충돌: {run} {key} {seen[key]} != {v}")
                dup += 1; continue
            seen[key] = v
            if key[0] == "r": n_msg += 1
            else: n_use += 1
            for k, x in zip(F, v): tot[k] += x
    proxy = tot["input"] + tot["output"] + tot["cacheWrite"]
    print(f"{run},{len(files)},{n_msg},{n_use},{dup},{miss}," + ",".join(str(tot[k]) for k in F) + f",{proxy}")
