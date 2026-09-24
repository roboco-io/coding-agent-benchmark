# pi 격리 환경 (driver.sh·smoke.sh가 source). 설정은 $BASE/pi-agent, 네트워크 부가 호출 차단.
# 호출 플래그 -nc -ns -ne -np -na: 상위 디렉터리 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 템플릿·프로젝트 로컬 설정 비노출.
source "$HOME/.zsh_secrets"
export PI_CODING_AGENT_DIR="$BASE/pi-agent" PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1
for kv in $PI_KEYMAP; do src="${kv#*=}"; export "${kv%%=*}=${!src}"; done
