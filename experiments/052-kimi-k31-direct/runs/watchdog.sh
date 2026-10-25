# iteration 정체 감시 (EXP-039 이후). driver.sh가 source한다.
# 사용: run_with_watchdog <idle_sec> <deadline_epoch> <watch 경로...> -- <명령...>
#   명령을 백그라운드로 실행하고 30초마다 확인한다.
#   - watch 경로 아래 파일이 idle_sec 동안 하나도 갱신되지 않으면 정체로 보고 프로세스 트리를 종료한다.
#   - 현재 시각이 deadline_epoch(run 상한)를 넘으면 같은 방식으로 종료한다.
#   - driver가 budget_check 함수를 정의했으면 30초마다 호출해, 출력이 있으면(비용 상한 초과) 종료한다(EXP-042 재발 방지).
#   종료 코드: 명령의 종료 코드, 정체 종료 124, 상한 종료 125, 비용 상한 종료 126. 사유는 WATCHDOG_REASON에 남긴다.
# 근거: EXP-039 luna-en-2에서 에이전트가 `npm run dev`를 포그라운드로 실행해 iteration이 반환되지 않았다.
#   pi bash 도구에는 기본 timeout이 없고, run 상한은 iteration 사이에서만 검사됐다.
#   EXP-020–036 세션 109개의 기록 간 최대 공백은 8.4분이었다(기본 idle 900초의 근거).

_wd_killtree() {
  local c
  for c in $(pgrep -P "$1" 2>/dev/null); do _wd_killtree "$c"; done
  kill -TERM "$1" 2>/dev/null
}

_wd_recent() {  # watch 경로 아래 최근 갱신 파일이 있으면 0
  # BSD find는 bash에서 -newermt "@<epoch>"를 해석하지 못하므로 기준 시각 파일과 -newer로 비교한다
  local since="$1"; shift
  local p newest marker rc=1
  marker=$(mktemp -t ralph-wd) || return 0
  touch -t "$(date -r "$since" +%Y%m%d%H%M.%S)" "$marker"
  for p in "$@"; do
    [ -e "$p" ] || continue
    newest=$(find "$p" -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -newer "$marker" -print -quit 2>/dev/null)
    [ -n "$newest" ] && { rc=0; break; }
  done
  rm -f "$marker"
  return $rc
}

run_with_watchdog() {
  local idle="$1" deadline="$2"; shift 2
  local watch=()
  while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do watch+=("$1"); shift; done
  shift
  WATCHDOG_REASON=""
  "$@" &
  local pid=$! last_active last_check now
  last_active=$(date +%s); last_check=$last_active
  # 종료는 1초 간격으로 확인해 정상 종료 시각을 늦추지 않고(세션 시간 계측), 갱신 검사만 30초 간격으로 한다
  while kill -0 "$pid" 2>/dev/null; do
    sleep 1
    kill -0 "$pid" 2>/dev/null || break
    now=$(date +%s)
    if [ "$now" -ge "$deadline" ]; then
      WATCHDOG_REASON="run 상한 도달"; _wd_killtree "$pid"; wait "$pid" 2>/dev/null; return 125
    fi
    [ $((now - last_check)) -lt 30 ] && continue
    if _wd_recent "$((last_check - 5))" "${watch[@]}"; then last_active=$now; fi
    last_check=$now
    if declare -F budget_check >/dev/null; then
      local over; over=$(budget_check)
      if [ -n "$over" ]; then
        WATCHDOG_REASON="비용 상한 — $over"; _wd_killtree "$pid"; wait "$pid" 2>/dev/null; return 126
      fi
    fi
    if [ $((now - last_active)) -ge "$idle" ]; then
      WATCHDOG_REASON="${idle}초 동안 세션·로그 갱신 없음"; _wd_killtree "$pid"; wait "$pid" 2>/dev/null; return 124
    fi
  done
  wait "$pid"
}
