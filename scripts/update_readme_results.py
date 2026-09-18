#!/usr/bin/env python3
"""experiments/*/report.md를 스캔해 README(ko/en/ja/zh-CN)의 실험 결과 섹션을 재생성한다.

각 report.md의 구조화된 헤더를 파싱한다:
  # EXP-NNN 결과 보고: <제목>
  - 가설: [코드](...) — <가설 문장>
  - **판정: <판정>** — <핵심 요약>

대상 파일과 언어:
  README.ko.md (ko, 원문) · README.md (en) · README.ja.md (ja) · README.zh-CN.md (zh-CN)
각 파일의 <!-- RESULTS:BEGIN --> ~ <!-- RESULTS:END --> 사이를 교체한다.
영·일·중 번역은 scripts/readme_i18n.json에서 가져오며, 누락된 실험은 한국어 원문을 넣고 경고한다.

실험 종료(report.md 작성/수정) 시마다 실행: python3 scripts/update_readme_results.py
(git pre-commit 훅이 report.md 스테이징을 감지해 자동 실행하기도 한다)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- RESULTS:BEGIN -->", "<!-- RESULTS:END -->"
I18N_PATH = ROOT / "scripts" / "readme_i18n.json"
FILES = {
    "README.ko.md": "ko",
    "README.md": "en",
    "README.ja.md": "ja",
    "README.zh-CN.md": "zh-CN",
}
KO_LABELS = {
    "note": "이 블록은 scripts/update_readme_results.py가 experiments/*/report.md에서 자동 생성한다. 직접 수정 금지.",
    "headers": ["실험", "가설", "판정"],
    "report": "보고서",
}
FIELDS = ("name", "hypothesis", "verdict", "summary")


def parse_report(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (EXP-\d+) 결과 보고: (.+)$", text, re.M)
    hypo = re.search(r"^- 가설: \[([A-Z]-\d+)\][^—]*—\s*(.+)$", text, re.M)
    verdict = re.search(r"^-? ?\*\*판정: ([^*]+)\*\*\s*—\s*(.+)$", text, re.M)
    if not (title and verdict):
        print(f"경고: 헤더 파싱 실패, 건너뜀: {path}", file=sys.stderr)
        return None
    return {
        "id": title.group(1),
        "name": title.group(2).strip(),
        "hcode": hypo.group(1) if hypo else "?",
        "hypothesis": hypo.group(2).strip() if hypo else "",
        "verdict": verdict.group(1).strip(),
        "summary": verdict.group(2).strip(),
        "path": path.relative_to(ROOT).as_posix(),
    }


def localize(report: dict, lang: str, i18n: dict, missing: list[str]) -> dict:
    if lang == "ko":
        return report
    entry = i18n.get("experiments", {}).get(report["id"], {}).get(lang)
    if not entry:
        missing.append(report["id"])
        return report
    out = dict(report)
    for f in FIELDS:
        if entry.get(f):
            out[f] = entry[f]
    return out


def build_section(reports: list[dict], labels: dict) -> str:
    h = labels["headers"]
    lines = [
        BEGIN,
        f"<!-- {labels['note']} -->",
        "",
        f"| {h[0]} | {h[1]} | {h[2]} |",
        "|------|------|------|",
    ]
    for r in reports:
        lines.append(f"| [{r['id']}]({r['path']}) {r['name']} | {r['hcode']}: {r['hypothesis']} | **{r['verdict']}** |")
    lines.append("")
    for r in reports:
        lines.append(f"**{r['id']} — {r['name']}** ({r['verdict']})  ")
        lines.append(f"{r['summary']} → [{labels['report']}]({r['path']})")
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    reports = []
    for p in sorted(ROOT.glob("experiments/*/report.md")):
        r = parse_report(p)
        if r:
            reports.append(r)
    if not reports:
        print("report.md 없음 — README 변경 없음", file=sys.stderr)
        return 0
    i18n = json.loads(I18N_PATH.read_text(encoding="utf-8")) if I18N_PATH.exists() else {}
    rc = 0
    for fname, lang in FILES.items():
        readme = ROOT / fname
        if not readme.exists():
            print(f"건너뜀: {fname} 없음", file=sys.stderr)
            continue
        text = readme.read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            print(f"오류: {fname}에 {BEGIN}/{END} 마커가 없음", file=sys.stderr)
            rc = 1
            continue
        labels = KO_LABELS if lang == "ko" else i18n.get("labels", {}).get(lang, KO_LABELS)
        missing: list[str] = []
        localized = [localize(r, lang, i18n, missing) for r in reports]
        new = re.sub(
            re.escape(BEGIN) + r".*?" + re.escape(END),
            build_section(localized, labels).replace("\\", r"\\"),
            text,
            flags=re.S,
        )
        if new != text:
            readme.write_text(new, encoding="utf-8")
            print(f"{fname} 갱신: 실험 {len(reports)}건 반영")
        else:
            print(f"{fname} 변경 없음")
        if missing:
            print(f"경고: {fname}({lang}) 번역 누락 → 한국어 원문 사용: {', '.join(missing)} "
                  f"(scripts/readme_i18n.json에 추가할 것)", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
