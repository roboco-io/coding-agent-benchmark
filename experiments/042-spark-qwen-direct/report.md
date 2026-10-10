# EXP-042 결과 보고: Claude Code × DGX Spark 탑재 가능 Qwen 3종 직결 (중단)

- 실험일: 2026-10-10 (11:35–15:41 KST, 단일 오케스트레이터 순차, 9 run 중 5 run 실행 후 중단)
- 가설: [M-35](../../hypotheses/catalog.md) — Claude Code(`claude -p` 2.1.296)를 DashScope Anthropic 호환 엔드포인트로 DGX Spark 1대(128GB)에 올릴 수 있는 크기의 오픈 웨이트 Qwen 3종(`qwen3.8-flash`·`qwen3-coder-next`·`qwen3.8-27b`, thinking 기본값)에 직결하면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 클라이언트: Claude Code 2.1.296
- **판정: 보류(실험 중단)** — 사용자 결정으로 5/9 run에서 중단해 사전 기준(조건별 3 run)을 채우지 못했다. 실행한 범위의 관측: flash 2/2, q27 1/1, coder 1/2 완주(완주 4 run 모두 게이트와 독립 재검증 2회 13/13·154/154 일치). 중단 원인은 DashScope Anthropic 호환 엔드포인트가 tool_result 토큰을 `message_start` usage에서 빼고 보고해 Claude Code의 자동 압축이 작동하지 않은 것이다. coder는 입력 한도(204,800)에 닿아 HTTP 400을 반복했고, 2 run의 환산 비용이 하한 약 $89(콘솔 청구 합계 $94.22)로 이 리포의 run당 비용 최고치를 크게 넘었다.

> 설계는 [README.md](README.md)에 실행 전 고정했다. 같은 모델의 pi 측정은 [EXP-044](../044-pi-spark-qwen/README.md)로 넘겼으나 그 실험도 첫 run에서 중단됐다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값 | 충족 여부 | 판정 범위 |
|---|---|---|---|
| 조건별 3/3 완주 → 검증 | flash 2/2, q27 1/1, coder 1/2 (나머지 4 run 미실행) | 판정 불가 | 완주 가능성 |
| run 단위 보류(제공자 장애·하네스 결함) | coder 2 run에서 제공자 usage 결함에 따른 400 반복(D-1) | 해당 — 실험 단위 중단 | — |

## run별 결과

| run | 결과 | 채점(게이트 / 재검증×2) | run 소요 | iteration | 커밋 | 요청 수 | 최대 프롬프트 | output(하한) | 환산 비용(하한) |
|---|---|---|---|---|---|---|---|---|---|
| flash-en-1 | iter 1 완주 | 13/154 · 13/154 ×2 | 13.7분 | 1 | 4 | 50 | 106K | 43.5K | $0.23 |
| coder-en-1 | iter 3 완주 | 13/154 · 13/154 ×2 | 123.1분 | 3 (1·2는 exit 1) | 5 | 665 | 205K | 139.3K | $47.3 |
| q27-en-1 | iter 1 완주 | 13/154 · 13/154 ×2 | 25.3분 | 1 | 5 | 75 | 139K | 60.1K | $1.29 |
| flash-en-2 | iter 1 완주 | 13/154 · 13/154 ×2 | 12.0분 | 1 | 3 | 55 | 110K | 37.8K | $0.25 |
| coder-en-2 | 중단 | 4/64 → 10/143 (미완) | 71.4분 (중단) | 2 완료 + 3 진행 중 | 5 | 534 | 205K | 133.6K | $41.3 |
| flash-en-3 · coder-en-3 · q27-en-2 · q27-en-3 | 미실행 | — | — | — | — | — | — | — | — |

