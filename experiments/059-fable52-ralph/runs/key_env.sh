# 비밀값 최소 노출 (EXP-036 D-3): ~/.zsh_secrets를 읽되, 인자로 준 이름만 export하고 나머지는 셸에서 제거한다.
# 에이전트가 `env`를 출력하면 세션 로그(리포 보관 대상)에 키가 남기 때문이다.
# 사용: source key_env.sh; load_secrets NAME...   (값이 필요한 다른 변수는 load 전에 $NAME으로 읽어 둘 것)
load_secrets() {
  local keep=" $* " n
  source "$HOME/.zsh_secrets"
  for n in $(sed -nE 's/^[[:space:]]*(export[[:space:]]+)?([A-Za-z_][A-Za-z0-9_]*)=.*/\2/p' "$HOME/.zsh_secrets"); do
    case "$keep" in *" $n "*) export "$n" ;; *) unset "$n" ;; esac
  done
}
