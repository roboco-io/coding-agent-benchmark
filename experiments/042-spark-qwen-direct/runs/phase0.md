# EXP-042 Phase 0 (2026-10-10)

## 환경
- 클라이언트: Claude Code 2.1.296 (`claude --version`), 변환 계층 없음
- 채점기: `/opt/homebrew/bin/hurl` → `hurl 8.0.1 (x86_64-apple-darwin25.0) libcurl/8.7.1`
- Node v24.14.0, macOS Darwin 25.6.0
- 엔드포인트: `https://dashscope-intl.aliyuncs.com/apps/anthropic`, 키 `DASHSCOPE_API_KEY`(~/.zsh_secrets, 값 미기록)

## 제공자·클라이언트 스모크 (smoke.sh, 10:42)
| 모델 | 결과 | 응답 modelUsage 키 | 비고 |
|---|---|---|---|
| qwen3.8-flash | PASS (SMOKE-OK, 5.5s) | qwen3.8-flash | cache_creation 19,691 계상 |
| qwen3-coder-next | PASS (SMOKE-OK, 4.5s) | qwen3-coder-next | 캐시 필드 0 (캐시 미계상 — 미지원 단정은 하지 않음) |
| qwen3.8-27b | PASS (SMOKE-OK, 10.1s) | qwen3.8-27b | cache_creation 19,688 계상 |

- 세 모델 모두 `[claude-code:unrecognized_model]` 경고. Claude Code가 보고한 contextWindow 200000·maxOutputTokens 32000은 클라이언트 기본값이며 제공자 실제 한도가 아니다. 창 제한은 `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`로 해제.
- 사전 직접 호출(curl `/v1/messages`)에서도 3모델 200·`end_turn`. `qwen3.6-35b-a3b`는 정상 응답이 없어 후보 제외(조사 문서 참조).

## 정본·채점기
- PROMPT-en.md md5 `2c28ea6b7f16125d9b3105f5ee00b126` (EXP-010 EN 정본과 일치)
- 채점기 정상 사례: `~/experiments/ralph-exp038/app-haiku55-en-1`(npm ci 후) → `13,154`. 오류 사례: 빈 디렉터리 → `0,0`.

## 노출 지침·스킬·MCP
- 격리 `CLAUDE_CONFIG_DIR=~/experiments/ralph-exp042/claude-config`: `.claude.json`(onboarding 우회)만 존재. settings·CLAUDE.md·스킬·MCP·훅 없음. `env -u ANTHROPIC_API_KEY`.

## 포트
- 3000·3001(VS Code 확장 호스트), 3003(DeepSRT) 외부 LISTEN. 종료하지 않음(2026-10-10 사용자 지시: 포트 고정 금지·빈 포트 사용). 하네스는 40000–49999 빈 포트를 `PORT`로 주입하고 리포 소속 프로세스의 포트로만 채점한다.
