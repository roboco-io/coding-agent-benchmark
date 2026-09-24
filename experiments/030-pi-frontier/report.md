# EXP-030 결과 보고: pi coding agent × Opus 5.5·gpt-6-sol 랄프 루프 완주 검증 (EN 각 n=3)

- 실험일: 2026-09-24 (17:47–18:14 KST, 단일 오케스트레이터 순차 6 run, 조건 교차 순서)
- 가설: [M-23](../../hypotheses/catalog.md) — pi coding agent(`pi -p` v0.87.1)로 `anthropic/claude-opus-5-5`(Anthropic API 키 직결)·`openai-codex/gpt-6-sol`(ChatGPT OAuth)을 돌리면(thinking pi 기본값) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iter·4h 안에 완주할 수 있다 (EN 각 n=3, 완주율 판정·과금 배제).
- **판정: 검증** — 두 조건 모두 3/3 완주, 6 run 전부 iteration 1 (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 응답 model 필드 전수 일치). 세션 시간은 Opus 5.5 3.1–4.9분, gpt-6-sol 4.2–5.6분이며, 각 모델의 네이티브 에이전트 기준선(EXP-026 Opus 5.5 4.0–8.4분, EXP-027 gpt-6-sol 4.8–5.2분)과 범위가 겹친다. 관측값이며 우열 확정이 아니다.

> EXP-029(오픈웨이트 계열)에 이어 pi 하네스를 두 번째로 적용한 실험이다. 이번에는 제조사 네이티브 에이전트(Claude Code·Codex)의 기준 모델을 pi로 돌렸다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값·불확실성 | 충족 여부 | 판정 범위 |
|------------------|----------------|-----------|----------|
| 조건별 3/3 예산 내(30 iter·4h) 게이트 + 재검증 2회 일치 완주 → 검증 | opus 3/3(iter 1·1·1), sol 3/3(iter 1·1·1). 조건당 n=3이라 완주율 구간은 넓다(3/3 관측, 95% 신뢰구간 하한 약 0.29) | 충족 | 완주 가능성 |
| run 단위 보류 조건(제공자 장애 연속 3회 즉시 실패) | 해당 없음. 스트림 오류·중단 0건 | — | — |

## run별 결과

| run | 완주 iter | 세션 시간(분) | 커밋 | 응답 수 | output | cacheRead | cacheWrite | 대리지표 | 공개 단가 환산 |
|-----|----------|--------------|-----|--------|--------|-----------|-----------|---------|--------------|
| opus-en-1 | 1 | 3.9 | 3 | 24 | 18,990 | 657,772 | 46,364 | 65,404 | $0.74 |
| opus-en-2 | 1 | 3.1 | 2 | 17 | 16,594 | 700,575 | 68,466 | 85,096 | $0.81 |
| opus-en-3 | 1 | 4.9 | 4 | 27 | 19,824 | 885,567 | 58,789 | 78,669 | $0.87 |
| sol-en-1 | 1 | 4.2 | 2 | 32 | 6,961 | 452,352 | 0 | 58,334 | $0.26 |
| sol-en-2 | 1 | 5.6 | 2 | 35 | 7,599 | 525,312 | 0 | 67,101 | $0.30 |
| sol-en-3 | 1 | 4.4 | 2 | 31 | 8,587 | 501,376 | 0 | 50,808 | $0.27 |

- 세션 시간: driver 로그의 run start부터 마지막 iteration end까지(`runs/durations.csv`).
- 대리지표 = `input + output + cacheWrite`(토큰 대리지표, 청구 비용 아님). 원자료 `runs/usage-pi.csv`.
- 공개 단가 환산은 [analysis/cost](../../analysis/cost/README.md)의 `prices.json` 단가(1M 토큰당 Opus 5.5 입력 $4·캐시 읽기 $0.2·5분 캐시 쓰기 $5·출력 $20, gpt-6-sol 입력 $2·캐시 읽기 $0.2·출력 $10)로 계산했다. pi가 세션에 기록한 자체 환산값(opus $0.74–0.87, sol $0.26–0.30)과 소수 둘째 자리까지 같다. **opus는 Anthropic API 키로 실제 과금됐으나 청구액은 확인하지 않았다. sol은 ChatGPT 구독 OAuth로 실행해 run별 실제 지출이 없으며, 이 값은 API 단가로 환산한 추정치다.**

