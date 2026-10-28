# EXP-055: pi × gpt-6.1-terra 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-28 (실행 전).

## 가설

- 가설 코드·문장: [M-48](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 `openai-codex/gpt-6.1-terra`(ChatGPT 구독 OAuth, thinking medium, 사용자 정의 모델 항목, PROMPT v2)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3). 효율 우위 실험으로 사후 해석을 바꾸지 않는다.
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 토큰 대리지표(`usage_pi.py`, responseId dedup), API 단가 환산 비용(청구 비용 아님).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| terra61 | `openai-codex/gpt-6.1-terra`, thinking `medium` (EXP-054 Codex effort medium과 맞춤) | pi 0.87.1 (`-nc -ns -ne -np -na` 격리) | ChatGPT 구독 OAuth(`~/.pi/agent/auth.json` 최신본 복사) | `runs/` |

- 모델 항목: pi 0.87.1 내장 목록에 `gpt-6.1-terra`가 없어, EXP-034 sol 항목과 같은 형식의 사용자 정의 `pi-models.json`(contextWindow 272,000, maxTokens 128,000, `openai-codex-responses`)으로 등록한다. ID만 바꾸고 나머지 값은 EXP-034와 같다.
- 짝 실험: [EXP-054](../054-gpt61-terra-codex/README.md)(Codex CLI 0.164.0, 같은 모델·effort·PROMPT v2). 두 실험의 차이는 에이전트 클라이언트·컨텍스트 창 설정(Codex 500K, pi 272K)·실행 시점의 차이를 함께 포함한다.

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 프롬프트 정본: 스킬 `assets/PROMPT-en.md` **v2** (md5 `3d11ae8d28546ac730d482d015cfd6d9`). EXP-034(v1)과 비교할 때 PROMPT 차이를 교란 변수로 적는다.
- 채점 정본: 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl`(hurl 8.0.1) 절대 경로.
- 완료 기준: 드라이버 게이트 `pass`와 독립 재검증 2회 `13,154`가 모두 성립한 run만 완주로 본다.

## 반복·예산·판정

- 반복: EN n=3, 순차 실행, 다른 실험과 동시 실행 금지.
- 상한: 30 iteration, run당 20분(1,200초), 정체 300초.
- 비용: ChatGPT 구독 OAuth라 실제 지출은 없다. 하네스 단가 0, `RUN_BUDGET_USD=1`·`EXP_BUDGET_USD=3`은 형식상 값이다. API 환산은 보고 단계에서 EXP-054와 같은 단가로 계산한다.
- 사람 개입: 없음. 채점기 정리 누락 시에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 판정: 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 인증·가용성 장애 run은 **보류**(새 run 번호로 재실행).

## 계측

- usage는 토큰 대리지표이며 청구 비용이 아니다. 시간은 driver 로그의 iteration start–end.
- 응답 model 필드와 thinking 수준을 세션 기록에서 전수 확인한다.
