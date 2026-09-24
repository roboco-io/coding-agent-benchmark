# EXP-027: Codex CLI × gpt-6-sol·gpt-6-luna 랄프 루프 완주 검증 (각 n=3)

> 이 실험은 `ralph-model-benchmark` 스킬(`.claude/skills/ralph-model-benchmark/`)로 설계·실행한 첫 실험이다. 하네스 스크립트는 EXP-021 driver·measure v4를 공통형으로 옮긴 것이다.

## 배경

OpenAI의 GPT-6 계열이 3개 모델로 나뉘었다. 2026-09-24 OpenAI `/v1/models`와 Codex 모델 목록(`models_cache.json`, fetched 2026-09-23)에서 확인한 GPT-6 모델은 다음 셋뿐이다.

| 모델 ID | Codex 설명(원문) | 기본 추론 설정 |
|---|---|---|
| `gpt-6-astra` | Frontier intelligence for the most demanding work. | medium |
| `gpt-6-sol` | Workhorse model for coding and everyday work. | medium |
| `gpt-6-luna` | Fast and affordable model for easier tasks. | medium |

사용자가 요청한 `gpt-6-earth`는 목록에 없고, Codex 스모크에서 400(`model is not supported`)으로 거부되었다(`gpt-6-terra`도 동일). astra는 EXP-021에서 같은 하네스로 3/3 완주했으므로 사용자 확인(2026-09-24)에 따라 이번 실험은 **sol·luna만** 새로 측정하고 astra는 EXP-021 결과를 과거 기준선으로 인용한다.

## 가설

- 가설 코드·문장: [M-20](../../hypotheses/catalog.md) — Codex CLI(`codex exec`) 하네스에서 gpt-6-sol·gpt-6-luna(effort medium)는 각각 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iter·4h 안에 완주할 수 있다 (각 n=3).
- 질문 유형: **완주 가능성**. 신규 모델의 후보 선별용 완주 스모크이며, 효율 우위 실험으로 사후 전환하지 않는다.
- 실험 단계: 탐색 (조건당 3 run).
- 사전 판정 기준 (모델별): 검증 3/3 / 부분 검증 1–2/3(run별 사실 보고) / 반증 0/3. 모델 외적 장애(제공자 5xx 지속·인증 만료 등)로 끝난 run은 run 단위 보류로 기록하고 재실행은 새 run 번호로 한다.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, rollout usage(토큰 대리지표). 비교는 기록만 하고 우열 판정은 하지 않는다.

## 과제·완료 기준

- 과제: [realworld-backend](../../tasks/realworld-backend/) 신규 구현 1개 (빈 git 리포에서 시작).
- 프롬프트: EN 정본 `PROMPT-en.md` md5 `2c28ea6b7f16125d9b3105f5ee00b126` (EXP-011/021과 동일, 스킬 `assets/checksums.md5`로 검증).
- 채점: 공식 Hurl 13파일(154 요청), `/opt/homebrew/bin/hurl` 8.0.1 절대 경로, measure v4(리포 소속 포트 자동 탐지). 채점 파일은 에이전트 작업 디렉터리 밖(`~/ralph-exp027/harness-hurl`)에 둔다.
- 완료 기준: 에이전트의 `.ralph-done` 선언 + 게이트 13/13. 완주 run은 종료 후 measure 2회 독립 재검증.
- 평가 과제 분리: 미적용 (완주 스모크, 기존 실험과 동일 과제 유지가 목적).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구·버전 | 작업 전략 | 연결 | 원자료 |
|---|---|---|---|---|---|
| sol | `gpt-6-sol`, effort medium | Codex CLI 0.155.1 | 랄프 루프 (iteration마다 새 `codex exec` 세션) | ChatGPT 플랜 OAuth, Responses API | `runs/` (`*-sol-en-*`) |
| luna | `gpt-6-luna`, effort medium | Codex CLI 0.155.1 | 동일 | 동일 | `runs/` (`*-luna-en-*`) |

## 환경·비교 범위

- 바꾸는 요인: 모델 ID 1개. 고정: 프롬프트·채점·driver·effort·상한.
- 환경: macOS Darwin 25.6.0, Codex CLI 0.155.1, hurl 8.0.1.
- 격리: 전용 `CODEX_HOME=~/ralph-exp027/codex-home` (auth.json 최신본 + 빈 config.toml). 사용자 `~/.codex`의 AGENTS.md·스킬·MCP는 노출되지 않는다.
- 인증: ChatGPT 플랜 OAuth — API 종량 과금이 아니므로 달러 환산은 추정치로만 표기한다.
- 기준선: astra(EXP-021, 2026-09-10, Codex 0.153.4)는 시점·CLI 버전이 다르다. 비교는 조합 전체의 관측 차이로만 서술한다.

## 반복·실행 순서·예산

- 순서: sol-en-1 → luna-en-1 → sol-en-2 → luna-en-2 → sol-en-3 → luna-en-3 (반복 번호 단위 교차), 순차 실행.
- run 초기화: run마다 새 `app-<run>` 리포, run 종료 시 Codex 세션을 `sessions-<run>`으로 이동.
- 상한: 30 iteration, run당 wall-clock 4h. 사람 개입 금지.

## 계측

- usage: Codex rollout의 세션별 마지막 `total_token_usage`(세션 누계)를 run 내 합산 — `usage_codex.py` (EXP-021 astra 3 run 기록값과 일치하도록 회귀 확인). input은 캐시 포함, reasoning은 output에 포함.
- 시간: 첫 iteration 시작부터 게이트 통과 iteration 종료까지.

## Phase 0

- [x] 모델 ID 확인 (`/v1/models`, Codex models_cache)
- [x] 스모크 (`runs/phase0.md`)
- [x] 프롬프트·채점 정본 해시 확인 (setup.sh)
