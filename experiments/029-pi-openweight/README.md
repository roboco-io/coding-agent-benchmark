# EXP-029: pi coding agent × 오픈웨이트 계열 모델(kimi·qwen·deepseek) 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-09-24 (실행 전).

## 가설

- 가설 코드·문장: [M-22](../../hypotheses/catalog.md) — pi coding agent(`pi -p`, v0.87.1)를 각 제공자의 OpenAI 호환 엔드포인트에 직결해 `kimi-k3`·`qwen3.8-max`·`deepseek-flash`(thinking은 pi 기본값)를 돌리면, 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성**. 이 실험은 새 하네스인 pi를 벤치마크 대상에 넣을 수 있는지 판단하기 위한 후보 선별 단계다. 사후에 효율 우위 실험으로 해석을 바꾸지 않는다.
- 실무 선택 질문: Claude Code 대신 경량 에이전트인 pi로 오픈웨이트 계열 모델을 쓸 때, 이 과제 유형(신규 백엔드 구현)을 무개입으로 끝낼 수 있는가.
- 실험 단계: 탐색 (조건별 n=3).
- 주 지표와 사전 판정 기준: 조건별 완주 수. 완주는 드라이버 게이트 `pass`(에이전트의 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 경우다. 조건별로 3/3이면 **검증**, 1–2/3이면 **부분 검증**, 0/3이면 **기각**이다. 제공자·하네스 장애로 run이 판정 불능이면 해당 run을 **보류**로 두고 전체 판정에 그 사실을 적는다.
- 보조 지표: 완주 iteration 수, 세션 시간(driver 로그의 start/end), 토큰 대리지표(`input + output + cacheWrite`), pi가 세션에 기록한 단가 환산 비용(청구액 아님).

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `~/ralph-exp029/app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` (md5 `2c28ea6b7f16125d9b3105f5ee00b126`), setup.sh가 `checksums.md5`로 검증한다. PROMPT 본문을 pi의 prompt 인자로 그대로 넘긴다(`@file` 첨부 방식은 태그 래핑 가능성 때문에 쓰지 않음).
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl` 8.0.1 절대 경로(EXP-020 npm shim 오검 재발 방지).
- 완료 기준: 위 주 지표 정의와 같다. 에이전트의 완료 선언만으로는 완주로 보지 않는다.
- 평가 과제 분리: 미적용. 기존 M축 실험과 같은 공개 Hurl 세트로 완주 여부만 본다.

## 조건 (Conditions)

| 조건 | 모델·추론 설정 | 실행 도구·버전 | 작업 전략 | 제공자·연결 계층 | 원자료 |
|------|--------------|--------------|----------|----------------|--------|
| kimi | `moonshotai/kimi-k3`, thinking pi 기본값(스모크 관측 `high`) | pi 0.87.1 | 랄프 루프 | Moonshot `https://api.moonshot.ai/v1` OpenAI 호환, pi 내장 provider | `runs/` |
| qwen | `dashscope/qwen3.8-max`, thinking pi 기본값(스모크 관측 `medium`, `enable_thinking` 방식) | pi 0.87.1 | 랄프 루프 | DashScope intl `compatible-mode/v1` OpenAI 호환, `models.json` 사용자 정의 provider | `runs/` |
| flash | `deepseek/deepseek-flash`, thinking pi 기본값(스모크 관측 `high`) | pi 0.87.1 | 랄프 루프 | DeepSeek `https://api.deepseek.com` OpenAI 호환, pi 내장 provider | `runs/` |

- `qwen3.8-max`는 API 전용 모델일 수 있어 엄밀한 오픈웨이트 모델이 아닐 가능성이 있다(미확인). 사용자가 대상으로 지정했으므로 포함한다.
- DashScope provider 설정(`assets/pi-models.json`)은 pi에 내장된 `qwen-token-plan` provider의 `qwen3.8-max` 항목과 같은 compat 설정(`thinkingFormat: qwen` 등)을 쓴다.

## 환경·비교 범위

- 연결 방식 결정(2026-09-24 사용자 선택): pi가 기본으로 쓰는 **OpenAI 호환 엔드포인트**를 쓴다. pi가 제공자 API를 직접 호출하므로 ccr 같은 변환 계층은 없다. 그러나 EXP-013/014/025의 Claude Code 직결은 같은 제공자의 **Anthropic 호환** 엔드포인트를 썼으므로, 그 결과와 비교하면 하네스(pi↔Claude Code)와 API 형식이 함께 달라진다. 차이는 조합 전체의 차이로만 서술한다.
- OS·런타임: macOS 26.6.2, Node v24.14.0, hurl 8.0.1. 리포 커밋 `03c7c34` 기준.
- 격리: `PI_CODING_AGENT_DIR=~/ralph-exp029/pi-agent`(전용 설정·인증), `--session-dir sessions-<run>`(run별 세션 분리), `PI_OFFLINE=1`·`PI_SKIP_VERSION_CHECK=1`(부가 네트워크 호출 차단).
- 지침 노출 차단: pi는 작업 디렉터리의 모든 상위 디렉터리에서 `AGENTS.md`/`CLAUDE.md`를 읽는다. 홈에 `~/AGENTS.md`가 있으므로 `-nc`로 컨텍스트 파일을 끄고, `-ns -ne -np -na`로 스킬·확장·프롬프트 템플릿·프로젝트 로컬 설정도 끈다. 실제 노출 여부는 Phase 0에서 세션 jsonl의 시스템 프롬프트로 확인한다.
- 도구 권한: pi는 기본 도구(read·bash·edit·write)를 승인 없이 실행한다. 샌드박스는 없다.
- 실제 응답 모델: 세션 jsonl assistant 메시지의 `provider`/`model` 필드가 조건과 일치하는지 전수 확인한다.
- 캐시: 제공자 서버측 캐시는 통제할 수 없다. 스모크에서 Moonshot은 `cacheWrite`, DashScope·DeepSeek는 `cacheRead`가 기록됐다.
- 기준선: 동시기 재측정 없음. EXP-013(qwen3.8-max)·EXP-014(kimi-k3)·EXP-025(deepseek-flash)의 Claude Code 직결 결과는 시점·CLI·API 형식이 다른 참고치로만 인용한다.

## 반복·실행 순서·예산

- 반복: 조건별 EN n=3, 총 9 run. 완주 가능성 탐색의 기존 M축 표준 규모다.
- 실행 순서: 반복 번호 단위로 조건을 교차(kimi-1 → qwen-1 → flash-1 → kimi-2 …), 순차 실행, 다른 실험과 동시 실행 금지.
- run 초기화: run마다 새 `app-<run>` 디렉터리·새 pi 세션(iteration마다 `pi -p` 새 프로세스).
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초). 비용 상한은 두지 않되 pi 세션 기록의 환산 비용을 run마다 확인한다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우(EXP-027 D-1 유형)에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 제공자 인증·가용성 장애로 iteration이 연속 3회 즉시 실패(exit≠0, 수 초 내 종료)하면 해당 run을 보류로 기록하고 원인 확인 후 새 run 번호로 재실행한다. 이전 기록은 덮어쓰지 않는다.

