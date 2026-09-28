# EXP-031: Claude Code × Sonnet 5.5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3)

> `ralph-model-benchmark` 스킬로 설계·실행. 조건은 EXP-028(Sonnet 5)·EXP-026(Opus 5.5)과 동일하게 맞추고 모델 ID만 바꾼다.

## 배경

사용자 요청(2026-09-29): Sonnet 5.5 벤치마크. 모델 ID는 `claude-sonnet-5-5`(Claude Code 시스템 안내의 공식 ID)이며, Anthropic API 키가 없어 모델 목록 API 대신 Claude Code 스모크 응답의 `modelUsage` 필드가 같은 ID로 기록되는지로 유효성을 확인한다(`runs/phase0.md`).

## 가설

- [M-24](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Sonnet 5.5(`claude-sonnet-5-5`, thinking 기본값)는 EN·KO 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration·4h 안에 무개입 완주할 수 있다 (EN·KO 각 n=3).
- 질문 유형: 완주 가능성(탐색). 효율 우위 실험으로 사후 전환하지 않는다.
- 판정 기준(언어별): 검증 3/3 / 부분 검증 1–2/3 / 반증 0/3. 모델 외적 장애 run은 run 단위 보류, 재실행은 새 run 번호.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, usage(토큰 대리지표), 응답 모델 필드. Sonnet 5(EXP-028) 대비 차이는 시점·CLI 버전 교락이 있으므로 조합 전체의 관측 차이로만 서술한다.

## 조건·환경

| 조건 | 모델 | 실행 도구 | 전략 | 연결 |
|---|---|---|---|---|
| sonnet55 × EN/KO | `claude-sonnet-5-5`, thinking 기본값 | Claude Code 2.1.284 `claude -p --dangerously-skip-permissions` | 랄프 루프(iteration마다 새 세션) | Anthropic 네이티브(구독 인증) |

- 프롬프트: 스킬 `assets/` 정본(EN/KO), setup.sh 해시 검증. 채점: Hurl 13파일·154요청, `/opt/homebrew/bin/hurl`, measure v4.
- 격리: claude-native는 EXP-023/026/028과 같이 **비격리**(사용자 기본 설정). 노출 항목은 `runs/phase0.md`에 기록.
- 순서: sonnet55-en-1 → sonnet55-ko-1 → … (반복 번호 단위 교차), 순차 실행. 상한 10 iteration·run당 4h, 개입 금지.
- usage: run별 세션 jsonl을 `scripts/aggregate_tokens.py`(message.id dedup, 서브에이전트 jsonl 포함)로 집계. 비용은 공개 단가 환산 추정치로만 표기.
- **포트 주입(이번 실험부터, 실행 전 확정)**: 실행 머신의 `:3000`·`:3001`(VS Code 확장 호스트)·`:3003`(DeepSRT)이 점유되어 있어, 하네스가 고정 3000 대신 빈 포트를 `PORT` 환경변수로 주입한다. driver는 run 단위로 에이전트 세션에, measure는 채점 기동마다 별도 빈 포트를 준다(40000–49999). PROMPT는 정본 그대로이며, 앱이 `PORT`를 따르는지는 에이전트 구현에 달려 있다(채점기는 기존대로 리포 소속 LISTEN 포트를 자동 탐지). 기존 실험(PORT 미주입)과의 차이는 하네스 환경 변수 1개이며 판정 기준에는 영향이 없다. 사전 검증: EXP-028 완주 앱을 새 measure로 채점해 `13,154` 확인(포트 45174).
