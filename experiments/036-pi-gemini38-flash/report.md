# EXP-036 결과 보고: pi coding agent × gemini-3.8-flash 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-07 (17:38–18:21 KST, 순차 3 run, EXP-035 종료 직후)
- 가설: [M-29](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 `google/gemini-3.8-flash`(thinking high, Gemini API 키)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4h 안에 완주할 수 있다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 검증** — 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 333건 전부 `google`/`gemini-3.8-flash`, thinking 전 run `high`). 세션 13.1–15.6분. run 3은 하네스 파일·이전 run 기록을 읽은 run으로 표시(D-2).

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| google/gemini-3.8-flash (thinking high) | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 로그의 iteration 1 start–end(채점 제외). pi `input`은 비캐시 입력이며 reasoning은 output에 포함된다. 대리지표 = `input + output + cacheWrite`(청구 비용 아님).

| run | 완주 iter | 세션 시간(분) | 커밋 | 응답 수 | input | output (reasoning) | cacheRead | cacheWrite | 대리지표 | 재검증 ×2 |
|---|---|---|---|---|---|---|---|---|---|---|
| flash38-en-1 | 1 | 15.6 | 7 | 112 | 502,693 | 46,827 (28,429) | 7,775,938 | 0 | 549,520 | 13/154 ×2 |
| flash38-en-2 | 1 | 14.0 | 4 | 119 | 771,118 | 47,052 (29,993) | 4,800,673 | 0 | 818,170 | 13/154 ×2 |
| flash38-en-3 | 1 | 13.1 | 4 | 102 | 568,228 | 29,650 (12,198) | 3,559,063 | 0 | 597,878 | 13/154 ×2 |

## 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 | output | 환산 비용(run당) |
|---|---|---|---|
| pi × gemini-3.8-flash (이번) | 13.1–15.6분 | 29.7–47.1K | $0.80–1.14 |
| agy × gemini-3.8-flash (EXP-035, 같은 날 직전) | 15.5–22.4분 | 50.5–63.4K | $1.39–1.68 |
| pi × deepseek-flash (EXP-029, 2026-09-24) | 1.9–4.1분 | (보고서 참조) | $0.06 (중앙값) |

- 같은 pi 0.87.1에서 다른 Flash급 모델보다 응답 수(102–119)와 세션 시간이 컸다. 모델·시점이 함께 다르므로 원인을 모델로 확정하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` jsonl 1개. `usage_pi.py`(responseId dedup) 결과 중복·누락 0. google provider는 cacheWrite를 기록하지 않았다(0).
- 키: pi google provider는 `GOOGLE_API_KEY`를 우선 쓰므로 그 값에 `GEMINI_API_KEY`를 넣었다(Phase 0에서 두 값 일치 확인).
- 비용: Gemini API 키로 실제 과금이 있었으나 청구액은 확인하지 않았다. 2026-10-07 공개 단가 환산 run당 $0.80–1.14([analysis/cost/](../../analysis/cost/README.md), 청구액 아님). pi 세션의 자체 `cost` 값은 쓰지 않는다.

## 한계와 교란 변수

- 과제 1개·n=3.
- **run 간 정보 노출(D-2)**: run 3의 에이전트가 하네스 디렉터리를 탐색해 채점기 스크립트를 읽고 실행했고, 이전 run의 로그 끝부분과 metrics를 읽었으며, 하네스의 Hurl 정본을 자기 리포로 복사했다. 채점은 하네스 절대 경로 재검증으로 했으므로 판정은 유효하나, 이 run의 시간·토큰은 독립 시행 값으로 보기 어렵다.
- **비밀값 기록(D-3)**: run 1 세션 로그에 하네스가 export한 비밀값이 남았다. 리포 보관본은 마스킹했다. 하네스를 필요한 키만 노출하도록 수정했다.
- 설치된 pi-clm 확장은 `-ne`로 로드되지 않았다.
- 이탈 상세: [runs/deviations.md](runs/deviations.md).

## 결론 및 후속 실험

- 결론: gemini-3.8-flash는 pi 하네스에서도 이 과제를 3/3 iteration 1에 완주했다. EXP-035와 합쳐 두 하네스 6/6 완주.
- 후속: 하네스·run 디렉터리 분리 후 재측정, 동시기 다른 Flash급 모델(deepseek-flash 등)과 교차 측정.
