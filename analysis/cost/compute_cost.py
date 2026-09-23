#!/usr/bin/env python3
"""run별 토큰(usage_all_runs.csv) × 공개 단가(prices.json) → cost_all_runs.csv.
결과는 공개 단가 환산 추정치이며 실제 청구액이 아니다(구독·OAuth·프리뷰 실행 포함)."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "prices.json")))
f = lambda v: None if v in ("", "null", None) else float(v)

def cost(r):
    p = P.get(r["model"])
    if not p:
        return None  # 공개 단가 없음(Solar Open 2)
    c = f(r["input_uncached"]) * p["input"] + f(r["cache_read"]) * p["cache_read"] + f(r["output"]) * p["output"]
    w5, w1, wu = (f(r[k]) or 0 for k in ("cache_write_5m", "cache_write_1h", "cache_write_unsplit"))
    c += w5 * (p["cache_write_5m"] if p["cache_write_5m"] is not None else p["input"])
    c += w1 * (p["cache_write_1h"] if p["cache_write_1h"] is not None else (p["cache_write_5m"] or p["input"]))
    c += wu * (p["cache_write_1h"] or p["cache_write_5m"] or p["input"])
    return round(c / 1e6, 4)

rows = list(csv.DictReader(open(os.path.join(HERE, "usage_all_runs.csv"))))
for r in rows:
    r["est_cost_usd"] = cost(r)
with open(os.path.join(HERE, "cost_all_runs.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} runs → cost_all_runs.csv")
