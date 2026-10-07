# EXP-038: pi coding agent × Haiku 5.5 완주 검증 (EN n=3)

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-08 (실행 전). `ralph-model-benchmark` 스킬 `pi` 하네스, EXP-032(pi × Sonnet 5.5)와 같은 절차.

## 가설

- [M-31](../../hypotheses/catalog.md) — pi coding agent(`pi -p` v0.87.1)로 `anthropic/claude-haiku-5-5`(Anthropic API 키 직결, thinking pi 기본값)를 돌리면, 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다 (EN n=3).
- 질문 유형: **완주 가능성**(탐색). 사후에 효율 우위 실험으로 해석을 바꾸지 않는다.
- 판정 기준: 완주는 드라이버 게이트 `pass` + 독립 재검증 2회 `13,154`. 3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**. 제공자·하네스 장애로 판정 불능인 run은 **보류**.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, 토큰 대리지표(`input + output + cacheWrite`), 공개 단가 환산 비용(청구액 아님, 프롬프트 100K 초과 요청의 장문맥 단가 포함). Claude Code × Haiku 5.5(EXP-037)와의 차이는 에이전트·시점이 함께 다른 조합 차이로만 서술한다. 두 실험 모두 Anthropic API 키로 실행된다(EXP-037은 이탈 D-1로 API 키 인증).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 전략 | 연결 |
|---|---|---|---|---|
| haiku55 | `anthropic/claude-haiku-5-5`, thinking pi 기본값 | pi 0.87.1 | 랄프 루프 | Anthropic API(Messages) 직결, `ANTHROPIC_API_KEY`(`~/.zsh_secrets`), pi 내장 anthropic provider |

- **사용자 정의 모델 항목(사전 등록)**: pi 0.87.1의 내장 모델 목록에 `claude-haiku-5-5`가 없다(2026-10-08 `pi --list-models` 확인). [`pi-models.json`](pi-models.json)으로 내장 anthropic provider에 모델을 추가했다. 구조(`thinkingLevelMap`·`compat: forceAdaptiveThinking, supportsStrictTools`·`promptCache`)는 EXP-032와 같이 pi 내장 `claude-sonnet-5` 정의를 복사했다. 모델 고유 값은 2026-10-08 Anthropic API로 확인했다.
  - `GET /v1/models/claude-haiku-5-5`: `max_input_tokens` 1,000,000, `max_tokens` 128,000, effort low–max 지원.
  - `max_tokens` 128,001 요청은 "maximum allowed … 128000" 오류. `thinking: {type: "adaptive"}` 요청은 정상 응답.
  - `cost`는 공식 가격 표의 100K 이하 단가(입력 $0.10·출력 $0.50·캐시 읽기 $0.01·5분 캐시 쓰기 $0.125). pi는 장문맥 단가를 모르므로 pi 세션의 자체 비용은 쓰지 않고 [analysis/cost](../../analysis/cost/README.md) 방식(`lc_*` 열)으로 따로 계산한다.
  - 따라서 이 조건은 "Haiku 5.5 전용으로 조정된 pi 설정"이 아니라 "Sonnet 5 계열 설정으로 Haiku 5.5 ID를 호출하는 조건"이다.
- Anthropic API 키로 과금된다(실제 청구액 미대조, 단가 환산만).
- 격리·지침 차단·포트: EXP-032와 같다(`PI_CODING_AGENT_DIR` 전용, `-nc -ns -ne -np -na`, `PI_OFFLINE=1`, 빈 포트 `PORT` 주입).
- 상한 30 iteration·run당 4시간, 순차 실행, 개입 금지. 프롬프트는 스킬 정본 EN(해시 검증).
