# EXP-057 Phase 0 (2026-10-28)
- smoke: PASS openai-codex/gpt-6.1-terra
- 클라이언트: pi 0.87.1
- 채점기: hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- PROMPT: v2 정본 (md5 3d11ae8d28546ac730d482d015cfd6d9)
- 추가 지침: --append-system-prompt persistence.md (md5 ac5b9e388772cf080f6af03e7ccf32ab)
- 주입 확인: (1) 대조 — 텍스트 인자 "MANGO-17"·파일 인자 "PINEAPPLE-42" 모두 모델이 회수. (2) 실제 지침 — "Do not end your turn after finishing one part of the work: ..." 문장 완성 요청에 원문 그대로 응답. 첫 탐침("Autonomy and persistence 절이 있나")에는 NO로 답해 모델 자기보고는 신뢰하지 않음.
- 인증: ChatGPT 구독 OAuth, 노출: pi -nc -ns -ne -np -na 격리 + 위 지침, thinking medium
- 포트: VS Code Code Helper 3000·3001 LISTEN (종료하지 않음)
