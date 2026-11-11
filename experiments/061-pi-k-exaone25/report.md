# EXP-061 결과 보고: pi × LG AI연구원 K-EXAONE 2.5 (EXAONE API) 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-11-11 (본 실행 14:45–17:47 KST, 순차 3 run). 같은 날 14:17–14:35에 정본 상한(run 20분·정체 300초)으로 먼저 기동한 실행은 run 1의 iteration 2개가 모두 정체 종료되어 중단했고 [runs/strict-aborted/](runs/strict-aborted/)에 보관했다.
- 가설: [M-53](../../hypotheses/catalog.md) — pi 0.87.1 × EXAONE API `k-exaone_v2.5`(reasoning_effort 제공자 기본 max, preserve_thinking, pi 정본 지속 지침)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 60분(비정본)·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 기각** — 상한을 60분·정체 900초로 완화해도 0/3 완주. 출력 속도가 약 20 tok/s로 느려 긴 응답 하나가 15분 정체 감시에 걸리는 일이 반복되었고, 가장 멀리 간 run 3도 60분에 4/13 파일(87 요청)에서 멈췄다.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| exaone/k-exaone_v2.5 | 3/3 완주 = 검증, 0/3 = 기각 | 0/3 (세 run 모두 60분 run 상한 도달) | 기각 |

## run별 결과

세션 시간은 세션 jsonl의 첫·마지막 기록 시각 차이다. usage는 `usage_pi.py`(responseId dedup) 값이다. EXAONE API는 캐시 usage를 보고하지 않으며, `completion_tokens`에 reasoning 토큰이 포함된다(속도 탐침에서 completion 3,000 중 reasoning 3,004로 보고됨).

| run | 완주 | iteration (종료 사유) | 세션 시간 | 호출 | input | output | 최대 프롬프트 | 커밋 | 마지막 채점 | 재검증 ×2 |
|---|---|---|---|---|---|---|---|---|---|---|
| kexaone-en-1 | 미완주 | 3 (정체·정체·run 상한) | 57.3분 | 36 | 330.1K | 24.4K | 35.8K | 0 | 0/13 | — |
| kexaone-en-2 | 미완주 | 2 (정체·정체+run 상한) | 59.7분 | 27 | 423.5K | 28.3K | 35.7K | 0 | 0/13 | — |
| kexaone-en-3 | 미완주 | 1 (run 상한) | 59.7분 | 87 | 6,299.1K | 80.7K | 113.7K | 0 | 4/13 (87 요청) | 4/87 ×2 |

run 1은 세 iteration 모두 Hurl 테스트를 읽고 요구사항을 정리하는 데 시간을 썼고 코드 파일을 만들지 않았다. run 2는 `package.json`·`tsconfig.json`·Prisma 스키마를 만들고 의존성을 설치한 뒤 정체 종료되었다. run 3은 iteration 1이 정체 없이 60분 동안 진행되어 `src/` 15개 파일을 만들었고, 통과 파일은 `auth`·`errors_auth`·`errors_profiles`·`profiles`였다. 세 run 모두 커밋이 없었다. 세 run 모두 Fastify + Prisma + SQLite 스택을 골랐다.

## 원인 분석: 서빙 속도와 정체 감시

pi는 모델 응답이 끝나야 세션 파일에 기록한다. 하네스의 정체 감시는 세션·로그·앱 파일이 갱신되지 않는 시간을 재므로, 생성 시간이 정체 한도를 넘는 응답 하나는 그대로 정체로 판정된다.

세션 기록에서 출력 1,500 토큰 이상인 완료 응답의 생성 속도(다음 기록까지 시간 기준, 도구 실행 시간 포함)는 대부분 16–33 tok/s, 중앙 약 20 tok/s였다. 가장 큰 완료 응답은 9,679 토큰이었다. 별도 속도 탐침에서도 `reasoning_effort` max 약 22 tok/s, high 약 19 tok/s로 추론 강도를 낮춰도 빨라지지 않았다. 이 속도로는 정체 300초 안에 약 6K 토큰, 900초 안에 약 18K 토큰까지만 생성할 수 있다. 과거 완주 run의 총 출력은 p50 약 31K·p90 약 63K 토큰이므로, 생성 시간만 25–50분이 필요하다.

