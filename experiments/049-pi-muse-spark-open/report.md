# EXP-049 결과 보고: pi × Muse Spark Open (OpenRouter, Together 고정) 완주 검증 (EN n=3)

- 실험일: 2026-10-18 (23:41 KST – 10-19 00:00 KST, 단일 오케스트레이터 순차 3 run)
- 가설: [M-42](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 OpenRouter의 `meta/muse-spark-open`(제공자 Together 고정, 사용자 정의 models.json, thinking high)을 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 클라이언트: pi 0.87.1
- **판정: 검증** — EN 3/3 모두 iteration 1에서 완주했다. 게이트 통과와 독립 재검증 2회가 모두 13/13·154/154로 일치했고 개입은 없었다. 세션 시간은 5.2–6.7분, OpenRouter 청구 기록 기준 비용은 run당 $0.45–0.67이다.

> `ralph-model-benchmark` 스킬 `pi` 하네스를 적용했다. 설계는 [README.md](README.md)에 실행 전 고정했다. Meta Muse 계열과 OpenRouter 경로는 이 리포에서 처음 측정했다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값·불확실성 | 충족 여부 | 판정 범위 |
|---|---|---|---|
| 게이트 통과 + 재검증 2회 13/13·154/154 | 3/3 run 충족, 모두 iter 1 | 충족 | 검증 (3/3) |
| 무개입 | 사람 개입 0, 정체·상한 종료 0 | 충족 | — |
| 비용 상한 run당 $3·실험 $6 | 비용 가드 추정 최대 $0.92(run 2), 청구 합계 $1.63 | 상한 미도달 | — |
| 제공자·모델 고정 | 168 호출 전부 Together, `meta/muse-spark-open-20261015` | 충족 | — |

## run별 결과

| run | 예산 내 합격 | 채점(게이트 / 재검증×2) | 세션 시간 | 커밋 | output | reasoning | 입력 / 캐시 읽기 | API 호출 | 최대 프롬프트 | 비용(청구 기록) |
|---|---|---|---|---|---|---|---|---|---|---|
| musespark-en-1 | iter 1 | 13/154 · 13/154 ×2 | 6분 11초 | 2 | 25.9K | 10.1K | 53.6K / 1.83M | 58 | 53.7K | $0.4515 |
| musespark-en-2 | iter 1 | 13/154 · 13/154 ×2 | 6분 42초 | 1 | 33.8K | 23.9K | 100.8K / 2.70M | 49 | 101.0K | $0.6746 |
| musespark-en-3 | iter 1 | 13/154 · 13/154 ×2 | 5분 13초 | 2 | 25.3K | 14.5K | 62.6K / 2.11M | 61 | 62.7K | $0.5027 |

- 세션 시간은 pi 세션 기록의 첫·마지막 타임스탬프 차이(iteration 1)다. 게이트 채점 약 15초는 포함하지 않는다.
- output은 reasoning을 포함한다(pi usage 기준). reasoning 열은 그중 추론 토큰이다.
- 비용 열은 OpenRouter `GET /api/v1/generation`의 `total_cost`를 run의 모든 responseId에 대해 합한 값이다. 공개 단가(100만 토큰당 입력 $1.25, 출력 $4.25, 캐시 읽기 $0.15)로 pi usage를 환산한 값과 소수 넷째 자리까지 같다. 이 리포에서 처음으로 제공자 측 청구 기록과 대조한 비용이지만, 월별 청구서와 대조한 것은 아니다.
- 비용 가드 추정($0.49–0.92)은 청구 기록보다 크다. 가드는 제공자 usage와 대화 기록 바이트 하한 중 큰 값을 쓰는 보수적 추정이기 때문이다.
- 산출물: 세 run 모두 Fastify를 썼고, run 2·3은 Prisma를 함께 썼다. 세 run 모두 하네스가 주입한 `PORT`를 따랐다.

## 다른 pi 조건과의 관측값 병치 (우위 판정 없음)

| 조건 | 실험·시점 | 세션 시간 중앙값 | run당 환산 비용 |
|---|---|---|---|
| pi × Muse Spark Open | EXP-049, 2026-10-18 | 6.2분 | $0.45–0.67 |
| pi × glm-5.3-flash | EXP-046, 2026-10-15 | 9.0분 | $0.04–0.07 |
| pi × gemini-4-argon | EXP-047, 2026-10-16 | 13.0분 | $0.85–0.89 |
| pi × DeepSeek V4.1-Flash | EXP-029, 2026-09 | 3.3분 | 약 $0.04–0.07 |

pi 하네스로 측정한 오픈 웨이트 모델 중 Muse Spark Open은 DeepSeek V4.1-Flash(EXP-029)보다 느리고 glm-5.3-flash(EXP-046)보다 빨랐다. 비용은 단가가 높아 두 모델보다 약 10배 컸다. 실행 시점·제공자 부하·pi 버전이 서로 달라 이 차이를 모델 성능의 우열로 단정하지 않는다.

## 모델 유지·노출 설정

- 제공자: `openRouterRouting {only: ["together"], allow_fallbacks: false}`. 사후 전수 대조에서 3 run 168 호출이 모두 Together였다.
- 응답 모델: OpenRouter 기록의 `model`이 전수 `meta/muse-spark-open-20261015`, pi 세션의 `model`은 `meta/muse-spark-open`이다.
- 노출: pi `-nc -ns -ne -np -na`로 상위 지침·스킬·확장을 노출하지 않았다. 세션 기록에서 하네스 경로(`measure.sh`·`driver.sh`·`metrics`·다른 run)를 참조한 건수는 0이다.
- 가중치: Hugging Face `meta-models/Muse-Spark-Open-816B-A42B`(Muse Model License, 수동 승인 gated)가 공개되어 있다. Together가 이 가중치를 그대로 서빙하는지와 양자화 여부는 확인하지 않았다.

## 이탈·특이 사항

- D-1 (키 노출, 로컬 한정): run 2에서 에이전트가 환경 변수를 출력하는 명령을 실행해 `OPENROUTER_API_KEY` 값이 로컬 세션 기록 1줄에 남았다. EXP-047 D-1과 같은 유형이다. 리포 보관본은 `redact_keys.py`로 1건 마스킹했고, 마스킹 뒤 키 값 직접 대조 0건이다. 로컬 원본(`~/experiments/ralph-exp049/sessions-musespark-en-2`)은 리포로 옮기지 않는다. 판정에는 영향이 없다.

## usage·집계 검증

- `usage_pi.py`(responseId dedup)로 집계했다. usage 누락 0이다. 결과는 [runs/usage-pi.csv](runs/usage-pi.csv)다.
- OpenRouter generation 기록의 호출 수(58·49·61)가 세션의 고유 responseId 수와 같다.
- 원자료: [runs/](runs/) — metrics, `recheck.csv`, 로그(gzip), `sessions.tar.gz`(마스킹본), `phase0.md`, `pi-models.json`, `model-specs.json`.

## 한계와 교란 변수

- 표본은 3 run, 과제는 1종(RealWorld 백엔드 신규 구현)이다. 3/3 완주는 관측 범위의 사실이며 일반적 성공률을 확정하지 않는다.
- 결과는 OpenRouter를 거쳐 Together가 서빙한 2026-10-15 스냅샷에 대한 것이다. 다른 제공자나 자체 서빙(폐쇄망 등)에서의 성능은 측정하지 않았다.
- 다른 pi 조건과의 차이에는 실행 시점과 제공자 부하가 섞여 있다.
