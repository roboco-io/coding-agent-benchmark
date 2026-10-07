# EXP-037 Phase 0 — 기동 전 확인 (2026-10-08 KST)

- 모델 ID: Anthropic API 키 미설정으로 모델 목록 API 미조회. `smoke.sh`(claude -p --model claude-haiku-5-5 --output-format json) PASS, 응답 `modelUsage` 키가 `claude-haiku-5-5`로 요청 ID와 일치(`phase0.log`).
- 정본 해시: setup.sh가 PROMPT-en/ko·Hurl 13파일을 스킬 checksums.md5와 대조 — 일치.
- 채점기: `hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1`, measure v4 + 빈 포트 주입(`PORT`, 40000–49999).
- 포트 점유: `127.0.0.1:3000`·`:3001`(VS Code 확장 호스트) LISTEN — smoke WARN. EXP-031 이후와 같이 하네스가 빈 포트를 주입.
- 도구: 2.1.293 (Claude Code), macOS Darwin 25.6.0.
- 노출 설정: claude-native 비격리 — 사용자 글로벌 CLAUDE.md·플러그인 스킬·MCP가 노출된다(EXP-023/026/028/031과 동일 조건). 인증: 구독으로 기록했으나 스모크 출력의 인증 출처가 `"apiKeySource":"ANTHROPIC_API_KEY"`였다 — API 키 인증([D-1](deviations.md), 2026-10-08 사후 정정).
- 기동: 2026-10-08 07:30:20.
