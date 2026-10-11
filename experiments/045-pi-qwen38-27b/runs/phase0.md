# EXP-045 Phase 0

- 일시: 2026-10-11 11:40 KST
- preflight: q27 적합(983,616), 최악 총액 $12. 사용자 승인 "진행 (Recommended)" (approve.sh 기록)
- 스모크: `dashscope/qwen3.8-27b` PASS (SMOKE-OK)
- 클라이언트: pi 0.87.1 (`pi --version`)
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1
- 노출: pi `-nc -ns -ne -np -na`로 상위 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 비노출, 환경 키는 `DASHSCOPE_API_KEY`만(`PI_KEEP_ENV`)
