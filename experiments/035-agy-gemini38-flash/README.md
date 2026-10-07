# EXP-035: Antigravity CLI × gemini-3.8-flash 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-07 (실행 전).

## 가설

- 가설 코드·문장: [M-28](../../hypotheses/catalog.md) — Antigravity CLI(`agy -p`)로 `gemini-3.8-flash`(effort high, Gemini API 키 인증)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3).
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 토큰 대리지표(`usage_agy.py`, 클라이언트 보고값 `input_tokens + output_tokens`).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| flash38 | `gemini-3.8-flash`, `--effort high` (CLI 내부 ID `gemini-3.8-flash-high`) | Antigravity CLI `agy` (Phase 0에서 버전 기록) | Gemini API 직결, `GEMINI_API_KEY` (`~/.zsh_secrets`) | `runs/` |

- 하네스는 이 실험에서 `ralph-model-benchmark` 스킬에 `HARNESS=agy`로 새로 추가했다(`scripts/agy_env.sh`, `usage_agy.py`).
- **인증 강제와 격리**: 실 HOME에서 `agy`를 실행하면 keyring에 저장된 Google 계정 OAuth가 먼저 선택된다(2026-10-07 로그 `authMethod=consumer` 확인). 그래서 run마다 격리 HOME(`agy-home/`)을 두고 `settings.json`에 `modelProvider: "gemini"`를 넣어 API 키 인증을 강제한다(같은 날 스모크 로그 `authMethod=gemini_api_key` 확인). 격리 HOME에는 `.tool-versions`와 git 사용자 이름·이메일만 넣는다. 도구 체인은 `ASDF_DATA_DIR`로 실 asdf를 가리킨다.
- **run 간 교란 차단**: agy는 대화 기록·요약 DB·brain(지식 항목)을 HOME 아래에 저장한다. run이 끝날 때마다 이 디렉터리를 `sessions-<run>/`로 옮기고 격리 HOME을 초기화한다.
- **지침 노출**: 격리 HOME에는 `~/AGENTS.md`, `~/.gemini/GEMINI.md`, 사용자 MCP 설정이 없다. agy 제품 내장 스킬(`builtin/skills`)과 시스템 프롬프트는 제품의 일부이므로 끄지 않고 Phase 0에서 목록을 기록한다.
- **키 고정**: 셸 환경에 `GOOGLE_API_KEY`도 있어, agy 호출 시 `env -u GOOGLE_API_KEY`로 제거하고 `GEMINI_API_KEY`만 넘긴다.
- **자동 업데이트 차단**: 사전 조사 중 agy가 1.2.16에서 1.3.1로 자동 업데이트되었다. run 중 버전이 바뀌지 않도록 `AGY_CLI_DISABLE_AUTO_UPDATE=1`을 설정한다.

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` (md5 `2c28ea6b7f16125d9b3105f5ee00b126`), setup.sh가 `checksums.md5`로 검증한다.
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl` 절대 경로.
- 완료 기준: 드라이버 게이트 `pass`(에이전트 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 run만 완주로 본다.

## 반복·실행 순서·예산

- 반복: EN n=3 (스킬 기본값). 순차 실행, 다른 실험과 동시 실행 금지. EXP-035(agy) 3 run 종료 후 EXP-036(pi) 3 run을 이어서 실행한다.
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초). Gemini API 키는 종량 과금이므로 실제 지출이 생긴다. 지출액은 이 실험에서 계측하지 않는다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 인증·쿼터·가용성 장애로 iteration이 연속 3회 즉시 실패하면 해당 run을 보류로 기록하고 새 run 번호로 재실행한다.
- 판정: 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 제공자·하네스 장애 run은 **보류**.

## 환경 주의 (실행 전 확인, 2026-10-07)

- 모델 ID 확인: Gemini API `GET /v1beta/models`(같은 키)에 `gemini-3.8-flash`가 있다. 이 목록에서 버전 번호가 가장 높은 텍스트 생성 모델이다. Pro 계열의 최신은 `gemini-3.1-pro-preview`다. `agy models` 목록에도 `gemini-3.8-flash-{low,medium,high}`가 있다.
- 기준선: 같은 하네스의 이전 실험은 없다. pi 하네스 결과(EXP-036)와 같은 모델로 비교하지만, 하네스·시스템 프롬프트·도구 구성이 다르므로 차이는 조합 전체의 차이로만 서술한다.

## 계측

- usage는 agy가 iteration마다 출력하는 결과 JSON의 `usage` 필드를 합산한 클라이언트 보고값이다. `input_tokens`에 캐시 읽기가 포함되는지는 문서로 확인하지 못했다. 따라서 다른 하네스의 대리지표와 직접 비교하지 않는다. 토큰 대리지표이며 청구 비용이 아니다.
- 시간은 driver 로그의 run start부터 마지막 iteration end까지.
- 응답 모델은 각 run의 agy 로그(`sessions-<run>/.gemini/antigravity-cli/log/`)에서 `resolved to "gemini-3.8-flash-high"`를 전수 확인한다.
