---
name: ralph-model-benchmark
description: Use when a new LLM model, model variant, or coding agent/harness is released and needs to be benchmarked in this repo's Ralph loop RealWorld backend task (완주 검증, 새 모델 벤치마크, EXP-NNN 추가), or when re-running an existing condition for comparison.
---

# 랄프 루프 모델 벤치마크

## 개요

새 모델·에이전트를 **기존 실험과 같은 과제·프롬프트·채점기·루프 규칙**으로 돌려 비교 가능한 결과를 만든다. 정본(EN/KO PROMPT, Hurl 13파일)과 공통 스크립트는 이 스킬의 `assets/`·`scripts/`에 있으며, 실행 시 `$HOME/ralph-expNNN`으로 복사·해시 검증되어 고정된다. 실험 품질 규칙은 `docs/experiment-quality-rules.md`가 정본이며 이 스킬은 그 절차를 실행 가능한 형태로 묶은 것이다.

## 하네스 선택

| 모델 제공 형태 | HARNESS | 근거 실험 |
|---|---|---|
| Anthropic 모델 | `claude-native` | EXP-023/026 |
| 제공자가 Anthropic 호환 `/v1/messages` 제공 | `claude-direct` | EXP-013/014/020/025 |
| OpenAI 계열(Responses API만 제공) | `codex` | EXP-011/021 |
| 위 어느 것도 아님 | 대상 제외 또는 설계에 변환 계층 사유·계측 한계 사전 등록 | CLAUDE.md 하네스 규칙 |

ccr 등 변환 계층은 기본 금지다 (tool call 인자 훼손·usage 유실 사례).

## 절차

1. **사전 조사**: 모델 ID를 추측하지 않는다. 제공자 모델 목록(예: `GET /v1/models`, `~/.codex/models_cache.json`)에서 정확한 ID·추론 설정·컨텍스트를 확인한다. 사용자가 말한 이름이 목록에 없으면 멈추고 `AskUserQuestion`으로 확인한다.
2. **설계 문서**: 다음 번호로 `experiments/NNN-<slug>/README.md`를 `templates/experiment-readme.md`로 작성한다. 질문 유형(완주 가능성 등), 조건, 반복 수, 상한, 판정 기준(예: 검증 3/3 / 부분 검증 1–2/3 / run 단위 보류)을 **실행 전에** 고정하고 `hypotheses/catalog.md`에 가설을 등록한다.
3. **하네스 생성**: `scripts/bench.env.example`을 복사해 채운 뒤 `bash .claude/skills/ralph-model-benchmark/scripts/setup.sh <bench.env>`.
4. **Phase 0**: `bash ~/ralph-expNNN/smoke.sh` — 조건 전부 PASS여야 기동. 결과와 CLI·hurl 버전, 노출된 지침·스킬·MCP(`claude-native`는 비격리)를 `runs/phase0.md`에 기록.
5. **기동**: `nohup caffeinate -is bash ~/ralph-expNNN/run-all.sh >/dev/null 2>&1 &`. 순차 실행이며 다른 실험과 동시 실행 금지. 진행은 `orchestrator.log`·`metrics-*.csv`로 확인하고 개입하지 않는다.
6. **독립 재검증**: 완주 run마다 `bash ~/ralph-expNNN/measure.sh ~/ralph-expNNN/app-<run>`을 2회 실행해 `13,154`를 확인하고 `recheck.csv`로 남긴다.
7. **usage 집계**: `codex` → `python3 ~/ralph-expNNN/usage_codex.py ~/ralph-expNNN <run>...`; Claude 계열 → `python3 scripts/aggregate_tokens.py --json <dir>` (message.id dedup; `<dir>`는 claude-direct면 `sessions-<run>/*/`, claude-native면 `sessions-<run>/`). 결과는 **토큰 대리지표**이며 청구 비용이 아니다.
8. **보관**: `bench.env`, 스크립트, `metrics-*.csv`, usage CSV, `orchestrator.log`, `phase0.md`, `recheck.csv`, 로그(`gzip`)를 `experiments/NNN-*/runs/`로 복사한다.
9. **보고·동기화**: `templates/report.md`로 `report.md` 작성 후 CLAUDE.md "실험 종료 시 필수 절차" 1–5(i18n·README 재생성·catalog·ROADMAP·대시보드)를 그대로 수행한다.

## metrics CSV

`iter,종료시각,exit,성공 hurl 파일 수,실행 요청 수,완료 선언,게이트` — 게이트 `pass`만 완주. 에이전트의 `.ralph-done` 선언은 채점기가 13/13이 아니면 `rejected`로 삭제된다. `timeout,<시각>` 행은 wall-clock 상한 도달.

## 흔한 실수

| 실수 | 결과 | 대응 |
|---|---|---|
| PATH의 `hurl` 사용 | npm shim이 실 Hurl을 가려 0건 통과 오검(EXP-020) | measure.sh의 절대 경로 유지 |
| 오래된 `auth.json` 사본 재사용 | Codex 401 (EXP-021) | setup.sh가 매번 `~/.codex/auth.json` 최신본 복사 |
| 공유 설정 디렉터리에서 실행 | 이전 세션·메모리 교란, usage 범위 혼입 (EXP-007) | `codex-home`/`claude-config` 격리, run별 `sessions-<run>` 분리 |
| 프롬프트 수정·재작성 | 기존 실험과 비교 불가 | `assets/` 정본만 사용, 해시 불일치 시 setup 중단 |
| 미인식 모델의 200k 창 제한 | 컨텍스트 조기 차단 | `claude-direct`는 `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1` 포함 |
| iteration 종료 후 metrics 행이 수 분째 안 생김 | 채점기 정리 누락으로 driver 대기 (EXP-027 D-1: 상대 경로 watcher 트리) | `hurl-last.log`로 채점 완료 확인 → 잔존 서버 트리 종료 → `runs/deviations.md`에 기록. 세션 시간은 로그 start/end로 산정 |
| "3/3 완주 = 재현성 확정" 서술 | 관측 범위 초과 | 표본 수와 조건을 함께 적는다 |
| 과거 실험과 속도·토큰 우열 단정 | 시점·CLI 버전 교락 | 차이를 조합 전체의 차이로 서술 |
