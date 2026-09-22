#!/bin/bash
# EXP-026: Opus 5.5 네이티브 — EN/KO 각 3 run, 교차 순서 6 run
# 기동: nohup caffeinate -is "$HOME/ralph-exp026/run-all.sh" > /dev/null 2>&1 &
BASE="$HOME/ralph-exp026"
LOG="$BASE/orchestrator.log"
log(){ echo "=== $* : $(date '+%F %T') ===" >> "$LOG"; }
run_one(){ [ -f "$BASE/done-$1" ] && { log "skip $1"; return; }
  log "start $1"; bash "$BASE/driver.sh" "$1"; log "end $1 | $(tail -1 "$BASE/metrics-$1.csv" 2>/dev/null)"; }
log "starting sequential runs"
for n in 1 2 3; do run_one en-$n; run_one ko-$n; done
log "ALL RUNS FINISHED"
touch "$BASE/done-all"
