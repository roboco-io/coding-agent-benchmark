#!/usr/bin/env python3
"""실행 전 모델 사양·과금 점검과 사용자 승인 게이트 (2026-10-10 사용자 지시).

사용: python3 preflight.py <BASE>
  입력: <BASE>/bench.env, <BASE>/model-specs.json, <BASE>/reference-profile.json
  출력: <BASE>/preflight-report.md (사용자에게 그대로 보여 줄 보고서), 표준 출력 요약
  종료 코드: 0 = 사양 완비·전 조건 적합, 2 = 사양 완비·부적합 조건 있음(사용자가 명시적으로 승인해야 진행),
            1 = 사양 누락(진행 불가)
승인: 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 물은 뒤, 사용자가 진행을 고른 경우에만
      bash <BASE>/approve.sh "<사용자 답변 원문>" 를 실행한다. smoke.sh·run-all.sh는 승인 파일이 없거나
      bench.env·model-specs.json이 승인 뒤 바뀌었으면 실행을 거부한다.

model-specs.json 형식 (키 = CONDITIONS의 모델 ID):
{
  "<모델 ID>": {
    "provider": "제공자·엔드포인트",
    "context_window": 정수(입력+출력 컨텍스트 또는 입력 한도 토큰 수),
    "max_output": 정수,
    "context_source": "출처 URL 또는 '직접 측정 <방법>'",
    "billing": "api" | "subscription",
    "pricing": {"input": 100만 토큰당 USD, "output": ..., "cache_read": 숫자 또는 null,
                "tiers": [[입력 상한 토큰, 입력 단가, 출력 단가], ...] (구간 단가 없으면 []),
                "source": "출처 URL", "checked_at": "YYYY-MM-DD"}
  }
}
"""
import json, os, re, shlex, subprocess, sys

BASE = sys.argv[1]


def load_env(path):
    out = subprocess.run(["bash", "-c", f"set -a; source {shlex.quote(path)}; env -0"],
                         capture_output=True, check=True).stdout.decode()
    return dict(x.split("=", 1) for x in out.split("\0") if "=" in x)


env = load_env(os.path.join(BASE, "bench.env"))
ref = json.load(open(os.path.join(BASE, "reference-profile.json")))
specs_path = os.path.join(BASE, "model-specs.json")
problems = []
specs = {}
if not os.path.exists(specs_path):
    problems.append("model-specs.json 없음 — 각 모델의 입력 한도·과금 체계를 조사해 작성해야 한다")
else:
    specs = json.load(open(specs_path))

conds = [c.split(":", 1) for c in env.get("CONDITIONS", "").split()]
langs = env.get("LANGS", "en").split()
n = int(env.get("N", "3"))
runs_per_cond = len(langs) * n
fit = ref["fit_rule"]; mp = ref["max_prompt_tokens"]; ti = ref["total_input_tokens_per_run"]; to = ref["output_tokens_per_run"]


def tier_price(p, tokens):
    for lim, pi_, po in sorted(p.get("tiers") or []):
        if tokens <= lim:
            return pi_, po
    t = sorted(p.get("tiers") or [])
    return (t[-1][1], t[-1][2]) if t else (p["input"], p["output"])


