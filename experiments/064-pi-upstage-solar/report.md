# EXP-064 결과 보고: pi × Upstage Solar Mini 4.5 Preview·Solar Pro 4·Solar Pro 4 Contributor 랄프 루프 완주 탐색 (EN 각 n=1)

- 실험일: 2026-11-24 (12:15–13:23 KST, 순차 3 run)
- 가설: [M-55](../../hypotheses/catalog.md) — pi 0.87.1 × Upstage `solar-mini-4-5-preview`·`solar-pro-4`·`solar-pro-4-contributor`(thinking high, pi 정본 지속 지침)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 40분(비정본)·30 iteration 안에 무개입 완주할 수 있다 (모델별 EN n=1, 탐색).
- 클라이언트: pi 0.87.1
- **판정: 탐색 — 3/3 완주 관측** — Mini 4.5 Preview iteration 1(11:34, 429 100건 포함), Pro 4 iteration 2(38:26), Pro 4 Contributor iteration 1(17:22). 비용은 정가 기준 run당 $0.12·$1.73·$0.73(Contributor는 Pro 4 정가 환산). 각 n=1이므로 재현성과 contributor·일반 모델의 성능 차이는 판정하지 않는다.

## 사전 기준 대조

| 조건 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| mini45 `solar-mini-4-5-preview` | 1/1 = 완주 관측 | iteration 1 완주 | 완주 관측 |
| pro4 `solar-pro-4` | 1/1 = 완주 관측 | iteration 2 완주 | 완주 관측 |
| pro4c `solar-pro-4-contributor` (실행 중 추가, 설계 문서 참조) | 1/1 = 완주 관측 | iteration 1 완주 | 완주 관측 |

모든 완주는 하네스 게이트 pass와 독립 재검증 2회(13/13·154/154 일치, `runs/recheck.csv`)로 확인했다.

## run별 결과

세션 시간은 orchestrator 로그의 run 시작·종료 시각 차이다. 토큰은 `usage_pi.py`(responseId dedup)로 집계한 응답 usage 합계다. input은 캐시 읽기를 뺀 값이고, output은 추론 토큰을 포함한다(pi usage `input+output+cacheRead = totalTokens`, Upstage 응답 `completion_tokens`가 `reasoning_tokens`를 포함함을 직접 호출로 확인). 비용은 이 토큰에 Upstage **정가**(할인 전 단가)를 곱한 추정값이며(사용자 지시, 2026-11-24) Upstage 청구액과 대조하지 않았다.

| run | iteration | 세션 | 응답 수 | input | cache read | output (reasoning) | 커밋 | 추정 비용 |
|---|---|---|---|---|---|---|---|---|
| mini45-en-1 | 1 | 11:34 | 199 | 64,664 | 7,905,024 | 74,787 (39,074) | 2 | $0.12 |
| pro4-en-1 | 2 | 38:26 | 301 | 714,684 | 22,273,600 | 146,559 (60,769) | 2 | $1.73 |
| pro4c-en-1 | 1 | 17:22 | 158 | 199,196 | 9,833,344 | 63,262 (19,448) | 1 | $0.73 |

정가(100만 토큰당 입력/캐시 읽기/출력, Upstage 모델 문서 2026-11-24 확인): Mini 4.5 Preview $0.10/$0.01/$0.40, Pro 4 $0.30/$0.06/$1.20. **Pro 4 Contributor는 사용자 지시로 Pro 4 정가로 환산해 공개한다.** 실행 시점의 실제 적용 단가는 이보다 낮다 — Mini 4.5 Preview는 preview 90% 할인가 $0.01/$0.001/$0.04(약 $0.012), Pro 4는 프로모션 할인가 $0.15/$0.03/$0.60(약 $0.86), Contributor는 $0.09/$0.018/$0.36(약 $0.22). 하네스 비용 상한은 Pro 4 할인가 기준으로 작동했다. 응답 수에는 mini45의 429 오류 응답 100건이 들어 있다.

## Pro 4와 Contributor 비교 (관측값, 우열 판정 아님)