정체로 끝난 응답 4건(정본 상한 실행 2건 포함 시 6건)은 내용이 기록되지 않아, 모델이 매우 긴 응답을 생성 중이었는지 서버 스트림이 멈췄는지 구분하지 못했다. 정체 직전 입력 크기와 같은 약 1만 5천 토큰 입력으로 스트리밍 탐침을 보냈을 때는 첫 청크 1.3초, 최대 청크 간격 1.3초로 158 토큰 짧은 응답을 정상 반환했다([runs/stream-probe.txt](runs/stream-probe.txt)). 즉 같은 크기의 입력에서 서버가 항상 멈추는 것은 아니며, 정체를 재현하지 못했다. 서버 쪽 스트림 종료는 run 1 iteration 3에서 1회(`terminated`, reasoning 약 4,000자 스트리밍 후) 관측되었다. 429(쓰로틀링) 오류는 3 run 동안 0건이었다(초당 1회 한도는 응답이 느려 닿지 않았다).

따라서 이 결과는 "K-EXAONE 2.5가 이 과제를 구현할 수 없다"를 보인 것이 아니라, **2026-11-11 시점 EXAONE API의 서빙 속도(약 20 tok/s)에서 pi 정본 하네스로 60분 안에 완주하지 못했다**는 관측이다. 모델 능력과 서빙 속도의 기여를 나누지 못했다.

## 이탈 기록

- **D-1 정본 상한 실행 중단**: 14:17 정본 상한으로 기동했으나 run 1 iteration 1·2가 모두 정체 종료(0/13)되어 14:35에 수동 중단했다. 속도 탐침 후 사용자 승인으로 정체 900초·run 60분으로 완화해 3 run을 새로 실행했다. 변경 사유는 실행 전에 설계 문서에 기록했다.
- **D-2 정체 종료 반복**: 본 실행에서 정체 종료(exit 124)가 run 1에서 2회, run 2에서 2회 발생했다. 사전 등록한 상한 그대로 개입하지 않았다.
- **D-3 서버 스트림 종료 1회**: run 1 iteration 3에서 `terminated` 오류 1회. pi가 같은 iteration 안에서 계속 진행했다.

## 다른 실험과 비교 (관측값, 우열 판정 아님)

이 실험은 run 상한(60분)·정체 한도(900초)가 다른 pi 실험(20–30분·300초)과 다르다. 같은 pi 정본 하네스·PROMPT v2의 EXP-053(GLM-5.3)·EXP-060(Muse Ember)은 3/3 iteration 1 완주에 세션 2–10분이었다. 국내 모델인 solar-pro4(EXP-020, Claude Code 직결, PROMPT v1)는 3/3 완주했으나 유효 119–258분이 걸렸다. 하네스·PROMPT 버전·상한·시점이 모두 달라 차이를 모델 차이로 단정하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` jsonl(run 1 3개, run 2 2개, run 3 1개), usage 누락 0. 토큰은 대리지표이며, 사용자 확인 기준 무료 API라 청구는 없다.
- 재현 자료: `runs/`의 `bench.env`, `model-specs.json`, `pi-models.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage-pi.csv`, 로그(gz), `sessions.tar.gz`, `stream-probe.*`, 중단 실행 `strict-aborted/`. 보관 전 `redact_keys.py` 마스킹 결과 0건.

## 한계와 교란 변수

- 과제 1개·n=3이다. 0/3은 이 조건·시점의 관측값이다.
- 서빙 속도는 시간대·제공자 부하에 따라 달라질 수 있다. 측정은 2026-11-11 오후 한 시간대뿐이다.
- 정체 응답의 내용이 남지 않아 원인을 확정하지 못했다. pi가 스트리밍 중 부분 응답을 기록하거나 하네스가 네트워크 수신을 활동으로 인정하면 구분할 수 있다(ROADMAP 후속 과제).
- `reasoning_effort` 기본값(max)만 측정했다. high에서도 속도는 비슷했으나 응답 길이(reasoning 양)는 다를 수 있다.
