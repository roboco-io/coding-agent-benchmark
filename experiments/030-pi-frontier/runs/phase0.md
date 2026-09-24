# EXP-030 Phase 0 (2026-09-24)

- 도구: pi 0.87.1 (Node v24.14.0), hurl 8.0.1 (`/opt/homebrew/bin/hurl`, `hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 ...`), macOS 26.6.2
- 모델 ID 확인 (`pi --list-models`, 2026-09-24): `anthropic claude-opus-5-5` (1M·128K), `openai-codex gpt-6-sol` (272K·128K) 존재
- 인증: anthropic은 `~/.zsh_secrets`의 `ANTHROPIC_API_KEY`를 `pi_env.sh`가 env로 전달(값 미기록). openai-codex는 `~/.pi/agent/auth.json`(OAuth, 만료까지 약 240시간)을 setup.sh가 `pi-agent/auth.json`(600)으로 복사. 복사본에는 deepseek api_key 항목도 있으나 이번 조건에서는 쓰이지 않는다. 사용자 `settings.json`(defaultProvider 등)은 복사하지 않았다.
- smoke.sh: PASS anthropic/claude-opus-5-5 · PASS openai-codex/gpt-6-sol (원문 phase0.log)
- 도구 왕복 스모크: 두 조건 모두 bash 도구로 `echo $((6*7))` 실행 후 `TOOL-42` 반환, "AGENTS.md/CLAUDE.md 내용이 컨텍스트에 있는가" 질문에 둘 다 `NO`
- thinking 기본값(세션 `thinking_level_change`): claude-opus-5-5 `medium`, gpt-6-sol `medium`
- usage 필드 (세션 jsonl assistant `usage`):
  - anthropic: `input·output·cacheRead·cacheWrite·cacheWrite1h·reasoning·totalTokens`. `totalTokens = input+output+cacheRead+cacheWrite` 검산 일치. `reasoning`은 0으로 기록(Anthropic 응답이 thinking 토큰을 별도 보고하지 않아 output에 포함). `cacheWrite1h`는 스모크에서 0 — 본 실행에서 0이 아니면 포함 관계를 재확인.
  - openai-codex: `input·output·cacheRead·cacheWrite·reasoning·totalTokens`. `input`은 비캐시 입력(input 207 + cacheRead 1024 + output 48 = total 1279), `reasoning` 37 ≤ output 48로 output에 포함. `cacheWrite`는 0.
  - 양쪽 모두 `responseId` 존재 → `usage_pi.py`의 중복 제거 키 사용 가능.
- 채점 환경: 기동 직전(17:47) 3000번대 외부 LISTEN은 `DeepSRT 127.0.0.1:3003`뿐(EXP-029 D-1 재채점 시와 동일, 설계에서 허용). 3000·3001·3002·4000 비점유.
- 격리: `PI_CODING_AGENT_DIR=~/ralph-exp030/pi-agent`(auth.json만 존재), `PI_OFFLINE=1`, `PI_SKIP_VERSION_CHECK=1`, run별 `--session-dir`, 호출 플래그 `-nc -ns -ne -np -na`
- 정본 해시: setup.sh checksums.md5 검증 통과
- 기동: 2026-09-24 17:47:32 (`orchestrator.log`)
