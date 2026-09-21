#!/bin/bash
# EXP-025: DeepSeek 직결 — flash/pro × EN/KO 각 3 run, 교차 순서 12 run, run별 세션 격리
# 기동: nohup caffeinate -is "$HOME/ralph-exp025/run-all.sh" > /dev/null 2>&1 &
BASE="$HOME/ralph-exp025"
LOG="$BASE/orchestrator.log"
log(){ echo "=== $* : $(date '+%F %T') ===" >> "$LOG"; }
run_one(){ # $1 run name
  [ -f "$BASE/done-$1" ] && { log "skip $1"; return; }
  log "start $1"
  bash "$BASE/driver.sh" "$1"
  mv "$BASE/claude-config/projects" "$BASE/claude-config-projects-$1" 2>/dev/null
  log "end $1 | $(tail -1 "$BASE/metrics-$1.csv" 2>/dev/null)"
}
log "starting sequential runs"
for n in 1 2 3; do
  run_one flash-en-$n
  run_one pro-en-$n
  run_one flash-ko-$n
  run_one pro-ko-$n
done
log "ALL RUNS FINISHED"
touch "$BASE/done-all"
