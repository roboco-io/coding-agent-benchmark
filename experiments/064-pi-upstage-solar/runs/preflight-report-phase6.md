# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp064` · HARNESS `pi` · 조건 1개 × 언어 1 × n=5 = run 5개
- 상한: run당 40분 · 비용 run당 $2 · 실험 $8 → **최악 총액 $8** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| mini45sb | `upstage/solar-mini-4-5-preview` | Upstage OpenAI 호환 chat/completions (https://api.upstage.ai/v1, Bearer UPSTAGE_API_KEY), pi 사용자 정의 models.json. GET /v1/models에 solar-mini-4-5-preview 존재(created 20261028), 응답 model 필드 solar-mini-4-5-preview (2026-11-24 확인) | 512,000 | 128,000 | **적합** | api | $0.01/$0.04 | 없음 | $0.02 / $0.09 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $0.12 · p90 기준: $0.43
- 출처: `upstage/solar-mini-4-5-preview` 컨텍스트 https://console.upstage.ai/docs/models/solar-mini-4-5-preview.md (2026-11-24 확인, 512K / 128K, 35B·활성 3B, 2026-11-30 종료 예정 preview), 단가 https://console.upstage.ai/docs/models/solar-mini-4-5-preview.md (2026-11-24 확인, preview 90% 할인가. 정가 $0.10/$0.40/$0.01). completion_tokens가 reasoning_tokens를 포함함을 직접 호출로 확인 (2026-11-24 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
