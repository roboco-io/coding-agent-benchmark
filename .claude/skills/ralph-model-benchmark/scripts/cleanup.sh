#!/bin/bash
# 사용: bash cleanup.sh <BASE>   (예: ~/experiments/ralph-exp035)
# 실험 종료 후 재생성 가능한 대용량 요소만 지운다 (2026-10-08 도입, 전체 용량의 약 95%).
#   삭제: app 안의 node_modules (lockfile이 있을 때만 — `npm ci`로 같은 버전 재설치 가능),
#         격리 HOME의 패키지 매니저 캐시(.npm, .cache, Library/Caches 등. Library 본체·.gemini 등 앱 상태는 보존)
#   보존: 산출 코드·.git·lockfile·SQLite DB, 세션 로그, run 로그, metrics, 하네스 스크립트, recheck.csv
# 재채점이 필요하면 해당 app에서 `npm ci` 후 measure.sh를 실행한다.
set -euo pipefail
BASE="$(cd "$1" && pwd)"
case "$BASE" in "$HOME"/experiments/ralph-exp*) ;; *) echo "대상이 ~/experiments/ralph-exp* 가 아님: $BASE" >&2; exit 1 ;; esac
[ -e "$BASE/done-all" ] || [ "${CLEANUP_LEGACY:-0}" = 1 ] || { echo "done-all 없음 — 실험이 끝나지 않았거나 기록이 없음 (과거 실험은 CLEANUP_LEGACY=1)" >&2; exit 1; }
pgrep -f "$BASE/(driver|run-all)\.sh" >/dev/null && { echo "실행 중인 run이 있음" >&2; exit 1; }

LOG="$BASE/cleanup.log"
before=$(du -sk "$BASE" | cut -f1)
echo "=== cleanup $(date '+%F %T') before=${before}KB ===" >> "$LOG"
locks="package-lock.json pnpm-lock.yaml yarn.lock bun.lock bun.lockb"
# node_modules: 바깥쪽 것만(-prune), 심볼릭 링크는 따라가지 않음
while IFS= read -r -d '' nm; do
  app="$(dirname "$nm")"; ok=0
  for l in $locks; do [ -f "$app/$l" ] && ok=1; done
  if [ "$ok" = 1 ]; then
    echo "rm node_modules: ${app#$BASE/} ($(du -sk "$nm" | cut -f1)KB)" >> "$LOG"; rm -rf "$nm"
  else
    echo "keep node_modules (lockfile 없음): ${app#$BASE/}" >> "$LOG"
  fi
done < <(find "$BASE" -type d -name node_modules -prune -print0)
# 격리 HOME(agy-home, codex-home, claude-config, pi-agent 등)의 패키지 캐시
for h in "$BASE"/*-home "$BASE"/claude-config "$BASE"/pi-agent; do
  [ -d "$h" ] || continue
  for c in .npm .cache .bun/install/cache .pnpm-store Library/Caches; do
    [ -e "$h/$c" ] && { echo "rm cache: ${h#$BASE/}/$c ($(du -sk "$h/$c" | cut -f1)KB)" >> "$LOG"; rm -rf "${h:?}/$c"; }
  done
done
after=$(du -sk "$BASE" | cut -f1)
echo "=== done after=${after}KB freed=$(( (before-after)/1024 ))MB ===" >> "$LOG"
echo "$(basename "$BASE"): $((before/1024))MB -> $((after/1024))MB"
