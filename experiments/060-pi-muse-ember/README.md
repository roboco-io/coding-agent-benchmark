# EXP-060 설계: pi × Meta Muse Ember (OpenRouter) 랄프 루프 완주 검증 (EN n=3)

## 배경

Meta의 `meta/muse-ember`가 2026-11-10 03:07 KST에 OpenRouter에 등록되었다. 같은 날 OpenRouter endpoints API로 제공자가 Meta 한 곳이고, 입력 한도 1,048,576·최대 출력 943,718이며, tools·reasoning을 지원함을 확인했다. 단가는 100만 토큰당 입력 $0.10·출력 $0.50·캐시 읽기 $0.004·캐시 쓰기 $0.125다. Muse 계열 기준선은 EXP-049 pi × Muse Spark Open(3/3 iter 1, 5.2–6.7분, $0.45–0.67, 지속 지침 없는 pi)이다. Anthropic 호환 엔드포인트가 없으므로 pi 하네스(OpenAI 호환 직결)를 쓴다.

## 가설

- [M-52](../../hypotheses/catalog.md) — pi 0.87.1 × OpenRouter `meta/muse-ember`(Meta 고정, thinking high, pi 정본 지속 지침 포함)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 20분·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 질문 유형: 완주 가능성. 실험 단계: 탐색 파일럿.
- 판정 기준(사전 등록): 검증(3/3 완주) / 부분 검증(1–2/3) / 기각(0/3) / run 단위 보류(모델 외적 장애).
- 보조 지표: 세션 시간, iteration 수, output 토큰, 호출 수, 커밋 수, 청구 비용(OpenRouter generation API 대조). EXP-049 Muse Spark Open과 병치하되 pi 지속 지침 유무·PROMPT v1→v2·시점이 교락하므로 방향성 기록만 한다.

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| museember | `openrouter/meta/muse-ember`, thinking high | pi 0.87.1 (`-nc -ns -ne -np -na`, `PI_PERSISTENCE=on`) | OpenRouter API 키, `openRouterRouting only=[meta]`·fallback 금지, 사용자 정의 `runs/pi-models.json` | `runs/` |

- PROMPT: 스킬 정본 v2 EN (md5 `3d11ae8d28546ac730d482d015cfd6d9`). 채점: 스킬 Hurl 13파일, `/opt/homebrew/bin/hurl`.
- 상한: run 20분, 정체 300초, 30 iteration, 순차 3 run. 비용 상한 run당 $1·실험 $3(preflight 추정 p50 $0.24·p90 $0.86/run).
- usage: `usage_pi.py`(responseId dedup). 청구액은 OpenRouter `GET /api/v1/generation?id=`로 provider·model·total_cost를 전수 대조한다.

## 리스크·한계

- 등록 당일 모델이라 제공자 쪽 안정성(오류·지연)이 확인되지 않았다. 같은 API 오류가 반복되면 조사 전에 먼저 중단한다.
- OpenRouter 키는 `PI_KEEP_ENV`로만 노출한다. 보관 전 `redact_keys.py`로 마스킹한다(EXP-049 D-1).
