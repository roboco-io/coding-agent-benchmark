# EXP-003 결과 보고: PTE + 스킬식 점진 공개

- 실험일: 2026-07-21
- 가설: [S-02](../../hypotheses/catalog.md) — 컨텍스트를 스킬 공식 권고(문서 200줄 이하, 스킬로 필요한 것만 로드)로 구조화하면 EXP-001 PTE 대비 토큰 대리지표 30% 이상 감소
- **판정: 기준 미달 (정정)** — 토큰 대리지표 1,128,420 → 875,083으로 22.45% 감소. 사전 30% 절감 기준 미달이며 기존 검증 판정을 철회한다.

## 2026-09-21 계측 정정

동일 run 안의 동일 `message.id`·usage를 한 번만 합산했다. 아래 값은 보관된 최상위 JSONL 파일 범위이며 실제 청구 비용이 아니다. `messages`는 고유 메시지 수, `sessions`는 JSONL 파일 수다. 누락된 외부 호출·서브에이전트 비용의 완전성은 미검증이다.

| run | 이전 대리지표 | 정정 대리지표 |
|---|---:|---:|
| plan-then-execute | 2,839,815 | 1,128,420 |
| pte-skills | 1,723,575 | 875,083 |

이전 값은 중복 usage 행을 합산했다. 기존 보고서의 해당 수치·파생 해석은 이 정정판으로 대체한다. 원자료는 변경하지 않았다.

## 정정 측정 결과

| 지표 | plan-then-execute | pte-skills |
|---|---:|---:|
| sessions | 16 | 15 |
| messages | 321 | 309 |
| usage_rows | 782 | 512 |
| duplicates | 461 | 203 |
| missing_usage | 0 | 0 |
| input_tokens | 598 | 589 |
| output_tokens | 289,000 | 157,000 |
| cache_creation_input_tokens | 838,822 | 717,494 |
| cache_read_input_tokens | 17,552,165 | 16,410,040 |
| token_proxy | 1,128,420 | 875,083 |

`token_proxy = input_tokens + output_tokens + cache_creation_input_tokens`. 캐시 읽기는 별도 표시하며 무료로 취급하지 않는다. reasoning은 공급자가 output에 포함한 값을 중복 가산하지 않는다.

## 판정·관측·한계

- 기존 완료 관측: PTE Newman 311 assertion, PTE+스킬 Hurl 154 요청 통과. 채점 정본이 달라 동일 품질의 비교는 아니다.
- 기존 시간 관측: 약 49분 → 34분. 이번 작업에서 재실행하지 않았다.
- n=1이며 태스크 분할과 스킬 구조가 함께 변경됐다. 감소의 원인을 스킬 하나로 분리할 수 없다.
- 수정 루프가 없었다는 기존 관측은 유지하되, 중복 집계에 의존한 구간별 절감액·기동 고정비·태스크당 절감률은 철회한다.
- Ralph 대비 토큰 대리지표는 약 6.41배지만 전략 전체의 비용 우위를 뜻하지 않는다.
- 과거 검증 환경의 패키지 손상 사고는 [원자료](runs/pte-skills/meta.md)에 남아 있다.

## 재현 근거

- [재집계 JSON](../../docs/2026-09-21-usage-corrections.json): 포함 파일 SHA-256, 집계기 SHA-256, 고유 ID·중복·누락 수.
- [정정 기록](../../docs/2026-09-21-corrections.md), [실험 품질 규칙](../../docs/experiment-quality-rules.md).
- 저장소 루트에서 `python3 scripts/aggregate_tokens.py --json experiments/00[1-4]-*/runs/*/logs`.
- [원자료](runs/). EXP-002 기준선과 EXP-001 PTE를 사용한 비교는 해당 실험의 `runs/`도 포함한다.
