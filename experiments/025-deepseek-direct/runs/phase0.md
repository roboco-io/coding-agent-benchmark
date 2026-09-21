# EXP-025 Phase 0 — 기동 전 확인 (2026-09-21 KST)

- 모델 목록(`GET /models`, Bearer): `deepseek-flash`, `deepseek-v4-pro`. 구 별칭 `deepseek-chat`은 응답 model `deepseek-v4-flash`로 라우팅됨 → 실험에는 명시 ID만 사용.
- Anthropic 호환 스모크(`POST /anthropic/v1/messages`, max_tokens 50): 두 모델 모두 `SMOKE-OK`, content 타입 `[thinking, text]`(thinking 기본 ON), usage `input/cache_creation/cache_read/output` 계상. Bearer·x-api-key 인증 모두 200.
- Claude Code 스모크(격리 `CLAUDE_CONFIG_DIR`, env 3요소 치환): 양 모델 `SMOKE-OK`. 세션 jsonl assistant `message.model` — `deepseek-flash` 2건, `deepseek-v4-pro` 2건, 요청 ID와 일치.
- 채점기: `measure.sh` = EXP-021 v4(`HURL_BIN=/opt/homebrew/bin/hurl`), 정상 사례 `~/ralph-exp023/app-fable-1` → `13,154`; 오류 사례 빈 디렉토리 → `0,0`.
- PROMPT md5: EN `2c28ea6b7f16125d9b3105f5ee00b126`, KO `fa75275f335b1552ad1baedb630c522a`. harness-hurl 13파일(EXP-023과 diff 무차이).
- 환경: Claude Code 2.1.273, Hurl 8.0.1, Node 24.14.0, macOS Darwin 25.6.0. 포트 8000 비점유.
- 스모크 세션은 `claude-config-projects-phase0/`로 이동해 본 계측에서 제외.
- 기동: `nohup caffeinate -is ~/ralph-exp025/run-all.sh` — 순서 flash-en-1 → pro-en-1 → flash-ko-1 → pro-ko-1 → 2회차 → 3회차.
- 공식 문서 조사(서브에이전트, 2026-09-21): V4.1-Flash 2026-09-10 출시(`news/news260910`), `deepseek-v4-pro`는 V4.1-Pro 출시 전 Flash 라우팅 공지와 서비스 지속 공지가 충돌 — 스모크·jsonl에서는 `deepseek-v4-pro`로 응답. 본 실험은 응답 model 필드를 run별 전수 확인해 판정한다.
