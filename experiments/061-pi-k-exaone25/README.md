# EXP-061 설계: pi × LG AI연구원 K-EXAONE 2.5 (EXAONE API) 랄프 루프 완주 검증 (EN n=3)

## 배경

LG AI연구원의 K-EXAONE 2.5(`k-exaone_v2.5`, 750B·활성 31B, 지식 기준 2026-01)는 EXAONE API(`https://api.exaone.ai/v1`)로 제공된다. 2026-11-11에 제공자 문서와 API를 직접 호출해 다음을 확인했다. API는 OpenAI 호환 `chat/completions`만 제공하며, `/v1/messages`·`/anthropic/v1/messages`는 404를 반환해 Anthropic 호환 엔드포인트가 없다. 따라서 `claude-direct`가 아닌 pi 하네스(OpenAI 호환 직결)를 쓴다. 컨텍스트는 524,288 토큰(입력과 `max_tokens`의 합 기준)이다. thinking은 항상 켜지며 `reasoning_effort` 기본값은 max다. tool calling은 실호출로 `tool_calls` 반환을 확인했다. usage는 보고되지만 캐시 항목은 없다. 과금은 문서에 없고 사용자가 무료라고 확인했다(2026-11-11). 요청 한도는 응답 헤더 기준 초당 1회·분당 60회·일 100회였다. 사용자가 사용 이력 분석에 동의해 일일 한도를 늘린 뒤 실행한다.

## 가설

- [M-53](../../hypotheses/catalog.md) — pi 0.87.1 × EXAONE API `k-exaone_v2.5`(reasoning_effort 제공자 기본 max, `preserve_thinking=true`, pi 정본 지속 지침 포함)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 60분(비정본)·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 질문 유형: 완주 가능성. 실험 단계: 탐색 파일럿.
- 판정 기준(사전 등록): 검증(3/3 완주) / 부분 검증(1–2/3) / 기각(0/3) / run 단위 보류(모델 외적 장애: 요청 한도 소진·제공자 오류로 run이 진행하지 못한 경우).
- 보조 지표: 세션 시간, iteration 수, output·reasoning 토큰, 호출 수, 커밋 수, **429(쓰로틀링) 발생 횟수와 재시도로 늘어난 시간**(사용자 지시로 관찰 대상). 국내 모델 기준선(EXP-020 Claude Code × solar-pro4 직결)과는 하네스·PROMPT 버전·시점이 교락하므로 방향성 기록만 한다.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| kexaone | `exaone/k-exaone_v2.5`, `reasoning_effort` 미전송(제공자 기본 max), `chat_template_kwargs.preserve_thinking=true` | pi 0.87.1 (`-nc -ns -ne -np -na`, `PI_PERSISTENCE=on`) | EXAONE API 키(`EXAONE_API_KEY`, `PI_KEEP_ENV`로만 노출), 사용자 정의 `runs/pi-models.json`(`thinkingFormat: chat-template`, maxTokens 65,536, strict mode 끔) | `runs/` |

- PROMPT: 스킬 정본 v2 EN. 채점: 스킬 Hurl 13파일, `/opt/homebrew/bin/hurl`.
- 상한: **run 60분, 정체 900초**(비정본, 아래 변경 기록), 30 iteration, 순차 3 run. 단가 0(무료)이라 비용 상한(run당 $1·실험 $3)은 형식상 값이며 실질 제약은 요청 한도다.
- usage: `usage_pi.py`(responseId dedup). 토큰 대리지표이며 청구 비용이 아니다.

## 리스크·한계

- 요청 한도(초당 1회)는 pi의 연속 도구 호출 속도와 부딪힐 수 있다. 429는 pi 재시도로 흡수되거나 iteration 종료로 나타날 수 있다. 세션 jsonl·로그에서 429를 집계해 보고하고, 같은 오류가 반복되며 진행이 멈추면 조사 전에 먼저 중단한다.
- 일일 한도가 run 도중 소진되면 그 run은 보류로 판정하고 한도가 회복된 뒤 재실행한다. 재실행은 이탈로 기록한다.
- pi maxTokens 65,536은 하네스 설정값이다. 문서상 최대 출력(512K)과 다르며, 입력+max_tokens가 524,288을 넘지 않도록 정한 값이다.
- 캐시 usage가 보고되지 않아 다른 모델과 입력 토큰 구성을 직접 비교할 수 없다.

## 실행 전 변경 기록 (2026-11-11, 본 실행 전 사전 등록)

처음에는 정본 상한(run 20분·정체 300초)으로 기동했다(14:17). run 1의 iteration 1·2가 모두 정체 감시(exit 124)로 종료되고 채점 0/13·커밋 0이었다. 세션 기록에서 출력 4,753 토큰 응답 하나가 약 5분 걸렸고, 다음 응답이 300초 안에 끝나지 않았다. pi는 응답이 끝나야 세션 파일에 기록하므로 긴 응답 하나가 정체로 판정된다. 실행을 멈추고(14:35) API를 직접 측정한 결과, 3,000 토큰 생성에 max 137초(약 22 tok/s)·high 157초(약 19 tok/s)가 걸렸고 두 경우 모두 3,000 토큰 전부가 reasoning이었다. 과거 완주 run의 출력 p50 약 31K·p90 약 63K 토큰을 이 속도로 생성하면 25–50분이 필요하다. 정본 상한으로는 모델 능력이 아니라 서빙 속도가 결과를 정하므로, 사용자 승인으로 **정체 900초·run 60분**으로 완화해 3 run을 새로 실행한다. 이 실험의 시간 지표는 다른 실험과 상한이 다르므로, 완주 여부는 비교하되 소요 시간 비교에는 상한 차이를 함께 적는다. 중단한 정본 상한 실행 원자료는 `~/experiments/ralph-exp061-strict-aborted/`에 보존하며 보고서에 이탈로 기록한다.