## 조건별 비교 (네이티브 에이전트 기준선 대조)

| 조합 | 완주 | 세션 시간 범위(중앙값) | output 범위 | 공개 단가 환산 중앙값 |
|------|------|--------------------|------------|-------------------|
| pi × Opus 5.5 (이번) | 3/3, iter 1 | 3.1–4.9분 (3.9) | 16.6–19.8K | $0.81 |
| Claude Code × Opus 5.5 (EXP-026 EN, 2026-09-23) | 3/3, iter 1 | 4.0–8.4분 (4.2) | 18.6–28.2K | $1.25 |
| pi × gpt-6-sol (이번) | 3/3, iter 1 | 4.2–5.6분 (4.4) | 7.0–8.6K | $0.27 |
| Codex × gpt-6-sol (EXP-027, 2026-09-24 오전) | 3/3, iter 1 | 4.8–5.2분 (4.9) | 10.4–11.0K | $0.43 |

- 두 비교 모두 **에이전트와 API 경로가 함께 다르다.** pi는 시스템 프롬프트·도구 정의(read·bash·edit·write)·thinking 설정 방식이 Claude Code·Codex와 다르고, 요청 형식과 캐시 지시도 다르다. 따라서 아래 차이는 조합 전체의 차이이며 pi의 효과로 단정하지 않는다. 기준선은 동시기 재측정이 아니다(EXP-026은 하루 전, EXP-027은 같은 날 오전).
- 세션 시간: 두 모델 모두 기준선과 범위가 겹친다. 겹침은 동등성의 증명이 아니다.
- output: pi 조합이 두 모델 모두 기준선 범위의 아래쪽에 있다(opus 16.6–19.8K vs 18.6–28.2K로 부분 겹침, sol 7.0–8.6K vs 10.4–11.0K로 비겹침). thinking 설정이 같다고 확인하지 못했으므로(아래) 원인을 분리하지 않았다.
- 환산 비용: pi 조합이 두 모델 모두 낮게 나왔다. opus는 캐시 쓰기 TTL 차이가 일부 기여한다. EXP-026 네이티브 run의 캐시 쓰기는 전부 1시간 TTL(1M당 $8)로 기록됐고, pi는 기본 5분 TTL($5)로 기록됐다(`cacheWrite1h` 0). 캐시 읽기도 pi opus 0.66–0.89M으로 EXP-026 EN(1.29–2.61M)보다 적었다. sol은 캐시 쓰기 과금이 없어 비캐시 입력·캐시 읽기·output 차이만 반영된다.

## thinking 설정 (관측)

- pi 기본값으로 실행했고 세션 `thinking_level_change`는 두 조건 모두 전 run `medium`이었다.
- opus: pi 0.87.1은 이 모델을 adaptive thinking으로 호출하고 effort를 대화 중 지시로 전달하며, assistant 메시지의 `providerThinkingLevel`이 전 응답 `medium`으로 기록됐다. Claude Code 네이티브(EXP-026)의 effort 기본값은 기록하지 않아 같은지 확인하지 못했다.
- sol: pi가 `medium`을 reasoning effort `medium`으로 매핑한다(pi 모델 정의의 `thinkingLevelMap`). EXP-027 Codex는 `model_reasoning_effort=medium`을 명시했다. 명목 설정은 같으나 요청 구성 전체가 같다는 뜻은 아니다.

## usage·집계 검증

