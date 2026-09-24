#!/bin/bash
# Phase 0 스모크: 조건별 모델 ID·인증·usage 기록 확인. 결과는 phase0.log, 세션은 본 계측에서 제외(삭제).
BASE="$(cd "$(dirname "$0")" && pwd)"
source "$BASE/bench.env"
OUT="$BASE/phase0.log"; mkdir -p "$BASE/smoke-tmp"
Q="Output exactly the string SMOKE-OK and nothing else."
fail=0
for c in $CONDITIONS; do
  m="${c#*:}"; echo "=== $m ($HARNESS) $(date '+%F %T') ===" >> "$OUT"
  case "$HARNESS" in
    codex) r=$(CODEX_HOME="$BASE/codex-home" codex exec --model "$m" ${EFFORT:+-c model_reasoning_effort="$EFFORT"} \
             --sandbox read-only --skip-git-repo-check -C "$BASE/smoke-tmp" "$Q" < /dev/null 2>&1) ;;
    pi) source "$BASE/pi_env.sh"
      r=$(cd "$BASE/smoke-tmp" && "$PI_BIN" -p -nc -ns -ne -np -na --session-dir "$BASE/smoke-tmp/sessions" \
          --model "$m" ${THINKING:+--thinking "$THINKING"} "$Q" < /dev/null 2>&1) ;;
    claude-native) r=$(cd "$BASE/smoke-tmp" && claude -p "$Q" --model "$m" --output-format json < /dev/null 2>&1) ;;
    claude-direct) source "$HOME/.zsh_secrets"
      r=$(cd "$BASE/smoke-tmp" && env -u ANTHROPIC_API_KEY CLAUDE_CONFIG_DIR="$BASE/claude-config" \
          ANTHROPIC_BASE_URL="$BASE_URL" ANTHROPIC_AUTH_TOKEN="${!AUTH_ENV}" ANTHROPIC_MODEL="$m" \
          ANTHROPIC_SMALL_FAST_MODEL="$m" ANTHROPIC_DEFAULT_HAIKU_MODEL="$m" \
          CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1 CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
          claude -p "$Q" --output-format json < /dev/null 2>&1) ;;
  esac
  echo "$r" | tail -20 >> "$OUT"
  if echo "$r" | grep -q 'SMOKE-OK' && ! echo "$r" | grep -qiE '"is_error":true|ERROR:'; then echo "PASS $m"; else echo "FAIL $m"; fail=1; fi
done
rm -rf "$BASE/smoke-tmp/sessions" "$BASE/codex-home/sessions" "$BASE/claude-config/projects"
exit $fail
