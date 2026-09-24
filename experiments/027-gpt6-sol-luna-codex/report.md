# EXP-027 결과 보고: Codex CLI × gpt-6-sol·gpt-6-luna 랄프 루프 완주 검증 (각 n=3)

- 실험일: 2026-09-24 (08:47–09:36 KST, 순차 6 run, sol·luna 교차)
- 가설: [M-20](../../hypotheses/catalog.md) — Codex CLI(`codex exec`) 하네스에서 gpt-6-sol·gpt-6-luna(effort medium)는 각각 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iter·4h 안에 완주할 수 있다 (각 n=3).
- **판정: 검증** — sol 3/3·luna 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 모델 필드 전수 일치). 채점 인프라 결함 1건(D-1)은 에이전트 개입 없이 처리했고 판정에 영향 없음.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| gpt-6-sol | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |
| gpt-6-luna | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 로그의 iteration 1 start–end(`codex exec` 실행 구간, 채점 제외)이다. usage는 rollout 세션 누계이며 input은 캐시 포함, reasoning은 output에 포함된다.

| run | 완주 | 세션 시간 | input(누계) | cache read | output (reasoning) | 커밋 | 재검증 ×2 |
|---|---|---|---|---|---|---|---|
| sol-en-1 | iter 1/30 | 5분 12초 | 1,460.2K | 1,412.4K | 10.8K (1.8K) | 3 | 13/154 ×2 |
| sol-en-2 | iter 1/30 | 4분 55초 | 1,068.0K | 1,007.6K | 11.0K (1.7K) | 3 | 13/154 ×2 |
| sol-en-3 | iter 1/30 | 4분 45초 | 1,080.3K | 1,035.5K | 10.4K (2.2K) | 3 | 13/154 ×2 |
| luna-en-1 | iter 1/30 | 9분 58초 | 4,018.5K | 3,903.7K | 21.5K (4.7K) | 8 | 13/154 ×2 |
| luna-en-2 | iter 1/30 | 6분 38초 | 1,532.7K | 1,455.1K | 14.1K (2.7K) | 5 | 13/154 ×2 |
| luna-en-3 | iter 1/30 | 5분 22초 | 1,116.3K | 1,059.3K | 13.4K (3.0K) | 4 | 13/154 ×2 |

## 모델 유지·루프 기여

- 요청 모델과 rollout의 `model` 필드가 6 run 전부 일치(sol run은 `gpt-6-sol`만, luna run은 `gpt-6-luna`만 기록). fallback 없음.
- 6 run 모두 첫 iteration에서 합격. 루프의 복구 기여는 이번 조건에서 관측되지 않았다.
- 인증은 ChatGPT 플랜 OAuth. 한도 도달·미실행 run 없음.

## 조건별 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 | output 범위 | input 누계 범위 | 캐시 히트 |
|---|---|---|---|---|
| gpt-6-sol (이번) | 4분 45초–5분 12초 | 10.4–11.0K | 1.07–1.46M | 94–97% |
| gpt-6-luna (이번) | 5분 22초–9분 58초 | 13.4–21.5K | 1.12–4.02M | 95–97% |
| gpt-6-astra (EXP-021, 2026-09-10) | 7분 06초–7분 36초 | 12.2–12.6K | 0.77–0.93M | 88–94% |

- sol은 3 run 모두 약 5분·커밋 3회로 산포가 작았다. luna는 run 1이 가장 길었고(약 10분, 커밋 8회, input 누계 4.0M) run 2·3은 sol과 가까운 범위였다.
- astra와의 차이는 날짜(09-10 vs 09-24)와 Codex CLI 버전(0.153.4 vs 0.155.1)이 함께 다르므로 모델 차이로 단정하지 않는다.
- Codex 설명상 luna는 "fast and affordable" 모델이지만, 이 과제에서는 세션 시간이 sol보다 짧은 run이 없었다(n=3 관측).

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` rollout 1개(= iteration 1회). 누락 0.
- 집계: `usage_codex.py` — 각 rollout의 마지막 `total_token_usage`(세션 누계)를 run 내 합산. EXP-021 astra 3 run의 기록값과 같은 값을 재현함을 확인했다. `aggregate_tokens.py`는 Codex 누계를 거부하므로 쓰지 않았다.
- 비용: ChatGPT 플랜 인증이라 청구 비용은 미측정. 공개 API 단가 환산 추정치(OpenAI pricing 페이지, 2026-09-24 확인, 단문맥 Standard, 캐시 쓰기 미기록으로 제외)는 sol run당 $0.40–0.49, luna run당 $0.02–0.06이다 (`analysis/cost/`). 실제 청구액이 아니다.
- 재현 자료: `bench.env`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `recheck.csv`, `sessions.csv`, `usage.csv`, 로그(gz), `deviations.md`.

## 한계와 교란 변수

- 과제 1개·조건당 3 run. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 전용 CODEX_HOME으로 사용자 지침·스킬·MCP는 노출되지 않았다. OpenAI 서버 측 캐시는 통제할 수 없다.
- **D-1 이탈**: sol-en-2 채점 후 measure.sh가 서버 watcher 트리를 정리하지 못해 driver가 약 10.8분 대기했다. 잔존 프로세스를 수동 종료했고(채점 인프라 한정 개입), luna-en-2부터 수정한 measure.sh(프로세스 트리 종료)를 적용했다. 채점 로직은 바뀌지 않았고 수정본으로 6 run 모두 재검증했다. 상세는 [deviations.md](runs/deviations.md).
- 사용자가 요청한 `gpt-6-earth`는 존재하지 않는 ID였다(Phase 0, 400 거부). astra는 재측정하지 않았다.

## 결론 및 후속 실험

- 결론: GPT-6 계열 3개 모델(astra·sol·luna) 모두 Codex CLI effort medium 하네스에서 이 과제를 iteration 1에 완주했다(각 n=3, astra는 EXP-021).
- 후속: 동시기 astra 재측정을 포함한 3모델 교차 비교, effort 축(low/high), KO 정본 조건.
- 동기화: catalog M-20, ROADMAP, 4개 README(`update_readme_results.py`), 대시보드 반영.
