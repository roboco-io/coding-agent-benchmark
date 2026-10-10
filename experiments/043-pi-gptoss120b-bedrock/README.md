# EXP-043: pi × gpt-oss-120b (Amazon Bedrock) 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료 — 기각(20분 상한 0/3)** (2026-10-10 설계 고정·실행). 결과: [report.md](report.md). 후보 선정 근거: [로컬 실행 가능 오픈 웨이트 모델 조사](../../docs/2026-10-10-local-runnable-open-weight-models.md).

## 가설

- 가설 코드·문장: [M-36](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DGX Spark 1대(128GB)에 올릴 수 있는 오픈 웨이트 `gpt-oss-120b`(Amazon Bedrock `amazon-bedrock/openai.gpt-oss-120b-1:0`, us-west-2, thinking pi 기본값, Bedrock API 키)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분(2026-10-10 변경, 원래 4시간) 안에 완주할 수 있다 — EN n=3, 완주율 판정·과금 배제.
- 질문 유형: **완주 가능성**(스모크). 사후에 효율 비교로 바꾸지 않는다.
- 실무 선택 질문: DGX Spark 등급 공개 가중치 모델 가운데 OpenAI 계열이 이 과제를 무개입으로 끝낼 수 있는가. 클라우드 API 실행이므로 로컬 서빙 속도·양자화 품질은 측정하지 않는다(Bedrock 서빙 정밀도는 공개 정보로 확인하지 않음).
- 주 지표와 판정: 예산 내 게이트 + 독립 재검증 2회 일치 완주 수. **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3, **run 단위 보류**는 모델 외적 장애(Bedrock 5xx·스로틀 지속, 하네스 결함).
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, usage, 응답 모델 필드, thinking 수준(세션 jsonl).

## 연결 경로 선택 근거

- gpt-oss-120b는 Anthropic 호환 엔드포인트가 없어 pi로 실행한다(2026-10-10 사용자 지시).
- OpenAI API(`api.openai.com`)는 이 모델을 제공하지 않는다(2026-10-10 모델 목록 139개에 없음, 호출 시 "does not exist").
- Hugging Face Inference Providers는 계정 크레딧 부족으로 호출 불가. 사용자 지시로 Amazon Bedrock을 사용한다.
- Bedrock은 pi 내장 `amazon-bedrock` 제공자(Converse 스트림 API)로 직접 호출하며 변환 계층이 없다. 사전 확인: us-east-1·us-west-2 Converse 호출에서 도구 호출(`stopReason: tool_use`) 정상.

## 인증·격리

- 인증: 전용 IAM 사용자 `ralph-bench-bedrock`(관리형 정책 `AmazonBedrockLimitedAccess`)의 Bedrock 장기 API 키를 `AWS_BEARER_TOKEN_BEDROCK`으로 주입한다(2026-10-10 발급, 30일 만료). 실험 종료 후 키와 사용자를 삭제한다.
- 관리자 자격증명 차단: 에이전트 환경에 `AWS_CONFIG_FILE=/dev/null`, `AWS_SHARED_CREDENTIALS_FILE=/dev/null`을 지정하고 `AWS_PROFILE`·IAM 키 환경변수를 두지 않는다. 따라서 pi와 에이전트의 bash 모두 `~/.aws`의 관리자 자격증명을 쓸 수 없다. 스모크 통과가 Bearer 키 경로의 증거다.
- pi 격리: 스킬 하네스(`PI_CODING_AGENT_DIR` 전용, `-nc -ns -ne -np -na`, `PI_OFFLINE=1`, `PI_KEEP_ENV`로 필요한 비밀값만 노출).

## 과제·조건·예산

- 과제·정본·채점기·완료 기준: [EXP-042](../042-spark-qwen-direct/README.md)와 같다(스킬 `assets/` EN 정본 md5 `2c28ea6b7f16125d9b3105f5ee00b126`, Hurl 13파일, `/opt/homebrew/bin/hurl` 8.0.1).
- 조건: `oss` = `amazon-bedrock/openai.gpt-oss-120b-1:0`, AWS_REGION us-west-2, thinking pi 기본값.
- 반복: 3 run 순차. 상한 30 iteration·20분(`MAX_SEC=1200`), 정체 300초(`STALL_SEC`). 원래 4시간·900초였으나 2026-10-10 사용자 지시로 두 번에 걸쳐 줄였다 — [runs/deviations.md](runs/deviations.md) D-1. 비용 상한: 3 run 환산 $10 초과 시 중단 검토(사후 집계).
- 사람 개입 없음. 제외·재실행 규칙은 EXP-042와 같다.

## 계측

- usage: `python3 ~/experiments/ralph-exp043/usage_pi.py ~/experiments/ralph-exp043 <run>...`(responseId dedup). 토큰 대리지표이며 청구 비용 아님. 환산 단가는 Bedrock 공개 단가를 보고 시점에 확인한다.

## Phase 0 기록

- [ ] pi 스모크(`~/.aws` 차단 상태에서 PASS), 응답 모델 필드
- [ ] 정본 해시, 채점기 정상/오류 사례
- [ ] 클라이언트 버전, 노출 지침·스킬·MCP
- 증거: [runs/phase0.md](runs/phase0.md)
