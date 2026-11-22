# EXP-063 Phase 0 (2026-11-22)

- 클라이언트: Antigravity CLI (agy) 1.5.14, AGY_CLI_DISABLE_AUTO_UPDATE=1
- 채점기: hurl 8.1.0 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- PROMPT: v2 EN, md5 3d11ae8d28546ac730d482d015cfd6d9
- 인증: AGY_AUTH=subscription — 격리 HOME(agy-home) + ~/Library/Keychains 링크, GEMINI_API_KEY 미노출. smoke에서 cli.log authMethod=consumer 확인(3 모델)
- smoke: PASS gemini-4-carbon / gemini-4-neon / gemini-4-hydrogen (SMOKE-OK 응답, effort high)
- 노출 항목: 격리 HOME settings.json '{}'(기본값), 전역 지침·스킬·MCP 미설정. 사용자 키체인 디렉터리 링크가 에이전트 HOME에 보임(이탈 후보)
- 사전 조회: 같은 날 API 키 경로로 agy models 목록 조회 1회(모델 호출 없음)
