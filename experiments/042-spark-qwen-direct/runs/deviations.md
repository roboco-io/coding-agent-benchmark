# EXP-042 이탈·중단 기록

## D-1. 실험 중단 (2026-10-10 15:41, 사용자 결정)

- 상태: 9 run 중 4 run 완료(전부 게이트 pass), coder-en-2는 iteration 2 종료(exit 1) 후 중단, 나머지 4 run 미실행.
- 결정: 사용자 지시로 Claude Code 경로(claude-direct)는 중단하고, 같은 모델 3종은 pi 하네스([EXP-044](../../044-pi-spark-qwen/README.md))로만 측정한다.
- 절차: run-all·driver·`claude -p`·앱 서버 프로세스 트리를 종료하고 orchestrator.log에 `ABORTED` 줄을 남겼다.

## 근본 원인: DashScope Anthropic 호환 엔드포인트의 usage 과소 보고

### 증상
- coder 조건(`qwen3-coder-next`)의 모든 iteration 실패가 같은 400 오류였다: `InternalError.Algo.InvalidParameter: Range of input length should be [1, 204800]`. coder-en-1은 iteration 1·2가 이 오류로 끝나고 iteration 3에서 완주했다. coder-en-2는 iteration 1·2가 같은 오류로 끝났다.
- 세 모델의 모든 세션에서 자동 압축(compact)이 0회였다.

### 증거 (세션 jsonl, 같은 날 분석)
- coder-en-1 세션 `da6d8224`: 대부분의 요청이 입력 약 2만 3천 토큰으로 기록되었고(출력 0, 캐시 필드 없음), 간헐적인 일부 요청만 12만 3천→20만 4천 토큰으로 기록되었다. 대화 본문 길이(문자 수/3.5 + 시스템 약 1만 9천)로 추정한 실제 컨텍스트는 11만 6천→20만 토큰으로 꾸준히 증가했다.
- 정상 완주한 조건도 같은 과소 보고가 있었다. flash-en-1: 마지막 기록 2만 1천 vs 추정 약 8만 6천. q27-en-1: 2만 2천 vs 약 11만 7천.

### 재현 (2026-10-10, curl/urllib 직접 호출)
| 요청 | 엔드포인트 | 모델 | 보고된 입력 토큰 |
|---|---|---|---|
| 단일 턴 5만 토큰 | Anthropic `/apps/anthropic` | coder, flash | `message_start` 약 50,004 / `message_delta` 약 50,012 (정확) |
| 다중 턴, tool_result 5만 토큰 | Anthropic | coder | `message_start` **37** / `message_delta` 50,323 |
| 다중 턴, tool_result 5만 토큰 | Anthropic | flash | `message_start` **37** / `message_delta` 50,362 (text 블록 형식은 186) |
| 다중 턴, tool 메시지 5만 토큰 | OpenAI 호환 `/compatible-mode/v1` | coder / flash | `prompt_tokens` 50,314 / 50,354 (정확) |

### 해석
- 확인된 사실: DashScope Anthropic 호환 엔드포인트는 `message_start`의 `input_tokens`에서 tool_result 본문을 빼고 보고한다. Claude Code 세션 기록의 대부분은 이 과소값을 담고 있다.
- 추론(Claude Code 내부 코드로 미확인): Claude Code는 이 과소값으로 컨텍스트가 작다고 판단해 자동 압축을 하지 않았다. 입력 한도가 204,800인 coder만 실제 컨텍스트가 한도에 닿아 400으로 iteration이 끝났다. flash·27b는 한도가 983,616이라 같은 결함이 오류로 드러나지 않았다.
- Claude Code 경로에서는 응답 usage를 고치는 프록시(변환 계층)가 필요하므로 리포 규칙상 해결할 수 없다. OpenAI 호환 엔드포인트는 정확하므로 pi 경로(EXP-044)는 영향이 없다.

### 영향
- EXP-042의 토큰 집계는 세 조건 모두 신뢰할 수 없다(미측정 처리).
- 같은 엔드포인트를 쓴 과거 실험(EXP-013·016·017, `qwen3.8-max`)의 토큰 수치도 같은 과소 보고의 영향을 받았을 수 있다. 재점검이 필요하다(미수행).
