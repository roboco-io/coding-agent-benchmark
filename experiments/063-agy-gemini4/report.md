# EXP-063 결과 보고: Antigravity CLI × Gemini 4 Carbon·Neon·Hydrogen (구독 인증) 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-11-22 (01:21–01:41, 08:22–09:17 KST, 순차 9 run). 01:42–08:22 사이에는 구독 인증 실패(D-1)로 실행을 멈췄고 사용자가 재로그인했다.
- 가설: [M-54](../../hypotheses/catalog.md) — agy 1.5.14 × `gemini-4-carbon`·`gemini-4-neon`·`gemini-4-hydrogen`(effort high, Google 계정 구독 인증)은 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 30분·30 iteration 안에 무개입 완주할 수 있다 (모델별 EN n=3).
- 클라이언트: Antigravity CLI (agy) 1.5.14
- **판정: 검증** — 세 모델 모두 3/3 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 전 run `authMethod=consumer`·요청 모델 해석 확인). 세션은 Hydrogen 4:04–4:39, Neon 6:22–6:58, Carbon 12:51–14:36이다.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| `gemini-4-carbon` | 3/3 완주 = 검증 | 3/3 iteration 1 완주 | 검증 |
| `gemini-4-neon` | 3/3 완주 = 검증 | 3/3 iteration 1 완주 | 검증 |
| `gemini-4-hydrogen` | 3/3 완주 = 검증 | 3/3 iteration 1 완주 | 검증 |

## run별 결과

세션 시간은 driver 로그의 iteration 1 시작·종료 시각 차이다. 토큰은 agy transcript(`brain/*/transcript_full.jsonl`)의 PLANNER_RESPONSE usage 합계이며 driver 로그의 결과 JSON usage와 모든 run에서 일치했다. input은 캐시 읽기를 뺀 값이고, output은 thinking 토큰을 포함한다. API 환산은 공개 단가(2026-11-22 확인)를 곱한 보고용 값이며, 이 실험은 구독 실행이라 run별 API 청구가 없다.

| run | iteration | 세션 | planner 스텝 | input | cache read | output (thinking) | API 환산 |
|---|---|---|---|---|---|---|---|
| carbon-en-1 | 1 | 12:51 | 16 | 122,142 | 953,528 | 48,777 (27,448) | $0.83 |
| carbon-en-2 | 1 | 12:53 | 22 | 134,408 | 1,432,469 | 47,512 (26,806) | $0.89 |
| carbon-en-3 | 1 | 14:36 | 26 | 156,689 | 2,050,745 | 52,354 (28,586) | $1.04 |
| neon-en-1 | 1 | 6:58 | 17 | 96,772 | 772,341 | 33,864 (14,963) | $0.91 |
| neon-en-2 | 1 | 6:31 | 17 | 103,856 | 862,918 | 34,013 (14,846) | $0.95 |
| neon-en-3 | 1 | 6:22 | 14 | 90,653 | 630,369 | 32,784 (14,330) | $0.86 |
| hydrogen-en-1 | 1 | 4:04 | 18 | 111,464 | 940,055 | 31,594 (13,985) | $0.48 |
| hydrogen-en-2 | 1 | 4:24 | 21 | 123,593 | 1,347,544 | 30,844 (12,798) | $0.52 |
| hydrogen-en-3 | 1 | 4:23 | 23 | 113,476 | 1,187,137 | 31,199 (13,653) | $0.49 |

