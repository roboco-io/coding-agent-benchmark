# EXP-051 Phase 0 (2026-10-25)

- preflight: [preflight-report.md](preflight-report.md) — 두 조건 모두 입력 한도 1,048,576으로 **적합**. 캐시 할인 없는 run당 추정 p50 pro $4.75·hs $9.49.
- 사용자 승인: 2026-10-25 "진행 (Recommended)" ([preflight-approved](preflight-approved)). 상한 RUN_BUDGET_USD=3, EXP_BUDGET_USD=15.
- smoke: 2026-10-25 13:00 — `moonshotai/kimi-k3.1-pro` PASS, `moonshotai/kimi-k3.1-pro-highspeed` PASS (SMOKE-OK).
- 클라이언트: pi 0.87.1 (`/Users/dohyunjung/.asdf/installs/nodejs/24.14.0/bin/pi`), 변환 계층 없음.
- 채점기: hurl 8.0.1 (`/opt/homebrew/bin/hurl`).
- 모델 정의: 사용자 정의 `pi-agent/models.json`(EXP-051 `pi-models.json` 사본) — 내장 kimi-k3 정의 복제, id·이름·단가만 변경. thinking `--thinking high`.
- 노출 지침·스킬·MCP: pi `-nc -ns -ne -np -na`로 상위 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 템플릿 비노출. 키는 `MOONSHOT_API_KEY`만 노출(PI_KEYMAP).
- 기동: 2026-10-25 13:00:19, 순차·조건 교차(k31pro-en-1 → k31hs-en-1 → k31pro-en-2 …).
