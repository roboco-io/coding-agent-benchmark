# EXP-052 Phase 0 (2026-10-25)

- preflight: [preflight-report.md](preflight-report.md) — 두 조건 모두 입력 한도 1,048,576으로 **적합**. 캐시 할인 없는 run당 추정 p50 pro $4.75·hs $9.49.
- 사용자 승인: 2026-10-25 "진행 (Recommended)" ([preflight-approved](preflight-approved)). 상한 RUN_BUDGET_USD=4, EXP_BUDGET_USD=20.
- smoke 1차(14:2x): pro usage_probe·smoke PASS, highspeed usage_probe가 Moonshot `HTTP 429 credit balance is running low`로 FAIL. 잔액 조회 $0.03. run 기동 전 중단하고 사용자에게 알림 → 사용자 충전(잔액 $19.88 확인) 후 재실행.
- smoke 2차: 두 조건 usage_probe PASS(기대 입력 약 8,625 / message_start 6,998 / message_delta 6,998), smoke PASS.
- 클라이언트: 2.1.310 (Claude Code), 변환 계층 없음. 엔드포인트 `https://api.moonshot.ai/anthropic`, 인증 `ANTHROPIC_AUTH_TOKEN`(KIMI_API_KEY).
- 채점기: hurl 8.0.1 (`/opt/homebrew/bin/hurl`).
- 격리: 전용 `CLAUDE_CONFIG_DIR`, run별 세션 디렉터리. thinking은 Claude Code 기본값.
- 기동: 2026-10-25 14:37:37, 순차·조건 교차(k31pro-en-1 → k31hs-en-1 → …).
- 중단·재개: 14:43:14에 사용자의 과금 이상 문의로 run-all을 중단했다(k31pro-en-1 iteration 1 진행 중, 커밋 2개, API 오류 0, 가드 추정 $0.47). 중단 run의 산출 리포·세션·로그는 `aborted-k31pro-en-1/`로 옮겨 완주 판정에서 제외했다. 잔액 대조: 충전 후 $19.8771 → 중단 직후 $19.4579 → 15:41 $19.2276(중단 후에도 $0.23 감소 — 정산 지연). 총 차감 $0.65는 k31pro-en-1 토큰의 공개 단가 환산(캐시 읽기 할인·캐시 쓰기 1h $4 적용 시 $0.59) + smoke와 일치. 15:41:53 처음부터 재기동.
