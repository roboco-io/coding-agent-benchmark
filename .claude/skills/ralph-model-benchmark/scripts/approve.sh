#!/bin/bash
# 사용: bash approve.sh "<사용자 답변 원문>"
# preflight 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 승인을 받은 뒤에만 실행한다(2026-10-10 사용자 지시).
# bench.env·model-specs.json·preflight-report.md의 해시와 답변 원문을 preflight-approved에 기록한다.
# smoke.sh·run-all.sh는 이 파일이 없거나 해시가 다르면(승인 뒤 설정 변경) 실행을 거부한다.
BASE="$(cd "$(dirname "$0")" && pwd)"
ANSWER="$1"
[ -n "$ANSWER" ] || { echo "사용자 답변 원문이 필요하다 (AskUserQuestion 결과)" >&2; exit 1; }
python3 "$BASE/preflight.py" "$BASE" >/dev/null; rc=$?
[ "$rc" = 1 ] && { echo "사양 누락 — 승인 불가. preflight-report.md 확인" >&2; exit 1; }
{
  echo "approved_at=$(date '+%F %T')"
  echo "preflight_exit=$rc"
  echo "answer=$ANSWER"
  echo "hash=$(cat "$BASE/bench.env" "$BASE/model-specs.json" "$BASE/preflight-report.md" | shasum -a 256 | cut -d' ' -f1)"
} > "$BASE/preflight-approved"
echo "승인 기록: $BASE/preflight-approved"
