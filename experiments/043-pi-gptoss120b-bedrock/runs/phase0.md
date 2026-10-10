# EXP-043 Phase 0 (2026-10-10)

## 환경
- 클라이언트: pi 0.87.1 (`/Users/dohyunjung/.asdf/installs/nodejs/24.14.0/bin/pi --version`), 변환 계층 없음(pi 내장 `amazon-bedrock` Converse 스트림)
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1, Node v24.14.0, macOS Darwin 25.6.0
- 리전 us-west-2. 인증 `AWS_BEARER_TOKEN_BEDROCK`(IAM 사용자 `ralph-bench-bedrock`, `AmazonBedrockLimitedAccess`, 30일 만료, 값 미기록)
- `AWS_CONFIG_FILE=/dev/null`, `AWS_SHARED_CREDENTIALS_FILE=/dev/null`, `AWS_PROFILE`·IAM 키 env 미설정 → `~/.aws` 관리자 자격증명 차단

## 스모크 (smoke.sh, 11:39)
- `amazon-bedrock/openai.gpt-oss-120b-1:0` → PASS (`SMOKE-OK`). `~/.aws` 차단 상태라 Bearer 키 경로로 호출됨.
- 응답 모델 필드는 smoke 로그에 남지 않음 → 본 실행 세션 jsonl에서 `usage_pi.py`로 전수 확인 예정.
- 이탈(하네스 설정): setup 직후 `PI_BIN`이 asdf shim, 이어 `npm prefix -g`(/opt/homebrew) 경로로 잘못 잡혀 첫 스모크 FAIL. EXP-038과 같은 실제 경로로 고친 뒤 PASS. 모델 원인 아님.
- 사전 직접 호출: Converse API us-east-1·us-west-2 도구 호출 `stopReason: tool_use` 정상, Bearer 키(ServiceCredentialSecret) 200.

## 정본·채점기
- PROMPT-en.md md5 `2c28ea6b7f16125d9b3105f5ee00b126`. 채점기 정상/오류 사례는 EXP-042 Phase 0(같은 날, 같은 measure.sh·hurl)과 같음: 정상 `13,154`, 빈 디렉터리 `0,0`.

## 노출
- pi 격리 플래그 `-nc -ns -ne -np -na`, `PI_CODING_AGENT_DIR` 전용, `PI_OFFLINE=1`. 비밀값은 `AWS_BEARER_TOKEN_BEDROCK`만 노출.
- 포트: 3000·3001(VS Code 확장), 3003(DeepSRT) 외부 LISTEN, 종료하지 않음(빈 포트 주입 규칙).
