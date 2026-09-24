#!/bin/bash
# 사용: nohup caffeinate -is bash $BASE/run-all.sh >/dev/null 2>&1 &
# 순차 실행(동시 실행 금지). 순서는 반복 번호 단위로 조건×언어를 교차해 시점 편향을 줄인다.
# run 종료마다 세션 로그를 run별 디렉터리로 옮겨 usage 계측 범위를 분리한다.
BASE="$(cd "$(dirname "$0")" && pwd)"
source "$BASE/bench.env"
LOG="$BASE/orchestrator.log"
log(){ echo "=== $* : $(date '+%F %T') ===" >> "$LOG"; }
archive_sessions(){ # $1 run
  case "$HARNESS" in
    codex) mv "$BASE/codex-home/sessions" "$BASE/sessions-$1" 2>/dev/null ;;
    claude-direct) mv "$BASE/claude-config/projects" "$BASE/sessions-$1" 2>/dev/null ;;
    claude-native) # 기본 설정 디렉터리의 해당 app 프로젝트 로그만 복사
      local enc; enc=$(echo "$BASE/app-$1" | sed 's|[/.]|-|g')
      cp -r "$HOME/.claude/projects/$enc" "$BASE/sessions-$1" 2>/dev/null ;;
  esac
}
run_one(){
  [ -f "$BASE/done-$1" ] && { log "skip $1"; return; }
  log "start $1"
  bash "$BASE/driver.sh" "$1"
  archive_sessions "$1"
  log "end $1 | $(tail -1 "$BASE/metrics-$1.csv" 2>/dev/null)"
}
log "starting sequential runs ($HARNESS: $CONDITIONS / $LANGS / n=$N)"
for n in $(seq 1 "$N"); do
  for l in $LANGS; do
    for c in $CONDITIONS; do run_one "${c%%:*}-$l-$n"; done
  done
done
log "ALL RUNS FINISHED"
touch "$BASE/done-all"
