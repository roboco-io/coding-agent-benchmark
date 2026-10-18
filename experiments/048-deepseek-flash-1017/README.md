# EXP-048: Claude Code × DeepSeek V4.1-Flash-1017 직결 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-18, 판정 검증 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-41](../../hypotheses/catalog.md) — Claude Code를 DeepSeek Anthropic 호환 엔드포인트로 `deepseek-flash`(2026-10-17부터 DeepSeek-V4.1-Flash-1017)에 직결하면(thinking 기본값) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN, n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. DeepSeek은 2026-10-17에 V4.1-Flash의 가중치를 1017 버전으로 갱신하고 같은 API 별칭 `deepseek-flash`로 대체했다(공식 changelog https://api-docs.deepseek.com/updates/ , 가격 페이지 Version 칸, 2026-10-18 확인). 날짜가 붙은 ID는 API가 거부한다(`deepseek-flash-1017`·`deepseek-v4.1-flash-1017` 모두 "supported API model names are deepseek-flash, deepseek-v4-pro" 오류, 2026-10-18). 따라서 EXP-025(2026-09-21)의 flash-en 조건은 9월 가중치를, 이 실험은 1017 가중치를 측정한다.
- 기준선: EXP-025 flash-en(3/3 iter 1, 4.6–6.0분, run당 약 $0.1). 하네스·과제·정본은 같지만 Claude Code 버전(2.1.278 → 2.1.302)·실행 시점·run 상한(4시간 → 20분)이 달라, 차이는 가중치 효과로 단정하지 않고 조합 전체의 차이로 서술한다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | 모델 ID | 실행 도구 | 연결 | thinking |
|---|---|---|---|---|
| flash1017 | `deepseek-flash` (V4.1-Flash-1017) | Claude Code 2.1.302 `claude -p --dangerously-skip-permissions` | `https://api.deepseek.com/anthropic` 직결(Bearer, `DEEPSEEK_API_KEY`만 노출) | 제공자 기본값(effort high) |

- 사양·단가는 [runs/model-specs.json](runs/model-specs.json)(2026-10-18 확인): 컨텍스트 1,048,576, 최대 출력 393,216, 100만 토큰당 입력 $0.30·출력 $1.20·캐시 읽기 $0.006(피크). 오프피크는 절반이고 구간 단가는 없다. 환산 비용은 EXP-025와 같이 피크 단가로 계산한다.
- EXP-025와 같이 DeepSeek 공식 Claude Code 권장 설정(`[1m]` 접미사, effort max, 압축 창 조정)은 적용하지 않는다.

## 예산·계측

- 상한: run당 20분(`MAX_SEC=1200`), 정체 감시 300초, 30 iteration.
- 비용 상한: `RUN_BUDGET_USD=1`, `EXP_BUDGET_USD=3`, 최악 총액 $3. preflight 추정(캐시 할인 없음) run당 p50 $0.70. 사용자 승인 2026-10-18("진행 (Recommended)").
- usage는 `scripts/aggregate_tokens.py`(message.id dedup)로 집계한다. 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-18)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md). 첫 smoke에서 `usage_probe.py`가 HTTP 400("`content[].thinking` in the thinking mode must be passed back")으로 실패했다. probe가 만든 assistant 턴에 thinking 블록이 없었기 때문이다. probe가 이 오류에 한해 thinking 블록을 넣어 1회 재요청하도록 스킬을 고친 뒤 PASS(기대 입력 약 8,625 / 보고 7,099). Claude Code 본체 smoke는 수정 전에도 PASS였다.
