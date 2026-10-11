# EXP-046 Phase 0

- 일시: 2026-10-11 18:35 KST
- preflight: g53f 적합(1,000,000), 최악 총액 $6. 사용자 승인 "상한 상향 후 진행 (Recommended)" (approve.sh 기록)
- 스모크: `zai/glm-5.3-flash` PASS (SMOKE-OK)
- 클라이언트: pi 0.87.1 (`pi --version`)
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1
- 노출: pi `-nc -ns -ne -np -na`로 상위 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 비노출, 환경 키는 `ZAI_API_KEY`만(`PI_KEYMAP`, 값은 GLM_API_KEY)
- 포트: 외부 프로세스 DeepSRT가 127.0.0.1:3003 LISTEN — 종료하지 않음, 하네스는 빈 포트 주입
