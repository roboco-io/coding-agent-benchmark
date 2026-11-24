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

# 파일 시스템 읽기 격리 (PI_SANDBOX=on, EXP-064 D-6·D-7): macOS Seatbelt(sandbox-exec)로 에이전트가 자기 리포·세션·도구 경로 밖의
# 홈 디렉터리 파일 내용을 읽거나 쓰지 못하게 한다. 근거: solar-mini-4-5-preview가 상위 하네스·다른 run·다른 실험 디렉터리를 탐색해
# 채점 정본과 이전 run 코드를 복사했다. 규칙은 "뒤에 오는 같은 연산 규칙이 우선"이므로 홈 전체 거부 뒤에 허용 경로를 둔다.
# 메타데이터(stat)는 막지 않는다(경로 해석·getcwd용). 디렉터리 목록·파일 내용(file-read-data)과 쓰기를 막는다.
pi_sandbox_profile() {  # $1 리포 경로 $2 세션 디렉터리
  local h="$HOME" rw ro
  rw=("$1" "$2" "$BASE/pi-agent" "$h/.npm" "$h/.cache" "$h/.config/prisma" "$h/.node-gyp" "$h/Library/Caches")
  ro=("$h/.asdf" "$h/.config/git")
  printf '(version 1)(allow default)'
  printf '(deny file-read-data file-write* (subpath "%s"))' "$h"
  for p in "${rw[@]}"; do printf '(allow file-read-data file-write* (subpath "%s"))' "$p"; done
  for p in "${ro[@]}"; do printf '(allow file-read-data (subpath "%s"))' "$p"; done
  printf '(allow file-read-data (literal "%s/.gitconfig") (literal "%s/.tool-versions"))' "$h" "$h"
}
# 사용: pi_exec <리포> <세션 디렉터리> pi 인자... (PI_SANDBOX=on이면 sandbox-exec로 감싼다)
pi_exec() {
  local repo="$1" sess="$2"; shift 2
  if [ "${PI_SANDBOX:-off}" = on ]; then
    sandbox-exec -p "$(pi_sandbox_profile "$repo" "$sess")" "$PI_BIN" "$@"
  else
    "$PI_BIN" "$@"
  fi
}
