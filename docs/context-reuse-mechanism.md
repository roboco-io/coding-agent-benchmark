# 단일 세션 컨텍스트 재활용의 메커니즘: 프롬프트 캐싱

> 2026-09-21 정정: 캐시는 가능한 설명 가설이다. 기존 실험만으로 비용 차이의 원인을 확정하지 않는다. 아래 제공자 정책 설명은 2026-07-22 조사 기록이며 현재 단가·정책은 재확인해야 한다.
> 조사: Perplexity 경유 Anthropic 공식 문서 (2026-07-22). 관련 실험: [EXP-001](../experiments/001-ralph-vs-plan-then-execute/report.md), [EXP-003](../experiments/003-pte-skills/report.md), [EXP-004](../experiments/004-ralph-skills/report.md)

## 1. 동작 원리 — prefix 기반 캐싱

- 캐시 대상은 **프롬프트 맨 앞에서부터의 연속 prefix**. prefix 내용의 해시가 키이며, 바이트 단위로 동일한 prefix가 다시 오면 모델이 재처리 없이 서버 측 상태를 로드한다.
- `cache_control` breakpoint는 요청당 최대 4개, breakpoint 앞 최대 20개 블록의 lookback으로 최장 일치 prefix를 찾는다. 최소 캐시 길이는 Sonnet/Opus 1,024토큰.
- usage 필드의 의미 (이 리포의 `aggregate_tokens.py`가 집계하는 값):
  - `cache_creation_input_tokens` — 이번 요청에서 **새로 캐시에 쓴** 토큰
  - `cache_read_input_tokens` — **캐시 히트로 읽어온** 토큰 (재처리 안 함)
  - `input_tokens` — 캐시 범위 밖의 새 입력만
- 출처: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## 2. 수명과 가격

| 항목 | 배율 (기본 input 대비) | Opus 기준 $/M |
|------|----------------------:|--------------:|
| input (비캐시) | 1.0 | $15 |
| cache write (5분 TTL) | 1.25 | $18.75 |
| cache write (1시간 TTL) | 2.0 | $30 |
| **cache read** | **0.1** | **$1.5** |
| output | 5.0 | $75 |

- 기본 TTL 5분, **히트할 때마다 무료로 리셋** — 에이전트가 5분 내 계속 턴을 이어가면 캐시는 사실상 세션 내내 유지된다.
- 5분 캐시는 히트 1회면 손익분기(1.25+0.1 < 2.0).
- 출처: https://platform.claude.com/docs/en/about-claude/pricing

## 3. 에이전트 루프에서 왜 "재활용"이 되나

- Claude Code는 시스템 프롬프트·도구 정의·CLAUDE.md 등 불변 내용을 **자동으로 캐싱**한다 (사용자 설정 불필요).
- 대화는 **append-only**로 누적된다 → 직전까지의 히스토리 전체가 안정된 prefix가 되어, 매 턴 "이전 전부 = cache read(0.1×), 이번 턴 새 입력·출력만 정가"로 과금된다. 턴이 쌓일수록 `cache_read`가 커지는 이유다.
- 출처: https://code.claude.com/docs/en/agent-sdk/agent-loop

**실측과의 연결**: 이전 메시지 수와 캐시 총계는 중복 집계였다. [정정 기록](2026-09-21-corrections.md)을 참조한다. 토큰 차이를 캐시 하나의 효과로 분리하지 못했다.

## 4. 캐시가 깨지는 조건 (실험 설계 시 통제 대상)

- 계층 구조 **tools → system → messages**: 상위가 바뀌면 그 이하 전부 무효화. 도구 정의 변경은 전체 캐시 무효화.
- 모델 변경 시 재사용 불가. thinking 설정·이미지 유무·`tool_choice` 변경은 messages 캐시 무효화.
- prefix에 타임스탬프 등 비결정적 내용이 섞이면 바이트 불일치로 미스.
- **새 세션이 비싼 정확한 이유**: 캐시는 세션이 아니라 prefix 내용에 키잉되므로, 시스템 프롬프트·도구가 같으면 새 세션도 그 공통 부분(약 20K, 우리가 "기동세"로 측정한 값)은 TTL 내 재사용될 수 있다. 그러나 **대화 히스토리·읽은 파일은 세션마다 다르므로** 그 부분은 매번 cache write(1.25×)로 재구축된다 — EXP-001 원인 1·2의 기전.
- 참고: 캐시는 동일 조직/workspace 내에서 공유되므로 병렬 세션이 같은 prefix를 히트할 수는 있으나, cold 상태의 동시 요청은 둘 다 미스할 수 있다(원자성 미보장, 공식 문서화 약함).

## 5. 토큰 대리지표와 비용의 구분

`token_proxy = input + output + cache_creation`은 캐시 읽기를 제외한 진단 지표이며 청구 비용이 아니다. 기존 $23.8 / $161.9 / $92.2 및 6.8배 비용 비교는 중복 usage에 기반하므로 철회한다. 실제 인증·단가·캐시 정책과 누락 호출을 검증하지 않아 새 달러 값을 제시하지 않는다.

EXP-003의 대리지표 감소는 39.3%가 아니라 22.45%이며 사전 30% 기준 미달이다. 단일 세션 최적·스킬은 멀티 세션에서만 유효·캐시가 원인이라는 일반화를 철회한다.

## 6. 후속 검증

같은 과제·품질·예산 아래 세션 정책과 캐시 조건을 기록하고, 실패와 복구까지 포함해 비교한다. 캐시 누적과 세션 길이의 관계는 진단 가설이며 과금 우위의 직접 증거가 아니다.
