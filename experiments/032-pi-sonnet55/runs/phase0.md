# EXP-032 Phase 0 — 기동 전 확인 (2026-09-29 KST)

- 모델 ID: pi 0.87.1(npm 최신, 2026-09-22 배포) 내장 anthropic 목록에 `claude-sonnet-5-5` 없음 → `pi-models.json`으로 추가(내장 `claude-sonnet-5` 정의 복사, ID만 변경). `pi --list-models anthropic`에 표시 확인. `smoke.sh` PASS(`SMOKE-OK` 응답) — Anthropic API가 이 ID를 받았다.
- 본 run 세션 확인: 전 assistant 메시지 `provider=anthropic`, `model=claude-sonnet-5-5`. thinking 기본값은 `thinking_level_change` 기준 `medium`.
- 정본 해시: setup.sh가 PROMPT-en·Hurl 13파일을 checksums.md5와 대조 — 일치.
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, measure v4 + 빈 포트 주입(EXP-031부터).
- 포트: `:3000`·`:3001`(VS Code 확장 호스트), `:3003`(DeepSRT) LISTEN — WARN. 빈 포트 주입으로 대응.
- 격리: `PI_CODING_AGENT_DIR=~/ralph-exp032/pi-agent`(auth.json·models.json만), `-nc -ns -ne -np -na`, `PI_OFFLINE=1`. 인증: `ANTHROPIC_API_KEY`(`~/.zsh_secrets`).
- 스모크 전 수동 시험에서 `pi -p`를 stdin 연결 상태로 실행하면 응답 없이 대기했다(120초 타임아웃). driver·smoke는 `< /dev/null`로 실행하므로 영향 없음.
- 기동: 2026-09-29 07:48:29.