Upstage 문서는 `solar-pro-4-contributor`를 `solar-pro-4`와 같은 모델로 설명하며, 요청·응답을 Upstage가 저장해 학습에 쓰는 대가로 가격을 낮춘다. 응답 model 필드는 `solar-pro4-260806`과 `solar-pro-4-260806-contributor`로 같은 리비전 날짜를 가리킨다. 이번 관측에서는 contributor가 iteration 1에 17:22로 완주했고, 일반 Pro 4는 iteration 1을 Hurl 0/13·완료 선언 없이 끝낸 뒤 iteration 2에서 38:26에 완주했다. output은 contributor 63K, 일반 146K였다. 그러나 각 조건이 1 run이고, 같은 조건 안의 run 간 편차(과거 실험에서 세션 시간이 수 배 차이 난 사례)가 이 차이보다 작다는 근거가 없다. 따라서 이 결과는 contributor도 같은 과제를 완주한다는 것까지만 보여 준다. 두 모델의 성능이 같은지 다른지는 조건별 n=3 이상의 비교로 확인해야 한다.

## Mini 4.5 Preview 관측

Mini 4.5 Preview(35B·활성 3B)는 세 조건 중 가장 짧은 11:34에 iteration 1로 완주했고 추정 비용은 정가 기준 $0.12(preview 할인가 기준 $0.012)였다. 사전 측정의 생성 속도는 약 297 tok/s로 Pro 4(약 55 tok/s)의 약 5배였다. 다만 run 중 요청 한도 초과(429)가 100건 발생해 최대 약 5분이 재시도 대기에 쓰였으므로(D-1), 세션 시간은 한도 대기를 포함한 값이다. 이 모델은 2026-11-30에 종료되고 정식 Mini 4.5가 2026-12-01에 출시될 예정이므로, 정식판의 동작은 다를 수 있다.

## 과거 Solar 실험과 비교 (관측값)

Solar Pro 4의 과거 기록은 Claude Code를 Upstage Anthropic 호환 엔드포인트에 직결한 EXP-020(2026-08, 3/3 완주, 유효 시간 119–258분, 캐시 0)이다. 이번 pi 실행은 17–38분이었다. 그러나 하네스(Claude Code → pi), API(Anthropic 호환 → OpenAI 호환), PROMPT 버전(v1 → v2), 캐시 보고(0 → 수백만 토큰), 시점이 함께 달라졌으므로 이 차이를 하네스 효과로 단정하지 않는다.

## 이탈 (runs/deviations.md)

- **D-1** mini45 run에서 429(요청 한도 초과) 100건, 재시도 대기 최대 약 305초.
- **D-2** mini45 실행 중 사용자 지시로 pro4c 조건을 추가하고 재설정·재승인·smoke 후 재기동, 실험 비용 상한 $3 → $5.
- **D-3** pro4는 run 상한 40분(비정본)에 근접한 38:26에 완주. 정본 상한 20분이었다면 미완주였다.

## 한계

- 모든 조건이 n=1이다. 완주 여부·시간·토큰 모두 단일 관측이다.
- run 상한(40분)과 정체 한도(600초)가 정본(20분·300초)과 다르다.
- 비용은 응답 usage 기반 추정이며 Upstage 청구액과 대조하지 않았다.

## 결론 및 후속 실험

pi 0.87.1에서 Upstage Solar Mini 4.5 Preview, Solar Pro 4, Solar Pro 4 Contributor는 모두 이 과제를 완주했다. 실험 후 사용자는 이후 Solar Pro 4 실험을 `solar-pro-4-contributor`로만 실행하고 비용은 `solar-pro-4` 단가로 공개하도록 정했다(2026-11-24). 따라서 Pro 4 계열의 후속 결과는 contributor 변형의 결과이며, 일반 모델과의 성능 동등성은 이 실험에서 확인되지 않은 전제로 남는다. 후속 과제는 2026-12-01 출시 예정인 정식 Mini 4.5 측정이다.
