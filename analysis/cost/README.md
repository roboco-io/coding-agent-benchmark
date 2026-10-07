# run당 비용 환산 (공개 단가 기준 추정)

작성일: 2026-09-23. 갱신: 2026-09-24(EXP-027 gpt-6-sol·gpt-6-luna, EXP-028 Sonnet 5, EXP-029 pi 하네스 3조건, EXP-030 pi × Opus 5.5·gpt-6-sol 추가), 2026-09-29(EXP-031 Sonnet 5.5, EXP-032 pi × Sonnet 5.5 추가), 2026-10-07(EXP-035 agy × gemini-3.8-flash, EXP-036 pi × gemini-3.8-flash 추가), 2026-10-08(EXP-037 Haiku 5.5 추가). 대시보드(<https://roboco.io/coding-agent-benchmark/>)의 "run당 환산 비용" 열의 근거 자료다.

## 이 수치가 뜻하는 것

각 run이 사용한 토큰을 네 항목(비캐시 입력·캐시 읽기·캐시 쓰기·출력)으로 나누고, 항목마다 2026-09-23(gpt-6-sol·gpt-6-luna는 2026-09-24, Sonnet 5.5는 2026-09-29, gpt-6.1-sol은 2026-10-03, gemini-3.8-flash는 2026-10-07, Haiku 5.5는 2026-10-08)에 확인한 공개 API 단가를 곱해 더한 값이다. **실제로 지출한 금액이 아니다.** 네이티브 Claude run은 구독(OAuth), pi × Opus 5.5(EXP-030)·pi × Sonnet 5.5(EXP-032)는 Anthropic API 키(실제 과금, 청구액 미확인), gpt-5.6-sol·gpt-6-astra·gpt-6-sol·gpt-6-luna·gpt-6.1-sol(pi × gpt-6-sol·pi × gpt-6.1-sol 포함)는 ChatGPT 플랜 OAuth로 실행했고, Solar 두 모델은 무료·프로모션 프리뷰 기간에 실행했다. gemini-3.8-flash(EXP-035/036)는 Gemini API 키로 실행해 실제 과금이 있었으나 청구액은 확인하지 않았다. 따라서 이 값은 "같은 사용량을 지금 공개 API 단가로 과금하면 얼마인가"에 대한 추정이다. 실험 품질 규칙([docs/experiment-quality-rules.md](../../docs/experiment-quality-rules.md) 4절)에 따라 구독 지출과 API 단가 환산을 구분하고, 단가 출처와 확인 시점을 남긴다.

## 결과 (run당 추정 비용 중앙값, USD)

| 모델 | EN | KO | 단가 적용 조건 |
|------|----|----|----------------|
| gpt-6-luna | 0.03 | — | 단문맥 단가 |
| pi × DeepSeek V4.1-Flash | 0.06 | — | 피크 단가(상한), pi 하네스 |
| DeepSeek V4.1-Flash | 0.09 | 0.12 | 피크 단가(상한) |
| Haiku 5.5 | 0.09 | — | 프롬프트 100K 초과 요청은 5배 단가, API 키 실행(캐시 5분 TTL, 실제 과금) |
| DeepSeek V4-Pro | 0.52 | 0.48 | 피크 단가(상한) |
| pi × gpt-6-sol | 0.27 | — | 단문맥 단가, pi 하네스(구독 OAuth, 실제 지출 없음) |
| pi × Sonnet 5.5 | 0.30 | — | pi 하네스, 캐시 쓰기 5분 TTL, 캐시 쓰기 단가는 미확인 가정(아래) |
| pi × gpt-6.1-sol | 0.30 | — | 단문맥 단가(캐시 입력 $0.10), pi 하네스(구독 OAuth, 실제 지출 없음) |
| gpt-6.1-sol | 0.36 | — | 단문맥 단가(캐시 입력 $0.10) |
| gpt-6-sol | 0.43 | — | 단문맥 단가 |
| pi × gemini-3.8-flash | 1.11 | — | 2026년 단가(2027-01-01부터 2배), pi 하네스 |
| agy × gemini-3.8-flash | 1.47 | — | 2026년 단가(2027-01-01부터 2배), Antigravity CLI 하네스 |
| pi × kimi-k3 | 0.65 | — | pi 하네스, 캐시 쓰기는 입력 단가 |
| Sonnet 5.5 | 0.68 | 0.70 | Sonnet 5와 같은 단가($2/$10), 캐시 쓰기 단가는 미확인 가정(아래) |
| kimi-k3 | 0.78 | 0.92 | |
| gpt-5.6-sol | 1.05 | 1.16 | 프로모션 단가 |
| pi × qwen3.8-max | 0.75 | — | 싱가포르 리전, pi 하네스 |
| qwen3.8-max | 1.11 | 1.56 | 싱가포르 리전 |
| pi × Opus 5.5 | 0.81 | — | pi 하네스, 캐시 쓰기 5분 TTL |
| Opus 5.5 | 1.25 | 1.21 | |
| gpt-6-astra | 2.02 | — | 단문맥 단가 |
| Sonnet 5 | 3.07 | 3.51 | 2026-09 표준가($2/$10) |
| Opus 4.8 | 3.24 | 2.86 | |
| Fable 5.1 | 3.51 | — | |
| Opus 5 | 5.76 | 4.35 | |
| Solar Pro 4 | 7.97 | — | 정가(실험 당시는 프리뷰·프로모션) |
| Solar Open 2 | 환산 불가 | — | 공개 단가 없음 |

run별 값은 [cost_all_runs.csv](cost_all_runs.csv)의 `est_cost_usd` 열에 있다. 모든 조건이 n=3(Opus 5 EN은 n=6, Solar Open 2는 n=1)이며, 과제 1종의 반복이므로 비용 우위를 일반화하지 않는다.

관측된 경향: 토큰 대부분이 캐시 읽기이므로 비용은 출력량보다 단가 구조에 크게 좌우된다. 예를 들어 Fable 5.1은 output이 Opus 4.8 수준이지만 단가가 두 배라 run당 비용이 비슷하거나 높고, Opus 5.5는 output이 적고 캐시 읽기 단가(입력의 0.05배)가 낮아 Opus 5의 약 1/5이다. 반대로 Sonnet 5는 입력·출력 단가가 Opus 5.5의 절반이지만 캐시 읽기 단가가 같고, run당 캐시 읽기(7.2–14.3M)와 output(57.6–73.7K)이 훨씬 많아 Opus 5.5의 약 2.5배다. Sonnet 5.5(EXP-031)는 단가가 Sonnet 5와 같지만 run당 캐시 읽기(1.06–1.62M)와 output(15.2–20.9K)이 Sonnet 5의 약 1/7·1/4이라 Sonnet 5의 약 1/5이다. 이 차이는 모델 외에 실험 시점·Claude Code 버전·포트 주입 유무가 다른 조건 사이의 관측값이다.

## 적용 단가와 가정

단가 원본과 출처 URL은 [prices.json](prices.json)에 있다. 판단이 들어간 가정은 다음과 같다.

- **Claude 캐시 쓰기**: 원자료가 남은 네이티브 run(EXP-009/010/023/026)은 캐시 쓰기가 전부 1시간 TTL로 기록됐다. TTL 구분이 없는 EXP-019 KO 6 run(원자료 삭제, 보고서 값만 존재)도 같은 하네스이므로 1시간 단가를 가정했다.
- **DeepSeek**: 피크 단가를 적용했다. 오프피크는 절반이므로 상한값이다. 캐시 쓰기는 별도 과금이 없고 제공자도 0으로 계상한다.
- **qwen3.8-max**: 싱가포르 리전 단가다. Claude Code가 캐시 지시(`cache_control`)를 보내 캐시 생성이 계상되므로 명시 캐시 생성 단가($2.50)를 적용했고, 캐시 읽기는 암묵 캐시 단가($0.25)로 보수적으로 잡았다(명시 캐시 읽기는 $0.17). 공식 문서 페이지 간 캐시 단가가 서로 달라 콘솔 확인이 필요하다.
- **gpt-5.6-sol**: 2026-11-21까지의 프로모션 단가다. 정가는 공개되지 않았다. reasoning 토큰은 출력에 포함돼 있고(rollout 기록 기준) 출력 단가로 계산했으나, 과금 방식은 문서로 확인하지 못했다. rollout에는 캐시 쓰기 필드가 없어 캐시 쓰기 비용을 넣지 않았다.
- **gpt-6-astra**: 단문맥 단가다. 장문맥 단가가 시작되는 기준이 공개되지 않았다.
- **gpt-6-sol·gpt-6-luna**: 2026-09-24에 OpenAI 가격 페이지(<https://developers.openai.com/api/docs/pricing>)의 Standard 단문맥 단가를 확인해 적용했다(1M 토큰당 sol 입력 $2.00·캐시 읽기 $0.20·출력 $10.00, luna 입력 $0.10·캐시 읽기 $0.01·출력 $0.50). astra와 같이 장문맥 기준은 공개되지 않았고, rollout에 캐시 쓰기 필드가 없어 캐시 쓰기 비용은 넣지 않았다.
- **pi 하네스(EXP-029)**: pi 세션 기록의 `input`(비캐시)·`cacheRead`·`cacheWrite`·`output`(reasoning 포함)을 같은 네 항목에 대응시켰고 모델별 단가는 Claude Code 직결 run과 같다. Moonshot은 pi에서 `cacheWrite`를 기록했는데 TTL 구분이 없어 `cache_write_5m` 열에 넣었다(kimi-k3의 5m 단가 $3 = 입력 단가). DashScope·DeepSeek는 `cacheWrite`가 0이다. pi가 세션에 남긴 자체 환산 비용(kimi $0.47–0.54 등)은 pi 내장 단가표 기준이라 이 표와 다르다. qwen-en-1은 채점 포트 교란(D-1)으로 늘어난 iteration 2–5를 포함한다.
- **pi × Opus 5.5·gpt-6-sol(EXP-030)**: 대응 방식은 EXP-029와 같다. pi의 anthropic provider는 기본 캐시 보존이 short(5분 TTL)이며 `cacheWrite1h`가 전 응답 0이어서 캐시 쓰기를 `cache_write_5m`($5)에 넣었다. 네이티브 Claude Code run(EXP-026)은 전부 1시간 TTL($8)이었으므로 두 조합의 환산 비용 차이에는 TTL 정책 차이가 포함된다. openai-codex는 `cacheWrite`를 0으로 기록했다. pi 자체 환산값과 이 표의 값은 소수 둘째 자리까지 같다.
- **Sonnet 5.5(EXP-031)**: 2026-09-29에 claude-api 스킬의 모델 표(2026-09-25 캐시본)로 입력 $2·출력 $10·캐시 읽기 $0.20(1M 토큰당)을 확인했고, Sonnet 5와 같은 가격이라고 적혀 있다. 캐시 쓰기 단가는 그 표에 없어 Claude 표준 배수(5분 TTL 입력의 1.25배 $2.50, 1시간 TTL 2배 $4)를 가정했으며 공식 가격 페이지와 직접 대조하지 않았다(미확인). 6 run의 캐시 쓰기는 원시 세션 로그 기준 전부 1시간 TTL이었다. 캐시 쓰기 비중은 run당 약 $0.22–0.29로, 단가가 다르면 이 부분이 바뀐다.
- **pi × Sonnet 5.5(EXP-032)**: 대응 방식은 EXP-030과 같고 단가는 위 Sonnet 5.5 항목을 그대로 쓴다. pi 0.87.1 내장 목록에 Sonnet 5.5가 없어 내장 `claude-sonnet-5` 정의를 복사한 사용자 정의 모델 항목으로 실행했다. `cacheWrite1h`가 전 응답(54건) 0이어서 캐시 쓰기를 `cache_write_5m`($2.50, 미확인 가정)에 넣었다. 캐시 쓰기 비중은 run당 약 $0.08–0.09다. 네이티브 Claude Code × Sonnet 5.5(EXP-031)는 전부 1시간 TTL($4)이었으므로 두 조합의 환산 비용 차이(EN 중앙값 0.30 vs 0.68)에는 TTL 정책·에이전트·thinking 설정 차이가 함께 들어 있다.
- **gemini-3.8-flash(EXP-035/036)**: 2026-10-07에 Gemini API 가격 페이지(<https://ai.google.dev/gemini-api/docs/pricing>)의 유료 티어 Standard 단가를 확인해 적용했다(1M 토큰당 입력 $0.75·캐시 입력 $0.075·출력 $3.75, thinking 포함). 2027-01-01부터 전 항목이 두 배가 되므로 그 이후 같은 사용량은 약 2배다. 명시 캐시 저장비($0.50/1M 토큰·시간)는 두 하네스 모두 암묵 캐시 읽기만 기록돼 넣지 않았다. agy의 `input_tokens`는 캐시 읽기를 제외한 값이다(`total_tokens = input + output` 검산). agy run 3은 하네스 채점기가 강제 종료한 iteration 1(D-1)의 사용량을 transcript에서 포함했다.
- **Haiku 5.5(EXP-037)**: 2026-10-08에 API 가격 표(<https://platform.claude.com/docs/en/build-with-claude/prompt-caching>)로 단가를 확인했다(1M 토큰당 100K 이하 입력 $0.10·5분 캐시 쓰기 $0.125·1시간 쓰기 $0.20·캐시 읽기 $0.01·출력 $0.50, 100K 초과 $0.50·$0.625·$1·$0.05·$2.50). 장문맥 단가는 요청 단위로 적용되므로, 프롬프트(`input + cache_creation + cache_read`)가 100K를 넘은 요청의 토큰을 `usage_all_runs.csv`의 `lc_*` 열(총량에 포함된 부분)에 따로 기록하고 `compute_cost.py`가 `prices.json`의 `long_context` 단가와의 차액을 더한다. 해당 요청은 en-1 2건·en-2 11건·en-3 0건이다. 이 3 run은 구독이 아니라 Anthropic API 키로 실행돼 실제로 과금됐고(실험 이탈 D-1, 청구액 미대조), 그 때문에 캐시 쓰기가 전부 5분 TTL이다(다른 네이티브 Claude run은 구독·1시간 TTL). 같은 토큰을 1시간 TTL 쓰기 단가로 계산하면 run당 $0.007–0.012(8–12%) 높으므로, 이 값은 구독 조건과 같은 기준의 비용이 아니다. 요청 간격이 최대 44초여서 5분 TTL로 인한 캐시 만료는 관측되지 않았다.
- **Solar Pro 4**: 정가로 환산했다. 실험 당시(2026-08)는 무료 또는 프로모션 기간이었다. 이 엔드포인트는 캐시를 계상하지 않아 입력 전량이 비캐시 단가로 계산된다. 이 때문에 값이 크다.
- **범위**: run 안의 재시도·추가 세션·서브에이전트 호출을 포함한다(실험 품질 규칙 5절 — 실패·재시도 포함). Opus 4.8 run 48-1은 재검증 세션을, Solar Pro 4 run 1은 게이트 오검으로 이어진 세션 12개를 포함한다.

## 토큰 데이터

[usage_all_runs.csv](usage_all_runs.csv)는 대시보드의 109 run을 한 표로 모은 것이다. 감사 절차와 판단은 [audit.md](audit.md)에 있다. 요약하면:

- 40 run은 기존 CSV를 원시 세션 로그로 재집계해 일치를 확인했고, 15 run은 원시 로그에서 새로 집계했으며, EXP-027 6 run은 2026-09-24에 원시 rollout을 재집계해 실험 `runs/usage.csv`와 일치를 확인했고, 6 run(EXP-019 Opus KO)은 원시 로그가 삭제돼 보고서 값을 썼다. EXP-029 9 run은 2026-09-24에 보관된 pi 세션 아카이브를 `usage_pi.py`(responseId 중복 제거)로 재집계해 실험 `runs/usage-pi.csv`와 일치를 확인했다. EXP-030 6 run은 같은 방법으로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼다. EXP-031 6 run은 2026-09-29에 원시 세션 로그(`~/ralph-exp031/sessions-sonnet55-*`)를 message.id 기준으로 다시 읽어 캐시 쓰기 TTL(전부 1시간)을 확인하고 실험 `runs/usage.csv`(`usage031.py`)와 일치를 확인했다. EXP-032 3 run은 EXP-030과 같은 방법으로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼고, 보관된 세션 아카이브에서 `cacheWrite1h`가 전부 0임을 확인했다. EXP-035 3 run은 agy transcript(`usage_agy.py`)를, EXP-036 3 run은 `usage_pi.py` 결과를 옮겼다.
- 중복 제거는 assistant `message.id` 기준이며, 같은 ID의 usage가 다르면 스트리밍 중간 기록(출력 0)과 최종 기록 패턴일 때만 최종 기록을 채택했다.
- 재집계 과정에서 기존 CSV 3건의 오류를 발견했다. qwen-ko-1·qwen-ko-3(EXP-017)은 최종 usage가 없는 중간 기록을 포함해 비캐시 입력이 약 8배·14배 과대했고, sol-1(EXP-011)은 실행 전 스모크 세션을 포함했다. 이 표에는 정정값을 썼다. 해당 실험의 `runs/` 원본 CSV는 기록 보존을 위해 수정하지 않았으며, 보고서 본문은 이 값을 인용하지 않아 판정에 영향이 없다.
- 집계 스크립트([aggregators/](aggregators/))는 실험 머신의 원시 로그 경로(`~/experiments/ralph-exp0NN/` 등, 2026-10-08 이전 `~/ralph-exp0NN/`)를 읽으므로 다른 환경에서는 그대로 재실행되지 않는다.

## 갱신 방법

새 실험을 대시보드에 추가할 때:

1. 새 run들의 행을 `usage_all_runs.csv`에 추가한다(같은 열 정의, 누락은 빈칸).
2. 새 모델이면 `prices.json`에 단가·출처 URL·확인일을 추가한다.
3. `python3 analysis/cost/compute_cost.py`로 `cost_all_runs.csv`를 갱신한다.
4. `dashboard/index.html`의 `M` 배열에서 해당 조건에 `usd:[...]`(대시보드 run 순서)를 넣는다.

단가는 수시로 바뀐다. 비교 시점이 달라지면 `prices.json` 전체를 다시 확인하고 확인일을 갱신한다.