API 환산 단가(100만 토큰당 입력/캐시 읽기/출력)는 Carbon $2/$0.10/$10, Neon $3/$0.15/$15, Hydrogen $1.5/$0.075/$7.5이다(https://aistudio.google.com/docs/pricing). Carbon 단가는 2026-12-01에 두 배가 되므로, 그 이후 기준으로 환산하면 Carbon 값은 두 배가 된다.

## 세 모델 비교 (관측값, 우열 판정 아님)

세 모델은 같은 하네스·인증·effort·PROMPT에서 모두 첫 iteration에 완주했으므로, 이 과제의 완주 가능성에서는 차이가 없었다. 차이는 소요 시간과 토큰에서 보였다. Hydrogen은 세션 중앙값 4:23으로 가장 짧았고, Neon은 6:31, Carbon은 12:53으로 Hydrogen의 약 3배였다. Carbon은 output 토큰(약 48–52K)과 thinking 토큰(약 27–29K)이 Neon·Hydrogen(output 약 31–34K, thinking 약 13–15K)보다 많았다. 소요 시간을 모델 대기와 로컬 도구 실행으로 나누면([analysis/latency](../../analysis/latency/README.md), agy transcript 타임스탬프 기준) 차이는 대부분 모델 대기에서 났다. 모델 대기는 Carbon 625–746초(세션의 84–89%), Neon 290–323초(79–82%), Hydrogen 151–164초(61–69%)였고, 도구 실행은 세 모델 모두 66–116초로 비슷했다. 응답 1회당 모델 대기는 Carbon 28–41초, Neon 17–21초, Hydrogen 7–9초였다. 모델 대기 1초당 output 토큰은 Carbon 약 70–76, Neon 약 105–117, Hydrogen 약 188–207이었다. 따라서 Carbon이 느린 이유는 생성량이 많은 것과 함께, 같은 양을 생성하는 데 걸리는 시간이 Hydrogen의 약 2.7배인 점에도 있다. 이 처리량 값은 입력 처리와 첫 토큰 대기를 포함한 값이므로 순수 생성 속도와 같지 않다.

API 환산 비용은 Hydrogen이 약 $0.5로 가장 낮았다. Neon은 단가가 Carbon보다 높지만 토큰이 적어 Carbon과 비슷한 약 $0.9였다. 각 조건의 표본은 3 run이고 시점(01시대와 08–09시대)이 섞여 있으므로, 이 차이는 이 과제·이 시점의 관측으로만 읽어야 한다.

## 과거 agy·Gemini 실험과 비교 (관측값)

같은 하네스의 유일한 과거 실험인 EXP-035(agy 1.3.1 × gemini-3.8-flash, API 키 인증, PROMPT v1)는 세션 15.5–22.4분이었고 3 run 중 1 run이 iteration 2에서 완주했다. 이번 세 모델은 모두 이보다 짧았다. 그러나 agy 버전(1.3.1 → 1.5.14), 인증 경로(API 키 → 구독), PROMPT 버전(v1 → v2), 시점이 함께 달라졌으므로 이 차이를 모델 차이로 단정하지 않는다. 같은 Carbon을 pi로 돌린 EXP-062는 사용자 지시로 폐기해 비교 근거로 쓰지 않는다.

## 이탈 (runs/deviations.md)

- **D-1 구독 토큰 미복사로 hydrogen-en-1 인증 실패 (01:41–01:43)**: agy 구독 OAuth 토큰은 보통 macOS 키체인에 저장되지만, 01:37 토큰 만료 후 갱신된 토큰은 실 HOME의 `~/.gemini/antigravity-cli/antigravity-oauth-token` 파일에 있었다. 격리 HOME에는 이 파일이 없어 hydrogen-en-1 iteration 1·2가 "Authentication required"로 즉시 끝났다. 모델 호출은 없었다. 실행을 멈추고, 실 HOME에 토큰 파일이 있으면 격리 HOME에 복사하도록 `agy_env.sh`를 고쳤다. 이 run은 무효 처리했다.
- **D-2 재개 시도 중단 (08:17)**: 재개 시점에 토큰 파일이 사라져 있어(토큰이 다시 키체인으로 옮겨진 것으로 보임) 즉시 중단했다. 사용자가 08:20에 재로그인했다. run-all이 run마다 시작 전에 `agy_auth_check`(격리 HOME `agy models` + `authMethod=consumer`)로 인증을 확인하고, 실패하면 모델 호출 전에 전체를 멈추도록 보완했다. 이후 7 run은 모두 이 확인을 통과했다.
- 두 무효 시도의 원자료는 `runs/aborted/hydrogen-en-1-auth.tar.gz`에 보관했다(토큰 파일 제외). 유효한 hydrogen-en-1은 08:22에 같은 이름으로 다시 실행한 run이다.
- carbon-en-1·neon-en-1은 D-1 수정 전 하네스로 실행했다. 두 run과 나머지 run은 인증 경로(구독, `authMethod=consumer`)와 그 밖의 조건이 같고, 차이는 토큰을 격리 HOME에 전달하는 방식뿐이다.
- run 순서는 설계 문서에 적은 모델별 묶음이 아니라 하네스 정본의 교차 순서(carbon-1 → neon-1 → hydrogen-1 → carbon-2 …)였다.

## 노출·격리 확인

- 9 run의 transcript에서 에이전트가 참조한 하네스 경로는 격리 HOME(`agy-home`)뿐이었다. `measure.sh`·metrics·다른 run 디렉터리를 읽거나 실행한 기록은 없다(EXP-035 D-1 같은 하네스 노출 없음).
- 구독 인증을 위해 에이전트 HOME에 `~/Library/Keychains` 링크를 두었고, D-1 수정 후에는 토큰 파일이 있을 때 이를 HOME에 복사한다. 에이전트가 이 자격 증명을 읽을 수 있는 상태였으나, transcript에서 키체인·토큰 파일을 참조한 기록은 없다.
- 로그·transcript에 `429`·`RESOURCE_EXHAUSTED`·quota 오류는 없었다. 구독 사용량 한도에는 닿지 않았다.

## 한계와 교란 변수

- 모델별 표본은 3 run이다. 3/3 완주는 이 과제·이 조건에서의 관측이며 재현성을 확정하지 않는다.
- 구독 실행이므로 실제 청구액이 없고, 토큰은 대리지표다. API 환산은 공개 단가로 계산한 값이며 Google 청구로 대조하지 않았다.
- 구독 경로와 API 키 경로가 같은 서빙·같은 모델 리비전을 쓰는지는 확인하지 못했다. 이 결과를 API 키 경로 결과와 비교할 때는 인증 경로를 교란 변수로 적는다.
- effort는 high로 고정했다. Neon·Hydrogen의 xhigh, Carbon의 Google 권장값 medium은 시험하지 않았다.

## 결론 및 후속 실험

agy 1.5.14에서 Gemini 4 Carbon·Neon·Hydrogen은 구독 인증과 effort high로 이 과제를 모두 3/3 첫 iteration에 완주했다. 이 조건에서 Hydrogen이 가장 빠르고 API 환산 비용도 가장 낮았다. 하네스에는 agy 구독 인증 모드(`AGY_AUTH=subscription`)와 run 시작 전 인증 확인을 추가했다. 후속 과제는 구독 경로와 API 키 경로를 같은 모델로 비교해, 위의 처리량 차이가 인증 경로별 서빙 조건에서도 유지되는지 확인하는 것이다.