- run 소요는 run 시작부터 마지막 채점까지의 wall-clock이다.
- 요청 수와 토큰은 세션 jsonl에서 `message.id`별로 각 usage 필드의 최대값을 취한 하한값이다([runs/usage042.py](runs/usage042.py), [runs/usage.csv](runs/usage.csv)). 표준 집계기 `aggregate_tokens.py`는 같은 id에 서로 다른 usage가 기록되어 "conflicting usage" 오류로 중단한다(D-1과 같은 원인). tool_result 누락분은 복원되지 않으므로 실제 토큰은 이보다 많을 수 있다.
- 환산 비용은 Alibaba Cloud Model Studio 공개 단가(싱가포르, 2026-10-09 갱신 페이지)로 계산한 추정이며 청구액이 아니다. qwen3.8-flash $0.15/$0.47, qwen3.8-27b $0.50/$3.00(100만 토큰당 입력/출력, 구간 없음), qwen3-coder-next는 요청 입력 길이 구간별 $0.30/$1.50(32K 이하)·$0.50/$2.50(32K–128K)·$0.80/$4.00(128K–256K)이다. 캐시 읽기는 공개 단가 표에 없어 입력 단가의 10%로 가정했다(flash·q27만 해당, coder는 캐시 기록 0). 실제 청구액은 Alibaba Cloud 결제 콘솔에서 사용자가 확인한 **$94.22**다(2026-10-10 확인). 이 금액에는 EXP-044(약 $0.03)와 Phase 0 확인 요청(약 $0.1)도 들어 있을 수 있고, 같은 계정의 다른 사용분이 섞였는지는 확인하지 않았다. 세션 기록 기반 하한 추정(EXP-042 합계 $90.4)은 청구액의 약 96%로, 하한 추정이 실제보다 약간 낮다는 해석과 맞는다.
- coder 2 run의 요청 1,199건 중 442건이 128K 초과 구간이었다. 자동 압축이 없어 매 요청이 입력 한도 근처의 전체 대화를 다시 보냈다.

## 모델 유지·루프 기여

- 응답 `model` 필드는 run별로 요청 모델과 전수 일치했다(flash `qwen3.8-flash` 124·149건, coder `qwen3-coder-next` 1,085건, q27 `qwen3.8-27b` 224건). coder-en-1의 `<synthetic>` 2건은 Claude Code가 API 오류를 대화에 기록한 항목이다.
- coder-en-1은 iteration 1(80분)·2(32분)가 입력 한도 400으로 비정상 종료(exit 1)됐고, 새 세션으로 시작한 iteration 3(10분)에서 완주했다. 랄프 루프의 새 세션 재시작이 컨텍스트 초과를 우회한 사례다.

## usage·집계 검증

- 결함 근거: 같은 요청을 직접 재현한 결과, 50K 토큰 tool_result를 포함한 요청의 `message_start.usage.input_tokens`가 37로 보고됐다. `message_delta`와 OpenAI 호환 엔드포인트는 정상값을 보고했다. 상세 재현 표는 [runs/deviations.md](runs/deviations.md) D-1.
- 재현 자료: `bench.env`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `recheck.csv`, 로그(gz), `sessions.tar.gz`(마스킹 점검 완료, 검출 0건). coder-en-2 세션은 중단으로 driver가 복사하지 못해 실험자가 격리 설정 디렉터리에서 복사했다.

## 관측과 설명

- 직접 관측: flash와 q27은 iteration 1에 12–25분 안에 완주했다. coder는 두 run 모두 입력 한도에 닿았다.
- 가능한 설명: Claude Code는 서버가 보고한 입력 토큰으로 컨텍스트 사용량을 판단해 자동 압축을 시작한다. DashScope가 tool_result를 빼고 보고하면 실제 컨텍스트가 한도에 가까워도 압축이 시작되지 않는다. coder의 입력 한도(204,800)가 flash·q27(983,616)보다 훨씬 작아 coder에서만 400으로 드러났다고 본다. flash·q27도 같은 결함을 겪었지만 한도에 닿기 전에 완주했다.
- 확인에 필요한 비교: 같은 결함이 과거 같은 엔드포인트 실험(EXP-013·016·017, qwen3.8-max)의 토큰 수치에도 영향을 주었는지 재점검이 필요하다(미실시).

## 한계와 교란 변수

- 조건별 표본이 1–2 run이라 완주 가능성 판정을 내리지 않는다.
- flash·q27 완주는 사전 등록 상한(4시간) 기준이다. 이후 EXP-043에서 도입한 20분 상한을 적용하면 q27-en-1(25.3분)과 coder-en-1은 미완주가 된다.
- 토큰과 비용은 제공자 결함 때문에 하한 추정이며 다른 실험과 직접 비교하지 않는다.

## 결론 및 후속 실험

- 결론: DashScope Anthropic 호환 엔드포인트는 tool_result 토큰을 usage에서 누락해 Claude Code 자동 압축을 무력화한다. 입력 한도가 작은 qwen3-coder-next에서는 이 결함이 400 반복과 큰 비용으로 이어졌다. flash와 27b는 이 경로에서 관측한 3 run 모두 완주했다.
- 후속: (1) EXP-013·016·017 토큰 수치 재점검, (2) DashScope Anthropic 호환 엔드포인트를 쓰는 claude-direct 실험은 이 결함이 해결될 때까지 보류하거나 입력 한도가 큰 모델로 제한, (3) 같은 모델의 pi(OpenAI 호환) 측정은 EXP-044가 중단되어 남아 있다.
