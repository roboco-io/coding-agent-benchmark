# EXP-063 이탈 기록

## D-1 구독 토큰 미복사로 hydrogen-en-1 인증 실패 (2026-11-22 01:41–01:43)
- 증상: hydrogen-en-1 iteration 1·2가 "Authentication required … authentication timed out"(exit 1)로 즉시 종료. 모델 호출 없음.
- 원인: agy 구독 OAuth 토큰은 실 HOME `~/.gemini/antigravity-cli/antigravity-oauth-token`에 저장된다. 01:37 토큰 만료 후 실 HOME 쪽에서 갱신됐고, 격리 HOME에는 이 파일이 없어 keyringAuth가 토큰을 찾지 못했다. carbon-en-1·neon-en-1과 smoke가 키체인 링크만으로 인증된 경로는 미확인.
- 조치: 01:43 run-all·driver·agy 프로세스를 하나씩 종료하고 소멸 확인. `agy_env.sh`의 `agy_reset_home`이 run마다 토큰 파일 최신본을 격리 HOME에 복사(600)하도록 수정, 격리 HOME에서 `agy models`로 authMethod=consumer 확인. 사용자 승인("재개 (권장)") 후 hydrogen-en-1을 무효 처리(원자료 `aborted-hydrogen-en-1-auth/`)하고 같은 이름으로 재실행. carbon-en-1·neon-en-1은 유지(수정 전 하네스, 인증 경로 외 조건 동일).
- 노출: 에이전트 HOME에 구독 OAuth 토큰 파일이 보인다(Codex 하네스의 auth.json과 같은 수준). 보관 전 마스킹 대상.

## D-2 토큰 파일 부재 상태로 재개한 hydrogen-en-1 시도 중단 (2026-11-22 08:17)
- 재개 직후 실 HOME의 토큰 파일이 없어(새 토큰은 키체인 저장) 복사가 실패한 것을 보고 즉시 중단했다. 격리 agy는 키체인으로 consumer 인증은 됐으나, 시작 수 초 안에 종료돼 원자료는 `aborted-hydrogen-en-1-0817/`에 보관하고 무효 처리.
- 사용자가 08:20 재로그인(토큰 키체인 저장, 만료 09:20:59). 하네스 보완: 토큰 파일은 있을 때만 복사, run-all이 run 시작 전 `agy_auth_check`(격리 HOME `agy models` + authMethod=consumer)로 확인하고 실패 시 모델 호출 전에 전체 중단(`auth-stop`).
