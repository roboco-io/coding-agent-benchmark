# EXP-049: pi × Muse Spark Open (OpenRouter, Together 고정) 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-19, 판정 검증 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-42](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 OpenRouter의 `meta/muse-spark-open`(제공자 Together 고정, 사용자 정의 models.json, thinking high)을 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. Meta Muse 계열은 이 리포에서 처음 측정한다. OpenRouter도 처음 쓰는 경로다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | thinking | 라우팅 |
|---|---|---|---|---|
| musespark | `openrouter/meta/muse-spark-open` | 1,048,576 / 943,718 | high | Together만 허용, fallback 금지 |

- 모델 정의는 [runs/pi-models.json](runs/pi-models.json)이다. pi 0.87.1 내장 목록에는 이 모델이 없어(2026-10-16 등록), 내장 `openrouter/meta/muse-spark-1.3` 항목(api `openai-completions`, thinkingFormat `openrouter`)을 따르고 id·라우팅만 바꿨다.
- 라우팅 고정 이유: OpenRouter는 이 모델을 Modal·Together·Nebius(fp4)·Fireworks·BaseTen(fp4) 5곳으로 라우팅한다(2026-10-18). 제공자가 바뀌면 양자화·서빙 스택이 달라질 수 있어 `openRouterRouting: {only: ["together"], allow_fallbacks: false}`로 고정했다. Together는 최근 30분 가동률 100%, 지연 p50 0.7초, 캐시 지원, 양자화 표기 없음이었다. run 1 첫 응답의 OpenRouter generation 기록에서 `provider_name` Together, `model` `meta/muse-spark-open-20261015`를 확인했다.
- 가중치: Hugging Face `meta-models/Muse-Spark-Open-816B-A42B`(Muse Model License, 수동 승인 gated, 2026-10-18 확인). Together 서빙이 이 가중치와 같은지는 제공자 문서로 확인하지 않았다.
- 키는 `~/.zsh_secrets`의 `OPENROUTER_API_KEY`만 노출한다(`PI_KEEP_ENV`).
- 사양·단가는 [runs/model-specs.json](runs/model-specs.json)(2026-10-18 확인): 100만 토큰당 입력 $1.25, 출력 $4.25, 캐시 읽기 $0.15, 구간 단가 없음, 5개 제공자 동일.

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-047과 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초다.
- 비용 상한: `RUN_BUDGET_USD=3`, `EXP_BUDGET_USD=6`, 최악 총액 $6. preflight 추정(캐시 할인 없음) run당 p50 $2.90. 사용자 승인 2026-10-18("바로 3 run (Recommended)").
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 토큰 대리지표이며 청구 비용이 아니다. OpenRouter generation 기록의 `total_cost`와 대조할 수 있다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-18)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
