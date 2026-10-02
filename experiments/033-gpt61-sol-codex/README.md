# EXP-033: Codex × gpt-6.1-sol 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-03 (실행 전).

## 가설

- 가설 코드·문장: [M-26](../../hypotheses/catalog.md) — Codex CLI(`codex exec`, 0.160.0) 하네스에서 `gpt-6.1-sol`(effort medium)은 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3). 효율 우위 실험으로 사후 해석을 바꾸지 않는다.
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 토큰 대리지표(`usage_codex.py`, input은 캐시 포함·reasoning은 output 포함).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| sol61 | `gpt-6.1-sol`, `model_reasoning_effort=medium` (EXP-027과 동일) | Codex CLI 0.160.0 | ChatGPT 구독 OAuth, 격리 `CODEX_HOME`(auth.json 최신본 + 빈 config.toml) | `runs/` |

- Codex 0.160.0은 이 모델의 메타데이터가 없어 "fallback metadata" 경고를 낸다. 컨텍스트 창 등 클라이언트 쪽 값이 대체값으로 동작하며, 이로 인한 차이는 이 조건의 일부로 기록한다.
- 격리: 사용자 `~/.codex`의 AGENTS.md·스킬·MCP·플러그인 훅은 노출되지 않는다(Phase 0에서 확인).

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/), 신규 구현 1개 과제.
- 초기 상태: run마다 빈 디렉터리 `app-<run>`에 `git init`과 PROMPT.md만 둔다.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/PROMPT-en.md` (md5 `2c28ea6b7f16125d9b3105f5ee00b126`), setup.sh가 `checksums.md5`로 검증한다.
- 채점 정본: 같은 스킬 `assets/harness-hurl/` 13파일, 154 요청. 채점기는 `/opt/homebrew/bin/hurl` 절대 경로.
- 완료 기준: 드라이버 게이트 `pass`(에이전트 `.ralph-done` 선언 + 채점기 13/13)와 독립 재검증 2회 `13,154`가 모두 성립한 run만 완주로 본다.

## 반복·실행 순서·예산

- 반복: EN n=3 (스킬 기본값 — 2026-10-03 사용자 지시로 특별 지시가 없으면 EN만). 순차 실행, 다른 실험과 동시 실행 금지. EXP-033(Codex) 3 run 종료 후 EXP-034(pi) 3 run을 이어서 실행한다.
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초). ChatGPT 구독 OAuth라 run별 실제 지출은 없다.
- 사람 개입: 없음. 채점기 정리 누락으로 driver가 멈추는 경우에만 잔존 서버를 종료하고 `runs/deviations.md`에 기록한다.
- 실패·제외 규칙: 인증·가용성 장애로 iteration이 연속 3회 즉시 실패하면 해당 run을 보류로 기록하고 새 run 번호로 재실행한다.
- 판정: 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 제공자·하네스 장애 run은 **보류**.

## 환경 주의 (실행 전 확인, 2026-10-03)

- 모델 ID 확인: `gpt-6.1-sol`은 `~/.codex/models_cache.json`(07:47 갱신)과 pi 0.87.1 내장 목록에 없다. 같은 ChatGPT 계정으로 `codex exec -m gpt-6.1-sol`은 정상 응답했고 세션 기록 model 필드가 `gpt-6.1-sol`이었으며, 대조로 넣은 존재하지 않는 ID `gpt-6.9-bogus`는 400 `model is not supported`로 거부되었다. 따라서 서버가 이 ID를 인식한다고 판단한다. 단, 클라이언트 쪽 모델 메타데이터(컨텍스트 창·추론 기본값)는 공식 값이 아니라 대체값이다(아래 조건 참조).
- 포트: 실행 전 VS Code(Code Helper)가 3000·3001을 LISTEN 중이고 DeepSRT가 3003을 LISTEN 중이다. driver·measure.sh가 run마다 빈 포트를 `PORT`로 주입하므로(EXP-031 도입) `PORT`를 따르는 앱은 영향받지 않는다. 앱이 `PORT`를 무시하고 3000에 고정 바인딩하면 거짓 음성이 생길 수 있으므로 기각된 iteration의 서버 로그를 확인해 이탈로 기록한다.
- 기준선: 동시기 재측정 없음. 같은 하네스의 gpt-6-sol 결과(EXP-027 Codex, EXP-030 pi, 각 EN n=3)와 비교하되 시점·CLI 버전 교락이 있으므로 차이는 조합 전체의 차이로만 서술한다.

## 계측

- usage는 토큰 대리지표이며 청구 비용이 아니다. 시간은 driver 로그의 run start부터 마지막 iteration end까지.
- 응답 모델 필드가 조건과 일치하는지 세션 기록을 전수 확인한다.
