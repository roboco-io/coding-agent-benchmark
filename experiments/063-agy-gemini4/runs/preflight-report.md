# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp063` · HARNESS `agy` · 조건 3개 × 언어 1 × n=3 = run 9개
- 상한: run당 30분 · 비용 run당 $1 · 실험 $3 → **최악 총액 $3** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| carbon | `gemini-4-carbon` | Google Gemini API (generativelanguage.googleapis.com) , via Antigravity CLI agy 1.5.14 (Google 계정 구독 OAuth(authMethod=consumer, 키체인), 격리 HOME) | 1,048,576 | 32,768 | **적합** | subscription | $0/$0 | 없음 | $0.00 / $0.00 |
| neon | `gemini-4-neon` | Google Gemini API (generativelanguage.googleapis.com) , via Antigravity CLI agy 1.5.14 (Google 계정 구독 OAuth(authMethod=consumer, 키체인), 격리 HOME) | 1,048,576 | 65,536 | **적합** | subscription | $0/$0 | 없음 | $0.00 / $0.00 |
| hydrogen | `gemini-4-hydrogen` | Google Gemini API (generativelanguage.googleapis.com) , via Antigravity CLI agy 1.5.14 (Google 계정 구독 OAuth(authMethod=consumer, 키체인), 격리 HOME) | 1,048,576 | 65,536 | **적합** | subscription | $0/$0 | 없음 | $0.00 / $0.00 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $0.00 · p90 기준: $0.00
- 출처: `gemini-4-carbon` 컨텍스트 Gemini API GET /v1beta/models/gemini-4-carbon (inputTokenLimit 1048576, outputTokenLimit 32768), 2026-11-22. agy models 목록에 gemini-4-carbon-{low,medium,high} 확인 2026-11-22, 단가 Google 계정 구독(Antigravity) 실행 — run별 API 청구 없음. API 환산 단가(보고용, 하네스 상한 미적용): 입력 $2.0·캐시 $0.1·출력 $10.0 (https://aistudio.google.com/docs/pricing (standard, output은 thinking 포함, 암시적 캐시만, 구간 없음, 2026-12-01부터 입력 $4·출력 $20·캐시 $0.20)) (2026-11-22 확인); `gemini-4-neon` 컨텍스트 Gemini API GET /v1beta/models/gemini-4-neon (inputTokenLimit 1048576, outputTokenLimit 65536), 2026-11-22. agy models 목록에 gemini-4-neon-{low,medium,high,xhigh} 확인 2026-11-22, 단가 Google 계정 구독(Antigravity) 실행 — run별 API 청구 없음. API 환산 단가(보고용, 하네스 상한 미적용): 입력 $3.0·캐시 $0.15·출력 $15.0 (https://aistudio.google.com/docs/pricing (standard, output은 thinking 포함, 암시적 캐시만, 구간 없음)) (2026-11-22 확인); `gemini-4-hydrogen` 컨텍스트 Gemini API GET /v1beta/models/gemini-4-hydrogen (inputTokenLimit 1048576, outputTokenLimit 65536), 2026-11-22. agy models 목록에 gemini-4-hydrogen-{low,medium,high,xhigh} 확인 2026-11-22, 단가 Google 계정 구독(Antigravity) 실행 — run별 API 청구 없음. API 환산 단가(보고용, 하네스 상한 미적용): 입력 $1.5·캐시 $0.075·출력 $7.5 (https://aistudio.google.com/docs/pricing (standard, output은 thinking 포함, 암시적 캐시만, 구간 없음)) (2026-11-22 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
