# EXP-029 이탈·장애 기록

## D-1: qwen-en-1 iteration 1–4 기각 — 포트 3000 외부 점유로 인한 채점 교란 추정 (2026-09-24 확인)

- 관측: qwen-en-1 iteration 1–4에서 에이전트가 `.ralph-done`을 선언했으나 measure.sh 결과가 `0,13`(0/13 파일)으로 게이트 기각. iteration 5에서 기본 포트를 3002로 바꾼 뒤(`2c072b8`) `13,154` pass.
- 근거: 에이전트 로그(`ralph-run-qwen-en-1.log` 32·58·85행)에 "port 3000 is occupied by an unrelated VS Code live-preview server (127.0.0.1:3000)", "requests to localhost:3000 returned that service's HTML" 기록. 앱이 3000에서 LISTEN하는 것을 measure.sh가 탐지했지만 hurl의 `localhost:3000` 요청이 127.0.0.1의 VS Code Live Preview로 간 것으로 추정한다(미확인 — 당시 lsof 스냅샷 없음). 15:20 확인 시 3000·3002 LISTEN 없음.
- 분류: 채점 환경 교란(실험 외부 프로세스). 모델/산출물 실패로 보지 않는다.
- 처리: run 결과(pass, iter 5)는 유지하되 iteration 수·시간은 교란이 포함된 값으로 표기한다. 전 run 종료 후, iteration 1 종료 시점 커밋 상태를 복사본에서 포트 비점유 상태로 재채점해 교란 여부를 확인한다(원 기록은 덮어쓰지 않음).
- 재발 방지 제안: Phase 0 체크리스트에 "채점 전 3000번대 포트 외부 LISTEN 없음" 확인 추가.
- 재채점 결과 (2026-09-24 15:48, `recheck.csv`): iteration 1 종료 시점 커밋 `c53937d`를 복사본 `rescore-qwen-en-1-iter1`에서 checkout해 measure.sh 2회 실행 → 2회 모두 `13,154`. 당시 3000 포트 외부 LISTEN 없음(3003에 DeepSRT만 존재). **iteration 1–4 기각은 채점 환경 교란에 의한 거짓 음성으로 판단한다.** qwen-en-1의 "완주 iteration 5·29.0분"은 교란 포함 관측값이며, 교란이 없었다면 iteration 1 완주(약 20분)였을 것으로 추정한다(추정 — 재실행으로 확인하지 않음).

## D-2: qwen-en-3 스트림 1건 `terminated` (2026-09-24 15:24:23 KST)

- assistant 메시지 1건이 `stopReason: error`, `errorMessage: terminated`로 기록됨. 같은 세션이 이어져 iteration 1에 완주. 제공자 스트림 중단으로 분류하며 개입 없음.
