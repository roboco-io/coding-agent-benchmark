# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp053` · HARNESS `pi` · 조건 2개 × 언어 1 × n=3 = run 6개
- 상한: run당 20분 · 비용 run당 $4 · 실험 $20 → **최악 총액 $20** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| glm53 | `openrouter/z-ai/glm-5.3` | OpenRouter (https://openrouter.ai/api/v1), 제공자 Z.AI 고정(openRouterRouting only=[z-ai], allow_fallbacks=false, 엔드포인트 태그 z-ai/fp8), pi 사용자 정의 models.json(내장 z-ai/glm-5.3 정의 + 라우팅) | 1,048,576 | 131,072 | **적합** | api | $1.4/$4.4 | 없음 | $3.24 / $11.87 |
| glm53prime | `openrouter/z-ai/glm-5.3-prime` | OpenRouter (https://openrouter.ai/api/v1), 제공자 Alibaba 고정(openRouterRouting only=[alibaba], allow_fallbacks=false, 엔드포인트 태그 alibaba — 유일 제공자), pi 사용자 정의 models.json(내장 z-ai/glm-5.3 정의 복제) | 1,000,000 | 131,072 | **적합** | api | $2.8/$8.8 | 없음 | $6.48 / $23.74 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $29.17 · p90 기준: $106.82
- 출처: `openrouter/z-ai/glm-5.3` 컨텍스트 OpenRouter GET /api/v1/models/<id>/endpoints, 2026-10-25 — Z.AI 엔드포인트 context_length 1048576, max_completion_tokens 131072, quantization fp8. 모델 등록 2026-08-18, 단가 OpenRouter GET /api/v1/models/<id>/endpoints, 2026-10-25 — Z.AI 엔드포인트 pricing(prompt 1.40, completion 4.40, input_cache_read 0.26, input_cache_write 0 / 100만 토큰, 구간 단가 없음) (2026-10-25 확인); `openrouter/z-ai/glm-5.3-prime` 컨텍스트 OpenRouter GET /api/v1/models/<id>/endpoints, 2026-10-25 — Alibaba 엔드포인트 context_length 1000000, max_completion_tokens 131072, quantization unknown. 모델 등록 2026-09-23(OpenRouter 설명: GLM-5.3 고속 변형, 출력 처리량 1.5–2배), 단가 OpenRouter GET /api/v1/models/<id>/endpoints, 2026-10-25 — Alibaba 엔드포인트 pricing(prompt 2.80, completion 8.80, input_cache_read 0.56, input_cache_write 0 / 100만 토큰, 구간 단가 없음) (2026-10-25 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
