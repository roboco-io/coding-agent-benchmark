# EXP-064 Phase 0

- 일시: 2026-11-24. smoke 두 조건 PASS(원문 `phase0.log`), pi 지속 지침 고유 문장 완성 탐침 통과.
- 클라이언트: pi 0.87.1 (`-nc -ns -ne -np -na`, `PI_PERSISTENCE=on`). 채점기: `/opt/homebrew/bin/hurl`.
- 연결: `https://api.upstage.ai/v1` OpenAI 호환, 사용자 정의 `pi-models.json`(`thinkingFormat: openai`). 키는 `PI_KEEP_ENV=UPSTAGE_API_KEY`로만 노출.
- 사전 탐침(curl): `GET /v1/models`에 두 ID 존재. `reasoning_effort=high` 응답에 `reasoning` 필드, `completion_tokens`가 `reasoning_tokens` 포함. 3,000 토큰 생성 mini45 10.1초, pro4 54.3초.
- pi 탐침: `--thinking high`로 세션에 `thinking_level_change high`와 thinking 블록 기록. pi usage `output`이 `reasoning`을 포함(input+output+cacheRead = totalTokens). mini45는 캐시 읽기 1,280 보고, pro4는 0.
- 외부 LISTEN 포트: DeepSRT 127.0.0.1:3003 (종료하지 않음, 하네스가 빈 포트 주입).
- 노출 지침·스킬·MCP: pi 격리 플래그로 상위 AGENTS.md/CLAUDE.md·스킬·확장 비노출. 추가 지침은 정본 지속 지침뿐.
- 2단계(12:27): pro4c 추가 후 smoke 3조건 PASS (`phase2-smoke.log`).
