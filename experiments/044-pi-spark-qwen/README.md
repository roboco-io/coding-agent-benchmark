# EXP-044: pi × DGX Spark 탑재 가능 Qwen 3종 (DashScope OpenAI 호환 직결) 랄프 루프 완주 검증 (EN n=3)

> 상태: **중단** (2026-10-10 18:53, 사용자 결정 — 첫 run iteration 1 진행 중). 결과: [report.md](report.md). [EXP-042](../042-spark-qwen-direct/README.md)와 같은 모델 3종을 pi 하네스로 실행하는 쌍 실험이다(2026-10-10 사용자 지시). 후보 근거: [조사 문서](../../docs/2026-10-10-local-runnable-open-weight-models.md).

## 가설

- 가설 코드·문장: [M-37](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DashScope OpenAI 호환 엔드포인트의 Qwen 3종(`dashscope/qwen3.8-flash`·`dashscope/qwen3-coder-next`·`dashscope/qwen3.8-27b`, thinking pi 기본값, 사용자 정의 `models.json`)을 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분(2026-10-10 변경, 원래 4시간) 안에 완주할 수 있다 — EN n=3, 완주율 판정·과금 배제.
- 질문 유형: **완주 가능성**. EXP-042와의 하네스 차이는 "Claude Code 직결 조합 vs pi 조합"의 전체 차이로만 서술하고, 하네스 단독 효과로 단정하지 않는다(실행 시점·API 형식·컨텍스트 관리가 함께 다름).
- 판정: 조건별 게이트 + 독립 재검증 2회 일치. **검증** 3조건 모두 3/3, **부분 검증** 일부, **기각** 모두 0/3, **run 단위 보류** 모델 외적 장애.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | reasoning |
|---|---|---|---|
| flash | `dashscope/qwen3.8-flash` | 983,616 / 131,072 | true |
| coder | `dashscope/qwen3-coder-next` | 204,800 / 65,536 | false |
| q27 | `dashscope/qwen3.8-27b` | 983,616 / 131,072 | true |

- 한도 근거: 2026-10-10 DashScope `compatible-mode/v1/chat/completions` 오류 응답에서 직접 확인(`Range of input length should be [1, 983616]`·`[1, 204800]`, `Range of max_tokens should be [1, 131072]`·`[1, 65536]`). EXP-042 coder-en-1에서 Claude Code가 입력 204,800 한도를 넘겨 400으로 iteration이 끝난 관측이 있어, pi에는 실제 한도를 넣었다.
- `compat`·`thinkingLevelMap`은 EXP-029 `qwen3.8-max` 정의를 복사했다. coder는 생각 모드가 없는 모델이라 `reasoning:false`, `supportsReasoningEffort:false`.
- 정의 파일: [runs/pi-models.json](runs/pi-models.json). 키는 EXP-042와 같은 `DASHSCOPE_API_KEY`(`PI_KEEP_ENV`로 이 키만 노출).

## 과제·예산·계측

- 과제·정본·채점기·완료 기준·상한·제외 규칙: EXP-042와 같다(EN 정본 md5 `2c28ea6b7f16125d9b3105f5ee00b126`, Hurl 13파일, 30 iteration). 상한은 EXP-043 D-1·D-2 변경을 기동 전에 반영해 20분(`MAX_SEC=1200`)·정체 300초(`STALL_SEC`)다([EXP-043 deviations](../043-pi-gptoss120b-bedrock/runs/deviations.md)).
- 반복: 조건당 3 run, 회차 교차 순차 총 9 run. 비용 상한: 9 run 환산 $20 초과 시 중단 검토.
- usage: `usage_pi.py`(responseId dedup). 토큰 대리지표이며 청구 비용 아님.

## Phase 0 기록

- [x] 스모크 3/3 PASS — [runs/phase0.md](runs/phase0.md)
