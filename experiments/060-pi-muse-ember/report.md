# EXP-060 결과 보고: pi × Meta Muse Ember (OpenRouter) 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-11-11 (11:20–11:30 KST, 순차 3 run). 2026-11-10 1차 smoke는 제공자 404로 실패해 기동하지 않았다.
- 가설: [M-52](../../hypotheses/catalog.md) — pi 0.87.1 × OpenRouter `meta/muse-ember`(Meta 고정, thinking high, pi 정본 지속 지침)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 20분·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 검증** — 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, OpenRouter generation 101건 전부 제공자 Meta·served `meta/muse-ember-20261109`). 세션 2분 52초–3분 19초, 청구 run당 $0.027–0.051로 리포 최저 비용 대역(gpt-6-luna 환산 $0.02–0.03 등)과 같은 수준이다.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| openrouter/meta/muse-ember | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 세션 jsonl의 첫·마지막 기록 시각 차이다(채점 제외). usage는 `usage_pi.py`(responseId dedup) 값이며 input은 캐시 제외 입력이다. 청구는 OpenRouter `GET /api/v1/generation`의 `total_cost`를 run의 모든 responseId에 대해 합한 값이다.

| run | 완주 | 세션 시간 | 호출 | input | cache read | output (reasoning) | 요청별 최대 프롬프트 | 커밋 | 재검증 ×2 | 청구 |
|---|---|---|---|---|---|---|---|---|---|---|
| museember-en-1 | iter 1/30 | 3분 15초 | 38 | 280.7K | 923.4K | 19.9K (5.4K) | 48.2K | 3 | 13/154 ×2 | $0.0417 |
| museember-en-2 | iter 1/30 | 3분 19초 | 35 | 375.4K | 1,023.5K | 17.8K (4.9K) | 68.7K | 3 | 13/154 ×2 | $0.0506 |
| museember-en-3 | iter 1/30 | 2분 52초 | 28 | 148.2K | 669.9K | 18.4K (4.6K) | 44.3K | 3 | 13/154 ×2 | $0.0267 |

도구는 bash 23–27회, write 9–18회, edit 0–4회였다. 세 run 모두 Fastify + Prisma 스택을 골랐다. 세션 기록에서 하네스 파일(`measure.sh`, 다른 run 디렉터리 등)을 참조한 호출은 없었다. `thinking_level_change`는 전부 `high`였다.

## 모델 유지·루프 기여

OpenRouter generation 101건이 모두 제공자 `Meta`, served model `meta/muse-ember-20261109`였다(조회 실패 0, [runs/openrouter-generations.csv](runs/openrouter-generations.csv)). 세 run 모두 첫 iteration에서 합격했으므로 루프의 복구 기여는 관측되지 않았다. 정체 종료(exit 124)·run 상한(125)·비용 상한(126)은 발생하지 않았다.

## 같은 하네스의 Muse Spark Open과 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 | output 범위 | 청구 범위 |
|---|---|---|---|
| Muse Ember (이번, pi 0.87.1, PROMPT v2, 지속 지침 있음) | 2.9–3.3분 | 17.8–19.9K | $0.027–0.051 |
| Muse Spark Open (EXP-049, 2026-10-18, pi 0.87.1, PROMPT v1, 지속 지침 없음) | 5.2–6.7분 | 25.3–33.8K | $0.45–0.67 |

이번 3 run은 EXP-049보다 세션이 짧았고, 청구는 약 10분의 1이었다. 청구 차이는 대부분 단가 차이(입력 $1.25 → $0.10, 출력 $4.25 → $0.50)에서 온다. 세션 시간 차이에는 PROMPT 버전(v1 → v2)과 pi 지속 지침 유무, 실험 시점이 함께 섞여 있어 모델 차이로 단정하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` jsonl 1개, usage 누락 0.
- 비용: OpenRouter API 키로 실행해 실제 과금이 있었다. 공개 단가(100만 토큰당 입력 $0.10, 출력 $0.50, 캐시 읽기 $0.004, 2026-11-10·11 endpoints API 확인)로 pi usage를 환산한 값이 generation `total_cost` 합과 run마다 소수 넷째 자리까지 같다. 월별 청구서와 대조한 것은 아니다. 하네스 비용 가드의 마지막 추정은 run 3에서 $0.0254, 실험 누계 $0.0927이었다(상한 run $1·실험 $3).
- 재현 자료: `runs/`의 `bench.env`, `model-specs.json`, `pi-models.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage-pi.csv`, `openrouter-generations.csv`, 로그(gz), `sessions.tar.gz`. 보관 전 `redact_keys.py` 마스킹 결과 0건.

## 한계와 교란 변수

- 과제 1개·n=3이다. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 2026-11-10 1차 smoke에서 OpenRouter → Meta 경로가 404 `model_not_found`를 반환했고, 2026-11-11에는 정상이었다. 원인(제공자 일시 오류 또는 접근 롤아웃)은 확인하지 못했다.
- 2026-11-11 확인 시 OpenRouter에 Google Vertex 제공자가 추가되었으나 다운 상태였다. 하네스는 Meta로 고정해 이 경로를 쓰지 않았다.
- 외부 프로세스(DeepSRT)가 3003을 점유했다. driver가 run별 빈 포트를 주입했고 3 run 모두 첫 채점에서 13/13이어서 거짓 음성은 발생하지 않았다.

## 결론 및 후속 실험

- 결론: Muse Ember는 pi 정본(지속 지침) 하네스에서 이 과제를 iteration 1에 완주했다(n=3). 청구는 run당 5센트 이하였다.
- 후속: Muse Spark Open을 PROMPT v2·pi 정본 지침으로 재측정하면, 이번 세션 시간 차이 중 모델이 차지하는 부분을 분리할 수 있다.
