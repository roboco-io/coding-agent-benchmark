# EXP-054: Codex × gpt-6.1-terra 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-27 (실행 전).

## 가설

- 가설 코드·문장: [M-47](../../hypotheses/catalog.md) — Codex CLI(`codex exec`, 0.164.0) 하네스에서 `gpt-6.1-terra`(effort medium, PROMPT v2)는 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3). 효율 우위 실험으로 사후 해석을 바꾸지 않는다.
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 토큰 대리지표(`usage_codex.py`, input은 캐시 포함·reasoning은 output 포함), API 단가 환산 비용(청구 비용 아님).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| terra61 | `gpt-6.1-terra`, `model_reasoning_effort=medium` (EXP-033 sol61과 동일) | Codex CLI 0.164.0 | ChatGPT 구독 OAuth, 격리 `CODEX_HOME`(auth.json 최신본 + 빈 config.toml) | `runs/` |

- 모델 ID 확인: `gpt-6.1-terra`는 `~/.codex/models_cache.json`(2026-10-27 확인)에 `display_name` "GPT-6.1 Terra"로 등록되어 있다. 클라이언트 컨텍스트 창 500,000(최대 872,000, 유효 95%), 기본 추론 low. API 문서 기준 컨텍스트 1,050,000·출력 최대 128,000. 사양·출처는 `runs/model-specs.json`.
- 격리: 사용자 `~/.codex`의 AGENTS.md·스킬·MCP·플러그인 훅은 노출되지 않는다(Phase 0에서 확인).

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` **v2** (md5 `3d11ae8d28546ac730d482d015cfd6d9`). EXP-033(v1)과 비교할 때 PROMPT 차이(PORT 안내 한 줄)를 교란 변수로 적는다.
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl`(hurl 8.0.1) 절대 경로.
- 완료 기준: 드라이버 게이트 `pass`(에이전트 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 run만 완주로 본다.

## 반복·실행 순서·예산

- 반복: EN n=3 (2026-10-03 사용자 지시로 특별 지시가 없으면 EN만). 순차 실행, 다른 실험과 동시 실행 금지.
- 상한: 30 iteration, run당 wall-clock 20분(1,200초), 정체 300초.
- 비용: ChatGPT 구독 OAuth라 run별 실제 지출은 없다. 하네스 단가는 0으로 두고 `RUN_BUDGET_USD=1`·`EXP_BUDGET_USD=3`을 형식상 둔다. API 환산(입력 $1·캐시 $0.05·출력 $5/1M, 272K 초과 요청은 $2·$0.10·$7.50)은 보고 단계에서만 계산한다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 인증·가용성 장애로 iteration이 연속 3회 즉시 실패하면 해당 run을 보류로 기록하고 새 run 번호로 재실행한다.
- 판정: 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 제공자·하네스 장애 run은 **보류**.

## 환경 주의 (실행 전 확인, 2026-10-27)

- 포트: VS Code(Code Helper)가 3000·3001을 LISTEN 중이다. driver·measure.sh가 빈 포트를 `PORT`로 주입하므로 외부 프로세스는 종료하지 않는다.
- 기준선: 동시기 재측정 없음. 같은 하네스의 gpt-6.1-sol(EXP-033, Codex 0.160.0, PROMPT v1, 상한 4시간)과 비교하되 시점·CLI 버전·PROMPT 버전 교락이 있으므로 차이는 조합 전체의 차이로만 서술한다.

## 계측

- usage는 토큰 대리지표이며 청구 비용이 아니다. 시간은 driver 로그의 run start부터 마지막 iteration end까지.
- 응답 모델 필드가 조건과 일치하는지 세션 기록을 전수 확인한다.
