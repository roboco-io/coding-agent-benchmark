#!/bin/bash
# 사용: bash setup.sh <bench.env>
# $HOME/ralph-exp$EXP 하네스를 만든다: 정본 PROMPT·Hurl 복사+해시 검증, 스크립트 동결 복사, 격리 설정 디렉터리 생성.
set -euo pipefail
CFG="$1"; SKILL="$(cd "$(dirname "$0")/.." && pwd)"
source "$CFG"
BASE="$HOME/ralph-exp$EXP"
[ -e "$BASE/done-all" ] && { echo "이미 완료된 하네스: $BASE" >&2; exit 1; }
mkdir -p "$BASE"
cp "$CFG" "$BASE/bench.env"
cp "$SKILL"/assets/PROMPT-en.md "$SKILL"/assets/PROMPT-ko.md "$BASE/"
rm -rf "$BASE/harness-hurl"; cp -r "$SKILL/assets/harness-hurl" "$BASE/"
(cd "$SKILL/assets" && md5 -r PROMPT-en.md PROMPT-ko.md harness-hurl/*.hurl | diff - checksums.md5) \
  || { echo "정본 해시 불일치 — assets 변경 여부 확인" >&2; exit 1; }
for f in driver.sh measure.sh run-all.sh smoke.sh usage_codex.py; do cp "$SKILL/scripts/$f" "$BASE/"; done

case "$HARNESS" in
  codex)
    mkdir -p "$BASE/codex-home"
    cp "$HOME/.codex/auth.json" "$BASE/codex-home/auth.json"   # 최신본 필수 (OAuth 만료 시 401)
    : > "$BASE/codex-home/config.toml" ;;
  claude-direct)
    mkdir -p "$BASE/claude-config"
    echo '{"hasCompletedOnboarding":true}' > "$BASE/claude-config/.claude.json" ;;
  claude-native) : ;;   # 사용자 기본 설정 사용 — 노출된 지침·스킬·MCP를 phase0.md에 기록할 것
  *) echo "unknown HARNESS=$HARNESS" >&2; exit 1 ;;
esac
command -v /opt/homebrew/bin/hurl >/dev/null || { echo "hurl 없음 (/opt/homebrew/bin/hurl)" >&2; exit 1; }
echo "OK: $BASE ($HARNESS)"
echo "다음: bash $BASE/smoke.sh  →  nohup caffeinate -is bash $BASE/run-all.sh >/dev/null 2>&1 &"
