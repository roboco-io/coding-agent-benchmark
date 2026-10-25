# EXP-053: pi × GLM-5.3·GLM-5.3-Prime (OpenRouter) 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-25, 판정 검증 — 조건별 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-46](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 OpenRouter를 거쳐 `z-ai/glm-5.3`(Z.AI 고정)·`z-ai/glm-5.3-prime`(Alibaba 고정)을 돌리면(thinking high) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (조건별 EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. 같은 계열을 Z.ai Coding Plan 직결로 측정한 EXP-046(glm-5.3-flash)과 관측값을 나란히 놓되 우열은 판정하지 않는다(모델·경로·PROMPT 버전 교락). 두 조건 간 차이도 방향성 기록에 그친다(제공자가 다르다: Z.AI 대 Alibaba).
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. 조건별로 **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | pi 모델 ID | 고정 제공자 | 컨텍스트 / 최대 출력 | thinking |
|---|---|---|---|---|
| glm53 | `openrouter/z-ai/glm-5.3` | Z.AI (fp8) | 1,048,576 / 131,072 | high |
| glm53prime | `openrouter/z-ai/glm-5.3-prime` | Alibaba (유일 제공자, 양자화 미공개) | 1,000,000 / 131,072 | high |

- **PROMPT v2 첫 적용 실험**이다(2026-10-25, `PORT` 안내 한 줄 추가). EXP-001–052(v1)와 비교할 때 PROMPT 차이를 교란 변수로 적는다.
- 모델 ID·제공자·단가는 2026-10-25 OpenRouter `GET /api/v1/models/<id>/endpoints`로 확인했다. `glm-5.3-prime`은 OpenRouter 설명상 GLM-5.3의 고속 변형(출력 처리량 1.5–2배)이며, Z.ai 공식 문서와는 대조하지 않았다.
- pi 0.87.1 내장 `z-ai/glm-5.3` 정의(thinkingFormat `openrouter`)를 바탕으로 제공자 고정(`openRouterRouting`, `allow_fallbacks=false`)을 넣은 [runs/pi-models.json](runs/pi-models.json)을 쓴다. prime은 내장 정의가 없어 같은 정의를 복제했다.
- thinking high: EXP-049(pi × OpenRouter)와 같은 수준.
- 키는 `~/.zsh_secrets`의 `OPENROUTER_API_KEY`만 노출한다(`PI_KEEP_ENV`).
- 사양·단가는 [runs/model-specs.json](runs/model-specs.json): 100만 토큰당 glm-5.3 입력 $1.40·출력 $4.40·캐시 읽기 $0.26, prime 입력 $2.80·출력 $8.80·캐시 읽기 $0.56. 구간 단가 없음.
- 실행 순서: 순차, run-all이 조건을 교차한다(glm53-en-1 → glm53prime-en-1 → …).

## 과제·예산·계측

- 과제, 채점기, 완료 기준은 EXP-051과 같다(EN 정본 v2, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초다.
- 비용 상한: `RUN_BUDGET_USD=4`, `EXP_BUDGET_USD=20`. OpenRouter 잔여 크레딧 $23.37(2026-10-25 확인). preflight 추정과 사용자 승인은 Phase 0에 기록한다.
- usage는 `usage_pi.py`(responseId dedup)로 집계하고, OpenRouter generation 기록과 대조한다(EXP-049 방식). 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-25, "진행 (Recommended)")
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
