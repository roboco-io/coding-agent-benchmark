# EXP-050 Phase 0 (2026-10-19)

- preflight: [preflight-report.md](preflight-report.md), 사용자 승인 2026-10-19 "진행 (Recommended)" ([preflight-approved](preflight-approved))
- smoke: `PASS deepseek/deepseek-flash` (16:11:18, SMOKE-OK) — [phase0.log](phase0.log)
- 클라이언트: pi 0.87.1 (`pi --version`), 내장 deepseek provider (openai-completions, https://api.deepseek.com)
- 채점기: `/opt/homebrew/bin/hurl` → `hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1`
- 노출: `pi -p -nc -ns -ne -np -na` (상위 지침·스킬·확장·프롬프트 템플릿 비노출), 에이전트 환경 키는 `DEEPSEEK_API_KEY`만
- thinking: `--thinking high`, 세션 기록 `thinking_level_change` 전수 `high`
- 포트: 외부 LISTEN 127.0.0.1:3003(DeepSRT) — 종료하지 않음, 하네스가 빈 포트 PORT 주입
