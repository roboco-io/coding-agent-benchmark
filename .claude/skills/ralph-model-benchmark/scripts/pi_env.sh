# pi 격리 환경 (driver.sh·smoke.sh가 source). 설정은 $BASE/pi-agent, 네트워크 부가 호출 차단.
# 호출 플래그 -nc -ns -ne -np -na: 상위 디렉터리 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 템플릿·프로젝트 로컬 설정 비노출.
# 비밀값: PI_KEYMAP 대상과 PI_KEEP_ENV에 적은 이름만 에이전트 환경에 남긴다 (EXP-036 D-3).
source "$BASE/key_env.sh"
source "$HOME/.zsh_secrets"
_keep="${PI_KEEP_ENV:-}"
for kv in $PI_KEYMAP; do src="${kv#*=}"; export "${kv%%=*}=${!src}"; _keep="$_keep ${kv%%=*}"; done
_saved=$(for n in $_keep; do printf '%s=%q\n' "$n" "${!n}"; done)
load_secrets $_keep
eval "$_saved"; for n in $_keep; do export "$n"; done
unset _keep _saved
export PI_CODING_AGENT_DIR="$BASE/pi-agent" PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1
