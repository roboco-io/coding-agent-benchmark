# EXP-063: Antigravity CLI(agy) × Gemini 4 Carbon·Neon·Hydrogen (구독 인증)

## 가설

- 가설 코드·문장: [M-54](../../hypotheses/catalog.md) — agy 1.5.14 × `gemini-4-carbon`·`gemini-4-neon`·`gemini-4-hydrogen`(effort high, Google 계정 구독 인증)은 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 30분·30 iteration 안에 무개입 완주할 수 있다 (모델별 EN n=3).
- 질문 유형: 완주 가능성. 세 모델은 같은 제공자의 같은 세대 모델이며, 하네스·인증·effort를 고정하고 모델만 바꾼다.
- 실험 단계: 탐색 파일럿 (모델별 n=3).
- 주 지표와 사전 판정 기준: 모델별로 검증 3/3, 부분 검증 1–2/3, 기각 0/3. 실험 전체 판정은 모델별 판정을 함께 적는다.
- 보조 지표: iteration 수, 세션 시간, transcript 기반 토큰 대리지표(청구 비용 아님), API 환산 비용(보고용).

## 과제·완료 기준

- 과제: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1건.
- 프롬프트 정본: 스킬 `assets/PROMPT-en.md` v2 (md5 `3d11ae8d28546ac730d482d015cfd6d9`).
- 채점: 스킬 정본 Hurl 13파일, `/opt/homebrew/bin/hurl` 8.1.0. 완료 기준은 하네스 채점 13/13·154 요청 통과(`gate=pass`)이며, 에이전트의 완료 선언만으로는 완주로 보지 않는다.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 인증·연결 | 원자료 |
|---|---|---|---|---|
| carbon | `gemini-4-carbon`, `--effort high` | agy 1.5.14 | Google 계정 구독 OAuth (`authMethod=consumer`) | `runs/` |
| neon | `gemini-4-neon`, `--effort high` | agy 1.5.14 | 같음 | `runs/` |
| hydrogen | `gemini-4-hydrogen`, `--effort high` | agy 1.5.14 | 같음 | `runs/` |

effort는 세 모델이 공통으로 지원하는 최고값인 high로 고정했다. Carbon은 low·medium·high만 지원하고, Neon과 Hydrogen은 xhigh도 지원한다. EXP-035(agy × gemini-3.8-flash)도 high였다.

## 환경·비교 범위

- **인증 (EXP-035와의 차이)**: EXP-035는 Gemini API 키(`authMethod=gemini_api_key`)를 썼다. 이번 실험은 사용자 지시(2026-11-22)에 따라 구독 인증을 쓴다. 하네스에 `AGY_AUTH=subscription` 모드를 추가했다. 이 모드는 격리 HOME에 `~/Library/Keychains` 링크만 두고, agy가 macOS 키체인(서비스 `gemini`)의 OAuth 토큰을 읽게 한다. 에이전트 환경에는 `GEMINI_API_KEY`를 넣지 않는다. smoke는 `cli.log`에서 `authMethod=consumer`를 확인했다(2026-11-22, 세 모델 PASS).
- **노출**: 에이전트 프로세스의 HOME 안에 사용자 키체인 디렉터리 링크가 보인다. 이 노출은 이탈로 기록한다. 그 밖의 격리(run별 HOME 초기화, 대화·brain 이동)는 EXP-035와 같다.
- **구독 한도**: 구독 사용량 한도에 닿으면 run이 진행하지 못할 수 있다. 한도 오류가 반복되면 run을 멈추고 사용자에게 알리며, 해당 run은 판정에서 보류로 처리한다.
- **모델 가용성**: 2026-11-22에 API 키 경로와 구독 경로 모두 `agy models`에 세 모델이 있음을 확인했다. EXP-047(agy 1.3.6) 당시에는 API 키 경로에 Gemini 4 계열이 없었다.
- **기준선**: 과거 agy 실험은 EXP-035 하나다. 인증 경로와 agy 버전이 다르므로, 비교할 때 차이를 조합 전체의 차이로 서술한다. 같은 모델의 pi 결과(EXP-047 Argon)는 하네스가 다르다.

## 반복·실행 순서·예산

- 반복: 모델별 EN 3 run. 모두 순차 실행한다. (작성 당시 실행 순서를 carbon 1–3, neon 1–3, hydrogen 1–3으로 적었으나, 하네스 정본은 반복 번호 단위로 모델을 교차한다 — 실제 순서 carbon-1 → neon-1 → hydrogen-1 → carbon-2 … , 보고서 이탈 절 참조.)
- 상한: run당 30분(`MAX_SEC=1800`), 30 iteration, 정체 300초. run 상한은 기본값 20분보다 길다. EXP-035의 agy 세션이 15.5–22.4분, 폐기한 EXP-062의 pi × Carbon 세션이 약 16–19분이었기 때문이다.
- 비용: 구독 실행이므로 하네스 단가는 0이다(EXP-054 방식). `RUN_BUDGET_USD`는 1, `EXP_BUDGET_USD`는 3이다. API 환산 단가(입력/캐시/출력, 100만 토큰당)는 Carbon $2/$0.10/$10, Neon $3/$0.15/$15, Hydrogen $1.5/$0.075/$7.5이다(https://aistudio.google.com/docs/pricing, 2026-11-22 확인). Carbon의 API 단가는 2026-12-01에 두 배가 된다. 이 단가는 보고용 환산에만 쓴다.
- 승인: 2026-11-22 사용자 승인 "모델별 3 run (권장)". 처음에는 API 과금 조건으로 승인했으나, smoke 실행 전에 사용자가 구독 과금으로 바꾸도록 지시했다. API 키 경로로는 모델 목록 조회 외의 호출을 하지 않았다.
- 사람 개입: 없음. 이상 징후가 보이면 먼저 멈추고 사용자에게 알린다.

## Ralph 정책

iteration마다 새 agy 세션을 연다. 코드와 git 이력은 유지하고, 하네스 채점 결과는 에이전트에 전달하지 않는다. 정책은 스킬 `driver.sh`의 정본을 따른다.

## 계측

- 세션 시간: 로그의 시작·종료 시각.
- 토큰: `usage_agy.py`(brain/*/transcript_full.jsonl 합계)로 집계한 토큰 대리지표. 구독 실행이므로 실제 청구액은 없다.
- 재검증: 완주 run마다 `measure.sh`를 2회 실행해 `13,154`를 확인한다.
