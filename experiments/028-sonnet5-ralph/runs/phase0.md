# EXP-028 Phase 0 — 기동 전 확인 (2026-09-24 KST)

- 모델 ID: Anthropic API 키 미설정으로 모델 목록 API 미조회. `smoke.sh`(claude -p --model claude-sonnet-5 --output-format json) PASS, 응답 `modelUsage` 키가 `claude-sonnet-5`로 요청 ID와 일치.
- 정본 해시: setup.sh가 PROMPT-en/ko·Hurl 13파일을 스킬 checksums.md5와 대조 — 일치.
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, measure v4 (EXP-027 D-1 수정본 — EXP-027에서 정상 13,154 / 빈 디렉터리 0,0 확인).
- 도구: Claude Code 2.1.281, macOS Darwin 25.6.0.
- 노출 설정: claude-native 비격리 — 사용자 글로벌 CLAUDE.md·플러그인 스킬·MCP가 노출된다(EXP-023/026과 동일 조건). 구독 인증.
- 기동: 2026-09-24 10:16:09.
