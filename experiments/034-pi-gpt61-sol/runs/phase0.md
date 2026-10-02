# EXP-034 Phase 0 (2026-10-03 07:49)

- 스모크: `openai-codex/gpt-6.1-sol` PASS (`phase0.log`, 응답 `SMOKE-OK`). pi 0.87.1, 사용자 정의 모델 항목(`pi-models.json`).
- 모델 ID 실재: 같은 계정 대조 호출에서 `gpt-6.9-bogus`는 400 `model is not supported when using Codex with a ChatGPT account`, `gpt-6.1-sol`은 정상 응답. pi 내장 목록에 없어 `gpt-6-sol` 정의를 복사한 사용자 정의 항목을 쓴다.
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, Hurl 13파일·154 요청, PROMPT-en md5 `2c28ea6b7f16125d9b3105f5ee00b126` (setup.sh 검증 통과).
- 격리: `PI_CODING_AGENT_DIR=~/ralph-exp034/pi-agent`(auth.json 최신본·models.json만), `-nc -ns -ne -np -na`로 상위 지침·스킬·확장 비노출, `PI_OFFLINE=1`.
- 포트: 3000·3001(VS Code Code Helper), 3003(DeepSRT) 외부 LISTEN. driver가 run별 빈 포트를 `PORT`로 주입.
