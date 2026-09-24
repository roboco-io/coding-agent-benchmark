#!/bin/bash
# 사용: bash driver.sh <run>   (run = <조건>-<언어>-<n>, 예: sol-en-1)
# 랄프 루프 1 run: iteration마다 에이전트 1회 호출 → measure.sh 채점 → .ralph-done 게이트.
# EXP-029(pi)·EXP-011/021(codex)·EXP-025(claude-direct)·EXP-026(claude-native) driver의 공통형.
RUN="$1"
BASE="$(cd "$(dirname "$0")" && pwd)"
source "$BASE/bench.env"
COND="${RUN%%-*}"; REST="${RUN#*-}"; LANG_="${REST%%-*}"
MODEL=""
for c in $CONDITIONS; do [ "${c%%:*}" = "$COND" ] && MODEL="${c#*:}"; done
[ -n "$MODEL" ] || { echo "unknown condition $COND ($RUN)" >> "$BASE/driver.log"; exit 1; }
PROMPT="$BASE/PROMPT-$LANG_.md"
[ -f "$PROMPT" ] || { echo "unknown lang $LANG_ ($RUN)" >> "$BASE/driver.log"; exit 1; }

REPO="$BASE/app-$RUN"; MET="$BASE/metrics-$RUN.csv"; LOG="$BASE/ralph-run-$RUN.log"
[ -f "$BASE/done-$RUN" ] && exit 0

invoke_agent() {
  case "$HARNESS" in
    codex)
      CODEX_HOME="$BASE/codex-home" codex exec --model "$MODEL" \
        ${EFFORT:+-c model_reasoning_effort="$EFFORT"} \
        --sandbox danger-full-access --skip-git-repo-check -C "$REPO" \
        "$(cat "$REPO/PROMPT.md")" ;;
    pi)
      source "$BASE/pi_env.sh"
      "$PI_BIN" -p -nc -ns -ne -np -na --session-dir "$BASE/sessions-$RUN" \
        --model "$MODEL" ${THINKING:+--thinking "$THINKING"} "$(cat "$REPO/PROMPT.md")" ;;
    claude-native)
      claude -p "$(cat "$REPO/PROMPT.md")" --model "$MODEL" --dangerously-skip-permissions ;;
    claude-direct)
      source "$HOME/.zsh_secrets"
      env -u ANTHROPIC_API_KEY \
        CLAUDE_CONFIG_DIR="$BASE/claude-config" \
        ANTHROPIC_BASE_URL="$BASE_URL" \
        ANTHROPIC_AUTH_TOKEN="${!AUTH_ENV}" \
        ANTHROPIC_MODEL="$MODEL" ANTHROPIC_SMALL_FAST_MODEL="$MODEL" ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL" \
        CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1 \
        CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
        CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
        API_TIMEOUT_MS=600000 \
        claude -p "$(cat "$REPO/PROMPT.md")" --dangerously-skip-permissions ;;
  esac
}

mkdir -p "$REPO"
cp "$PROMPT" "$REPO/PROMPT.md"
git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || git -C "$REPO" init -q
cd "$REPO" || exit 1
DONE_ITER=$(grep -c '^[0-9]' "$MET" 2>/dev/null | head -1)
DONE_ITER=${DONE_ITER:-0}
START=$(date +%s)
echo "=== RUN $RUN ($HARNESS $MODEL, $(basename "$PROMPT")) start: $(date '+%F %T') ===" >> "$BASE/driver.log"
for i in $(seq $((DONE_ITER + 1)) "$MAX_ITER"); do
  if [ $(( $(date +%s) - START )) -gt "$MAX_SEC" ]; then
    echo "=== [$RUN] wall-clock cap ${MAX_SEC}s reached before iteration $i: $(date '+%F %T') ===" >> "$LOG"
    echo "timeout,$(date '+%F %T')" >> "$MET"
    break
  fi
  echo "=== [$RUN] iteration $i start: $(date '+%F %T') ===" >> "$LOG"
  invoke_agent < /dev/null >> "$LOG" 2>&1
  EXIT=$?
  echo "=== [$RUN] iteration $i end (exit $EXIT): $(date '+%F %T') ===" >> "$LOG"
  RESULT=$(bash "$BASE/measure.sh" "$REPO")
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
  # metrics 열: iter,종료시각,exit,성공 hurl 파일 수,실행 요청 수,완료 선언,게이트
  echo "$i,$(date '+%F %T'),$EXIT,$RESULT,$CLAIM,$GATE" >> "$MET"
  [ -f "$REPO/.ralph-done" ] && break
done
touch "$BASE/done-$RUN"
echo "=== RUN $RUN finished: $(date '+%F %T') | $(tail -1 "$MET") ===" >> "$BASE/driver.log"
