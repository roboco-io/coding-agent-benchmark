# EXP-047: pi × Gemini 4 Argon 랄프 루프 완주 검증 (EN, 비용 측정 1 run 선행)

> 상태: **완료** (2026-10-16, 판정 검증 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-40](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 Gemini API의 `google/gemini-4-argon`(사용자 정의 models.json, thinking high)을 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. Gemini 4 계열은 이 리포에서 처음 측정한다. EXP-036(pi × gemini-3.8-flash, thinking high)과의 시간·토큰 차이는 모델·실행 시점·설정 조합 전체의 차이로만 서술한다.
- 단계: 이 모델은 단가가 기존 Gemini 측정 모델보다 높아(입력 $2.00·출력 $10.00 / 100만 토큰) **1단계로 1 run만 실행해 실제 비용을 측정**한다(2026-10-16 사용자 지시). 2단계(추가 2 run, 합계 n=3)는 1단계 비용을 보고 사용자가 다시 승인할 때만 실행한다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. n=3까지 실행하면 **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3이다. 1단계에서 끝나면 판정은 **보류(n=1)** 로 두고 관측만 보고한다. 모델 외적 장애(제공자 장애·쿼터·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**로 둔다.

## 하네스 선택 경위 (2026-10-16)

처음에는 사용자가 agy(Antigravity CLI)만 고르고 실행했다. smoke 단계에서 agy 1.3.2가 `--effort`를 거부했고, effort를 빼자 `gemini-4-argon is not recognized as a known model`로 실패했다. `agy update`로 확인한 최신 1.3.6의 모델 목록에도 argon이 없었다(Gemini 3.1 Pro, 3.6–3.8 Flash만 있음). 세 번 모두 API 호출 전 실패라 비용은 없다. 사용자가 Google 계정으로 로그인한 대화형 agy 1.3.6의 `/model` 메뉴에는 "Gemini 4 Argon"이 보이지만 "Unavailable · Gemini 4 Argon is currently available to Ultra and paid Pro plan subscribers."로 표시된다(사용자 스크린샷, 계정 등급 Antigravity Starter Quota). 즉 agy에서 argon은 Ultra·유료 Pro 구독 전용이며, API 키 경로와 현재 계정으로는 쓸 수 없다. 사용자가 pi 전환을 골랐다. pi 0.87.1 내장 목록에도 argon이 없어 사용자 정의 models.json으로 추가한다.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | thinking |
|---|---|---|---|
| argon | `google/gemini-4-argon` | 1,048,576 / 32,768 | high (EXP-036과 동일) |

- 모델 정의는 [runs/pi-models.json](runs/pi-models.json)이다. pi 내장 `google/gemini-3.8-flash` 항목(api `google-generative-ai`, thinkingLevelMap low/medium/high)을 그대로 따르고 id·단가·maxTokens만 바꿨다.
- 키는 `~/.zsh_secrets`의 `GEMINI_API_KEY`만 노출한다(`PI_KEEP_ENV`). pi 0.87.1 google provider는 `GEMINI_API_KEY`를 읽는다(docs/providers.md). EXP-036의 `GOOGLE_API_KEY` 매핑으로는 smoke에서 "No API key found for google"로 실패했다(2026-10-16). 다른 비밀값은 에이전트 환경에서 제거한다.
- 사양·단가 출처는 [runs/model-specs.json](runs/model-specs.json)에 있다(2026-10-16 확인). 출력 단가는 thinking 토큰을 포함하며, 구간 단가는 없고 암시적 캐시만 지원한다. 모델 문서는 최대 출력을 65,536으로 적어 API 모델 목록 값(32,768)과 다르다. 2026-12-01부터 단가가 2배로 오른다.

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-046과 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초(`STALL_SEC`)다.
- 비용 상한은 1단계 run당 추정 $5, 실험 $5다. preflight 추정(캐시 할인 없음)은 run당 p50 $4.75다. 참고로 EXP-035 gemini-3.8-flash(agy)의 실제 토큰량에 이 단가를 적용하면 약 $2.9–3.5다.
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 이 값은 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (1단계 2026-10-16 10:31, 2단계 10:54)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
