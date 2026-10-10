# EXP-044 Phase 0 (2026-10-10)

- 클라이언트: pi 0.87.1 (`/Users/dohyunjung/.asdf/installs/nodejs/24.14.0/bin/pi`), 변환 계층 없음(DashScope OpenAI 호환 직결)
- 채점기 `/opt/homebrew/bin/hurl` 8.0.1, Node v24.14.0. 채점기 정상/오류 사례는 EXP-042 Phase 0(같은 날·같은 measure.sh)과 같음.
- 스모크: `dashscope/qwen3.8-flash`·`dashscope/qwen3-coder-next`·`dashscope/qwen3.8-27b` 모두 PASS(SMOKE-OK). 응답 모델 필드는 본 실행 세션 jsonl에서 전수 확인 예정.
- 한도 조사 요청(curl): 300K 입력 시험이 flash·27b에서 수락되어 각 약 30만 입력 토큰이 과금됨(실험 계측 밖). 1.2M 입력은 거절(과금 없음).
- 노출: pi 격리 플래그 `-nc -ns -ne -np -na`, `PI_CODING_AGENT_DIR` 전용, `PI_OFFLINE=1`, 비밀값 `DASHSCOPE_API_KEY`만.
- 포트: 3000·3001(VS Code 확장), 3003(DeepSRT) 외부 LISTEN, 종료하지 않음(빈 포트 주입 규칙).
