# 실행 전 점검 보고서 (preflight)

- 하네스: `/Users/dohyunjung/experiments/ralph-exp061` · HARNESS `pi` · 조건 1개 × 언어 1 × n=3 = run 3개
- 상한: run당 60분 · 비용 run당 $1 · 실험 $3 → **최악 총액 $3** (상한이 강제되는 경우)
- 적합성 기준: 입력 컨텍스트 256,000 이상 적합, 200,000 이상 주의, 미만 부적합. 근거: 과거 완주 run 최대 프롬프트 p50 96,524 · p90 152,713 · 최대 174,422 토큰 (61 run, 2026-10-10 측정)

| 조건 | 모델 | 제공자 | 컨텍스트 | 최대 출력 | 적합성 | 과금 | 입력/출력 단가(100만 토큰) | 구간 단가 | run당 추정 p50 / p90 |
|---|---|---|---|---|---|---|---|---|---|
| kexaone | `exaone/k-exaone_v2.5` | LG AI연구원 EXAONE API (https://api.exaone.ai/v1, OpenAI 호환 chat/completions), pi 사용자 정의 models.json. Anthropic 호환 엔드포인트 없음(/v1/messages·/anthropic/v1/messages 404, 2026-11-11 확인) | 524,288 | 65,536 | **적합** | api | $0/$0 | 없음 | $0.00 / $0.00 |

- run당 추정은 과거 완주 run의 총 입력(p50 2,217,287 · p90 8,278,631)과 출력(p50 31,102 · p90 63,420)에 캐시 할인 없이 단가를 곱한 값이다. 입력 단가는 최대 프롬프트 p90이 속한 구간을 적용했다. 완주하지 못하고 상한까지 도는 run은 이보다 클 수 있으며, 그 경우 비용 상한이 run을 멈춘다.
- 실험 전체 추정(p50 기준): $0.00 · p90 기준: $0.00
- 출처: `exaone/k-exaone_v2.5` 컨텍스트 https://docs.exaone.ai/ko/docs/k-exaone-2.5 — context length 524,288(입력+max_tokens 초과 시 400), models 페이지 최대 출력 512K, GET /v1/models에 k-exaone_v2.5 단일 등록, tool calling 실호출 확인(2026-11-11). max_output 65536은 하네스가 pi maxTokens로 지정한 값, 단가 제공자 문서에 단가 없음. 사용자 확인 '무료임'(2026-11-11). 요청 한도: 초당 1·분당 60·일 100(응답 헤더, 2026-11-11), 사용 이력 분석 동의 시 일일 한도 증설 (2026-11-11 확인)

다음 단계: 이 보고서를 사용자에게 보여 주고 AskUserQuestion으로 진행 여부를 묻는다. 사용자가 진행을 고른 경우에만 `bash approve.sh "<답변 원문>"`을 실행한다.
