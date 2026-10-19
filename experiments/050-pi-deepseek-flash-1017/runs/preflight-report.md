# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp050` · HARNESS `pi` · 조건 1개 × 언어 1 × n=3 = run 3개
- 상한: run당 20분 · 비용 run당 $1 · 실험 $3 → **최악 총액 $3** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| flash1017 | `deepseek/deepseek-flash` | DeepSeek API OpenAI 호환 엔드포인트 (https://api.deepseek.com), pi 0.87.1 내장 deepseek provider, 별칭 deepseek-flash = DeepSeek-V4.1-Flash-1017 (2026-10-17 갱신) | 1,048,576 | 393,216 | **적합** | api | $0.3/$1.2 | 없음 | $0.70 / $2.56 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $2.11 · p90 기준: $7.68
- 출처: `deepseek/deepseek-flash` 컨텍스트 DeepSeek GET /models (context_window 1048576, max_output_tokens 393216), 2026-10-18. 날짜 붙은 ID(deepseek-flash-1017 등)는 API가 거부 — 별칭만 존재 (EXP-048 확인값 재사용, pi 내장 카탈로그 contextWindow 1000000·maxTokens 384000), 단가 https://api-docs.deepseek.com/quick_start/pricing (Version 칸 DeepSeek-V4.1-Flash-1017, 피크 단가로 보수 기록 — 오프피크는 절반, 구간 단가 없음) (2026-10-18 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
