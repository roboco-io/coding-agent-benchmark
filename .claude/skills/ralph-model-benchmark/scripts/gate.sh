# 실행 승인 게이트 (2026-10-10 사용자 지시): smoke.sh·run-all.sh가 source한다.
# preflight.py 보고서를 사용자에게 보여 주고 승인받아 approve.sh로 기록한 경우에만 통과한다.
require_approval() {
  local f="$BASE/preflight-approved" want have
  [ -f "$f" ] || { echo "거부: 실행 승인 없음 — python3 $BASE/preflight.py $BASE → 사용자 승인(AskUserQuestion) → bash $BASE/approve.sh \"<답변>\"" >&2; return 1; }
  want=$(sed -n 's/^hash=//p' "$f")
  have=$(cat "$BASE/bench.env" "$BASE/model-specs.json" "$BASE/preflight-report.md" 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
  [ "$want" = "$have" ] || { echo "거부: 승인 뒤 bench.env·model-specs.json·보고서가 바뀜 — preflight를 다시 실행하고 다시 승인받을 것" >&2; return 1; }
}
