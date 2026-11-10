# EXP-059 설계: Claude Code × Fable 5.2 네이티브 랄프 루프 완주 검증 (EN n=3)

## 배경

Anthropic이 2026-11-09에 `claude-fable-5-2`(Claude Fable 5.2)를 공개했다. 2026-11-10에 Models API(`GET /v1/models/claude-fable-5-2`)로 ID·입력 한도 1,000,000·최대 출력 128,000·adaptive thinking 전용임을 확인했다. 리포의 Fable 계열 기준선은 EXP-023 Fable 5.1(3/3 iter 1, 6–8분, PROMPT v1)이다. 이 실험은 `ralph-model-benchmark` 스킬의 `claude-native` 하네스로 Fable 5.2가 같은 과제를 무개입 완주하는지 확인한다.

## 가설

- [M-51](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Fable 5.2(`claude-fable-5-2`, thinking 기본값)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 20분·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 질문 유형: 완주 가능성. 실험 단계: 탐색 파일럿.
- 판정 기준(사전 등록): 검증(3/3 완주) / 부분 검증(1–2/3, run별 사실 보고) / 기각(0/3) / run 단위 보류(모델 외적 장애).
- 보조 지표: 세션 시간, iteration 수, output 토큰, API 호출 수, 커밋 수, API 환산 비용. EXP-023 Fable 5.1·EXP-026 Opus 5.5·EXP-031 Sonnet 5.5와 병치하되 PROMPT 버전(v1→v2)·Claude Code 버전·시점 차이가 교락하므로 방향성 기록만 한다.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| fable52 | `claude-fable-5-2`, thinking·effort 기본값 | Claude Code 2.1.321 (`claude -p`) | 구독 OAuth(`apiKeySource=none`), 비격리 `~/.claude` | `runs/` |

- PROMPT: 스킬 정본 v2 EN (md5 `3d11ae8d28546ac730d482d015cfd6d9`). 채점: 스킬 Hurl 13파일, `/opt/homebrew/bin/hurl` 절대 경로.
- 상한: run 20분(`MAX_SEC=1200`), 정체 300초, 30 iteration. 순차 3 run, 다른 실험과 동시 실행 금지.
- 비용: 구독 실행이라 하네스 비용 상한은 단가 0으로 실질 미적용(EXP-054와 같은 방식). API 환산 단가(입력 $8·출력 $40·캐시 읽기 $0.20·캐시 쓰기 1h $16, 2026-11-10 pricing 페이지)는 보고용으로만 쓴다.
- usage: 세션 jsonl `message.id` dedup(`scripts/aggregate_tokens.py`), 서브에이전트 jsonl 별도 집계. 토큰 대리지표이며 청구 비용이 아니다.

## 리스크·한계

- 비격리 조건이라 글로벌 CLAUDE.md·플러그인·MCP가 노출된다. 노출 상태는 `runs/phase0.md`에 기록한다.
- 조율 세션(이 대화)도 같은 구독 계정을 쓰므로 run 중 사용량 한도를 공유한다. 한도 도달은 run 단위 보류 사유로 기록한다.
- 로컬 `~/experiments/ralph-exp058`(solar-pro4 직결, 2026-10-28, 리포 미보관)이 058 번호를 쓰고 있어 이 실험은 059를 쓴다.
