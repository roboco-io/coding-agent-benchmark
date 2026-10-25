# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp051` · HARNESS `pi` · 조건 2개 × 언어 1 × n=3 = run 6개
- 상한: run당 20분 · 비용 run당 $3 · 실험 $15 → **최악 총액 $15** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| k31pro | `moonshotai/kimi-k3.1-pro` | Moonshot OpenAI 호환 엔드포인트 (https://api.moonshot.ai/v1), pi 0.87.1 내장 moonshotai provider + 사용자 정의 models.json 항목(내장 kimi-k3 정의 복제, 단가만 변경) | 1,048,576 | 131,072 | **적합** | api | $2/$10 | 없음 | $4.75 / $17.19 |
| k31hs | `moonshotai/kimi-k3.1-pro-highspeed` | Moonshot OpenAI 호환 엔드포인트 (https://api.moonshot.ai/v1), pi 0.87.1 내장 moonshotai provider + 사용자 정의 models.json 항목(내장 kimi-k3 정의 복제, 단가만 변경) | 1,048,576 | 131,072 | **적합** | api | $4/$20 | 없음 | $9.49 / $34.38 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $42.71 · p90 기준: $154.72
- 출처: `moonshotai/kimi-k3.1-pro` 컨텍스트 Moonshot GET https://api.moonshot.ai/v1/models context_length 1048576 (2026-10-25). max_completion_tokens 기본 131072(quickstart); highspeed 별도 한도 문서 없음 — 미확인, 단가 https://platform.kimi.ai/docs/pricing/chat (구 platform.moonshot.ai, 301), https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart.md — 구간 단가 없음("no tiering by context length"). 캐시 쓰기 별도 과금(5m $2/1h $4) — 추정에는 입력 단가로 포함 (2026-10-25 확인); `moonshotai/kimi-k3.1-pro-highspeed` 컨텍스트 Moonshot GET https://api.moonshot.ai/v1/models context_length 1048576 (2026-10-25). max_completion_tokens 기본 131072(quickstart); highspeed 별도 한도 문서 없음 — 미확인, 단가 https://platform.kimi.ai/docs/pricing/chat (구 platform.moonshot.ai, 301), https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart.md — 구간 단가 없음("no tiering by context length"). 캐시 쓰기 별도 과금(5m $4/1h $8) — 추정에는 입력 단가로 포함 (2026-10-25 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
