# EXP-057: pi × gpt-6.1-terra + 지속 실행 지침 (비정본 스택)

> 사후 주기 (2026-10-28, 실행 후): 사용자 결정으로 이 지침이 pi 정본이 되었다. 아래 설계는 실행 전 기록이다. [보고서](report.md)의 "정본 편입" 참조.

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-28 (실행 전).

## 배경과 질문

[EXP-055](../055-pi-gpt61-terra/README.md)(PROMPT v2)와 [EXP-056](../056-pi-gpt61-terra-v1/README.md)(PROMPT v1, run 1 도중 중단)에서 pi × gpt-6.1-terra는 iteration마다 기능 묶음 하나를 구현·커밋한 뒤 `stopReason: stop`으로 스스로 종료해, 완주까지 5–7 iteration이 걸렸다. 같은 모델이 Codex CLI(EXP-054)에서는 3/3 iteration 1에 완주했다. Codex 기본 지침(세션 기록 `base_instructions`, 약 21K자)에는 "Autonomy and persistence" 절("persist until the user's intended goal is complete" 등)이 있고, pi 0.87.1 기본 시스템 프롬프트(`dist/core/system-prompt.js`)에는 이에 해당하는 지침이 없다. 사용자 지시(2026-10-28): pi에서도 단일 iteration에 완료하도록 지시하는 방법을 찾아 재실험한다.

- 가설 코드·문장: [M-50](../../hypotheses/catalog.md) — pi 시스템 프롬프트에 지속 실행 지침(`persistence.md`)을 덧붙이면 pi × gpt-6.1-terra가 iteration 1에 완주한다.
- 주 지표: run별 게이트 pass iteration. 보조 지표: 완주 수, 세션 시간, iteration별 `stopReason`, 토큰 대리지표.

## 조건 (EXP-055 대비 변경 1개)

EXP-055와 같다(pi 0.87.1 `-nc -ns -ne -np -na`, `openai-codex/gpt-6.1-terra` 사용자 정의 항목 contextWindow 272,000, thinking medium, ChatGPT 구독 OAuth, PROMPT v2 정본, 30 iteration·20분·정체 300초, EN n=3). **변경**: `PI_APPEND_SYSTEM_PROMPT`로 [`persistence.md`](persistence.md)(113단어)를 `--append-system-prompt`에 넘긴다. 문구는 Codex 기본 지침의 Autonomy and persistence 절 요지를 옮기고, 비대화형 실행임을 알리며, 일부 완료·진행 보고로 턴을 끝내지 말라는 문장을 더했다. 과제 정보(API·테스트·기능 목록)는 넣지 않았다.

**비정본 스택**: 에이전트 노출 지침이 정본 조건과 다르므로, 결과는 기존 pi 결과와 직접 비교하지 않고 대시보드·README에서 "pi + 지속 지침"으로 별도 표기한다.

## 판정 기준 (실행 전 고정)

- 3/3 run이 iteration 1에 게이트 pass → M-50 **검증**.
- 1–2/3 → **부분 검증**, 0/3 → **반증**.
- 완주 여부(게이트 pass + 재검증 2회 13/154)는 별도로 기록한다. 인증·가용성 장애 run은 보류 후 새 run 번호로 재실행.

## 계측

usage는 토큰 대리지표이며 청구 비용이 아니다(구독 OAuth). 세션 기록에서 응답 model·thinking·stopReason을 전수 확인하고, 시스템 프롬프트에 지침이 실제로 들어갔는지 Phase 0에서 확인한다.
