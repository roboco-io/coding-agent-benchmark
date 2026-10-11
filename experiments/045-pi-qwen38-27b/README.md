# EXP-045: pi × Qwen 3.8 27B (DashScope OpenAI 호환 직결) 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-11, 판정 검증 3/3). 결과: [report.md](report.md). [EXP-044](../044-pi-spark-qwen/README.md)는 사용자 결정으로 첫 run에서 중단되어 27b를 한 번도 실행하지 못했다. 이 실험은 그중 27b 조건만 다시 실행한다. run 상한은 사용자 지시(2026-10-11)로 20분에서 30분으로 올렸다. 상한을 올린 이유는 [EXP-042](../042-spark-qwen-direct/report.md)의 q27-en-1이 Claude Code 직결 경로에서 25.3분에 완주했기 때문이다.

## 가설

- 가설 코드·문장: [M-38](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DashScope OpenAI 호환 엔드포인트의 `dashscope/qwen3.8-27b`(thinking pi 기본값, 사용자 정의 models.json)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·30분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. EXP-042(Claude Code 직결, 4시간 상한, 1 run)와 비교할 때 달라지는 것은 하네스·API 형식·컨텍스트 관리·상한·실행 시점 전체다. 따라서 결과 차이를 조합 전체의 차이로만 서술하고, 하네스 단독의 효과로 단정하지 않는다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. **검증**은 3/3, **부분 검증**은 1–2/3, **기각**은 0/3이다. 모델 외적 장애(제공자 장애·하네스 결함)로 끝난 run은 **run 단위 보류**로 둔다.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | reasoning |
|---|---|---|---|
| q27 | `dashscope/qwen3.8-27b` | 983,616 / 131,072 | true |

- 정의 파일은 [runs/pi-models.json](runs/pi-models.json)이다. 이 파일은 EXP-044 정의에서 27b 항목만 남긴 것이다. 키는 `DASHSCOPE_API_KEY` 하나만 노출한다(`PI_KEEP_ENV`).
- 입력 한도와 최대 출력은 EXP-044 Phase 0(2026-10-10)에서 오류 메시지로 직접 확인한 값이다. 단가는 100만 토큰당 입력 $0.50, 출력 $3.00이며 입력 길이 구간은 없다. 이 단가는 EXP-042에서 확인한 공개 단가 페이지 값을 재사용한 것이다. 상세 출처는 [runs/model-specs.json](runs/model-specs.json)에 있다.

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-044와 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 30분(`MAX_SEC=1800`)이다. 300초(`STALL_SEC`) 동안 진행이 없으면 정체 감시가 iteration을 종료한다.
- 반복은 3 run이며 순차로 실행한다.
- 비용 상한은 하네스가 30초 간격으로 강제한다. run당 상한은 추정 $4, 실험 전체 상한은 $12다.
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 이 값은 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-11)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
