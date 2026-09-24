# EXP-030: pi coding agent × Opus 5.5·gpt-6-sol 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-09-24 (실행 전).

## 가설

- 가설 코드·문장: [M-23](../../hypotheses/catalog.md) — pi coding agent(`pi -p`, v0.87.1)로 `anthropic/claude-opus-5-5`(Anthropic API 키 직결)와 `openai-codex/gpt-6-sol`(ChatGPT OAuth)을 돌리면(thinking은 pi 기본값), 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성**. EXP-029에서 오픈웨이트 계열 모델로 확인한 pi 하네스가 각 제조사 네이티브 에이전트(Claude Code·Codex)의 기준 모델에서도 같은 절차로 쓸 수 있는지 확인한다. 사후에 효율 우위 실험으로 해석을 바꾸지 않는다.
- 실무 선택 질문: Opus 5.5·gpt-6-sol을 제조사 에이전트 대신 경량 에이전트인 pi로 쓸 때 이 과제 유형(신규 백엔드 구현)을 무개입으로 끝낼 수 있는가.
- 실험 단계: 탐색 (조건별 n=3).
- 주 지표와 사전 판정 기준: 조건별 완주 수. 완주는 드라이버 게이트 `pass`(에이전트의 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 경우다. 조건별로 3/3이면 **검증**, 1–2/3이면 **부분 검증**, 0/3이면 **반증**이다. 제공자·하네스 장애로 run이 판정 불능이면 해당 run을 **보류**로 두고 전체 판정에 그 사실을 적는다.
- 보조 지표: 완주 iteration 수, 세션 시간(driver 로그의 start/end), 토큰 대리지표(`input + output + cacheWrite`), pi가 세션에 기록한 단가 환산 비용(청구액 아님).

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `~/ralph-exp030/app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` (md5 `2c28ea6b7f16125d9b3105f5ee00b126`), setup.sh가 `checksums.md5`로 검증한다. PROMPT 본문을 pi의 prompt 인자로 그대로 넘긴다.
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl` 8.0.1 절대 경로.
- 완료 기준: 위 주 지표 정의와 같다. 에이전트의 완료 선언만으로는 완주로 보지 않는다.
- 평가 과제 분리: 미적용. 기존 M축 실험과 같은 공개 Hurl 세트로 완주 여부만 본다.

## 조건 (Conditions)

| 조건 | 모델·추론 설정 | 실행 도구·버전 | 작업 전략 | 제공자·연결 계층 | 원자료 |
|------|--------------|--------------|----------|----------------|--------|
| opus | `anthropic/claude-opus-5-5`, thinking pi 기본값(Phase 0에서 관측값 기록) | pi 0.87.1 | 랄프 루프 | Anthropic API(Messages) 직결, `ANTHROPIC_API_KEY`(`~/.zsh_secrets`에서 env로 전달), pi 내장 provider | `runs/` |
| sol | `openai-codex/gpt-6-sol`, thinking pi 기본값(Phase 0에서 관측값 기록) | pi 0.87.1 | 랄프 루프 | ChatGPT 구독 OAuth(Codex 백엔드), `~/.pi/agent/auth.json` 최신본을 격리 디렉터리에 복사, pi 내장 provider | `runs/` |

- sol 조건은 ChatGPT 구독 OAuth로 호출하므로 run별 실제 지출이 발생하지 않는다. 대시보드의 run당 환산 비용은 API 단가로 계산한 추정치다.
- opus 조건은 Anthropic API 키로 과금된다(실제 청구액은 미측정, 단가 환산만 한다).

## 환경·비교 범위

- 조건 확정(2026-09-24 사용자): 하네스는 pi, 두 조건, EN만, 조건당 n=3.
- OS·런타임: macOS 26.6.2, Node v24.14.0, hurl 8.0.1. 리포 커밋 `6e33898` 기준(스킬 setup.sh의 pi auth.json 복사 단계 추가 전).
- 격리: `PI_CODING_AGENT_DIR=~/ralph-exp030/pi-agent`(전용 설정·인증; `auth.json`만 복사하고 사용자 `settings.json`은 복사하지 않음), `--session-dir sessions-<run>`, `PI_OFFLINE=1`·`PI_SKIP_VERSION_CHECK=1`.
- 지침 노출 차단: EXP-029와 같이 `-nc -ns -ne -np -na`로 상위 디렉터리 `AGENTS.md`/`CLAUDE.md`, 스킬·확장·프롬프트 템플릿·프로젝트 로컬 설정을 끈다.
- 도구 권한: pi 기본 도구(read·bash·edit·write)를 승인 없이 실행한다. 샌드박스는 없다.
- 실제 응답 모델: 세션 jsonl assistant 메시지의 `provider`/`model` 필드가 조건과 일치하는지 전수 확인한다.
- 캐시: 제공자 서버측 캐시는 통제할 수 없다. 기록된 `cacheRead`/`cacheWrite`를 그대로 보고한다.
- 채점 환경: 기동 전 3000번대 포트 외부 LISTEN을 확인한다(EXP-029 D-1·D-3). 3003의 DeepSRT는 EXP-029 재채점 때부터 존재했고 앱 기본 포트(3000)와 겹치지 않아 허용한다. 그 외 점유가 있으면 기동하지 않는다.
- 기준선: 동시기 재측정 없음. 네이티브 기준선 EXP-026(Claude Code × Opus 5.5, EN n=3, 2026-09-23)·EXP-027(Codex × gpt-6-sol, EN n=3, 2026-09-24)과 비교한다. 에이전트(pi↔Claude Code/Codex)와 API 경로(요청 형식·시스템 프롬프트·도구 정의·thinking 설정 방식)가 함께 달라지므로 차이는 **조합 전체의 차이**로만 서술하고 pi의 효과로 단정하지 않는다.

## 반복·실행 순서·예산

- 반복: 조건별 EN n=3, 총 6 run. 완주 가능성 탐색의 기존 M축 표준 규모다.
- 실행 순서: 반복 번호 단위로 조건을 교차(opus-1 → sol-1 → opus-2 …), 순차 실행, 다른 실험과 동시 실행 금지.
- run 초기화: run마다 새 `app-<run>` 디렉터리·새 pi 세션(iteration마다 `pi -p` 새 프로세스).
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초). 비용 상한은 두지 않되 pi 세션 기록의 환산 비용을 run마다 확인한다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우(EXP-027 D-1 유형)에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 제공자 인증·가용성 장애로 iteration이 연속 3회 즉시 실패(exit≠0, 수 초 내 종료)하면 해당 run을 보류로 기록하고 원인 확인 후 새 run 번호로 재실행한다. 이전 기록은 덮어쓰지 않는다.

## Ralph 정책

- iteration 세션: 매 iteration 새 pi 프로세스·새 세션. 코드와 git 이력만 이어진다.
- 공개 피드백: 없음. 고정 PROMPT만 반복 전달한다.
- 최종 채점: driver가 iteration마다 measure.sh로 채점하고, `.ralph-done` 선언이 13/13 미만이면 선언 파일을 지우고 계속한다.

## 계측·분석 계획

- usage 원자료: pi 세션 jsonl(`sessions-<run>/*.jsonl`).
- 집계기: `usage_pi.py`(EXP-029 작성, responseId 중복 제거·충돌 시 중단). Phase 0에서 anthropic·openai-codex 응답의 usage 필드(input·output·cacheRead·cacheWrite·totalTokens)가 기록되는지와 `totalTokens` 검산을 확인한다.
- 토큰 정의: pi `input`은 비캐시 입력, `cacheRead`/`cacheWrite`는 별도, reasoning은 `output`에 포함. 대리지표는 `input + output + cacheWrite`이며 청구 비용이 아니다.
- 비용: pi 기록 `cost`는 pi 내장 단가표 환산값이다. 대시보드 반영은 [analysis/cost/README.md](../../analysis/cost/README.md) 절차로 별도 환산하며, sol은 구독 OAuth라 실제 지출이 아님을 명시한다.
- 시간: driver 로그의 run start부터 마지막 iteration end까지.

## Phase 0 기록

- [x] 제공자 스모크 및 usage 의미·기록 확인 (2026-09-24: 2조건 smoke PASS, bash 도구 왕복 `TOOL-42`, 지침 노출 `NO`)
- [x] 프롬프트·초기 상태·설정·채점 정본 확인
- [x] 채점기 경로·버전·파일 수 확인
- [x] 3000번대 포트 외부 LISTEN 확인
- [x] 원자료·산출물·이탈 기록 경로 확정
- 증거: `runs/phase0.md`
