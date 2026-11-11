# EXP-060 결과 보고: pi × Meta Muse Ember (OpenRouter) 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-11-11 (본 결과 13:48–13:57 KST, AC 전원, 순차 3 run). 같은 날 11:20–11:30에 배터리·저전력 모드로 먼저 실행한 3 run은 전원 영향 비교 기록으로 [runs/lowpower/](runs/lowpower/)에 보관했다. 2026-11-10 1차 smoke는 제공자 404로 실패해 기동하지 않았다.
- 가설: [M-52](../../hypotheses/catalog.md) — pi 0.87.1 × OpenRouter `meta/muse-ember`(Meta 고정, thinking high, pi 정본 지속 지침)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 20분·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 검증** — AC 전원 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, OpenRouter generation 114건 전부 제공자 Meta·served `meta/muse-ember-20261109`). 세션 1분 48초–3분 39초, 청구 run당 $0.028–0.056이다. 저전력 모드 3 run도 3/3 iteration 1 완주였다.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| openrouter/meta/muse-ember | 3/3 완주 = 검증 | AC 3/3 iter 1 완주 (저전력 3/3 iter 1) | 검증 |

## run별 결과 (AC 전원, 본 결과)

세션 시간은 세션 jsonl의 첫·마지막 기록 시각 차이다(채점 제외). 모델·도구 시간은 `analysis/latency/timeline.py`로 나눈 값이다. usage는 `usage_pi.py`(responseId dedup) 값이며 input은 캐시 제외 입력이다. 청구는 OpenRouter `GET /api/v1/generation`의 `total_cost`를 run의 모든 responseId에 대해 합한 값이다.

| run | 완주 | 세션 시간 | 모델 / 도구 시간 | 호출 | input | cache read | output (reasoning) | 최대 프롬프트 | 커밋 | 재검증 ×2 | 청구 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| museember-en-1 | iter 1/30 | 1분 48초 | 78초 / 30초 | 26 | 182.9K | 442.3K | 15.1K (4.2K) | 38.1K | 2 | 13/154 ×2 | $0.0276 |
| museember-en-2 | iter 1/30 | 2분 12초 | 105초 / 26초 | 37 | 242.4K | 840.4K | 18.4K (5.8K) | 44.7K | 2 | 13/154 ×2 | $0.0368 |
| museember-en-3 | iter 1/30 | 3분 39초 | 151초 / 68초 | 51 | 377.9K | 1,839.8K | 22.1K (6.6K) | 65.3K | 2 | 13/154 ×2 | $0.0562 |

도구는 bash 20–32회, write 7–16회, edit 0–5회, read 0–2회였다. 세 run 모두 Fastify + Prisma 스택을 골랐다. 세션 기록에서 하네스 파일이나 `lowpower/` 디렉터리를 참조한 호출은 없었다. `thinking_level_change`는 전부 `high`였다.

## 전원 조건 비교 (저전력 모드 vs AC)

사용자가 첫 실행이 배터리·저전력 모드였다고 알려 와서 AC 전원으로 같은 조건을 다시 실행했다. `pmset -g log`에서 첫 실행 시간대 앞뒤 기록은 배터리 사용(10:57 잔량 36%, 11:56 잔량 21%)이었다. pmset 로그에는 저전력 모드 상태가 남지 않으므로, 저전력 모드였다는 사실은 사용자 진술에 근거한다. 재실행 직전에는 `lowpowermode 0`·AC 전원을 확인했다([runs/power-check.txt](runs/power-check.txt)).

| 조건 | 세션 시간 (중앙값) | 모델 시간 | 도구 시간 | 호출당 모델 시간 | 호출 | output | 청구 |
|---|---|---|---|---|---|---|---|
| 저전력 (11:20–11:30) | 2분 52초–3분 19초 (3분 15초) | 110–138초 | 61–62초 | 3.5–3.9초 | 28–38 | 17.8–19.9K | $0.027–0.051 |
| AC (13:48–13:57) | 1분 48초–3분 39초 (2분 12초) | 78–151초 | 26–68초 | 2.9–3.0초 | 26–51 | 15.1–22.1K | $0.028–0.056 |

AC 조건은 도구 시간 중앙값이 62초에서 30초로 줄었고, 호출당 모델 시간도 3.5–3.9초에서 2.9–3.0초로 짧았다. 도구 시간 감소는 CPU 제한이 풀린 효과와 맞는 방향이다. 호출당 모델 시간 감소는 클라이언트 쪽 처리 속도 차이일 수도 있고 두 시간대의 제공자 부하 차이일 수도 있어 원인을 나누지 못했다. AC run 3은 호출이 51회로 많아 세션이 저전력 run보다 길었다. 따라서 run 사이 작업량 차이가 전원 효과만큼 크며, n=3씩이라 전원 효과의 크기는 확정하지 않는다. 완주 판정·토큰·청구는 전원 조건과 무관한 지표이며 두 조건 모두 3/3 iteration 1이었다. 대시보드와 비용·지연 CSV에는 AC 결과만 넣었다.