## Ralph 정책

- iteration 세션: 매 iteration 새 pi 프로세스·새 세션. 코드와 git 이력만 이어진다.
- 공개 피드백: 없음. 고정 PROMPT만 반복 전달한다.
- 최종 채점: driver가 iteration마다 measure.sh로 채점하고, `.ralph-done` 선언이 13/13 미만이면 선언 파일을 지우고 계속한다.

## 계측·분석 계획

- usage 원자료: pi 세션 jsonl(`sessions-<run>/*.jsonl`). assistant `message`의 `usage`와 `type:"usage"` 엔트리(캐시 워밍·압축 등)를 포함한다.
- 집계기: `usage_pi.py`(이번 실험에서 신규 작성). 중복 제거 키는 assistant 메시지의 `responseId`, 없으면 파일+entry id. 같은 키에 다른 usage가 나오면 오류로 중단한다. 스모크 세션 복제 파일로 중복 제거를 확인했다.
- 토큰 정의: pi `input`은 비캐시 입력, `cacheRead`/`cacheWrite`는 별도, `reasoning`은 `output`에 포함(`totalTokens = input+output+cacheRead+cacheWrite` 검산). 대리지표는 `input + output + cacheWrite`이며 청구 비용이 아니다.
- 비용: pi가 기록한 `cost`는 pi 내장 단가표 기반 환산값이다(DashScope 사용자 정의 provider는 단가 0으로 등록). 청구액은 미측정이며, 대시보드 반영 시 [analysis/cost/README.md](../../analysis/cost/README.md) 절차로 별도 환산한다.
- 시간: driver 로그의 run start부터 마지막 iteration end까지.

## Phase 0 기록

- [x] 제공자 스모크 및 usage 의미·기록 확인 (사전 스모크 2026-09-24: 3조건 모두 bash 도구 왕복 `SMOKE-OK`/`TOOL-42`)
- [x] 프롬프트·초기 상태·설정·채점 정본 확인
- [x] 채점기 경로·버전·파일 수 확인
- [x] 원자료·산출물·이탈 기록 경로 확정
- 증거: `runs/phase0.md`
