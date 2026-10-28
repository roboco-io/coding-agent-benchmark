# EXP-055 Phase 0 (2026-10-28)
- smoke: PASS openai-codex/gpt-6.1-terra
- 클라이언트: pi 0.87.1
- 채점기: hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- 인증: ChatGPT 구독 OAuth (~/.pi/agent/auth.json 최신본을 격리 pi-agent에 복사)
- 노출: pi -nc -ns -ne -np -na 격리 — 상위 AGENTS.md·CLAUDE.md·스킬·확장 비노출, 사용자 정의 models.json(gpt-6.1-terra)만 추가
- thinking: medium 명시
- 포트: VS Code Code Helper 3000·3001 LISTEN (종료하지 않음, 하네스가 빈 PORT 주입)
