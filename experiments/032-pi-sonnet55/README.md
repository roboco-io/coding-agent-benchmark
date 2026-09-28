# EXP-032: pi coding agent × Sonnet 5.5 완주 검증 (EN n=3)

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-09-29 (실행 전). `ralph-model-benchmark` 스킬 `pi` 하네스, EXP-030과 같은 절차.

## 가설

- [M-25](../../hypotheses/catalog.md) — pi coding agent(`pi -p` v0.87.1)로 `anthropic/claude-sonnet-5-5`(Anthropic API 키 직결, thinking pi 기본값)를 돌리면, 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다 (EN n=3).
- 질문 유형: **완주 가능성**(탐색). 사후에 효율 우위 실험으로 해석을 바꾸지 않는다.
- 판정 기준: 완주는 드라이버 게이트 `pass` + 독립 재검증 2회 `13,154`. 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**. 제공자·하네스 장애로 판정 불능인 run은 **보류**.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, 토큰 대리지표(`input + output + cacheWrite`), 공개 단가 환산 비용(청구액 아님). 네이티브 Claude Code × Sonnet 5.5(EXP-031)와의 차이는 에이전트·API 경로·시점이 함께 다른 조합 차이로만 서술한다.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 전략 | 연결 |
|---|---|---|---|---|
| sonnet55 | `anthropic/claude-sonnet-5-5`, thinking pi 기본값 | pi 0.87.1 | 랄프 루프 | Anthropic API(Messages) 직결, `ANTHROPIC_API_KEY`(`~/.zsh_secrets`), pi 내장 anthropic provider |

- **사용자 정의 모델 항목(사전 등록)**: pi 0.87.1(2026-09-29 npm 최신)의 내장 모델 목록에 `claude-sonnet-5-5`가 없다. 그래서 [`pi-models.json`](pi-models.json)으로 내장 anthropic provider에 모델을 추가했다. 메타데이터(비용·컨텍스트 1M·maxTokens 128K·`thinkingLevelMap`·`compat: forceAdaptiveThinking, supportsStrictTools`·`promptCache`)는 pi 내장 `claude-sonnet-5` 정의를 그대로 복사하고 ID만 바꿨다. Sonnet 5.5 전용 compat(예: Opus 5.5의 mid-convo 옵션)은 확인할 근거가 없어 넣지 않았다. 따라서 pi가 Sonnet 5.5에 최적화된 설정을 쓰는 조건이 아니라 "직전 세대 Sonnet 설정으로 새 모델 ID를 호출하는 조건"이며, 결과 해석에 이 한계를 함께 적는다.
- Anthropic API 키로 과금된다(실제 청구액 미측정, 단가 환산만).
- 격리·지침 차단·포트: EXP-030과 같다(`PI_CODING_AGENT_DIR` 전용, `-nc -ns -ne -np -na`, `PI_OFFLINE=1`). EXP-031부터 하네스가 빈 포트를 `PORT`로 주입한다.
- 상한 30 iteration·run당 4시간, 순차 실행, 개입 금지. 프롬프트는 스킬 정본 EN(해시 검증).
