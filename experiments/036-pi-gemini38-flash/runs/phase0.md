# Phase 0 — ralph-exp036 (2026-10-07 16:42 KST)

- 스모크: PASS (`phase0.log`)
- 클라이언트: pi 0.87.1
- 채점기: hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- 인증: Gemini API 키 (`GEMINI_API_KEY`, ~/.zsh_secrets). PI_KEYMAP으로 GOOGLE_API_KEY=GEMINI_API_KEY 값 통일 (pi는 GOOGLE_API_KEY 우선 사용)
- 노출 지침: -nc -ns -ne -np -na — AGENTS.md/CLAUDE.md·스킬·확장(pi-clm 포함)·프롬프트 템플릿 비노출
- 포트: VS Code Code Helper가 127.0.0.1:3000·3001 LISTEN. driver가 run마다 빈 포트를 PORT로 주입.
