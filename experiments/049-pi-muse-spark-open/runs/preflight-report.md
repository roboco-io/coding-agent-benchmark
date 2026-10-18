# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp049` · HARNESS `pi` · 조건 1개 × 언어 1 × n=3 = run 3개
- 상한: run당 20분 · 비용 run당 $3 · 실험 $6 → **최악 총액 $6** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| musespark | `openrouter/meta/muse-spark-open` | OpenRouter (https://openrouter.ai/api/v1), 제공자 Together 고정(openRouterRouting only=[together], allow_fallbacks=false), pi 사용자 정의 models.json | 1,048,576 | 943,718 | **적합** | api | $1.25/$4.25 | 없음 | $2.90 / $10.62 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $8.71 · p90 기준: $31.85
- 출처: `openrouter/meta/muse-spark-open` 컨텍스트 OpenRouter GET /api/v1/models/meta/muse-spark-open/endpoints — Together 엔드포인트 context_length 1048576, max_completion_tokens 943718, 2026-10-18. 모델 등록 2026-10-16, 단가 OpenRouter endpoints API, Together 엔드포인트 pricing (prompt 1.25, completion 4.25, input_cache_read 0.15 / 100만 토큰, 5개 제공자 동일, 구간 단가 없음) (2026-10-18 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