- 집계기: `usage_pi.py`(EXP-029 작성, 변경 없음). assistant 메시지는 `responseId`로 중복 제거하며 같은 ID에 다른 usage면 오류로 중단한다. 전 run 중복 0건·usage 누락 0건·`type:"usage"` 엔트리 0건.
- 필드 의미 확인(Phase 0 + 전 응답 검산): 두 제공자 모두 `totalTokens = input + output + cacheRead + cacheWrite`가 전 응답에서 성립했고 `reasoning ≤ output`이었다(위반 0건). anthropic의 `reasoning`은 응답의 `thinking_tokens`이며 output에 포함된다. anthropic `cacheWrite1h`는 pi 타입 정의상 `cacheWrite`의 부분집합이며 이번 실험에서 전부 0이었다. openai-codex는 `cacheWrite`를 0으로 기록했다.
- 응답 모델: 전 assistant 메시지의 `provider/model`이 조건과 일치(opus 68건, sol 98건), 대체 모델 응답(`responseModel`) 기록 0건.

## 관측과 설명

- 관측: Opus 5.5는 pi의 네 도구 중 `bash`만 썼다(run당 17–27회, 파일 작성도 셸 heredoc). gpt-6-sol은 bash 17–23회에 write·edit·read를 함께 썼다.
- 관측: 두 조건 모두 세션 안에서 PATH의 `hurl`이 npm `@hurl/cli`라는 점을 다뤘다(세션 jsonl에 `@hurl/cli` 또는 Homebrew 경로 언급). 판정은 하네스 채점기(절대 경로)로 했으므로 영향은 없다.
- 관측: 채점 포트 충돌 징후(`EADDRINUSE`, 서버 대기 시간 초과 등)는 6 run 로그 모두에 없었다. 기동 전 3000번대 외부 LISTEN은 3003(DeepSRT)뿐이었다.
- 설명 가설(미검증): pi 조합의 output이 적은 것은 pi의 짧은 시스템 프롬프트와 작은 도구 집합 때문일 수 있다. 에이전트만 바꾼 동시기 교차 실험을 하지 않아 확인하지 않았다.

## 한계와 교란 변수

- 조건당 n=3, 과제 1개(신규 백엔드 구현), EN 프롬프트만. 다른 과제 유형·KO 조건으로 일반화하지 않는다.
- 네이티브 기준선과는 에이전트·API 경로·시점이 함께 다르다. 차이는 조합 전체의 차이로만 읽는다.
- opus 조건의 실제 청구액은 미측정이다. sol 조건은 구독 OAuth라 실제 지출이 없고, 구독 한도 소진량도 계측하지 않았다.
- 격리 디렉터리에 복사한 `auth.json`에는 openai-codex OAuth 외에 deepseek API 키 항목도 들어 있다(이번 조건에서는 쓰이지 않음). OAuth 토큰은 실행 중 만료되지 않았다(기동 시 만료까지 약 240시간).
- 이탈 없음. 재검증 중 measure.sh가 서버 프로세스를 정리하며 출력한 `Killed: 9` 메시지는 정상 정리 절차다.

## 정정 이력

- 없음.

## 결론 및 후속 실험

- pi는 오픈웨이트 계열(EXP-029)에 이어 Opus 5.5(Anthropic API)·gpt-6-sol(ChatGPT OAuth)에서도 같은 절차로 완주하는 하네스로 관측됐다(각 3/3, n=3 관측값).
- 후속 1: 에이전트 효과를 분리하려면 같은 시점에 같은 모델을 네이티브 에이전트와 pi로 교차 실행하고 thinking/effort 설정을 명시적으로 맞춰야 한다.
- 후속 2: Opus 5.5 pi 조건은 캐시 TTL(5분)이 네이티브(1시간)와 달라 환산 비용 비교가 TTL 정책에 좌우된다. `PI_CACHE_RETENTION=long` 조건을 추가하면 TTL을 맞춘 비교가 가능하다.
