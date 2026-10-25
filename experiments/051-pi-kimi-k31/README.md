# EXP-051: pi × Kimi K3.1 Pro·Pro Highspeed 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-25, 판정 검증 — 조건별 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-44](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 Moonshot OpenAI 호환 엔드포인트의 `kimi-k3.1-pro`·`kimi-k3.1-pro-highspeed`(사용자 정의 models.json 항목, thinking high)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (조건별 EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. 같은 하네스·같은 thinking 수준으로 kimi-k3를 측정한 EXP-029 kimi 조건과 관측값을 나란히 놓되 우열은 판정하지 않는다(시점·모델 교락). 두 변형 간 소요 차이도 방향성 기록에 그친다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. 조건별로 **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | thinking |
|---|---|---|---|
| k31pro | `moonshotai/kimi-k3.1-pro` | 1,048,576 / 131,072 | high |
| k31hs | `moonshotai/kimi-k3.1-pro-highspeed` | 1,048,576 / 131,072 | high |

- 두 모델 ID는 2026-10-25 Moonshot `GET /v1/models`에서 확인했다. pi 0.87.1 내장 카탈로그에는 없으므로, 내장 `kimi-k3` 정의(api `openai-completions`, thinkingFormat `openai`, `requiresReasoningContentOnAssistantMessages`)를 복제하고 id·이름·단가만 바꾼 [pi-models.json](pi-models.json)을 쓴다.
- thinking high 고정 이유: EXP-029 kimi 세션 기록에서 `thinking_level_change` → `high`를 확인했다. 제공자 기본값(`max`)이 아니라 EXP-029와 같은 수준으로 맞춘다.
- 키는 `~/.zsh_secrets`의 `KIMI_API_KEY`를 `MOONSHOT_API_KEY`로만 노출한다(`PI_KEYMAP`).
- 사양·단가는 [runs/model-specs.json](runs/model-specs.json)(출처 platform.kimi.ai 가격 페이지, 2026-10-25 확인): 100만 토큰당 pro 입력 $2·출력 $10, highspeed 입력 $4·출력 $20, 캐시 읽기 $0.20. 구간 단가 없음. highspeed 최대 출력은 문서에 별도 값이 없어 미확인이다.

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-050과 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초다. 순차 실행이며 run-all이 조건을 교차한다(k31pro-en-1 → k31hs-en-1 → k31pro-en-2 …).
- 비용 상한: `RUN_BUDGET_USD=3`, `EXP_BUDGET_USD=15`. preflight 추정과 사용자 승인은 Phase 0에 기록한다.
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-25, "진행 (Recommended)")
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
