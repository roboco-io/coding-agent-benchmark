# EXP-051 결과 보고: pi × Kimi K3.1 Pro·Pro Highspeed 완주 검증 (EN n=3)

- 실험일: 2026-10-25 (13:00–13:41 KST, 단일 오케스트레이터 순차 6 run, 조건 교차)
- 가설: [M-44](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 Moonshot OpenAI 호환 엔드포인트의 `kimi-k3.1-pro`·`kimi-k3.1-pro-highspeed`(사용자 정의 models.json 항목, thinking high)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (조건별 EN n=3, 완주율 판정·과금 배제).
- 클라이언트: pi 0.87.1
- **판정: 검증** — 두 조건 모두 3/3, 6 run 전부 iteration 1에서 완주했다. 게이트 통과와 독립 재검증 2회가 모두 13/13·154/154로 일치했고 개입은 없었다. 세션 시간은 pro 7.3–10.2분, highspeed 3.7–5.2분이며, 공개 단가 환산 비용은 run당 pro $0.45–0.60, highspeed $0.57–0.98이다.

> `ralph-model-benchmark` 스킬 `pi` 하네스를 적용했다. 설계는 [README.md](README.md)에 실행 전 고정했다. 같은 하네스·같은 pi 버전·같은 thinking 수준(high)으로 kimi-k3를 측정한 결과는 EXP-029다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값·불확실성 | 충족 여부 | 판정 범위 |
|---|---|---|---|
| 게이트 통과 + 재검증 2회 13/13·154/154 | k31pro 3/3, k31hs 3/3, 모두 iter 1 | 충족 | 검증 (조건별 3/3) |
| 무개입 | 사람 개입 0, 정체·상한 종료 0 | 충족 | — |
| 비용 상한 run당 $3·실험 $15 | 비용 가드 추정 최대 $1.24(k31hs-en-1), 환산 합계 $3.82 | 상한 미도달 | — |
| 응답 모델·thinking 유지 | 세션 assistant `model` 전수 요청 ID와 일치, `thinking_level_change` 전수 `high` | 충족 | — |

## run별 결과

| run | 예산 내 합격 | 채점(게이트 / 재검증×2) | 세션 시간 | 커밋 | output | reasoning | 입력 / 캐시 읽기 / 캐시 쓰기 | API 호출 | 최대 프롬프트 | 환산 비용 |
|---|---|---|---|---|---|---|---|---|---|---|
| k31pro-en-1 | iter 1 | 13/154 · 13/154 ×2 | 10분 11초 | 5 | 19.3K | 3.9K | 6.2K / 1.49M / 47.1K | 51 | 48.4K | $0.597 |
| k31pro-en-2 | iter 1 | 13/154 · 13/154 ×2 | 7분 17초 | 4 | 16.5K | 3.3K | 4.3K / 0.98M / 45.3K | 36 | 45.4K | $0.461 |
| k31pro-en-3 | iter 1 | 13/154 · 13/154 ×2 | 9분 5초 | 2 | 16.6K | 3.7K | 3.8K / 0.92M / 46.6K | 32 | 47.9K | $0.452 |
| k31hs-en-1 | iter 1 | 13/154 · 13/154 ×2 | 5분 13초 | 2 | 21.1K | 5.2K | 4.9K / 1.38M / 66.3K | 40 | 66.5K | $0.982 |
| k31hs-en-2 | iter 1 | 13/154 · 13/154 ×2 | 3분 44초 | 3 | 12.3K | 1.8K | 5.1K / 0.84M / 33.0K | 43 | 33.1K | $0.568 |
| k31hs-en-3 | iter 1 | 13/154 · 13/154 ×2 | 4분 16초 | 5 | 20.6K | 6.3K | 3.2K / 0.81M / 44.0K | 30 | 44.2K | $0.763 |

- 세션 시간은 pi 세션 기록의 첫·마지막 타임스탬프 차이(iteration 1)다. 게이트 채점 시간은 포함하지 않는다.
- 커밋 수는 산출 리포의 전체 커밋 수다.
- output은 reasoning을 포함한다(pi usage 기준).
- 환산 비용은 공개 단가(100만 토큰당 pro 입력 $2·출력 $10, highspeed 입력 $4·출력 $20, 캐시 읽기 둘 다 $0.20, 2026-10-25 확인)로 계산한 토큰 대리지표이며 청구액이 아니다. Moonshot이 기록한 `cacheWrite`는 TTL 구분이 없어 EXP-029와 같이 5분 쓰기 단가(입력 단가와 같음)로 계산했다.
- 비용 가드 추정(pro $0.54–0.68, highspeed $0.61–1.24)은 환산 비용보다 크다. 가드는 제공자 usage와 대화 기록 바이트 하한 중 큰 값을 쓰는 보수적 추정이기 때문이다.
- 산출물: 6 run 모두 TypeScript + Fastify + Prisma를 썼고, `src/server.ts`에서 하네스가 주입한 `PORT`를 읽었다.

## 조건 간·같은 계열 측정과의 병치 (우위 판정 없음)

| 조건 | 실험·시점 | 클라이언트 | 세션 시간 | output | 환산 비용 |
|---|---|---|---|---|---|
| pi × kimi-k3.1-pro | EXP-051, 2026-10-25 | pi 0.87.1 | 10.2 / 7.3 / 9.1분 | 19.3 / 16.5 / 16.6K | $0.597 / $0.461 / $0.452 |
| pi × kimi-k3.1-pro-highspeed | EXP-051, 2026-10-25 | pi 0.87.1 | 5.2 / 3.7 / 4.3분 | 21.1 / 12.3 / 20.6K | $0.982 / $0.568 / $0.763 |
| pi × kimi-k3 | EXP-029, 2026-09-24 | pi 0.87.1 | 9.5 / 9.9 / 9.9분 | 17.4 / 18.7 / 18.7K | $0.572 / $0.657 / $0.653 |

두 K3.1 조건은 같은 시점에 교차 순서로 실행했으므로 실행 시점 차이는 작다. 그래도 highspeed의 세션 시간(3.7–5.2분)이 pro(7.3–10.2분)보다 모든 run에서 짧았다는 관측은 n=3의 방향성 기록이며, 제공자가 밝힌 "2–3배 속도"를 이 과제에서 검증한 것으로 서술하지 않는다. output과 API 호출 수는 두 조건의 범위가 겹친다. 환산 비용은 highspeed가 단가가 2배라 run당 더 높았다.

EXP-029 kimi-k3와는 pi 버전과 thinking 수준(high)이 같고, 다른 것은 모델과 실행 시점(약 4주 차이)이다. pro의 세션 시간·output·환산 비용은 EXP-029 kimi-k3와 범위가 겹친다. EXP-029의 표는 [EXP-029 보고서](../029-pi-openweight/report.md)와 [cost_all_runs.csv](../../analysis/cost/cost_all_runs.csv) 값이다.

## 모델 유지·노출 설정

- 응답 모델: pi 세션 assistant 메시지의 `model`이 k31pro 3 run은 전수 `kimi-k3.1-pro`, k31hs 3 run은 전수 `kimi-k3.1-pro-highspeed`다.
- 모델 정의: pi 0.87.1 내장 카탈로그에 K3.1이 없어서 내장 `kimi-k3` 정의(api `openai-completions`, thinkingFormat `openai`, `requiresReasoningContentOnAssistantMessages`)를 복제하고 id·이름·단가만 바꾼 [pi-models.json](pi-models.json)을 썼다. highspeed의 최대 출력은 제공자 문서에 별도 값이 없어 pro와 같은 131,072로 두었다(미확인). 이번 run의 최대 output은 한도보다 훨씬 작아 영향은 없었다.
- 노출: pi `-nc -ns -ne -np -na`로 상위 지침·스킬·확장을 노출하지 않았다. 에이전트 환경의 키는 `MOONSHOT_API_KEY`만 남겼다. 세션 기록에서 하네스 경로(`measure.sh`·`driver.sh`·`metrics`·다른 run)를 참조한 건수는 0이다.

## 이탈·특이 사항

- 설계 문서는 실행 순서를 "k31pro 3 run → k31hs 3 run"으로 적었으나, run-all은 조건을 교차해 실행했다(k31pro-en-1 → k31hs-en-1 → …). 기동 직후 문서를 실제 순서로 고쳤다. 판정 기준과 조건은 바뀌지 않았다.
- 그 밖의 이탈은 없다. smoke는 첫 시도에 두 조건 모두 PASS했다.

## usage·집계 검증

- `usage_pi.py`(responseId dedup)로 집계했다. usage 누락 0이다. 결과는 [runs/usage-pi.csv](runs/usage-pi.csv)다.
- 키 점검: `KIMI_API_KEY` 값이 세션·실행 로그·산출 리포에 나타난 건수 0(직접 대조). 보관본은 `redact_keys.py` 마스킹 0건이며 커밋 시 `check_staged_keys.py`가 검사한다.
- 원자료: [runs/](runs/) — metrics, `recheck.csv`, 로그(gzip), `sessions.tar.gz`, `phase0.md`, `model-specs.json`, `preflight-report.md`.

## 한계와 교란 변수

- 표본은 조건별 3 run, 과제는 1종(RealWorld 백엔드 신규 구현)이다. 3/3 완주는 관측 범위의 사실이며 일반적 성공률을 확정하지 않는다.
- 세션 시간에는 실행 시점의 제공자 응답 속도가 섞여 있다. EXP-029와의 차이에는 모델 외에 약 4주의 시점 차이가 들어 있다.
- 사용자 정의 모델 항목은 내장 kimi-k3 정의를 가정으로 쓴 것이다. 제공자가 K3.1에 다른 호환 설정을 요구하더라도 이번 6 run에서 오류는 관측되지 않았다.
- 환산 비용은 청구액과 대조하지 않았다.
