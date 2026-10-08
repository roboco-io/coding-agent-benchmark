# EXP-041: pi coding agent × gemini-3.1-pro-preview (Preview) 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-08 (실행 전).

## 가설

- 가설 코드·문장: [M-34](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 Preview 모델 `google/gemini-3.1-pro-preview`(thinking high, Gemini API 키)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3). 부차 질문: 같은 하네스의 gemini-3.8-flash(EXP-036)보다 모델 호출 수·세션 시간이 적은가(관측 병치, 우열 판정 아님).
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 응답 수, 토큰 대리지표(`usage_pi.py`).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| pro31 | `google/gemini-3.1-pro-preview` **(Preview)**, `--thinking high` | pi 0.87.1 | pi 내장 `google` provider, `GEMINI_API_KEY` (`~/.zsh_secrets`) | `runs/` |

- **Preview 상태**: `gemini-3.1-pro-preview`는 2026-10-08 현재 Google이 정식 출시(GA)하지 않은 **미리보기(Preview)** 모델이다. Preview 모델은 예고 없이 동작·성능·가격이 바뀌거나 회수될 수 있다. 따라서 이 실험 결과는 실행 시점(2026-10-08)의 Preview 버전에 대한 관측값이며, 이후 GA 버전에 그대로 적용하지 않는다. 비교 대상인 `gemini-3.8-flash`(EXP-035/036)는 GA 모델이다.
- pi 0.87.1 내장 모델 목록에 `google/gemini-3.1-pro-preview`(컨텍스트 1.0M, 출력 65.5K)가 있어 사용자 정의 항목이 필요 없다. `-customtools` 변형은 쓰지 않는다.
- 키: `PI_KEYMAP="GOOGLE_API_KEY=GEMINI_API_KEY"`로 두 변수를 같은 값으로 맞추고 `PI_KEEP_ENV="GEMINI_API_KEY"`로 남긴다. 첫 스모크는 `GEMINI_API_KEY`가 환경에서 제거되어 `No API key found for google`로 실패했고, 이 설정 후 통과했다. pi는 두 변수가 모두 있으면 `GOOGLE_API_KEY`를 쓴다(스모크 경고). 그 외 `~/.zsh_secrets` 값은 에이전트 환경에서 제거된다.
- thinking은 EXP-036과 같은 `high`. 지침 노출 차단은 `-nc -ns -ne -np -na`(EXP-029·036과 동일).

## 과제·완료 기준


- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` (md5 `2c28ea6b7f16125d9b3105f5ee00b126`), setup.sh가 `checksums.md5`로 검증한다.
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl` 절대 경로.
- 완료 기준: 드라이버 게이트 `pass`(에이전트 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 run만 완주로 본다.

## 반복·실행 순서·예산

- 반복: EN n=3 (스킬 기본값). 순차 실행, 다른 실험과 동시 실행 금지. EXP-040(agy) 3 run 종료 후 EXP-041(pi) 3 run을 이어서 실행한다.
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초), iteration 정체 한도 900초(`STALL_SEC`). Gemini API 키는 종량 과금이므로 실제 지출이 생긴다. 지출액은 이 실험에서 계측하지 않는다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 인증·쿼터·가용성 장애로 iteration이 연속 3회 즉시 실패하면 해당 run을 보류로 기록하고 새 run 번호로 재실행한다.
- 판정: 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 제공자·하네스 장애 run은 **보류**.

## 환경 주의 (실행 전 확인, 2026-10-08)

- 모델 ID 확인: Gemini API `GET /v1beta/models`(같은 키)에서 Pro 등급 최신 텍스트 모델은 `gemini-3.1-pro-preview`다(그 외 `gemini-2.5-pro`, 별칭 `gemini-pro-latest`). Ultra 등급은 목록에 없다.
- 실험 번호: EXP-039는 다른 작업(gpt-6-luna, 스킬 커밋 859ab14에 언급)에서 쓰고 있어 건너뛴다. 가설 코드도 같은 이유로 M-32를 비워 두고 M-33·M-34를 쓴다.
- 기준선: 같은 하네스·같은 날 구성으로 실행한 gemini-3.8-flash(EXP-035 agy, EXP-036 pi, 2026-10-07). 모델 외에 시점(하루 차이)이 다르므로 차이는 조합 전체의 차이로 서술한다.
- 3000·3001·3003 포트를 VS Code 등이 점유 중이다(Phase 0 WARN). driver가 빈 포트를 `PORT`로 주입한다.

## 계측

- usage는 `usage_pi.py`(responseId dedup) 토큰 대리지표이며 청구 비용이 아니다. 시간은 driver 로그의 run start부터 마지막 iteration end까지.
- 응답 모델 필드가 `gemini-3.1-pro-preview`와 일치하는지 세션 기록을 전수 확인한다.
