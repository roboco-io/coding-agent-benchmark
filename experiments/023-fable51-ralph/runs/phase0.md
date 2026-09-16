# EXP-023 Phase 0 — 기동 전 스모크

- 일시: 2026-09-16 15:47 KST
- 환경: Claude Code 2.1.273, Hurl 8.0.1 (`/opt/homebrew/bin/hurl`), macOS Darwin 25.6.0
- 명령: `cd ~/ralph-exp023 && claude -p 'Reply with exactly SMOKE-OK and nothing else.' --model claude-fable-5-1`
- 결과: **통과** — `SMOKE-OK` 정확 출력. 모델 ID `claude-fable-5-1` 유효·구독 인증 확인
- 하네스 대조: `driver.sh` = EXP-019 driver-opus.sh (diff는 주석 1줄·BASE 경로), `measure.sh` = EXP-021 measure v4 (diff는 주석 2줄·BASE 경로), `harness-hurl/` = EXP-010/021과 동일(diff -rq 무차이)
- PROMPT md5 `2c28ea6b7f16125d9b3105f5ee00b126` (EXP-010 EN 정본과 일치)
- 포트 8000 비점유, `~/ralph-exp0*` 관련 잔여 프로세스 없음
- 스모크 세션은 `~/.claude/projects/-Users-dohyunjung-ralph-exp023/`에 생성됨 — 본 계측(app-fable-N 디렉토리)에서 제외
- 기동: `nohup caffeinate -is ~/ralph-exp023/run-all.sh` 2026-09-16 15:48:06
