#!/bin/bash
# EXP-026: Opus 5.5 네이티브 랄프 루프 EN/KO — EXP-023 driver 이식
# 변경점: BASE 경로, PROMPT를 RUN 이름(<en|ko>-N)에서 유도, run당 wall-clock 상한 4시간(EXP-025와 동일)
# 비격리(기본 ~/.claude) — EXP-009/010/023 네이티브 기준선과 동일 조건 (OAuth 키체인 제약)
RUN="$1"
BASE="$HOME/ralph-exp026"
MODEL="claude-opus-5-5"
MAX_ITER=10
MAX_SEC=14400
case "$RUN" in
  en-*) PROMPT="$BASE/PROMPT-en.md" ;;
  ko-*) PROMPT="$BASE/PROMPT-ko.md" ;;
  *) echo "unknown run $RUN" >> "$BASE/driver.log"; exit 1 ;;
esac
REPO="$BASE/app-$RUN"; MET="$BASE/metrics-$RUN.csv"; LOG="$BASE/ralph-run-$RUN.log"
[ -f "$BASE/done-$RUN" ] && exit 0
mkdir -p "$REPO"
cp "$PROMPT" "$REPO/PROMPT.md"
git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || git -C "$REPO" init -q
cd "$REPO" || exit 1
DONE_ITER=$(grep -c '^[0-9]' "$MET" 2>/dev/null | head -1)
DONE_ITER=${DONE_ITER:-0}
START=$(date +%s)
echo "=== RUN $RUN ($MODEL, $(basename "$PROMPT")) start: $(date '+%F %T') ===" >> "$BASE/driver.log"
for i in $(seq $((DONE_ITER + 1)) $MAX_ITER); do
  if [ $(( $(date +%s) - START )) -gt $MAX_SEC ]; then
    echo "=== [$RUN] wall-clock cap ${MAX_SEC}s reached before iteration $i: $(date '+%F %T') ===" >> "$LOG"
    echo "timeout,$(date '+%F %T')" >> "$MET"
    break
  fi
  echo "=== [$RUN] iteration $i start: $(date '+%F %T') ===" >> "$LOG"
  claude -p "$(cat "$REPO/PROMPT.md")" --model "$MODEL" --dangerously-skip-permissions \
    < /dev/null >> "$LOG" 2>&1
  EXIT=$?
  echo "=== [$RUN] iteration $i end (exit $EXIT): $(date '+%F %T') ===" >> "$LOG"
  RESULT=$("$BASE/measure.sh" "$REPO")
  CLAIM=0; [ -f "$REPO/.ralph-done" ] && CLAIM=1
  GATE=na
  if [ "$CLAIM" = 1 ]; then
    if [ "${RESULT%%,*}" = "13" ]; then
      GATE=pass
    else
      GATE=rejected
      rm -f "$REPO/.ralph-done"
      echo "=== [$RUN] GATE 기각 (hurl $RESULT) iter $i ===" >> "$LOG"
    fi
  fi
  echo "$i,$(date '+%F %T'),$EXIT,$RESULT,$CLAIM,$GATE" >> "$MET"
  [ -f "$REPO/.ralph-done" ] && break
done
touch "$BASE/done-$RUN"
echo "=== RUN $RUN finished: $(date '+%F %T') | $(tail -1 "$MET") ===" >> "$BASE/driver.log"
