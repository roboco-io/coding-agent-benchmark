#!/bin/bash
# Phase 0 스모크: 조건별 모델 ID·인증·usage 기록 확인. 결과는 phase0.log, 세션은 본 계측에서 제외(삭제).
BASE="$(cd "$(dirname "$0")" && pwd)"
source "$BASE/bench.env"
OUT="$BASE/phase0.log"; mkdir -p "$BASE/smoke-tmp"
Q="Output exactly the string SMOKE-OK and nothing else."
fail=0
for v in PRICE_IN PRICE_OUT RUN_BUDGET_USD EXP_BUDGET_USD; do
  [ -n "${!v:-}" ] || { echo "FAIL $v 미설정 — 비용 상한 없이 기동 금지 (EXP-042)" | tee -a "$OUT"; fail=1; }
done
# 채점 교란 방지 (EXP-029 D-1: VS Code Live Preview가 127.0.0.1:3000 점유 → 거짓 음성)
busy=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $1" "$9}' | grep -E ':3[0-9]{3}$')
[ -n "$busy" ] && { echo "INFO 3000번대 포트 외부 LISTEN — 종료 불필요. 하네스는 빈 포트(PORT)를 주입하고 리포 소속 프로세스의 포트로만 채점한다. PORT를 무시하고 이 포트에 고정 바인딩한 앱은 기동 실패로 기각될 수 있다(산출물 결함, 부검 시 확인):"; echo "$busy"; } | tee -a "$OUT"
for c in $CONDITIONS; do
  m="${c#*:}"; echo "=== $m ($HARNESS) $(date '+%F %T') ===" >> "$OUT"
  case "$HARNESS" in
    codex) r=$(CODEX_HOME="$BASE/codex-home" codex exec --model "$m" ${EFFORT:+-c model_reasoning_effort="$EFFORT"} \
             --sandbox read-only --skip-git-repo-check -C "$BASE/smoke-tmp" "$Q" < /dev/null 2>&1) ;;
    pi) source "$BASE/pi_env.sh"
      r=$(cd "$BASE/smoke-tmp" && "$PI_BIN" -p -nc -ns -ne -np -na --session-dir "$BASE/smoke-tmp/sessions" \
          --model "$m" ${THINKING:+--thinking "$THINKING"} "$Q" < /dev/null 2>&1) ;;
    agy) source "$BASE/agy_env.sh"
      r=$(cd "$BASE/smoke-tmp" && agy_run -p "$Q" --model "$m" ${EFFORT:+--effort "$EFFORT"} --output-format json < /dev/null 2>&1) ;;
    claude-native) r=$(cd "$BASE/smoke-tmp" && env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
          claude -p "$Q" --model "$m" --output-format json < /dev/null 2>&1)
      # 구독 인증 확인 (EXP-037: API 키 혼입으로 apiKeySource=ANTHROPIC_API_KEY)
      echo "$r" | grep -q '"apiKeySource":"none"' || { echo "FAIL $m — 구독 인증 아님: $(echo "$r" | grep -o '"apiKeySource":"[^"]*"')"; fail=1; } ;;
    claude-direct) source "$HOME/.zsh_secrets"
      r=$(cd "$BASE/smoke-tmp" && env -u ANTHROPIC_API_KEY CLAUDE_CONFIG_DIR="$BASE/claude-config" \
          ANTHROPIC_BASE_URL="$BASE_URL" ANTHROPIC_AUTH_TOKEN="${!AUTH_ENV}" ANTHROPIC_MODEL="$m" \
          ANTHROPIC_SMALL_FAST_MODEL="$m" ANTHROPIC_DEFAULT_HAIKU_MODEL="$m" \
          CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1 CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
          claude -p "$Q" --output-format json < /dev/null 2>&1)
      # usage 정확도: tool_result 토큰을 입력 usage에서 빠뜨리는 엔드포인트는 자동 압축을 무력화해 비용이 폭증한다 (EXP-042 D-1)
      p=$(env "$AUTH_ENV=${!AUTH_ENV}" python3 "$BASE/usage_probe.py" "$BASE_URL" "$m" "$AUTH_ENV" 2>&1)
      echo "$p" | tee -a "$OUT"; echo "$p" | grep -q '^PASS' || fail=1 ;;
  esac
  echo "$r" | tail -20 >> "$OUT"
  if echo "$r" | grep -q 'SMOKE-OK' && ! echo "$r" | grep -qiE '"is_error":true|ERROR:|"status":"ERROR"'; then echo "PASS $m"; else echo "FAIL $m"; fail=1; fi
done
[ "$HARNESS" = agy ] && { source "$BASE/agy_env.sh"; agy_reset_home; }
rm -rf "$BASE/smoke-tmp/sessions" "$BASE/codex-home/sessions" "$BASE/claude-config/projects"
exit $fail
