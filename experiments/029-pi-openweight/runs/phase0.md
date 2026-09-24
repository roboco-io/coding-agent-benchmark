# EXP-029 Phase 0 (2026-09-24)

- 도구: pi 0.87.1 (`@earendil-works/pi-coding-agent`, Node v24.14.0), hurl 8.0.1 (/opt/homebrew/bin/hurl), macOS 26.6.2
- 모델 ID 확인 (제공자 /models API, 2026-09-24): Moonshot `kimi-k3`, DashScope intl `qwen3.8-max`, DeepSeek `deepseek-flash` 존재
- smoke.sh: PASS moonshotai/kimi-k3 · PASS dashscope/qwen3.8-max · PASS deepseek/deepseek-flash (원문 phase0.log)
- 사전 도구 왕복 스모크: 3조건 모두 bash 도구 호출 후 `TOOL-42` 반환, 세션 jsonl에 usage·responseId·provider/model 기록 확인
- thinking 기본값(세션 thinking_level_change): kimi-k3 high, qwen3.8-max medium, deepseek-flash high
- usage 의미: input=비캐시 입력, cacheRead/cacheWrite 별도, reasoning ⊂ output (totalTokens 검산 일치)
- 지침 노출: 홈에 ~/AGENTS.md 존재. deepseek-flash로 확인 — `-nc` 포함 시 "NO", 제외 시 "/Users/dohyunjung/AGENTS.md" 노출. 본 실행은 `-nc -ns -ne -np -na` 고정
- 격리: PI_CODING_AGENT_DIR=~/ralph-exp029/pi-agent (models.json만 존재), PI_OFFLINE=1, run별 --session-dir
- 정본 해시: setup.sh checksums.md5 검증 통과
