# EXP-053 Phase 0 (2026-10-25)

- preflight: [preflight-report.md](preflight-report.md) — 두 조건 모두 입력 한도 1M급으로 **적합**. 캐시 할인 없는 run당 추정 p50 glm-5.3 $3.24·prime $6.48.
- 사용자 승인: 2026-10-25 "진행 (Recommended)" ([preflight-approved](preflight-approved)). 상한 RUN_BUDGET_USD=4, EXP_BUDGET_USD=20. OpenRouter 잔여 크레딧 $23.37.
- smoke: 2026-10-25 17:38 — `openrouter/z-ai/glm-5.3` PASS, `openrouter/z-ai/glm-5.3-prime` PASS (SMOKE-OK).
- 제공자 고정 확인: 각 조건 첫 run의 첫 응답 2건을 OpenRouter generation API로 조회 — glm-5.3 `Z.AI`(served `z-ai/glm-5.3-20260816`), prime `Alibaba`(served `z-ai/glm-5.3-prime-20260921`). 실험 종료 후 전 호출 316건 대조(runs/openrouter-generations.csv).
- 클라이언트: pi 0.87.1, 변환 계층 없음(OpenRouter OpenAI 호환 API). 채점기: hurl 8.0.1.
- PROMPT: 정본 **v2**(md5 `3d11ae8d28546ac730d482d015cfd6d9`, PORT 안내 포함) — [PROMPT-en.md](PROMPT-en.md).
- 노출: pi `-nc -ns -ne -np -na`, 키는 `OPENROUTER_API_KEY`만(PI_KEEP_ENV). thinking `--thinking high`.
- 기동: 2026-10-25 17:38:53, 순차·조건 교차.
