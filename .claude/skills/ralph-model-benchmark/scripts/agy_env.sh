# agy(Antigravity CLI) 격리 실행 (driver.sh·smoke.sh가 source, EXP-035).
# 격리 HOME($BASE/agy-home)의 settings.json `modelProvider: "gemini"` + GEMINI_API_KEY로 API 키 인증을 강제한다
# (실 HOME에서는 keyring의 Google 계정 OAuth가 우선 선택됨 — 2026-10-07 로그 확인).
# 격리 HOME은 대화·brain(지식)·요약 DB를 run마다 비워 run 간 교란을 막는다. 도구 체인은 실 asdf를 가리킨다.
source "$BASE/key_env.sh"
load_secrets GEMINI_API_KEY   # 비밀값은 GEMINI_API_KEY만 노출 (EXP-036 D-3)
REAL_HOME="$HOME"
agy_run() { # $@ = agy 인자
  env HOME="$BASE/agy-home" ASDF_DATA_DIR="$REAL_HOME/.asdf" AGY_CLI_DISABLE_AUTO_UPDATE=1 \
    GEMINI_API_KEY="$GEMINI_API_KEY" "$AGY_BIN" "$@"
}
agy_reset_home() { # 격리 HOME 초기화 (setup·run 종료 시)
  local h="$BASE/agy-home"
  rm -rf "$h/.gemini"
  mkdir -p "$h/.gemini/antigravity-cli"
  echo '{"modelProvider":"gemini"}' > "$h/.gemini/antigravity-cli/settings.json"
  cp "$REAL_HOME/.tool-versions" "$h/.tool-versions" 2>/dev/null
  printf '[user]\n\tname = %s\n\temail = %s\n[init]\n\tdefaultBranch = main\n' \
    "$(git config --global user.name)" "$(git config --global user.email)" > "$h/.gitconfig"
}
