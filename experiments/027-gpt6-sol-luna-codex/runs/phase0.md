# EXP-027 Phase 0 — 기동 전 확인 (2026-09-24 KST)

- **모델 ID**: OpenAI `GET /v1/models`의 GPT-6 항목은 `gpt-6-astra`·`gpt-6-luna`·`gpt-6-sol` 3개. Codex `models_cache.json`(fetched 2026-09-23T23:42Z)도 동일.
- **존재하지 않는 ID**: `gpt-6-earth`·`gpt-6-terra` → Codex 400 `"The '<id>' model is not supported when using Codex with a ChatGPT account."` (models_cache에도 없음). 사용자 확인 후 대상에서 제외.
- **스모크**: `smoke.sh`(전용 CODEX_HOME, effort medium, read-only) — gpt-6-sol PASS(tokens used 2,267 — 사전 스모크 기준), gpt-6-luna PASS. 스모크 세션은 삭제 후 기동.
- **정본 해시**: setup.sh가 PROMPT-en(md5 `2c28ea6b…`)·PROMPT-ko·Hurl 13파일을 스킬 `assets/checksums.md5`와 대조 — 일치.
- **채점기 확인**: `/opt/homebrew/bin/hurl` 8.0.1. 정상 사례(EXP-021 `app-astra-1`) → `13,154`, 오류 사례(빈 디렉터리) → `0,0`.
- **도구 버전**: Codex CLI 0.155.1, macOS Darwin 25.6.0.
- **인증**: `~/.codex/auth.json` 최신본 복사(ChatGPT 플랜 OAuth). `OPENAI_API_KEY`는 모델 목록 조회에만 사용.
- **노출 설정**: 전용 CODEX_HOME의 config.toml은 빈 파일, AGENTS.md·스킬·MCP 없음.
- 기동: 2026-09-24 08:47:31.
