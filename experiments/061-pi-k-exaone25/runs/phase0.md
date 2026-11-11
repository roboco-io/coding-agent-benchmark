# EXP-061 Phase 0

- 일시: 2026-11-11. 정본 상한 smoke 14:17(통과), 상한 완화 재설정 후 smoke 14:45(통과). 원문은 `phase0.log`, 중단 실행은 `strict-aborted/phase0.log`.
- 클라이언트: pi 0.87.1 (`-nc -ns -ne -np -na`, `PI_PERSISTENCE=on` — smoke 지속 지침 고유 문장 완성 탐침 통과). 채점기: `/opt/homebrew/bin/hurl`.
- 연결: `https://api.exaone.ai/v1` OpenAI 호환, 사용자 정의 `pi-models.json`(`thinkingFormat: chat-template`, `chatTemplateKwargs.preserve_thinking=true`, `reasoning_effort` 미전송 → 제공자 기본 max, maxTokens 65,536, strict mode 끔). 키는 `PI_KEEP_ENV=EXAONE_API_KEY`로만 노출.
- 사전 탐침(2026-11-11, curl 직접 호출): `GET /v1/models` → `k-exaone_v2.5` 단일. `/v1/messages`·`/anthropic/v1/messages` 404. tool calling `tool_calls` 반환 확인. 요청 한도 헤더 초당 1·분당 60·일 100 → 사용자 옵트인 후 일 86,400.
- 속도 탐침(정본 상한 실행 중단 후): 3,000 토큰 생성 `reasoning_effort=max` 137초(약 22 tok/s), `high` 157초(약 19 tok/s), 두 경우 모두 3,000 토큰 전부 reasoning.
- 노출 지침·스킬·MCP: pi 격리 플래그로 상위 AGENTS.md/CLAUDE.md·스킬·확장 비노출. 추가 지침은 정본 지속 지침뿐.