rows = []; unfit = []
for cond, model in conds:
    s = specs.get(model) or specs.get(model.split("/", 1)[-1])
    if not s:
        problems.append(f"{model}: model-specs.json 항목 없음"); continue
    p = s.get("pricing") or {}
    for k in ("provider", "context_window", "max_output", "context_source", "billing"):
        if s.get(k) in (None, ""):
            problems.append(f"{model}: {k} 누락")
    for k in ("input", "output", "source", "checked_at"):
        if p.get(k) in (None, ""):
            problems.append(f"{model}: pricing.{k} 누락")
    if p.get("checked_at") and not re.match(r"\d{4}-\d{2}-\d{2}$", str(p["checked_at"])):
        problems.append(f"{model}: pricing.checked_at 형식 오류")
    if any(x.startswith(model) for x in problems):
        continue
    ctx = int(s["context_window"])
    verdict = "적합" if ctx >= fit["recommended_context_tokens"] else ("주의" if ctx >= fit["min_context_tokens"] else "부적합")
    if verdict == "부적합":
        unfit.append(model)
    # 비용 추정: 캐시 할인 없이(보수적) 과거 완주 run의 총 입력·출력, 입력은 p90 최대 프롬프트 구간 단가 적용
    pin, pout = tier_price(p, mp["p90"])
    est = lambda i, o: (i * pin + o * pout) / 1e6
    rows.append(dict(cond=cond, model=model, provider=s["provider"], ctx=ctx, maxo=s["max_output"],
                     verdict=verdict, billing=s["billing"], p=p, p50=est(ti["p50"], to["p50"]),
                     p90=est(ti["p90"], to["p90"]), ctx_src=s["context_source"]))

rb = float(env.get("RUN_BUDGET_USD") or 0); eb = float(env.get("EXP_BUDGET_USD") or 0)
total_runs = len(conds) * runs_per_cond
L = ["# 실행 전 점검 보고서 (preflight)", "",
     f"- 하네스: `{BASE}` · HARNESS `{env.get('HARNESS')}` · 조건 {len(conds)}개 × 언어 {len(langs)} × n={n} = run {total_runs}개",
     f"- 상한: run당 {int(env.get('MAX_SEC', 0)) // 60}분 · 비용 run당 ${rb:g} · 실험 ${eb:g} → **최악 총액 ${min(eb, rb * total_runs):g}** (상한이 강제되는 경우)",
     f"- 적합성 기준: 입력 컨텍스트 {fit['recommended_context_tokens']:,} 이상 적합, {fit['min_context_tokens']:,} 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 {mp['p50']:,} · p90 {mp['p90']:,} · 최대 {mp['max']:,} 토큰 ({ref['max_prompt_runs']} run, {ref['measured_at']} 측정)",
     ""]
if rows:
    L += ["| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        p = r["p"]; tiers = ", ".join(f"≤{t[0] // 1000}K ${t[1]}/${t[2]}" for t in sorted(p.get("tiers") or [])) or "없음"
        L.append(f"| {r['cond']} | `{r['model']}` | {r['provider']} | {r['ctx']:,} | {r['maxo']:,} | **{r['verdict']}** | {r['billing']} | ${p['input']}/${p['output']} | {tiers} | ${r['p50']:.2f} / ${r['p90']:.2f} |")
    L += ["", "- run당 추정은 과거 완주 run의 총 입력(p50 {:,} · p90 {:,})과 출력(p50 {:,} · p90 {:,})에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.".format(ti["p50"], ti["p90"], to["p50"], to["p90"]),
          f"- 실험 전체 추정(p50 기준): ${sum(r['p50'] for r in rows) * runs_per_cond:.2f} · p90 기준: ${sum(r['p90'] for r in rows) * runs_per_cond:.2f}",
          "- 출처: " + "; ".join(f"`{r['model']}` 컨텍스트 {r['ctx_src']}, 단가 {r['p']['source']} ({r['p']['checked_at']} 확인)" for r in rows)]
if unfit:
    L += ["", f"**부적합 조건: {', '.join(unfit)}** — 입력 한도가 이 과제의 최대 프롬프트 범위보다 작다. 진행하면 자동 압축에 의존하게 되고, 압축이 늦거나 usage 보고가 틀리면 입력 한도 오류가 반복된다(EXP-042)."]
if problems:
    L += ["", "**사양 누락 — 진행 불가**", *[f"- {x}" for x in problems]]
L += ["", "다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh \"<답변 원문>\"`을 실행한다."]
open(os.path.join(BASE, "preflight-report.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
sys.exit(1 if problems else (2 if unfit else 0))
