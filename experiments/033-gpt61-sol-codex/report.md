# EXP-033 결과 보고: Codex CLI × gpt-6.1-sol 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-03 (07:50–08:15 KST, 순차 3 run)
- 가설: [M-26](../../hypotheses/catalog.md) — Codex CLI(`codex exec` 0.160.0) 하네스에서 `gpt-6.1-sol`(effort medium)은 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4h 안에 완주할 수 있다 (EN n=3).
- 클라이언트: Codex CLI 0.160.0
- **판정: 검증** — 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 모델 필드 15건 전부 `gpt-6.1-sol`). 세션 6–10분으로 EXP-027 gpt-6-sol(약 5분)보다 길었으나 CLI 버전·시점 교락이 있다.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| gpt-6.1-sol | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 로그의 iteration 1 start–end(`codex exec` 실행 구간, 채점 제외)이다. usage는 rollout 세션 누계이며 input은 캐시 포함, reasoning은 output에 포함된다.

| run | 완주 | 세션 시간 | input(누계) | cache read | output (reasoning) | 커밋 | 재검증 ×2 |
|---|---|---|---|---|---|---|---|
| sol61-en-1 | iter 1/30 | 9분 48초 | 1,230.2K | 1,136.5K | 16.2K (1.2K) | 4 | 13/154 ×2 |
| sol61-en-2 | iter 1/30 | 8분 43초 | 920.5K | 853.0K | 14.3K (1.5K) | 4 | 13/154 ×2 |
| sol61-en-3 | iter 1/30 | 6분 13초 | 811.1K | 763.8K | 10.0K (1.0K) | 4 | 13/154 ×2 |

## 모델 유지·루프 기여

- 요청 모델과 rollout의 `model` 필드가 3 run 전부 일치(15건 모두 `gpt-6.1-sol`). Codex 0.160.0 로컬 모델 캐시에 이 ID가 없어 클라이언트는 fallback 메타데이터로 동작했다.
- 3 run 모두 첫 iteration에서 합격. 루프의 복구 기여는 관측되지 않았다.

## 같은 하네스의 gpt-6-sol과 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 | output 범위 | input 누계 범위 | 캐시 히트 |
|---|---|---|---|---|
| gpt-6.1-sol (이번, CLI 0.160.0) | 6분 13초–9분 48초 | 10.0–16.2K | 0.81–1.23M | 92–94% |
| gpt-6-sol (EXP-027, 2026-09-24, CLI 0.155.1) | 4분 45초–5분 12초 | 10.4–11.0K | 1.07–1.46M | 94–97% |

- 이번 3 run은 세션 시간과 output 산포가 EXP-027 sol보다 컸고, input 누계는 더 작았다. 날짜·Codex CLI 버전·클라이언트 모델 메타데이터(fallback)가 함께 달라 모델 차이로 단정하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` rollout 1개. 누락 0. 집계는 `usage_codex.py`(EXP-027과 같은 스크립트).
- 비용: ChatGPT 플랜 OAuth라 청구 비용 없음. gpt-6.1-sol의 공개 API 단가는 이 실험 시점에 확인하지 못해 환산하지 않았다.
- 재현 자료: `runs/`의 `bench.env`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `recheck.csv`, `usage.csv`, 로그(gz), `sessions.tar.gz`.

## 한계와 교란 변수

- 과제 1개·n=3. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 실행 중 VS Code가 3000·3001을 점유했다. driver가 run별 빈 포트를 `PORT`로 주입했고 3 run 모두 첫 채점에서 13/13이어서 거짓 음성은 발생하지 않았다.
- 클라이언트 모델 메타데이터가 공식 값이 아니라 fallback이다. 컨텍스트 압축 시점 등이 공식 지원 이후와 다를 수 있다.

## 결론 및 후속 실험

- 결론: gpt-6.1-sol은 Codex CLI effort medium 하네스에서 이 과제를 iteration 1에 완주했다(n=3).
- 후속: Codex가 공식 메타데이터를 포함한 뒤 gpt-6-sol과의 동시기 교차 재측정.

## 후속 분석 (2026-10-03)

- [gpt-6.1-sol 세션 시간 증가 원인 분석](../../analysis/gpt61-sol-slowdown/README.md): Codex·pi 세션 기록을 모델 대기와 도구 실행으로 나눈 결과, 도구 실행 시간과 모델 호출 수는 gpt-6-sol과 비슷했고 모델 호출당 대기 시간이 약 2배였다. 같은 시각에 번갈아 보낸 단일 요청 비교에서도 gpt-6.1-sol이 약 1.4배 느렸다(초당 output 약 20% 감소). 같은 pi 0.87.1에서도 차이가 나서 클라이언트 버전은 주원인이 아니다.
