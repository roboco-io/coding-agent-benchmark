# EXP-064 설계: pi × Upstage Solar Mini 4.5 Preview·Solar Pro 4 랄프 루프 완주 탐색 (EN 각 n=1)

## 배경

Upstage는 2026-11-23에 `solar-mini-4-5-preview`(35B·활성 3B, 512K 컨텍스트, 2026-11-30 종료 예정 preview)를 공개했다. 사용자가 이 모델과 `solar-pro-4`를 pi 에이전트로 각 1회 실행하도록 지시했다(2026-11-24). 2026-11-24에 `GET https://api.upstage.ai/v1/models`로 두 ID가 실재함을 확인했다. `solar-pro-4`는 별칭이며 응답 model 필드는 `solar-pro4-260806`이다. 두 모델 모두 OpenAI 호환 `chat/completions`에서 `reasoning_effort`를 받고, 응답 메시지에 `reasoning` 필드를 돌려준다. usage의 `completion_tokens`는 `reasoning_tokens`를 포함한다(직접 호출로 확인). Solar Pro 4의 과거 기록은 Claude Code 직결(EXP-020, 3/3 완주, 119–258분)과 리포에 보관되지 않은 로컬 EXP-058(Claude Code 직결, 0/1 시간 초과)이며, pi 하네스로는 처음이다.

## 가설

- [M-55](../../hypotheses/catalog.md) — pi 0.87.1 × Upstage `solar-mini-4-5-preview`·`solar-pro-4`(thinking high, pi 정본 지속 지침)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 40분(비정본)·30 iteration 안에 무개입 완주할 수 있다 (모델별 EN n=1).
- 질문 유형: 완주 가능성. 실험 단계: 탐색 파일럿(n=1, 사용자 지시).
- 판정 기준(사전 등록): 모델별 완주 1/1 = 완주 관측, 0/1 = 미완주 관측. n=1이므로 검증·기각을 확정하지 않고 "탐색"으로 적는다. 제공자 장애로 run이 진행하지 못하면 보류.
- 보조 지표: 세션 시간, iteration 수, input·cache·output(reasoning 포함) 토큰, 추정 비용, 커밋 수.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| mini45 | `upstage/solar-mini-4-5-preview`, `--thinking high` (`reasoning_effort=high`) | pi 0.87.1 (`-nc -ns -ne -np -na`, `PI_PERSISTENCE=on`) | Upstage OpenAI 호환 `https://api.upstage.ai/v1`, `UPSTAGE_API_KEY`(`PI_KEEP_ENV`로만 노출), 사용자 정의 `runs/pi-models.json`(`thinkingFormat: openai`, maxTokens 65,536, strict mode·developer role 끔) | `runs/` |
| pro4 | `upstage/solar-pro-4`, `--thinking high` | 같음 | 같음 | `runs/` |

- PROMPT: 스킬 정본 v2 EN (md5 `3d11ae8d28546ac730d482d015cfd6d9`). 채점: 스킬 Hurl 13파일, `/opt/homebrew/bin/hurl`.
- 상한: **run 40분, 정체 600초**(비정본), 30 iteration, 순차(mini45 → pro4). 근거: 2026-11-24 직접 측정에서 3,000 토큰 생성이 mini45 10.1초(약 297 tok/s), pro4 54.3초(약 55 tok/s)였다. 과거 완주 run의 출력 p90 약 63K 토큰을 pro4 속도로 생성하면 약 19분이 걸리고, 긴 응답 하나가 300초 정체 감시에 걸릴 수 있다(EXP-061 선례). 두 조건에 같은 상한을 쓴다.
- 비용: 단가(100만 토큰당 입력/출력/캐시 읽기) mini45 $0.01/$0.04/$0.001(preview 90% 할인), pro4 $0.15/$0.60/$0.03(프로모션 할인), 출처 Upstage 모델 문서(2026-11-24 확인). 비용 상한 run당 $2, 실험 $3. preflight 추정 실험 전체 p50 $0.37·p90 $1.37.
- 승인: 2026-11-24 사용자 승인 "이 조건으로 실행 (권장)".
- usage: `usage_pi.py`(responseId dedup). 토큰과 추정 비용은 응답 usage 기반 추정이며 청구액이 아니다.

## 리스크·한계

- n=1이므로 결과는 이 시점의 관측이다. 재현성을 말하지 않는다.
- run 상한이 정본(20분)과 다르므로 다른 실험과 시간을 비교할 때 상한 차이를 함께 적는다.
- pi maxTokens 65,536은 하네스 설정값이다(문서상 최대 출력 128K).
- preview 모델은 정식 출시 전에 동작이 바뀔 수 있다.

## 실행 중 조건 추가 (2026-11-24, pro4 run 시작 전 사전 등록)

mini45 run이 진행 중일 때 사용자가 `solar-pro-4-contributor` 조건 추가를 지시했다. 이 모델은 `solar-pro-4`와 같은 모델이며, 요청과 응답을 Upstage가 저장해 학습에 쓰는 대가로 정가의 70% 할인가(입력 $0.09·출력 $0.36·캐시 $0.018)로 제공된다(Upstage 문서, 2026-11-24 확인). 2026-11-24 직접 호출에서 응답 model 필드는 `solar-pro-4-260806-contributor`였다. 사용자 지시는 두 가지다. 첫째, `solar-pro-4`와 contributor를 모두 실행해 성능 차이가 있는지 확인한다. 둘째, 공개하는 비용은 두 조건 모두 `solar-pro-4` 단가로 환산한다. 따라서 `model-specs.json`의 contributor 단가는 `solar-pro-4` 단가로 두고, 실제 단가는 출처 문구에 적었다. 이 설정은 비용 상한도 실제보다 보수적으로 작동하게 한다.

| 조건 | 모델 | 실행 도구·연결 |
|---|---|---|
| pro4c | `upstage/solar-pro-4-contributor`, `--thinking high` | pro4와 같음 |

- 실행 순서: mini45 → pro4 → pro4c (순차). pro4 run은 설정 변경을 위해 mini45가 끝날 때까지 시작을 보류했다.
- 실험 비용 상한을 $3에서 $5로 올렸다. run이 3개가 되어 p90 추정 합계(약 $2.7)가 기존 상한에 가깝기 때문이다. run당 상한 $2는 그대로다.
- 성능 비교의 한계: 각 조건 n=1이므로 pro4와 pro4c의 차이는 한 번의 관측이다. 같은 모델의 run 간 변동(과거 실험에서 세션 시간이 수 배 차이 나는 사례)이 조건 차이보다 클 수 있다. 이 실험은 contributor가 완주하는지와 토큰·시간이 같은 범위에 있는지만 관측하며, "성능 차이 없음"을 확정하지 않는다.
