#!/bin/bash
# EXP-023: Fable 5.1 네이티브 랄프 루프 EN 정본 — 순차 3 run
# 기동: nohup caffeinate -is "$HOME/ralph-exp023/run-all.sh" > /dev/null 2>&1 &
BASE="$HOME/ralph-exp023"
LOG="$BASE/orchestrator.log"
MODEL="claude-fable-5-1"
log(){ echo "=== $* : $(date '+%F %T') ===" >> "$LOG"; }
run(){ # $1 run
  [ -f "$BASE/done-$1" ] && { log "skip $1"; return; }
  log "start $1 ($MODEL)"
  bash "$BASE/driver.sh" "$1" "$MODEL"
  log "end $1 | $(tail -1 "$BASE/metrics-$1.csv" 2>/dev/null)"
}
log "starting sequential runs"
run fable-1
run fable-2
run fable-3
log "ALL RUNS FINISHED"
touch "$BASE/done-all"
