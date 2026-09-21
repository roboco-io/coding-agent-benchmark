#!/bin/bash
# EXP-025: Claude Code x DeepSeek 직결(ANTHROPIC_BASE_URL) 랄프 루프 — EXP-020 driver 이식
# 변경점: BASE 경로, 모델 ID·PROMPT를 RUN 이름(<flash|pro>-<en|ko>-N)에서 유도, run당 wall-clock 상한 4시간 추가
RUN="$1"
source "$HOME/.zsh_secrets"
BASE="$HOME/ralph-exp025"
MAX_ITER=30
MAX_SEC=14400
case "$RUN" in
  flash-*) MODEL=deepseek-flash ;;
  pro-*)   MODEL=deepseek-v4-pro ;;
  *) echo "unknown run $RUN" >> "$BASE/driver.log"; exit 1 ;;
esac
case "$RUN" in
  *-en-*) PROMPT="$BASE/PROMPT-en.md" ;;
  *-ko-*) PROMPT="$BASE/PROMPT-ko.md" ;;
  *) echo "unknown lang $RUN" >> "$BASE/driver.log"; exit 1 ;;
esac

REPO="$BASE/app-$RUN"; MET="$BASE/metrics-$RUN.csv"; LOG="$BASE/ralph-run-$RUN.log"
[ -f "$BASE/done-$RUN" ] && exit 0
[ -n "$DEEPSEEK_API_KEY" ] || { echo "DEEPSEEK_API_KEY missing" >> "$BASE/driver.log"; exit 1; }
mkdir -p "$REPO"
cp "$PROMPT" "$REPO/PROMPT.md"
git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || git -C "$REPO" init -q
cd "$REPO" || exit 1
DONE_ITER=$(grep -c '^[0-9]' "$MET" 2>/dev/null | head -1)
DONE_ITER=${DONE_ITER:-0}
START=$(date +%s)
echo "=== RUN $RUN (direct $MODEL, $(basename "$PROMPT")) start: $(date '+%F %T') ===" >> "$BASE/driver.log"
for i in $(seq $((DONE_ITER + 1)) $MAX_ITER); do
  if [ $(( $(date +%s) - START )) -gt $MAX_SEC ]; then
    echo "=== [$RUN] wall-clock cap ${MAX_SEC}s reached before iteration $i: $(date '+%F %T') ===" >> "$LOG"
    echo "timeout,$(date '+%F %T')" >> "$MET"
    break
  fi
  echo "=== [$RUN] iteration $i start: $(date '+%F %T') ===" >> "$LOG"
  env -u ANTHROPIC_API_KEY \
    CLAUDE_CONFIG_DIR="$BASE/claude-config" \
    ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic \
    ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY" \
    ANTHROPIC_MODEL="$MODEL" \
    ANTHROPIC_SMALL_FAST_MODEL="$MODEL" \
    ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL" \
    CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1 \
    CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
    API_TIMEOUT_MS=600000 \
    claude -p "$(cat "$REPO/PROMPT.md")" --dangerously-skip-permissions \
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
