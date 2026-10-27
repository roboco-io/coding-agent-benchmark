# EXP-054 결과 보고: Codex CLI × gpt-6.1-terra 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-27 (23:44–23:51 KST, 순차 3 run)
- 가설: [M-47](../../hypotheses/catalog.md) — Codex CLI(`codex exec` 0.164.0, ChatGPT 구독 OAuth)에서 `gpt-6.1-terra`(effort medium, PROMPT v2)는 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3).
- 클라이언트: Codex CLI 0.164.0
- **판정: 검증** — 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 모델 필드 21건 전부 `gpt-6.1-terra`). 세션 1분 40초–2분 10초로 리포 기록 중 최단 대역이며, API 단가 환산은 run당 $0.09–0.12다(청구액 아님).

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| gpt-6.1-terra | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 로그의 iteration 1 start–end(`codex exec` 실행 구간, 채점 제외)다. usage는 rollout 세션 누계이며 input은 캐시 포함, reasoning은 output에 포함된다. 환산 비용은 아래 "usage·집계 검증"의 공개 API 단가로 계산한 값이며 실제 청구액이 아니다.

| run | 완주 | 세션 시간 | input(누계) | cache read (히트율) | output (reasoning) | 요청별 최대 프롬프트 | 커밋 | 재검증 ×2 | API 환산 |
|---|---|---|---|---|---|---|---|---|---|
| terra61-en-1 | iter 1/30 | 1분 40초 | 511.4K | 481.7K (94%) | 6.3K (0.2K) | 39.1K | 1 | 13/154 ×2 | $0.086 |
| terra61-en-2 | iter 1/30 | 2분 10초 | 751.5K | 701.7K (93%) | 7.2K (0.2K) | 38.6K | 1 | 13/154 ×2 | $0.121 |
| terra61-en-3 | iter 1/30 | 2분 2초 | 617.8K | 562.6K (91%) | 6.8K (0.2K) | 33.7K | 2 | 13/154 ×2 | $0.117 |

## 모델 유지·루프 기여

요청 모델과 rollout의 `model` 필드는 3 run 전부 일치했다(21건 모두 `gpt-6.1-terra`). EXP-033과 달리 Codex 0.164.0의 로컬 모델 캐시에 이 ID가 등록되어 있어, 클라이언트는 fallback이 아니라 등록 메타데이터(컨텍스트 창 500,000)로 동작했다. 세 run 모두 첫 iteration에서 합격했으므로 루프의 복구 기여는 관측되지 않았다. 정체 종료(exit 124)·run 상한(125)·비용 상한(126)은 한 번도 발생하지 않았다.

## 같은 하네스의 gpt-6.1-sol과 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 | output 범위 | input 누계 범위 | 캐시 히트 | API 환산 |
|---|---|---|---|---|---|
| gpt-6.1-terra (이번, CLI 0.164.0, PROMPT v2) | 1분 40초–2분 10초 | 6.3–7.2K | 0.51–0.75M | 91–94% | $0.09–0.12 |
| gpt-6.1-sol (EXP-033, 2026-10-03, CLI 0.160.0, PROMPT v1) | 6분 13초–9분 48초 | 10.0–16.2K | 0.81–1.23M | 92–94% | $0.27–0.46 |

이번 3 run은 세션 시간이 EXP-033 sol의 약 4분의 1이었고, output과 input 누계도 더 작았다. 그러나 날짜, Codex CLI 버전(0.160.0 → 0.164.0), 클라이언트 모델 메타데이터(fallback → 등록값), PROMPT 버전(v1 → v2, PORT 안내 한 줄 추가)이 함께 달라졌다. 따라서 이 차이를 모델 차이로 단정하지 않고 조합 전체의 차이로만 기록한다. 기존 리포 최단 세션(EXP-032 pi × Sonnet 5.5, 1분 49초)과도 하네스·모델·PROMPT가 모두 달라 순위로 해석하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` rollout 1개, 누락 0. 집계는 `usage_codex.py`(EXP-027·033과 같은 스크립트). rollout의 `cli_version`은 3건 모두 0.164.0이다.
- 비용: ChatGPT 구독 OAuth라 run별 실제 지출은 없다. 하네스 비용 가드는 단가 0으로 동작했다. 2026-10-27 [모델 페이지](https://developers.openai.com/api/docs/models/gpt-6.1-terra)의 공개 API 단가(1M 토큰당 입력 $1, 캐시 입력 $0.05, 출력 $5, 272K 초과 요청은 $2·$0.10·$7.50)를 적용했다. 요청별 최대 프롬프트가 39.1K로 272K 이하여서 Standard 단가만 적용된다. 이 단가는 하위 에이전트가 요약 도구로 읽은 값이며 원문 대조는 하지 않았다.
- 재현 자료: `runs/`의 `bench.env`, `model-specs.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage.csv`, 로그(gz), `sessions.tar.gz`. 보관 전 `redact_keys.py` 마스킹 결과 0건.

## 한계와 교란 변수

- 과제 1개·n=3이다. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 실행 중 VS Code가 3000·3001을 점유했다. driver가 run별 빈 포트를 `PORT`로 주입했고 3 run 모두 첫 채점에서 13/13이어서 거짓 음성은 발생하지 않았다.
- 커밋이 run당 1–2개로 적다. 과제 산출물은 채점기로만 판정하며 커밋 수는 판정에 쓰지 않는다.

## 결론 및 후속 실험

- 결론: gpt-6.1-terra는 Codex CLI effort medium 하네스에서 이 과제를 iteration 1에 완주했다(n=3).
- 후속: gpt-6.1-sol을 Codex 0.164.0·PROMPT v2로 같은 시기에 재측정하면, 이번 속도 차이 중 모델이 차지하는 부분을 분리할 수 있다.
