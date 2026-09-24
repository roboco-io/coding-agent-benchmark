# EXP-028: Claude Code × Sonnet 5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3)

> `ralph-model-benchmark` 스킬로 설계·실행. 조건은 EXP-026(Opus 5.5)과 동일하게 맞추고 모델 ID만 바꾼다.

## 배경

사용자 요청(2026-09-24): Claude Sonnet 최신 버전 벤치마크. 최신 Sonnet은 Sonnet 5(`claude-sonnet-5`)이다. Anthropic API 키가 없어 모델 목록 API는 조회하지 못했고, Claude Code 스모크에서 `claude-sonnet-5` 요청이 응답 `modelUsage`에 같은 ID로 기록되는 것으로 유효성을 확인했다(`runs/phase0.md`).

## 가설

- [M-21](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Sonnet 5(`claude-sonnet-5`, thinking 기본값)는 EN·KO 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration·4h 안에 무개입 완주할 수 있다 (EN·KO 각 n=3).
- 질문 유형: 완주 가능성(탐색). 효율 우위 실험으로 사후 전환하지 않는다.
- 판정 기준(언어별): 검증 3/3 / 부분 검증 1–2/3 / 반증 0/3. 모델 외적 장애 run은 run 단위 보류, 재실행은 새 run 번호.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, usage(토큰 대리지표), 응답 모델 필드.

## 조건·환경

| 조건 | 모델 | 실행 도구 | 전략 | 연결 |
|---|---|---|---|---|
| sonnet5 × EN/KO | `claude-sonnet-5`, thinking 기본값 | Claude Code 2.1.281 `claude -p --dangerously-skip-permissions` | 랄프 루프(iteration마다 새 세션) | Anthropic 네이티브(구독 인증) |

- 프롬프트: EN md5 `2c28ea6b7f16125d9b3105f5ee00b126`, KO md5 `fa75275f335b1552ad1baedb630c522a`. 채점: Hurl 13파일·154요청, `/opt/homebrew/bin/hurl` 8.0.1, measure v4(EXP-027 D-1 수정본).
- 격리: claude-native는 EXP-023/026과 같이 **비격리**(사용자 기본 설정). 글로벌 CLAUDE.md·스킬·MCP가 노출되며 EXP-026과 같은 조건이다.
- 순서: sonnet5-en-1 → sonnet5-ko-1 → … (반복 번호 단위 교차), 순차 실행. 상한 10 iteration·run당 4h, 개입 금지.
- usage: run별 세션 jsonl을 `scripts/aggregate_tokens.py`(message.id dedup)로 집계. 비용은 공개 단가 환산 추정치로만 표기.
