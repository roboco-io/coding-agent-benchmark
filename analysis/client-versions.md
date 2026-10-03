# 실험별 에이전트 클라이언트·버전

- 작성일: 2026-10-03. 방법: 실험 문서(README·report·phase0)에 적힌 버전을 먼저 찾고, 세션 원자료(Claude Code jsonl의 `version` 필드, Codex rollout·로그 머리말의 `cli_version`/`OpenAI Codex vX`)와 대조했다. 어디에도 기록이 없으면 추정하지 않고 "미기록"으로 둔다.
- 근거 파일 중 `~/ralph-expNNN/`, `~/.claude/projects/`로 시작하는 경로는 실험 머신의 로컬 하네스 원자료이며 이 리포에는 포함되어 있지 않다(2026-10-03 확인 시점에 존재). 리포 상대 경로는 이 리포에 있는 파일이다.
- pi 세션 jsonl의 `"version":3`은 세션 스키마 버전이지 pi 버전이 아니다. pi 버전은 문서·phase0 기록에서만 얻었다.
- 각 report.md 헤더의 `- 클라이언트:` 줄은 이 표의 "클라이언트·버전" 열과 같다.

| 실험 | 클라이언트·버전 | 근거 파일 |
|------|----------------|----------|
| EXP-001 | Claude Code 2.1.215 | `experiments/001-ralph-vs-plan-then-execute/runs/*/logs/*.jsonl` 17개 전수 `version` 필드 |
| EXP-002 | Claude Code 2.1.216 | `experiments/002-korean-vs-english/runs/*/logs/*.jsonl` 4개 |
| EXP-003 | Claude Code 2.1.216 | `experiments/003-pte-skills/runs/pte-skills/logs/*.jsonl` 15개 |
| EXP-004 | Claude Code 2.1.216 | `experiments/004-ralph-skills/runs/*/logs/*.jsonl` 2개 |
| EXP-005 | Claude Code 2.1.220 + claude-code-router 1.0.73 | `experiments/005-solar-pro3-backend/runs/solar-1/logs/*.jsonl` 6개(`version`), `runs/solar-1/meta.md`·`report.md`(ccr 1.0.73) |
| EXP-006 | Claude Code 2.1.220. open2-1만 claude-code-router 1.0.73 경유, open2-2는 Upstage 직결 | `experiments/006-solar-open2-backend/runs/open2-*/logs/*.jsonl` 16개, `runs/open2-1/meta.md`·`runs/open2-2/meta.md` |
| EXP-007 | 해당 없음 (EXP-006 세션의 사후 분석, 신규 에이전트 실행 없음) | `experiments/007-solar-open2-autopsy/README.md` |
| EXP-008 | Claude Code 2.1.220 (Upstage 직결, ccr 미사용) | `experiments/008-solar-open2-clean-run/runs/open2-3/logs/*.jsonl` 10개 + `smoke.jsonl` |
| EXP-009 | Claude Code 2.1.220 | `experiments/009-opus5-ralph-en/runs/opus5-*/logs/*.jsonl`, `runs/opus5-1/phase0-smoke.jsonl` |
| EXP-010 | Claude Code 2.1.220 | `experiments/010-opus48-vs-opus5/runs/*/logs/*.jsonl` 7개 |
| EXP-011 | Codex CLI 0.144.0 | `experiments/011-codex-gpt56-sol/runs/phase0.md`, `runs/sol-1/ralph-run-sol-1.log.gz` 머리말, `plan.md` |
| EXP-012 | Claude Code 2.1.220 + claude-code-router 1.0.73 | `experiments/012-ccr-gpt56-sol/runs/phase0.md`·`report.md`(ccr), `~/ralph-exp012/` 세션 jsonl 25개(Claude Code) |
| EXP-013 | Claude Code 2.1.220 | `~/ralph-exp013/claude-config-projects-qwen-1/` 세션 jsonl(`version`), phase0 smoke 포함 |
| EXP-014 | Claude Code 2.1.220 | `~/ralph-exp014/claude-config-projects-kimi-1/` 세션 jsonl |
| EXP-015 | Claude Code 2.1.220 | `~/ralph-exp015/claude-config-projects-solar-1/`·`claude-config-projects-phase0/` 세션 jsonl |
| EXP-016 | Claude Code 2.1.220 (kimi-2·3, qwen-2·3), Codex CLI 0.144.0 (sol-2·3) | `~/ralph-exp013/…qwen-2·3`, `~/ralph-exp014/…kimi-2·3` 세션 jsonl, `experiments/016-n3-replication/runs/sol-*/ralph-run-sol-*.log.gz` 머리말 |
| EXP-017 | Claude Code 2.1.221 | `~/ralph-exp017k/`, `~/ralph-exp017q/` 세션 jsonl 8개 |
| EXP-018 | Claude Code 2.1.222 | `~/ralph-exp015/claude-config/projects/-Users-dohyunjung-ralph-exp015-app-solar-2/` 세션 jsonl 10개(solar-2는 EXP-015 하네스 디렉터리에서 실행) |
| EXP-019 | Codex CLI 0.144.0 (solko 3 run). Claude Code(Opus 4.8·5 한국어 6 run)는 미기록 | `experiments/019-ko-native-codex/runs/ralph-run-solko-*.log.gz` 머리말, `~/ralph-exp019/codex-sessions-solko-*`. Opus run은 비격리 `~/.claude`를 썼으나 세션 jsonl이 남아 있지 않고 문서에도 버전이 없다 |
| EXP-020 | Claude Code 2.1.235 | `~/ralph-exp020/claude-config*/` 세션 jsonl 17개. 리포 문서에는 버전 숫자가 없고 "현 Claude Code 버전"이라고만 적혀 있다 |
| EXP-021 | Codex CLI 0.153.4 | `experiments/021-gpt6-astra-codex/runs/phase0.md`, `runs/ralph-run-astra-*.log.gz` 머리말, `~/ralph-exp021/` rollout `cli_version` |
| EXP-022 | (리포에 실험 폴더·보고서 없음. 참고: 로컬 `~/ralph-exp022/` 세션 jsonl은 Claude Code 2.1.267) | `~/ralph-exp022/` — 실험 기록이 리포에 없어 표 밖 참고 정보로만 둔다 |
| EXP-023 | Claude Code 2.1.273 | `experiments/023-fable51-ralph/runs/phase0.md`, `~/.claude/projects/-Users-dohyunjung-ralph-exp023*` 세션 jsonl 4개 |
| EXP-024 | 본 실험 미실행. Phase 0 시점 설치본 Claude Code 2.1.278, Codex CLI 0.155.1 | `experiments/024-practical-combinations/manifest.json`, `runs/phase0.md` (report.md 없음) |
| EXP-025 | Claude Code 2.1.278 | `~/ralph-exp025/claude-config-projects-*/` 세션 jsonl 14개 전수(phase0 포함). **불일치**: `experiments/025-deepseek-direct/README.md`·`runs/phase0.md`는 2.1.273으로 기록 |
| EXP-026 | Claude Code 2.1.280 | `experiments/026-opus55-ralph/README.md`, `~/.claude/projects/-Users-dohyunjung-ralph-exp026-app-*` 세션 jsonl 6개 |
| EXP-027 | Codex CLI 0.155.1 (sol-1, sol-2, luna-1), 0.156.1 (sol-3, luna-2, luna-3) | `~/ralph-exp027/sessions-*/` rollout `cli_version` 6개. **불일치**: README·`runs/phase0.md`·`report.md`는 0.155.1 하나로만 기록 — 실험 중간에 클라이언트가 갱신된 것으로 보인다 |
| EXP-028 | Claude Code 2.1.281 | `experiments/028-sonnet5-ralph/README.md`, `runs/phase0.md`, `~/ralph-exp028/` 세션 jsonl 10개 |
| EXP-029 | pi 0.87.1 | `experiments/029-pi-openweight/runs/phase0.md`, `README.md` |
| EXP-030 | pi 0.87.1 | `experiments/030-pi-frontier/runs/phase0.md`, `README.md` |
| EXP-031 | Claude Code 2.1.284 | `experiments/031-sonnet55-ralph/runs/phase0.md`, `~/ralph-exp031/` 세션 jsonl 6개 |
| EXP-032 | pi 0.87.1 | `experiments/032-pi-sonnet55/README.md`, `runs/phase0.md` |
| EXP-033 | Codex CLI 0.160.0 | `experiments/033-gpt61-sol-codex/runs/phase0.md`·`phase0.log`, `runs/sessions.tar.gz` rollout `cli_version` 3개 |
| EXP-034 | pi 0.87.1 | `experiments/034-pi-gpt61-sol/runs/phase0.md`, `README.md` |

## 읽는 법

- 같은 Claude Code 계열이라도 2.1.215부터 2.1.284까지 여러 버전에 걸쳐 있고, Codex CLI는 0.144.0·0.153.4·0.155.1·0.156.1·0.160.0이 섞여 있다. 실험 간 시간 비교에는 클라이언트 버전 차이가 모델 차이와 함께 들어 있다.
- "미기록"은 문서와 세션 원자료 어디에서도 버전을 확인하지 못했다는 뜻이다. 현재 해당하는 곳은 EXP-019의 Claude Code(Opus run)뿐이다.
- EXP-025(문서 2.1.273 vs 세션 2.1.278)와 EXP-027(문서 0.155.1 vs 세션 일부 0.156.1)의 불일치는 원 문서를 수정하지 않았다. 이 표는 세션 원자료를 우선했다.
