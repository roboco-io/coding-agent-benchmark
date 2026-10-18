# EXP-048 Phase 0

- 일시: 2026-10-18 KST
- 모델 확인: DeepSeek `GET /models`에 `deepseek-flash`(name DeepSeek-V4.1-Flash, context_window 1,048,576, max_output_tokens 393,216)와 `deepseek-v4-pro`만 있다. `deepseek-flash-1017`·`deepseek-v4.1-flash-1017`·`deepseek-v4.1-flash`는 가짜 ID(`zz-fake-model-xyz`)와 같은 "supported API model names are deepseek-flash, deepseek-v4-pro" 오류로 거부. 별칭이 1017을 가리킨다는 근거는 공식 changelog(2026-10-17 "DeepSeek-V4.1-Flash-1017 Update")와 가격 페이지 Version 칸.
- preflight: flash1017 적합(1,048,576), 3 run, 상한 run당 $1·실험 $3, 최악 총액 $3. 사용자 승인 "진행 (Recommended)" (approve.sh 기록)
- smoke 1차: Claude Code 본체 PASS, `usage_probe.py` FAIL — HTTP 400 "The `content[].thinking` in the thinking mode must be passed back to the API". probe의 assistant 턴에 thinking 블록이 없었기 때문. API 호출 1회분(약 6K 입력)만 소모.
- 조치: 스킬 `usage_probe.py`가 400 + "thinking" 오류일 때만 assistant 턴에 thinking 블록을 넣어 1회 재요청하도록 수정(다른 제공자 동작 불변). 가짜 모델 ID 오류는 여전히 FAIL로 보고됨을 확인.
- smoke 2차: PASS — usage probe 기대 입력 약 8,625 / message_start 7,099 / message_delta 7,099, 본체 PASS
- 클라이언트: Claude Code 2.1.302 (`claude --version`, 세션 jsonl `version` 전수 2.1.302)
- 연결: `https://api.deepseek.com/anthropic` 직결(Bearer), 키는 `DEEPSEEK_API_KEY`만 노출, `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`
- 격리: 전용 `CLAUDE_CONFIG_DIR`(설정 파일 없음 — 스킬·MCP·사용자 지침 비노출), thinking 제공자 기본값
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1
- 외부 포트: DeepSRT 127.0.0.1:3003 LISTEN(종료하지 않음). 하네스가 run마다 빈 포트를 PORT로 주입
