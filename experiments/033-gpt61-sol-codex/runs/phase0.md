# EXP-033 Phase 0 (2026-10-03 07:49)

- 스모크: `gpt-6.1-sol` PASS (`phase0.log`). Codex CLI 0.160.0, model `gpt-6.1-sol`, reasoning effort medium, provider openai.
- 모델 ID 실재: 같은 계정 대조 호출에서 `gpt-6.9-bogus`는 400 `model is not supported when using Codex with a ChatGPT account`, `gpt-6.1-sol`은 정상 응답. Codex 로컬 모델 캐시에 없어 fallback metadata 경고가 난다.
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, Hurl 13파일·154 요청, PROMPT-en md5 `2c28ea6b7f16125d9b3105f5ee00b126` (setup.sh 검증 통과).
- 격리: `CODEX_HOME=~/ralph-exp033/codex-home` (auth.json 최신본 + 빈 config.toml). 사용자 `~/.codex`의 AGENTS.md·스킬·MCP·플러그인 훅 비노출.
- 포트: 3000·3001(VS Code Code Helper), 3003(DeepSRT) 외부 LISTEN. driver가 run별 빈 포트를 `PORT`로 주입(run 1–3: 44009·47261·47039).
