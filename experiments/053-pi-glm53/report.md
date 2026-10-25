# EXP-053 결과 보고: pi × GLM-5.3·GLM-5.3-Prime (OpenRouter) 완주 검증 (EN n=3)

- 실험일: 2026-10-25 (17:38–18:20 KST, 단일 오케스트레이터 순차 6 run, 조건 교차)
- 가설: [M-46](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 OpenRouter를 거쳐 `z-ai/glm-5.3`(Z.AI 고정)·`z-ai/glm-5.3-prime`(Alibaba 고정)을 돌리면(thinking high, PROMPT v2) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (조건별 EN n=3, 완주율 판정·과금 배제).
- 클라이언트: pi 0.87.1
- **판정: 검증** — 두 조건 모두 3/3, 6 run 전부 iteration 1에서 완주했다. 게이트 통과와 독립 재검증 2회가 모두 13/13·154/154로 일치했고 개입·정체 종료는 없었다. 세션 시간은 glm-5.3 6.1–7.6분, prime 5.8–8.1분이며, 공개 단가 환산 비용은 run당 glm-5.3 $0.41–0.50, prime $0.92–1.95로 OpenRouter 호출별 청구 기록 합과 일치했다.

> `ralph-model-benchmark` 스킬 `pi` 하네스를 적용했다. 설계는 [README.md](README.md)에 실행 전 고정했다. **정본 PROMPT v2를 처음 적용한 실험**이다(PORT 안내 한 줄 추가). EXP-001–052는 v1이므로 비교 시 PROMPT 차이가 교란 변수로 들어간다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값·불확실성 | 충족 여부 | 판정 범위 |
|---|---|---|---|
| 게이트 통과 + 재검증 2회 13/13·154/154 | glm53 3/3, glm53prime 3/3, 모두 iter 1 | 충족 | 검증 (조건별 3/3) |
| 무개입 | 사람 개입 0, 정체·상한 종료 0 | 충족 | — |
| 비용 상한 run당 $4·실험 $20 | 비용 가드 추정 최대 $2.64(glm53prime-en-3), 가드 누계 약 $7.29, 청구 합계 $5.25 | 상한 미도달 | — |
| 제공자·모델 유지 | OpenRouter generation 316건 전수 — glm-5.3 `Z.AI`·served `z-ai/glm-5.3-20260816`, prime `Alibaba`·served `z-ai/glm-5.3-prime-20260921`. `thinking_level_change` 전수 `high` | 충족 | — |

## run별 결과

| run | 예산 내 합격 | 채점(게이트 / 재검증×2) | 세션 시간 | 커밋 | output | reasoning | 입력 / 캐시 읽기 | API 호출 | 최대 프롬프트 | 환산 비용 (= 청구) |
|---|---|---|---|---|---|---|---|---|---|---|
| glm53-en-1 | iter 1 | 13/154 · 13/154 ×2 | 7분 34초 | 4 | 24.3K | 11.5K | 43.2K / 1.27M | 46 | 43.2K | $0.497 |
| glm53-en-2 | iter 1 | 13/154 · 13/154 ×2 | 6분 3초 | 2 | 20.3K | 6.6K | 37.8K / 1.04M | 43 | 38.0K | $0.414 |
| glm53-en-3 | iter 1 | 13/154 · 13/154 ×2 | 6분 16초 | 2 | 21.0K | 7.6K | 41.4K / 1.13M | 43 | 41.7K | $0.443 |
| glm53prime-en-1 | iter 1 | 13/154 · 13/154 ×2 | 6분 32초 | 1 | 24.3K | 10.1K | 48.4K / 1.22M | 45 | 43.6K | $1.034 |
| glm53prime-en-2 | iter 1 | 13/154 · 13/154 ×2 | 5분 48초 | 4 | 18.6K | 6.5K | 44.2K / 1.13M | 49 | 38.7K | $0.918 |
| glm53prime-en-3 | iter 1 | 13/154 · 13/154 ×2 | 8분 8초 | 3 | 25.5K | 6.8K | 62.3K / 2.76M | 90 | 50.6K | $1.946 |

- 세션 시간은 pi 세션 기록의 첫·마지막 타임스탬프 차이(iteration 1)다. 게이트 채점 시간은 포함하지 않는다.
- 커밋 수는 산출 리포의 전체 커밋 수다. output은 reasoning을 포함한다(pi usage 기준).
- 환산 비용은 고정 제공자의 OpenRouter 공개 단가(100만 토큰당 glm-5.3 입력 $1.40·출력 $4.40·캐시 읽기 $0.26, prime 입력 $2.80·출력 $8.80·캐시 읽기 $0.56, 캐시 쓰기 0, 2026-10-25 확인)로 계산한 값이며, OpenRouter generation API의 호출별 `total_cost` 합과 run마다 소수 넷째 자리까지 같다([runs/openrouter-generations.csv](runs/openrouter-generations.csv)). 계정 사용액 증가($25 중 $1.63 → $6.73, smoke 포함 $5.10)는 generation 합($5.25)보다 작아 정산 반영 지연으로 본다.
- glm53prime-en-3은 짧은 Bash·편집 호출을 몇 초 간격으로 반복해 호출 수(90)와 캐시 읽기(2.76M)가 다른 run의 약 2배였고, prime의 높은 캐시 읽기 단가 때문에 비용도 약 2배였다. 비용 가드 추정은 이 run에서 $2.64로 청구($1.95)의 약 1.35배였고, 6 run 누계는 약 $7.29로 청구의 약 1.4배였다(EXP-052 Claude Code × Kimi의 약 2.3배보다 작다).
- 산출물: 6 run 모두 TypeScript + Fastify + Prisma를 썼다. 세션 기록에서 `$PORT` 참조가 run당 29–55회 나타났고 정체 종료는 0이었다.

## 조건 간·같은 계열 측정과의 병치 (우위 판정 없음)

| 조건 | 실험·시점 | 경로 | PROMPT | 세션 시간 | output | 환산 비용 |
|---|---|---|---|---|---|---|
| pi × glm-5.3 | EXP-053, 2026-10-25 | OpenRouter → Z.AI | v2 | 7.6 / 6.1 / 6.3분 | 24.3 / 20.3 / 21.0K | $0.497 / $0.414 / $0.443 |
| pi × glm-5.3-prime | EXP-053, 2026-10-25 | OpenRouter → Alibaba | v2 | 6.5 / 5.8 / 8.1분 | 24.3 / 18.6 / 25.5K | $1.034 / $0.918 / $1.946 |
| pi × glm-5.3-flash | EXP-046, 2026-10-11 | Z.ai Coding Plan 직결 | v1 | 9.0 / 7.1 / 11.0분 | 23.2 / 19.0 / 27.4K | $0.047 / $0.039 / $0.068 (종량제 환산) |

두 EXP-053 조건은 같은 날 교차 순서로 실행했지만 제공자(Z.AI / Alibaba)가 다르다. prime은 OpenRouter 설명상 출력 처리량이 1.5–2배인 고속 변형인데, 이번 세션 시간은 glm-5.3과 범위가 겹쳐(5.8–8.1분 대 6.1–7.6분) 이 과제에서 빠르다는 관측은 없었다. 세션 시간은 도구 실행·호출 수에 크게 좌우되므로 처리량 차이를 검증한 것이 아니다. EXP-046과는 모델(flash)·경로·PROMPT 버전·시점이 모두 달라 차이를 어느 하나로 돌리지 않는다.

## 모델 유지·노출 설정

- 응답 모델: pi 세션의 `model`은 요청 ID(`z-ai/glm-5.3`, `z-ai/glm-5.3-prime`)이고, OpenRouter가 기록한 실제 처리 모델은 `z-ai/glm-5.3-20260816`, `z-ai/glm-5.3-prime-20260921`이다(316건 전수).
- 제공자 고정: [runs/pi-models.json](runs/pi-models.json)의 `openRouterRouting`(`only`, `allow_fallbacks=false`)이 적용됐고, 다른 제공자로 넘어간 호출은 0이다. prime의 Alibaba 엔드포인트는 양자화를 공개하지 않는다(OpenRouter `quantization: unknown`).
- 노출: pi `-nc -ns -ne -np -na`로 상위 지침·스킬·확장을 노출하지 않았다. 에이전트 환경의 키는 `OPENROUTER_API_KEY`만 남겼다. 세션 기록에서 하네스 경로를 참조한 건수는 0이다.

## 이탈·특이 사항

- 없음. smoke는 첫 시도에 두 조건 모두 PASS했다. smoke 임시 세션은 smoke 스크립트가 정리해 smoke 단계의 제공자는 확인하지 못했고, 대신 본 run의 전 호출로 확인했다.

## usage·집계 검증

- `usage_pi.py`(responseId dedup)로 집계했다. usage 누락 0이다. 결과는 [runs/usage-pi.csv](runs/usage-pi.csv)다.
- OpenRouter generation API 조회 316건, 조회 실패 0.
- 키 점검: `OPENROUTER_API_KEY` 값이 세션·실행 로그·산출 리포에 나타난 건수 0(직접 대조). 보관본 `redact_keys.py` 마스킹 0건이며 커밋 시 `check_staged_keys.py`가 검사한다.
- 원자료: [runs/](runs/) — metrics, `recheck.csv`, 로그(gzip), `sessions.tar.gz`, `phase0.md`, `model-specs.json`, `preflight-report.md`, `openrouter-generations.csv`, `PROMPT-en.md`(v2).

## 한계와 교란 변수

- 표본은 조건별 3 run, 과제는 1종이다. 3/3 완주는 관측 범위의 사실이며 일반적 성공률을 확정하지 않는다.
- OpenRouter 경유라 지연·처리량에는 라우터와 제공자 인프라가 함께 들어 있다. 같은 모델을 Z.ai API 직결로 측정한 결과는 없다.
- PROMPT v2 첫 적용이라, v1 실험과의 차이에는 PROMPT 변경이 섞인다. 이번 6 run에서 정체 종료가 없었던 것을 PROMPT 변경의 효과로 단정하지 않는다(모델·하네스가 EXP-052와 다르다).
