#!/bin/bash
# 사용: bash setup.sh <bench.env>
# $HOME/experiments/ralph-exp$EXP 하네스를 만든다: 정본 PROMPT·Hurl 복사+해시 검증, 스크립트 동결 복사, 격리 설정 디렉터리 생성.
set -euo pipefail
CFG="$1"; SKILL="$(cd "$(dirname "$0")/.." && pwd)"
source "$CFG"
BASE="$HOME/experiments/ralph-exp$EXP"
# 비용 상한 필수 (EXP-042: 사후 집계 상한만 두어 2 run에 약 $92 과금). 구독 실행(claude-native·codex OAuth)은 단가 0을 명시한다.
for v in RUN_BUDGET_USD EXP_BUDGET_USD MODEL_SPECS; do
  [ -n "${!v:-}" ] || { echo "$v 미설정 — 비용 상한과 모델 사양 파일은 필수 (bench.env.example 참조)" >&2; exit 1; }
done
[ -f "$MODEL_SPECS" ] || { echo "MODEL_SPECS 파일 없음: $MODEL_SPECS — 모델별 입력 한도·과금 체계를 조사해 작성 (preflight.py 주석의 형식)" >&2; exit 1; }
NRUNS=$(( $(echo $CONDITIONS | wc -w) * $(echo $LANGS | wc -w) * N ))
echo "비용 상한: run당 \$$RUN_BUDGET_USD, 실험 \$$EXP_BUDGET_USD (run ${NRUNS}개, 최악 run당 상한×run 수 = \$$(awk -v a="$RUN_BUDGET_USD" -v n="$NRUNS" 'BEGIN{print a*n}'))"
[ -e "$BASE/done-all" ] && { echo "이미 완료된 하네스: $BASE" >&2; exit 1; }
mkdir -p "$BASE"
cp "$CFG" "$BASE/bench.env"
cp "$MODEL_SPECS" "$BASE/model-specs.json"
cp "$SKILL/assets/reference-profile.json" "$BASE/"
rm -f "$BASE/preflight-approved"   # 설정을 다시 만들면 승인도 다시 받는다
cp "$SKILL"/assets/PROMPT-en.md "$SKILL"/assets/PROMPT-ko.md "$BASE/"
rm -rf "$BASE/harness-hurl"; cp -r "$SKILL/assets/harness-hurl" "$BASE/"
(cd "$SKILL/assets" && md5 -r PROMPT-en.md PROMPT-ko.md harness-hurl/*.hurl | diff - checksums.md5) \
  || { echo "정본 해시 불일치 — assets 변경 여부 확인" >&2; exit 1; }
for f in driver.sh watchdog.sh measure.sh run-all.sh smoke.sh usage_codex.py usage_pi.py usage_agy.py cost_guard.py usage_probe.py preflight.py approve.sh gate.sh pi_env.sh agy_env.sh key_env.sh cleanup.sh; do cp "$SKILL/scripts/$f" "$BASE/"; done

case "$HARNESS" in
  codex)
    mkdir -p "$BASE/codex-home"
    cp "$HOME/.codex/auth.json" "$BASE/codex-home/auth.json"   # 최신본 필수 (OAuth 만료 시 401)
    : > "$BASE/codex-home/config.toml" ;;
  claude-direct)
    mkdir -p "$BASE/claude-config"
    echo '{"hasCompletedOnboarding":true}' > "$BASE/claude-config/.claude.json" ;;
  pi)
    mkdir -p "$BASE/pi-agent"
    [ -n "${PI_MODELS_JSON:-}" ] && cp "$PI_MODELS_JSON" "$BASE/pi-agent/models.json"
    # OAuth provider(openai-codex 등) 자격증명: ~/.pi/agent/auth.json 최신본 복사 (EXP-030, 만료 시 401 — codex 분기와 같은 이유)
    if [ -f "$HOME/.pi/agent/auth.json" ]; then
      install -m 600 "$HOME/.pi/agent/auth.json" "$BASE/pi-agent/auth.json"
    fi
    command -v "$PI_BIN" >/dev/null || { echo "pi 없음 ($PI_BIN)" >&2; exit 1; } ;;
  agy)
    command -v "$AGY_BIN" >/dev/null || { echo "agy 없음 ($AGY_BIN)" >&2; exit 1; }
    (set +u; source "$BASE/agy_env.sh"; agy_reset_home) ;;
  claude-native) : ;;   # 사용자 기본 설정 사용 — 노출된 지침·스킬·MCP를 phase0.md에 기록할 것
  *) echo "unknown HARNESS=$HARNESS" >&2; exit 1 ;;
esac
command -v /opt/homebrew/bin/hurl >/dev/null || { echo "hurl 없음 (/opt/homebrew/bin/hurl)" >&2; exit 1; }
echo "OK: $BASE ($HARNESS)"
echo
python3 "$BASE/preflight.py" "$BASE" || true
echo
echo "다음: 위 보고서($BASE/preflight-report.md)를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다."
echo "      승인 시에만 bash $BASE/approve.sh \"<답변 원문>\" → bash $BASE/smoke.sh → nohup caffeinate -is bash $BASE/run-all.sh >/dev/null 2>&1 &"
