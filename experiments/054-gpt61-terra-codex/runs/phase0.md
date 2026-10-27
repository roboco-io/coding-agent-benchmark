# EXP-054 Phase 0 (2026-10-27)
- smoke: PASS gpt-6.1-terra (SMOKE-OK, effort medium, session 01a17dd2-18ec-7432-9029-fc66ecb53b53)
- 클라이언트: codex-cli 0.164.0
- 채점기: hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- 인증: ChatGPT 구독 OAuth (격리 CODEX_HOME에 ~/.codex/auth.json 최신본 복사)
- 노출: 격리 CODEX_HOME, 빈 config.toml — 사용자 AGENTS.md·MCP·플러그인 훅 비노출
- 포트: VS Code Code Helper 3000·3001 LISTEN (종료하지 않음, 하네스가 빈 PORT 주입)
