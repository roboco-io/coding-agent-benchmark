# agy(Antigravity CLI) 격리 실행 (driver.sh·smoke.sh가 source, EXP-035).
# 격리 HOME($BASE/agy-home)의 settings.json `modelProvider: "gemini"` + GEMINI_API_KEY로 API 키 인증을 강제한다
# (실 HOME에서는 keyring의 Google 계정 OAuth가 우선 선택됨 — 2026-10-07 로그 확인).
# 격리 HOME은 대화·brain(지식)·요약 DB를 run마다 비워 run 간 교란을 막는다. 도구 체인은 실 asdf를 가리킨다.
# AGY_AUTH=subscription (EXP-063): Google 계정 구독 인증. agy는 macOS 키체인(서비스 "gemini")의 OAuth 토큰을
#   읽으며 키체인 위치를 HOME 기준으로 찾으므로, 격리 HOME에 ~/Library/Keychains 링크만 둔다. GEMINI_API_KEY는 노출하지 않는다.
#   smoke가 cli.log의 authMethod=consumer를 확인한다 (apikey 모드는 gemini_api_key).
AGY_AUTH="${AGY_AUTH:-apikey}"
REAL_HOME="$HOME"
if [ "$AGY_AUTH" = subscription ]; then
  agy_run() { # $@ = agy 인자
    env -u GEMINI_API_KEY -u GOOGLE_API_KEY HOME="$BASE/agy-home" ASDF_DATA_DIR="$REAL_HOME/.asdf" \
      AGY_CLI_DISABLE_AUTO_UPDATE=1 "$AGY_BIN" "$@"
  }
else
  source "$BASE/key_env.sh"
  load_secrets GEMINI_API_KEY   # 비밀값은 GEMINI_API_KEY만 노출 (EXP-036 D-3)
  agy_run() { # $@ = agy 인자
    env HOME="$BASE/agy-home" ASDF_DATA_DIR="$REAL_HOME/.asdf" AGY_CLI_DISABLE_AUTO_UPDATE=1 \
      GEMINI_API_KEY="$GEMINI_API_KEY" "$AGY_BIN" "$@"
  }
fi
agy_reset_home() { # 격리 HOME 초기화 (setup·run 종료 시)
  local h="$BASE/agy-home"
  rm -rf "$h/.gemini"
  mkdir -p "$h/.gemini/antigravity-cli"
  if [ "$AGY_AUTH" = subscription ]; then
    echo '{}' > "$h/.gemini/antigravity-cli/settings.json"
    mkdir -p "$h/Library"; ln -sfn "$REAL_HOME/Library/Keychains" "$h/Library/Keychains"
    # 구독 OAuth 토큰은 실 HOME의 이 파일에 있다(keyringAuth가 읽음). 만료 후 실 HOME에서 갱신되면
    # 격리 HOME에는 토큰이 없어 "Authentication required"로 실패했다(EXP-063 D-1) → run마다 최신본 복사
    #   새 로그인 토큰은 키체인에 저장되고 파일은 없을 수 있다(2026-11-22 08:21 확인) → 있을 때만 복사
    local tf="$REAL_HOME/.gemini/antigravity-cli/antigravity-oauth-token"
    [ -f "$tf" ] && install -m 600 "$tf" "$h/.gemini/antigravity-cli/antigravity-oauth-token"
  else
    echo '{"modelProvider":"gemini"}' > "$h/.gemini/antigravity-cli/settings.json"
  fi
  cp "$REAL_HOME/.tool-versions" "$h/.tool-versions" 2>/dev/null
  printf '[user]\n\tname = %s\n\temail = %s\n[init]\n\tdefaultBranch = main\n' \
    "$(git config --global user.name)" "$(git config --global user.email)" > "$h/.gitconfig"
}
agy_auth_check() { # run 시작 전 구독 인증 확인 (EXP-063 D-1). 모델 호출 없이 목록 조회만 한다
  [ "$AGY_AUTH" = subscription ] || return 0
  local h="$BASE/agy-home" ok=1
  agy_reset_home
  (cd "$h" && agy_run models < /dev/null 2>&1) | grep -q '^gemini-' || ok=0
  grep -q 'authMethod=consumer' "$h/.gemini/antigravity-cli/cli.log" 2>/dev/null || ok=0
  agy_reset_home
  [ $ok = 1 ]
}
