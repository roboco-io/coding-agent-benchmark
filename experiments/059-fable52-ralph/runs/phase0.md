# EXP-059 Phase 0 (2026-11-10 10:06 KST)

- smoke.sh: `PASS claude-fable-5-2` — `SMOKE-OK` 정확 출력, 응답 `message.model` = `claude-fable-5-2`, `modelUsage.canonicalModel` = `claude-fable-5-2`, `provider` = `firstParty`.
- 인증: `"apiKeySource":"none"` — 구독 OAuth. rate_limit_event에서 `overageStatus: rejected`(`org_level_disabled`), `isUsingOverage: false` — 유료 추가 사용 비활성 확인. 5시간 창 사용률 0.02.
- 클라이언트: Claude Code 2.1.321 (`claude --version`, init `claude_code_version` 일치). hurl: `/opt/homebrew/bin/hurl`.
- 캐시: 캐시 쓰기 1h TTL(`ephemeral_1h_input_tokens`).
- 노출(비격리 `~/.claude`): 글로벌 `~/.claude/CLAUDE.md`, MCP(browsermcp·context7·exa·claude.ai Docs/Exa/Calendar/Drive/Gmail), 플러그인(claude-hud·codex·documentation·hookify·ralph-loop·workflow·superlite·cowork-plugin-management), 스킬 다수. `permissionMode` 보고값은 `auto`.
- 외부 포트: DeepSRT 127.0.0.1:3003 LISTEN(종료하지 않음, 하네스는 빈 포트 주입).
