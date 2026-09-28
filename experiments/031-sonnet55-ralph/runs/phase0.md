# EXP-031 Phase 0 — 기동 전 확인 (2026-09-29 KST)

- 모델 ID: Anthropic API 키 미설정으로 모델 목록 API 미조회. `smoke.sh`(claude -p --model claude-sonnet-5-5 --output-format json) PASS, 응답 `modelUsage` 키가 `claude-sonnet-5-5`로 요청 ID와 일치.
- 정본 해시: setup.sh가 PROMPT-en/ko·Hurl 13파일을 스킬 checksums.md5와 대조 — 일치.
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, measure v4 + 빈 포트 주입(`PORT`, 40000–49999). 사전 검증: EXP-028 완주 앱(`app-sonnet5-en-2`)을 새 measure로 채점해 `13,154`(포트 45174).
- 포트 점유: `127.0.0.1:3000`·`:3001`(VS Code 확장 호스트), `:3003`(DeepSRT) LISTEN — smoke WARN. 사용자 지시(2026-09-29)로 프로세스를 종료하지 않고 하네스가 빈 포트를 주입하도록 변경.
- 도구: Claude Code 2.1.284, macOS Darwin 25.6.0.
- 노출 설정: claude-native 비격리 — 사용자 글로벌 CLAUDE.md·플러그인 스킬·MCP가 노출된다(EXP-023/026/028과 동일 조건). 구독 인증.
- 기동: 2026-09-29 06:51:07.
