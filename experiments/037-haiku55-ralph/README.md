# EXP-037: Claude Code × Haiku 5.5 네이티브 랄프 루프 완주 검증 (EN n=3)

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. `ralph-model-benchmark` 스킬로 설계·실행. 설계 확정: 2026-10-08 (실행 전).

## 배경

사용자 요청(2026-10-08): Haiku 5.5 출시에 따른 벤치마크. 모델 ID는 `claude-haiku-5-5`(Claude Code 시스템 안내의 공식 ID)다. Anthropic API 키로 모델 목록을 조회하지 않고, EXP-031과 같이 Claude Code 스모크 응답의 `modelUsage` 필드가 같은 ID로 기록되는지로 유효성을 확인한다(`runs/phase0.md`).

## 가설

- [M-30](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Haiku 5.5(`claude-haiku-5-5`, thinking 기본값)는 EN 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4h 안에 무개입 완주할 수 있다 (EN n=3).
- 질문 유형: 완주 가능성(탐색). 효율 우위 실험으로 사후 전환하지 않는다.
- 판정 기준: 검증 3/3 / 부분 검증 1–2/3 / 반증 0/3. 모델 외적 장애 run은 run 단위 보류, 재실행은 새 run 번호.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, usage(토큰 대리지표), 응답 모델 필드. Sonnet 5.5(EXP-031)·Opus 5.5(EXP-026) 대비 차이는 시점·CLI 버전 교락이 있으므로 조합 전체의 관측 차이로만 서술한다.

## 조건·환경

| 조건 | 모델 | 실행 도구 | 전략 | 연결 |
|---|---|---|---|---|
| haiku55 × EN | `claude-haiku-5-5`, thinking 기본값 | Claude Code (Phase 0에서 버전 기록) `claude -p --dangerously-skip-permissions` | 랄프 루프(iteration마다 새 세션) | Anthropic 네이티브(구독 인증) |

- 언어: EN만(2026-10-03 사용자 지시 기본값). KO는 실행하지 않는다.
- 프롬프트: 스킬 `assets/` 정본(EN), setup.sh 해시 검증. 채점: Hurl 13파일·154요청, `/opt/homebrew/bin/hurl`, measure v4, 빈 포트 `PORT` 주입(EXP-031부터).
- 격리: claude-native는 EXP-023/026/028/031과 같이 **비격리**(사용자 기본 설정). 노출 항목은 `runs/phase0.md`에 기록.
- 순차 실행, 상한 30 iteration·run당 4h, 개입 금지. 다른 실험과 동시 실행하지 않는다.
- usage: run별 세션 jsonl을 `scripts/aggregate_tokens.py`(message.id dedup, 서브에이전트 jsonl 포함)로 집계. 비용은 공개 단가 환산 추정치로만 표기.
