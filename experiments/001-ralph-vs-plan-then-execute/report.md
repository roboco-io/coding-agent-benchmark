# EXP-001 결과 보고: Ralph loop vs Plan-then-execute

- 실험일: 2026-07-20
- 가설: [S-01](../../hypotheses/catalog.md) — Plan-then-execute가 Ralph loop보다 동일 과제에서 토큰을 적게 쓴다
- **판정: 기각 (관측 범위 한정)** — 보관 로그의 토큰 대리지표는 PTE 1,128,420, Ralph 136,506으로 약 8.27배. 동일 품질의 비용 우위로 일반화하지 않는다.

## 2026-09-21 계측 정정

동일 run 안의 동일 `message.id`·usage를 한 번만 합산했다. 아래 값은 보관된 최상위 JSONL 파일 범위이며 실제 청구 비용이 아니다. `messages`는 고유 메시지 수, `sessions`는 JSONL 파일 수다. 누락된 외부 호출·서브에이전트 비용의 완전성은 미검증이다.

| run | 이전 대리지표 | 정정 대리지표 |
|---|---:|---:|
| ralph-loop | 324,775 | 136,506 |
| plan-then-execute | 2,839,815 | 1,128,420 |

이전 값은 중복 usage 행을 합산했다. 기존 보고서의 해당 수치·파생 해석은 이 정정판으로 대체한다. 원자료는 변경하지 않았다.

## 정정 측정 결과

| 지표 | ralph-loop | plan-then-execute |
|---|---:|---:|
| sessions | 1 | 16 |
| messages | 54 | 321 |
| usage_rows | 112 | 782 |
| duplicates | 58 | 461 |
| missing_usage | 0 | 0 |
| input_tokens | 101 | 598 |
| output_tokens | 38,090 | 289,000 |
| cache_creation_input_tokens | 98,315 | 838,822 |
| cache_read_input_tokens | 4,096,470 | 17,552,165 |
| token_proxy | 136,506 | 1,128,420 |

`token_proxy = input_tokens + output_tokens + cache_creation_input_tokens`. 캐시 읽기는 별도 표시하며 무료로 취급하지 않는다. reasoning은 공급자가 output에 포함한 값을 중복 가산하지 않는다.

## 판정·관측·한계

- 기존 완료 관측: Ralph Hurl 154/154, PTE Newman 311 assertion 통과. 서로 다른 채점 정본이므로 품질 동등성은 미검증이다.
- 기존 시간 관측: Ralph 약 14분, PTE 약 49분. 재실행한 수치가 아니다.
- n=1·단일 과제이며, Ralph는 첫 iteration에 완료되어 반복 재시작의 효과를 측정하지 못했다.
- PTE의 계획·인수인계 문서 가치는 측정하지 않았다. 세션 분할·캐시가 차이의 원인이라는 설명은 별도 통제 실험이 필요한 가설이다.
- 기존 세션별 비용 분해와 비용 원인 확정 서술은 중복 집계에 의존하므로 철회한다. 모든 서브에이전트 사용량이 보관됐는지는 검증하지 못했다.

## 재현 근거

- [재집계 JSON](../../docs/2026-09-21-usage-corrections.json): 포함 파일 SHA-256, 집계기 SHA-256, 고유 ID·중복·누락 수.
- [정정 기록](../../docs/2026-09-21-corrections.md), [실험 품질 규칙](../../docs/experiment-quality-rules.md).
- 저장소 루트에서 `python3 scripts/aggregate_tokens.py --json experiments/00[1-4]-*/runs/*/logs`.
- [원자료](runs/). EXP-002 기준선과 EXP-001 PTE를 사용한 비교는 해당 실험의 `runs/`도 포함한다.
