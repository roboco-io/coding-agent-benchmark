# Phase 0 — 2026-09-21

본 실험은 시작하지 않았다. 두 번의 단순 응답 smoke는 모델 성능 점수에 포함하지 않는다.

| 조건 | 관측 | 판단 |
|---|---|---|
| Fable | 요청 `claude-fable-5-1`, exit 0, 최종 OK. 중간 제공자 안전 필터 및 `model_fallback` 이벤트. assistant 모델과 modelUsage에 요청하지 않은 모델이 등장 | **실행 차단**. 정상 종료·OK만으로 요청 모델 성공 판정 불가 |
| Astra | 요청 `gpt-6-astra`, exit 0, OK, turn.completed usage 수신 | 서비스 응답 확인. compact JSON stdout에 실제 served model 필드가 없어 모델 유지 검증 미완료 |

Claude 기록의 fallback 안내는 Opus 4.8을, modelUsage는 Opus 5를 포함한다. 이 불일치를 임의 해석하지 않으며 요청 모델 외 실행이 발생했다는 사실만 판정한다. 제공자 필터를 우회하거나 다른 모델로 자동 재시도하지 않았다.

Claude rate_limit 이벤트는 `isUsingOverage=false`였다. `overageStatus=allowed`도 기록되어 있으므로 본 실험 전 추가 유료 사용의 비활성 상태를 확인해야 한다. 이번 smoke가 실제 추가 과금이었다고 해석하지 않는다. 목록 단가 `total_cost_usd`는 구독 실제 청구액이 아니다.

인증 점검: Claude first-party claude.ai Max, Codex ChatGPT. 인증정보는 저장하지 않았다. smoke 환경은 PATH/HOME/USER/LOGNAME/SHELL/TMPDIR/LANG/LC_ALL/TERM만 상속했고 API 키와 endpoint 환경 변수는 전달하지 않았다.

CLI: Claude Code 2.1.278, Codex CLI 0.155.1. Docker daemon 접속 실패. 로컬 과거 Hurl 사본 존재를 확인했지만 정본 해시·기능 검증은 아직 수행하지 않았다.

[원자료](phase0-smoke.json)는 명령·소요 시간·종료 코드·stdout/stderr를 보존한다. 종료 코드 0은 Phase 0 통과를 뜻하지 않는다.
