# EXP-038 이탈 기록

## D-1. 에이전트의 프로세스 목록 조회로 다른 프로세스의 비밀값이 세션 기록에 남음 (run 1)

- **사실**: run 1 iteration 1의 마지막 검증 단계에서 에이전트가 남은 서버 프로세스를 확인하려고 `pgrep -fl "server"`를 실행했다. 이 명령은 실험과 무관한 실행 머신의 프로세스 명령줄 27줄을 출력했고, 그 가운데 다음이 있었다(세션 jsonl 99번째 줄).
  - 사용자의 다른 Claude Code 세션이 띄운 `exa-mcp-server` 프로세스 줄에 `KIMI_API_KEY`·`DATA_GO_KR_SERVICE_KEY` 대입 문자열. `KIMI_API_KEY` 값은 현재 `~/.zsh_secrets` 값과 달랐다(이전 값으로 보임, 유효성 미확인).
  - Google Drive 앱(crashpad) 실행 인자에 들어 있는 앱 내장 `AIza…` 형식 키 20개.
- **영향**:
  - 이 출력은 도구 결과로 모델 요청에 포함됐으므로 Anthropic API로 전송됐다.
  - 완주 판정과 채점에는 영향이 없다. 하네스 디렉터리나 다른 run 기록에 대한 접근은 없었다(3 run 세션 기록 전수 확인).
- **조치**:
  - 보관본(`sessions.tar.gz`)은 `redact_keys.py`(값 기반, 2건) 후 패턴 기반 마스킹(`sk-…` 2건, `AIza…` 20건)을 추가로 적용했고, pre-commit 키 검사를 통과했다. `redact_keys.py`는 `~/.zsh_secrets`의 현재 값만 찾으므로 이전 값은 놓친다.
  - 로컬 원본(`~/experiments/ralph-exp038/sessions-*`)에는 값이 남아 있다.
  - 노출된 `KIMI_API_KEY`가 아직 유효하면 회전이 필요하다(사용자 판단).
- **구조적 원인**: pi 하네스는 에이전트 환경의 비밀값을 제거하지만(EXP-036 D-3 조치), 같은 머신의 다른 프로세스 명령줄·환경은 `ps`·`pgrep`으로 볼 수 있다. 프로세스 격리(별도 사용자·컨테이너)는 하지 않는다.
