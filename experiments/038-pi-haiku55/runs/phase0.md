# EXP-038 Phase 0 — 기동 전 확인 (2026-10-08 KST)

- 모델 ID: `GET /v1/models/claude-haiku-5-5`(Anthropic API 키) 응답으로 실재·max_input 1M·max_tokens 128K 확인. pi 0.87.1 내장 목록에 없어 `pi-models.json` 사용자 정의 항목 사용(설계 README 참조).
- 스모크: 1차 FAIL — "No API key found for anthropic". EXP-036 이후 하네스가 지정된 키만 노출하므로 `PI_KEEP_ENV="ANTHROPIC_API_KEY"`를 bench.env에 추가하고 setup 재실행 → PASS (`phase0.log`). 기동 전 설정 보완이며 실험 조건 변경이 아니다.
- 정본 해시: setup.sh가 PROMPT-en·Hurl 13파일을 checksums.md5와 대조 — 일치.
- 채점기: `hurl 8.0.1`, measure v4 + 빈 포트 주입.
- 포트 점유: `127.0.0.1:3000`·`:3001`(VS Code) — WARN, 하네스가 빈 포트 주입.
- 도구: pi 0.87.1, macOS Darwin 25.6.0. 격리: `PI_CODING_AGENT_DIR` 전용, `-nc -ns -ne -np -na`, 에이전트 환경의 비밀값은 `ANTHROPIC_API_KEY`만.
- 인증: Anthropic API 키(실제 과금).
- 기동: 2026-10-08 08:27:12.
