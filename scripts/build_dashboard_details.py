#!/usr/bin/env python3
"""대시보드 성능 매트릭스 아코디언용 실험 상세 데이터(dashboard/details.js)를 생성한다.

입력:
  - experiments/*/report.md 헤더(한국어 가설·클라이언트·판정·요약) + scripts/readme_i18n.json(영·일·중)
  - analysis/cost/cost_all_runs.csv (run별 토큰·비용)
  - analysis/dashboard-details/EXP-NNN.json (조건·편차·행동·run별 iteration/커밋, 4개 언어)
출력: dashboard/details.js — window.DETAILS = { "<매트릭스 모델명>": [ {실험}, ... ] }
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from update_readme_results import parse_report  # noqa: E402

CLIENT_LANG = {"ko": None, "en": "en", "ja": "ja", "zh": "zh-CN"}
LANGS = {"ko": None, "en": "en", "ja": "ja", "zh": "zh-CN"}  # 대시보드 키 → i18n 키
DETAIL_DIR = ROOT / "analysis/dashboard-details"


def row_name(r: dict) -> str:
    """cost CSV 행 → 대시보드 매트릭스 모델명 (pi 하네스는 'pi × ' 접두)."""
    return ("pi × " + r["model"]) if r["harness"].startswith("pi") else r["model"]


def num(v: str):
    if v in ("", None):
        return None
    f = float(v)
    return int(f) if f.is_integer() else f


def main() -> int:
    i18n = json.loads((ROOT / "scripts/readme_i18n.json").read_text(encoding="utf-8"))["experiments"]
    reports = {}
    for p in sorted(ROOT.glob("experiments/*/report.md")):
        rep = parse_report(p)
        if rep:
            reports[rep["id"]] = rep

    groups: dict[tuple[str, str], list[dict]] = {}
    for r in csv.DictReader(open(ROOT / "analysis/cost/cost_all_runs.csv", encoding="utf-8")):
        groups.setdefault((row_name(r), r["exp"]), []).append(r)

    errors, out = [], {}
    for (name, exp), rows in groups.items():
        dpath = DETAIL_DIR / f"{exp}.json"
        if not dpath.exists():
            errors.append(f"{exp}: {dpath.name} 없음")
            continue
        det = json.loads(dpath.read_text(encoding="utf-8"))
        rep = reports.get(exp)
        if not rep:
            errors.append(f"{exp}: report.md 헤더 없음")
            continue
        text = {}
        for k, ik in LANGS.items():
            src = rep if ik is None else i18n.get(exp, {}).get(ik)
            if not src:
                errors.append(f"{exp}: i18n {ik} 누락")
                src = rep
            text[k] = {f: src[f] for f in ("name", "hypothesis", "verdict", "summary")}
        if det.get("client") != rep["client"]:
            errors.append(f"{exp}: client 불일치 json={det.get('client')!r} report={rep['client']!r}")
        terms_all = json.loads((ROOT / "scripts/readme_i18n.json").read_text(encoding="utf-8"))["labels"]
        client = {}
        for k, ik in CLIENT_LANG.items():
            c = rep["client"]
            for ko_term, tr in ((terms_all.get(ik) or {}).get("client_terms", {})).items():
                c = c.replace(ko_term, tr)
            client[k] = c
        for sec in ("conditions", "deviations", "behavior"):
            lens = {k: len(det.get(sec, {}).get(k, [])) for k in LANGS}
            if len(set(lens.values())) != 1:
                errors.append(f"{exp}: {sec} 언어별 항목 수 불일치 {lens}")
        runs = []
        for r in rows:
            meta = det.get("runs", {}).get(r["run_id"])
            if meta is None:
                errors.append(f"{exp}: runs에 {r['run_id']} 없음")
                meta = {}
            cw = sum(num(r[c]) or 0 for c in ("cache_write_5m", "cache_write_1h", "cache_write_unsplit"))
            runs.append({
                "run": r["run_id"], "lang": r["lang"], "iter": meta.get("iter"), "commits": meta.get("commits"),
                "time": num(r["time_min"]), "input": num(r["input_uncached"]), "cacheRead": num(r["cache_read"]),
                "cacheWrite": cw, "output": num(r["output"]), "requests": num(r["unique_requests"]),
                "usd": num(r["est_cost_usd"]),
            })
        out.setdefault(name, []).append({
            "exp": exp, "date": det.get("date"), "report": det.get("report") or rep["path"],
            "hcode": rep["hcode"], "client": client, "text": text, "runs": runs,
            "conditions": det.get("conditions", {}), "deviations": det.get("deviations", {}),
            "behavior": det.get("behavior", {}),
        })

    for v in out.values():
        v.sort(key=lambda e: e["exp"])
    if errors:
        print("\n".join("오류: " + e for e in errors), file=sys.stderr)
        return 1
    js = ("/* 자동 생성: scripts/build_dashboard_details.py — 직접 수정 금지 */\n"
          "window.DETAILS = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (ROOT / "dashboard/details.js").write_text(js, encoding="utf-8")
    print(f"dashboard/details.js: 모델 {len(out)}개, 실험 블록 {sum(len(v) for v in out.values())}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