## 모델 유지·루프 기여

AC 조건 OpenRouter generation 114건(저전력 101건)이 모두 제공자 `Meta`, served model `meta/muse-ember-20261109`였다(조회 실패 0). 세 run 모두 첫 iteration에서 합격했으므로 루프의 복구 기여는 관측되지 않았다. 정체 종료(exit 124)·run 상한(125)·비용 상한(126)은 두 조건 모두 발생하지 않았다.

## 같은 하네스의 Muse Spark Open과 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 (중앙값) | output 범위 (중앙값) | 청구 범위 (중앙값) |
|---|---|---|---|
| Muse Ember (이번 AC, pi 0.87.1, PROMPT v2, 지속 지침 있음) | 1.8–3.7분 (2.2분) | 15.1–22.1K (18.4K) | $0.028–0.056 ($0.037) |
| Muse Spark Open (EXP-049, 2026-10-18, pi 0.87.1, PROMPT v1, 지속 지침 없음) | 5.2–6.7분 (6.2분) | 25.3–33.8K (25.9K) | $0.45–0.67 ($0.50) |

이번 3 run은 EXP-049보다 세션이 짧았고, 청구는 약 14분의 1이었다. 청구 차이는 대부분 단가 차이(입력 $1.25 → $0.10, 출력 $4.25 → $0.50)에서 온다. 세션 시간 차이에는 PROMPT 버전(v1 → v2), pi 지속 지침 유무, 실험 시점, 실행 머신의 전원 상태(EXP-049는 기록 없음)가 함께 섞여 있어 모델 차이로 단정하지 않는다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` jsonl 1개, usage 누락 0.
- 비용: OpenRouter API 키로 실행해 실제 과금이 있었다. 공개 단가(100만 토큰당 입력 $0.10, 출력 $0.50, 캐시 읽기 $0.004, 2026-11-10·11 endpoints API 확인)로 pi usage를 환산한 값이 generation `total_cost` 합과 run마다 소수 넷째 자리까지 같다. 월별 청구서와 대조한 것은 아니다. 두 조건 합계 청구는 $0.240이다(저전력 $0.119 + AC $0.121).
- 재현 자료: `runs/`의 `bench.env`, `model-specs.json`, `pi-models.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `power-check.txt`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage-pi.csv`, `openrouter-generations.csv`, 로그(gz), `sessions.tar.gz`. 저전력 조건의 같은 파일은 `runs/lowpower/`. 보관 전 `redact_keys.py` 마스킹 결과 0건.

## 한계와 교란 변수

- 과제 1개·n=3이다. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 리포의 이전 실험은 실행 머신의 전원 상태를 기록하지 않았다. 이번 비교에서 도구 시간이 전원 조건에 따라 달라질 수 있음을 관측했으므로, 이전 실험의 세션 시간에도 기록되지 않은 전원 차이가 섞여 있을 수 있다.
- 2026-11-10 1차 smoke에서 OpenRouter → Meta 경로가 404 `model_not_found`를 반환했고, 2026-11-11에는 정상이었다. 원인(제공자 일시 오류 또는 접근 롤아웃)은 확인하지 못했다.
- 2026-11-11 확인 시 OpenRouter에 Google Vertex 제공자가 추가되었으나 다운 상태였다. 하네스는 Meta로 고정해 이 경로를 쓰지 않았다.
- 외부 프로세스(DeepSRT)가 3003을 점유했다. driver가 run별 빈 포트를 주입했고 모든 run이 첫 채점에서 13/13이어서 거짓 음성은 발생하지 않았다.

## 결론 및 후속 실험

- 결론: Muse Ember는 pi 정본(지속 지침) 하네스에서 이 과제를 전원 조건과 무관하게 iteration 1에 완주했다(각 n=3). AC 조건 청구는 run당 6센트 이하였다.
- 후속: 하네스가 run 시작 시 전원 상태(`pmset -g batt`, `lowpowermode`)를 기록하도록 하면 이후 실험의 시간 비교에서 전원 교란을 배제할 수 있다. Muse Spark Open을 PROMPT v2·pi 정본 지침·AC 전원으로 재측정하면 세션 시간 차이 중 모델 몫을 분리할 수 있다.
