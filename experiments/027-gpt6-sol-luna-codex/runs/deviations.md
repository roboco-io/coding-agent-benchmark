# EXP-027 이탈 기록

## D-1: sol-en-2 게이트 채점 행(hang) — 채점 인프라 결함, 모델 무관 (2026-09-24)

- 현상: sol-en-2 iteration 1이 09:07:58에 종료(exit 0, `.ralph-done` 선언)한 뒤 `measure.sh`가 반환하지 않아 driver가 09:18:44까지 약 10.8분 대기. Hurl 자체는 `hurl-last.log`에 13파일·154요청 성공으로 이미 완료된 상태였다.
- 원인: 이 run의 앱은 `npm run dev` → `node scripts/run.mjs --watch` → `node node_modules/.bin/tsx watch src/server.ts`로 상대 경로 watcher를 띄운다. measure v4의 정리 로직(리포 소속 LISTEN pid 종료 + `pkill -f "$REPO/node_modules"`)은 서버 pid만 종료하고 상위 watcher 트리를 놓쳤다. 서버를 띄운 백그라운드 서브셸이 호출 측 `$(measure.sh)`의 stdout 파이프를 쥔 채 살아 있어 명령 치환이 끝나지 않았다. sol-en-1·luna-en-1은 dev 스크립트 구조가 달라 드러나지 않았다.
- 조치(09:18, 사람 개입 — 채점 인프라 한정): 잔존 트리(pid 22678/22679/22723/22817)를 수동 종료 → driver가 이미 계산된 결과 `13,154`로 게이트 pass 기록. 에이전트·산출물에는 개입하지 않았다.
- 수정: measure.sh에 서버 서브셸 pid 기준 프로세스 트리 종료(`kill_tree`)와 서브셸 stdout 분리(`> /dev/null`)를 추가. 채점 로직(Hurl 파일·호출 인자·판정)은 변경 없음. luna-en-2부터 수정본 적용. 수정본으로 app-sol-en-2 재채점 → `13,154`, 10.7초, 잔존 프로세스 0.
- 계측 영향: sol-en-2의 metrics 종료 시각(09:18:44)에는 행 시간이 포함되므로 세션 시간은 로그의 iteration start/end(09:03:03–09:07:58)로 산정한다. 판정에는 영향 없음.
