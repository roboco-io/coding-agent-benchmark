# Phase 0 — ralph-exp035 (2026-10-07 16:42 KST)

- 스모크: PASS (`phase0.log`)
- 클라이언트: Antigravity CLI agy 1.3.1
- 채점기: hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1
- 인증: Gemini API 키 (`GEMINI_API_KEY`, ~/.zsh_secrets). agy 호출 시 GOOGLE_API_KEY 제거, 격리 HOME settings.json modelProvider=gemini
- 노출 지침: 격리 HOME — ~/AGENTS.md·GEMINI.md·사용자 MCP 없음. agy 제품 내장 스킬·시스템 프롬프트는 유지
- 포트: VS Code Code Helper가 127.0.0.1:3000·3001 LISTEN. driver가 run마다 빈 포트를 PORT로 주입.
- agy 내장 스킬(builtin/skills, 제품 기본): agy-customizations, antigravity_guide, automation, generative_ui, migrate-workflows, permissioned-github, plugin, ui-plugin-navigation
