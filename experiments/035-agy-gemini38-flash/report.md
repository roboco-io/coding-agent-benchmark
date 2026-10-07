# EXP-035 결과 보고: Antigravity CLI × gemini-3.8-flash 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-07 (16:42–17:38 KST, 순차 3 run, 이어서 EXP-036 실행)
- 가설: [M-28](../../hypotheses/catalog.md) — Antigravity CLI(`agy -p`)로 `gemini-3.8-flash`(effort high, Gemini API 키)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4h 안에 완주할 수 있다 (EN n=3).
- 클라이언트: Antigravity CLI (agy) 1.3.1
- **판정: 검증** — 3/3 완주 (run 1·2 iteration 1, run 3 iteration 2 — 에이전트가 실행한 하네스 채점기가 agy를 종료시킨 D-1 때문). 게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 전 run `gemini_api_key` 인증·`gemini-3.8-flash-high` 해석 확인. 세션 15.5–22.4분.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| gemini-3.8-flash (effort high) | 3/3 완주 = 검증 | 3/3 완주 (iter 1, 1, 2) | 검증 |

## run별 결과

세션 시간은 로그의 첫 iteration start부터 마지막 iteration end까지다. 토큰은 agy transcript의 모델 응답 스텝 합계다(`usage_agy.py`). `input`은 캐시 읽기를 뺀 값이고 `output`은 thinking을 포함한다. 대리지표 = `input + output`(청구 비용 아님).

| run | 완주 iter | 세션 시간(분) | 커밋 | 모델 응답 스텝 | input | output (thinking) | cache_read | 대리지표 | 재검증 ×2 |
|---|---|---|---|---|---|---|---|---|---|
| flash38-en-1 | 1 | 17.5 | 4 | 119 | 601,789 | 63,420 (37,317) | 10,441,183 | 665,209 | 13/154 ×2 |
| flash38-en-2 | 1 | 15.5 | 4 | 121 | 607,788 | 57,039 (31,421) | 9,604,533 | 664,827 | 13/154 ×2 |
| flash38-en-3 | 2 | 22.4 | 6 | 192 | 965,502 | 50,454 (iter 2만 9,965) | 10,238,889 | 1,015,956 | 13/154 ×2 |

- run 3의 iteration 1(11.5분)은 driver 채점에서 이미 `13,154`였지만 완료 선언 전에 종료되었다. iteration 2(10.5분)가 처음부터 다시 확인하고 완료를 선언했다.

## 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 | output | 환산 비용(run당) |
|---|---|---|---|
| agy × gemini-3.8-flash (이번) | 15.5–22.4분 | 50.5–63.4K | $1.39–1.68 |
| pi × gemini-3.8-flash (EXP-036, 같은 날 직후) | 13.1–15.6분 | 29.7–47.1K | $0.80–1.14 |

- 같은 모델·같은 날이지만 하네스(시스템 프롬프트·도구 구성·내장 스킬)와 클라이언트 쪽 usage 정의가 달라 차이를 하네스 효과로 확정하지 않는다. run 3은 D-1로 iteration이 하나 늘어 시간·토큰이 커졌다.
- 이 리포의 다른 모델보다 세션이 길고 run당 모델 응답 스텝이 많다(119–192). 예: pi × gpt-6.1-sol(EXP-034) 29–34 응답, 8.3–9.2분.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript_full.jsonl`. 결과 JSON이 있는 대화 3개는 transcript 합계와 결과 JSON `usage`가 정확히 일치했다. `total_tokens = input + output`이 성립해 `input`이 캐시 읽기를 제외한 값임을 확인했다.
- 비용: Gemini API 키로 실행해 실제 과금이 있었으나 청구액은 확인하지 않았다. 2026-10-07에 확인한 공개 단가(입력 $0.75 / 캐시 입력 $0.075 / 출력 $3.75 per 1M, 2026-12-31까지)로 환산하면 run당 $1.39–1.68이다([analysis/cost/](../../analysis/cost/README.md), 청구액 아님). 2027-01-01부터 단가가 두 배다.

## 한계와 교란 변수

- 과제 1개·n=3. 3/3은 이 조건의 관측값이다.
- **하네스 노출**: run 디렉터리(`app-<run>`)가 하네스 디렉터리 안에 있어 에이전트가 채점기·이전 run 기록에 접근할 수 있다. run 3에서 실제로 채점기를 실행했다(D-1). 같은 구조는 이전 실험에도 있었고, EXP-029의 세션 3개에서도 하네스 파일 참조가 확인되었다(후속 조치 필요).
- agy 제품 내장 스킬 8종(`builtin/skills`)과 시스템 프롬프트는 끄지 않았다(Phase 0 기록).
- 실행 중 VS Code가 3000·3001을 점유했다. driver가 빈 포트를 `PORT`로 주입했고 거짓 음성 기각은 없었다.
- 이탈 상세: [runs/deviations.md](runs/deviations.md).

## 결론 및 후속 실험

- 결론: gemini-3.8-flash는 Antigravity CLI에서 이 과제를 3/3 완주했다. 하네스 개입이 없던 두 run은 iteration 1에 완주했다.
- 후속: 하네스 디렉터리와 run 디렉터리 분리(채점기·이전 run 기록 비노출) 후 재측정, effort low·medium 비교.
