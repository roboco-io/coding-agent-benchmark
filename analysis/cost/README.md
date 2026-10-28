# run당 비용 환산 (공개 단가 기준 추정)

작성일: 2026-09-23. 갱신: 2026-09-24(EXP-027 gpt-6-sol·gpt-6-luna, EXP-028 Sonnet 5, EXP-029 pi 하네스 3조건, EXP-030 pi × Opus 5.5·gpt-6-sol 추가), 2026-09-29(EXP-031 Sonnet 5.5, EXP-032 pi × Sonnet 5.5 추가), 2026-10-07(EXP-035 agy × gemini-3.8-flash, EXP-036 pi × gemini-3.8-flash 추가), 2026-10-08(EXP-037 Haiku 5.5, EXP-038 pi × Haiku 5.5 추가), 2026-10-11(EXP-045 pi × qwen3.8-27b, EXP-046 pi × GLM-5.3-Flash 추가), 2026-10-16(EXP-047 pi × gemini-4-argon 추가), 2026-10-18(EXP-048 DeepSeek V4.1-Flash-1017 추가), 2026-10-19(EXP-049 pi × Muse Spark Open, EXP-050 pi × DeepSeek V4.1-Flash-1017 추가), 2026-10-25(EXP-051 pi × Kimi K3.1 Pro·Pro Highspeed, EXP-052 Claude Code × Kimi K3.1 Pro·Pro Highspeed 직결, EXP-053 pi × GLM-5.3·GLM-5.3-Prime(OpenRouter) 추가), 2026-10-27(EXP-054 Codex × gpt-6.1-terra 추가), 2026-10-28(EXP-055 pi × gpt-6.1-terra, EXP-057 pi × gpt-6.1-terra + 지속 지침 추가). 대시보드(<https://roboco.io/coding-agent-benchmark/>)의 "run당 환산 비용" 열의 근거 자료다.

## 이 수치가 뜻하는 것

각 run이 사용한 토큰을 네 항목(비캐시 입력·캐시 읽기·캐시 쓰기·출력)으로 나누고, 항목마다 2026-09-23(gpt-6-sol·gpt-6-luna는 2026-09-24, Sonnet 5.5는 2026-09-29, gpt-6.1-sol은 2026-10-03, gpt-6.1-terra(pi 포함)는 2026-10-27, gemini-3.8-flash는 2026-10-07, Haiku 5.5는 2026-10-08, gemini-4-argon은 2026-10-16, DeepSeek V4.1-Flash-1017·Muse Spark Open은 2026-10-18, Kimi K3.1 Pro·Pro Highspeed는 2026-10-25)에 확인한 공개 API 단가를 곱해 더한 값이다. **실제로 지출한 금액이 아니다.** 네이티브 Claude run은 구독(OAuth), pi × Opus 5.5(EXP-030)·pi × Sonnet 5.5(EXP-032)는 Anthropic API 키(실제 과금, 청구액 미확인), gpt-5.6-sol·gpt-6-astra·gpt-6-sol·gpt-6-luna·gpt-6.1-sol(pi × gpt-6-sol·pi × gpt-6.1-sol 포함)·gpt-6.1-terra(pi 조건 포함)는 ChatGPT 플랜 OAuth로 실행했고, Solar 두 모델은 무료·프로모션 프리뷰 기간에 실행했다. gemini-3.8-flash(EXP-035/036)·gemini-4-argon(EXP-047)은 Gemini API 키로, DeepSeek V4.1-Flash-1017(EXP-048)은 DeepSeek API 키로 실행해 실제 과금이 있었으나 청구액은 확인하지 않았다. Muse Spark Open(EXP-049)은 OpenRouter API 키로 실행해 실제 과금이 있었고, 이 조건만은 환산값을 OpenRouter의 호출별 청구 기록과 대조해 일치를 확인했다(아래). 따라서 이 값은 "같은 사용량을 지금 공개 API 단가로 과금하면 얼마인가"에 대한 추정이다. 실험 품질 규칙([docs/experiment-quality-rules.md](../../docs/experiment-quality-rules.md) 4절)에 따라 구독 지출과 API 단가 환산을 구분하고, 단가 출처와 확인 시점을 남긴다.

## 결과 (run당 추정 비용 중앙값, USD)

| 모델 | EN | KO | 단가 적용 조건 |
|------|----|----|----------------|
| gpt-6-luna | 0.03 | — | 단문맥 단가 |
| pi × GLM-5.3-Flash | 0.05 | — | Z.ai 종량제 단가, pi 하네스, 실제 호출은 Coding Plan 쿼터 차감(종량제 환산 추정, 아래) |
| pi × DeepSeek V4.1-Flash | 0.06 | — | 피크 단가(상한), pi 하네스 |
| pi × DeepSeek V4.1-Flash-1017 | 0.06 | — | 피크 단가(상한), pi 하네스, 2026-10-17 가중치(별칭 `deepseek-flash`), API 키 실행(실제 과금) |
| DeepSeek V4.1-Flash-1017 | 0.07 | — | 피크 단가(상한), 2026-10-17 가중치 갱신 후 같은 별칭(`deepseek-flash`), API 키 실행(실제 과금) |
| DeepSeek V4.1-Flash | 0.09 | 0.12 | 피크 단가(상한) |
| Haiku 5.5 | 0.09 | — | 프롬프트 100K 초과 요청은 5배 단가, API 키 실행(캐시 5분 TTL, 실제 과금) |
| pi × Haiku 5.5 | 0.06 | — | pi 하네스, 100K 초과 요청 5배 단가, API 키 실행(캐시 5분 TTL) |
| gpt-6.1-terra | 0.12 | — | Standard 단가(272K 이하, 캐시 입력 $0.05), Codex 하네스(구독 OAuth, 실제 지출 없음) |
| pi × gpt-6.1-terra (지침 없음, EXP-055) | 0.14 | — | Standard 단가(캐시 입력 $0.05), pi 하네스(구독 OAuth, 실제 지출 없음), iteration 5-7회 완주. CSV 모델명 `gpt-6.1-terra (no persistence)`, 대시보드에서 제외 |
| pi × gpt-6.1-terra | 0.06 | — | 지속 실행 지침이 들어간 pi 정본(EXP-057, 2026-10-28부터 pi 정본), 위와 같은 단가. 지침 추가 전 pi 결과와 비교할 때 지침 유무를 교란 변수로 적음 |
| DeepSeek V4-Pro | 0.52 | 0.48 | 피크 단가(상한) |
| pi × qwen3.8-27b | 0.23 | — | 싱가포르 리전, pi 하네스, 캐시 읽기는 입력의 10% 가정(아래), API 키 실행(실제 과금) |
| pi × gpt-6-sol | 0.27 | — | 단문맥 단가, pi 하네스(구독 OAuth, 실제 지출 없음) |
| pi × Sonnet 5.5 | 0.30 | — | pi 하네스, 캐시 쓰기 5분 TTL, 캐시 쓰기 단가는 미확인 가정(아래) |
| pi × gpt-6.1-sol | 0.30 | — | 단문맥 단가(캐시 입력 $0.10), pi 하네스(구독 OAuth, 실제 지출 없음) |
| gpt-6.1-sol | 0.36 | — | 단문맥 단가(캐시 입력 $0.10) |
| gpt-6-sol | 0.43 | — | 단문맥 단가 |
| pi × Muse Spark Open | 0.50 | — | OpenRouter(Together 고정) 공개 단가, pi 하네스, API 키 실행(실제 과금), OpenRouter 호출별 청구 기록 합과 일치(아래) |
| pi × gemini-4-argon | 0.86 | — | 2026-11-30까지 단가(2026-12-01부터 2배), pi 하네스, API 키 실행(실제 과금) |
| pi × gemini-3.8-flash | 1.11 | — | 2026년 단가(2027-01-01부터 2배), pi 하네스 |
| agy × gemini-3.8-flash | 1.47 | — | 2026년 단가(2027-01-01부터 2배), Antigravity CLI 하네스 |
| pi × kimi-k3 | 0.65 | — | pi 하네스, 캐시 쓰기는 입력 단가 |
| pi × kimi-k3.1-pro | 0.46 | — | pi 하네스, 캐시 쓰기는 입력 단가, API 키 실행(실제 과금) |
| pi × kimi-k3.1-pro-highspeed | 0.76 | — | pi 하네스, pro의 2배 단가, 캐시 쓰기는 입력 단가, API 키 실행(실제 과금) |
| kimi-k3.1-pro | 0.92 | — | Claude Code 직결, 완주 2 run 중앙값(미완주 1 run $0.67 제외), 캐시 쓰기는 입력 단가, API 키 실행(실제 과금) |
| kimi-k3.1-pro-highspeed | 1.28 | — | Claude Code 직결, pro의 2배 단가, 캐시 쓰기는 입력 단가, API 키 실행(실제 과금) |
| pi × glm-5.3 | 0.44 | — | OpenRouter(Z.AI 고정) 공개 단가, pi 하네스, API 키 실행(실제 과금), OpenRouter 호출별 청구 기록 합과 일치 |
| pi × glm-5.3-prime | 1.03 | — | OpenRouter(Alibaba 고정) 공개 단가, pi 하네스, API 키 실행(실제 과금), OpenRouter 호출별 청구 기록 합과 일치 |
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
- **pi × Haiku 5.5(EXP-038)**: 단가·장문맥 처리는 위 Haiku 5.5 항목과 같다. pi의 `cacheWrite`는 `cacheWrite1h`가 전 응답 0이어서 `cache_write_5m`에 넣었다. pi 세션 기록의 자체 비용은 장문맥 단가를 반영하지 않으므로 쓰지 않았다. 100K 초과 요청은 en-1 3건뿐이다.
- **pi × qwen3.8-27b(EXP-045)**: 모델 사양 파일(`experiments/045-pi-qwen38-27b/runs/model-specs.json`)에 기록된 2026-10-10 확인 단가(싱가포르 리전, 1M 토큰당 입력 $0.50·출력 $3.00, <https://www.alibabacloud.com/help/en/model-studio/model-pricing>)를 실험 당일 재확인 없이 적용했다. 캐시 읽기 단가는 공개 표에 없어 EXP-042·045 보고서와 같이 입력 단가의 10%($0.05)로 가정했다. pi 세션 기록의 `cacheWrite`는 전 응답 0이다. DashScope API 키로 실행해 실제 과금이 있었으나 청구액은 대조하지 않았다. 결과(run당 $0.2432·0.2328·0.2215)는 보고서 값과 같다.
- **pi × GLM-5.3-Flash(EXP-046)**: 2026-10-11에 Z.ai 가격 페이지(<https://docs.z.ai/guides/overview/pricing>)의 종량제 단가를 확인해 적용했다(1M 토큰당 입력 $0.15·캐시 읽기 $0.03·출력 $0.50, 구간 단가 없음). pi 세션 기록의 `cacheWrite`는 전 응답 0이다. 실제 호출은 GLM Coding Plan 엔드포인트(`https://api.z.ai/api/coding/paas/v4`)로 보내져 구독 쿼터에서 차감됐고 토큰 단위 청구가 없으므로, 이 값은 같은 토큰을 종량제 API로 보냈을 때의 추정이며 청구액과 대조하지 않았다. 결과(run당 $0.0468·0.0393·0.0683)는 보고서 값과 같다.
- **pi × gemini-4-argon(EXP-047)**: 2026-10-16에 Gemini API 가격 페이지(<https://ai.google.dev/gemini-api/docs/pricing>)의 유료 티어 Standard 단가를 확인해 적용했다(1M 토큰당 입력 $2.00·캐시 입력 $0.10·출력 $10.00, thinking 포함). 2026-12-01부터 전 항목이 두 배가 되므로 그 이후 같은 사용량은 run당 약 $1.7–1.8이다. 명시 캐시 저장비는 암묵 캐시 읽기만 기록돼 넣지 않았고, pi 세션 기록의 `cacheWrite`는 전 응답 0이다. Gemini API 키로 실행해 실제 과금이 있었으나 청구액은 대조하지 않았다. 결과(run당 $0.8600·0.8905·0.8462)는 보고서 값($0.860·0.891·0.846)과 반올림 범위에서 같다.
- **DeepSeek V4.1-Flash-1017(EXP-048)**: 2026-10-18에 DeepSeek 가격 페이지(<https://api-docs.deepseek.com/quick_start/pricing>, Version 칸 DeepSeek-V4.1-Flash-1017)에서 단가를 확인했다(1M 토큰당 입력 $0.30·캐시 읽기 $0.006·출력 $1.20, 9월 가중치와 같음). EXP-025와 비교할 수 있도록 피크 단가를 적용했으며, 실행 시각(일요일 14:07–14:20 UTC)은 오프피크라 실제 단가는 절반이다. 제공자가 캐시 생성을 0으로 계상했다. DeepSeek API 키로 실행해 실제 과금이 있었으나 청구액은 대조하지 않았다. `prices.json`에는 9월 가중치(`DeepSeek V4.1-Flash`)와 구분해 별도 항목으로 넣었다. 결과(run당 $0.0768·0.0603·0.0658)는 실험 `runs/usage-claude.csv`의 `usd_peak`와 같다.
- **pi × Muse Spark Open(EXP-049)**: 2026-10-18에 OpenRouter endpoints API(<https://openrouter.ai/api/v1/models/meta/muse-spark-open/endpoints>)로 Together 엔드포인트 단가를 확인해 적용했다(1M 토큰당 입력 $1.25·캐시 읽기 $0.15·출력 $4.25, reasoning 포함, 구간 단가 없음, 5개 제공자 동일). pi 세션 기록의 `cacheWrite`는 전 응답 0이다. OpenRouter API 키로 실행해 실제 과금이 있었다. 결과(run당 $0.4515·0.6746·0.5027)는 OpenRouter generation 기록(`GET /api/v1/generation`)의 `total_cost`를 run의 모든 responseId에 대해 합한 값과 소수 넷째 자리까지 같다. **이 리포에서 환산 비용을 제공자 측 청구 기록과 대조한 첫 사례**다. 다만 호출별 기록과의 대조이며 월별 청구서와 대조한 것은 아니다. 다른 조건의 환산값은 여전히 청구액과 대조하지 않은 추정이다.
- **pi × DeepSeek V4.1-Flash-1017(EXP-050)**: EXP-048과 같은 `prices.json` 항목(`DeepSeek V4.1-Flash-1017`, 2026-10-18 확인 피크 단가: 1M 토큰당 입력 $0.30·캐시 읽기 $0.006·출력 $1.20)을 그대로 적용했다. 실행 시각(월요일 07:11–07:26 UTC)은 피크 시간대라 이 단가가 실제 적용 단가와 같은 구간이다. pi 세션 기록의 `cacheWrite`는 전 응답 0이다. DeepSeek API 키로 실행해 실제 과금이 있었으나 청구액은 대조하지 않았다. 결과(run당 $0.0531·0.0654·0.0570)는 보고서 값($0.053·0.065·0.057)과 반올림 범위에서 같고, 보고서에 따르면 pi가 세션에 기록한 비용(내장 단가표)과도 같다.
- **pi × Kimi K3.1 Pro·Pro Highspeed(EXP-051)**: 2026-10-25에 Moonshot 가격 페이지(<https://platform.kimi.ai/docs/pricing/chat>)의 단가를 확인해 적용했다(1M 토큰당 pro 입력 $2·캐시 읽기 $0.20·출력 $10, highspeed 입력 $4·캐시 읽기 $0.20·출력 $20, 구간 단가 없음). 대응 방식은 EXP-029 kimi-k3와 같고, Moonshot이 기록한 `cacheWrite`는 TTL 구분이 없어 `cache_write_5m`(입력 단가와 같음)에 넣었다. pi 0.87.1 내장 목록에 두 모델이 없어 내장 kimi-k3 정의를 복제한 사용자 정의 항목으로 실행했다. Moonshot API 키로 실행해 실제 과금이 있었으나 청구액은 대조하지 않았다.
- **Claude Code × Kimi K3.1 Pro·Pro Highspeed(EXP-052)**: 단가는 위 EXP-051 항목과 같다. Moonshot Anthropic 호환 엔드포인트의 usage `cache_creation`에 TTL 구분이 없어 `cache_write_5m`(입력 단가)에 넣었다. 계정 잔액 조회로 실제 차감액을 대조했다 — 재실행 6 run 환산 합계 $6.19 대 잔액 차감 $5.77(2026-10-25 17:08 기준, 정산 지연 가능). 캐시 읽기를 할인 없이 계산하면 약 $20이라, 이 엔드포인트에서는 캐시 읽기 할인이 적용된 것으로 본다. k31pro-en-3(미완주)은 run별 값에는 있고 결과 표 중앙값에서는 뺐다.
- **pi × glm-5.3·glm-5.3-prime(EXP-053)**: 2026-10-25에 OpenRouter endpoints API로 고정 제공자 단가를 확인했다(1M 토큰당 glm-5.3/Z.AI 입력 $1.40·캐시 읽기 $0.26·출력 $4.40, prime/Alibaba $2.80·$0.56·$8.80, 캐시 쓰기 0, 구간 단가 없음). pi 세션의 `cacheWrite`는 전 응답 0이다. 환산값은 OpenRouter generation API의 호출별 `total_cost` 합(316건)과 run마다 일치했다.
- **gpt-6.1-terra(EXP-054)**: 2026-10-27에 OpenAI 모델 페이지(<https://developers.openai.com/api/docs/models/gpt-6.1-terra>)의 Standard 단가를 적용했다(1M 토큰당 입력 $1·캐시 입력 $0.05·출력 $5, 캐시 쓰기 해당 없음). 272K 초과 요청은 입력 $2·캐시 $0.10·출력 $7.50이지만 요청별 최대 프롬프트가 39.1K라 해당하지 않는다. 단가는 원문 직접 대조 없이 하위 에이전트 요약 값을 썼다(보고서 기록). ChatGPT 구독 OAuth로 실행해 실제 지출은 없다. 환산값은 run당 $0.0855·0.1210·0.1172다.
- **pi × gpt-6.1-terra(EXP-055)·pi × gpt-6.1-terra + 지속 지침(EXP-057)**: 단가는 위 EXP-054 항목과 같다(1M 토큰당 입력 $1·캐시 입력 $0.05·출력 $5). pi 세션 기록의 `input`(비캐시)·`cacheRead`·`output`(reasoning 포함)을 같은 항목에 대응시켰고 `cacheWrite`는 전 응답 0이다. 요청별 최대 프롬프트가 272K를 넘지 않아 장문맥 단가는 적용하지 않았다(EXP-054와 같은 기준으로 가정, 두 실험의 요청별 프롬프트 최댓값은 따로 확인하지 않았다). ChatGPT 구독 OAuth로 실행해 실제 지출은 없다. EXP-055는 run당 $0.1417·0.1086·0.1504, EXP-057은 $0.0719·0.0593·0.0533이며 보고서 값($0.142·0.109·0.150, $0.072·0.059·0.053)과 반올림 범위에서 같다. EXP-055는 iteration 6·5·7회에 걸쳐 완주해 토큰에 iteration마다 저장소 상태를 다시 읽는 비용이 들어 있다. EXP-057은 정본과 다른 지침을 노출한 비정본 스택이므로 `prices.json`에 같은 단가의 별도 항목(EXP-055용 `gpt-6.1-terra (no persistence)`)을 두어 EXP-055를 대시보드에서 제외할 수 있게 했다(2026-10-28 사용자 결정으로 EXP-055는 대시보드에서 뺐고 CSV 기록은 유지, EXP-057 행의 모델명은 `gpt-6.1-terra`). `time_min`은 보고서의 세션 시간(iteration 1 시작부터 마지막 iteration 종료까지, iteration 사이 채점 포함)이다. 같은 모델의 Codex 조건(EXP-054, $0.09-0.12)과 하네스·지침·iteration 수가 모두 다르므로 차이를 하네스 탓으로 단정하지 않는다.
- **Solar Pro 4**: 정가로 환산했다. 실험 당시(2026-08)는 무료 또는 프로모션 기간이었다. 이 엔드포인트는 캐시를 계상하지 않아 입력 전량이 비캐시 단가로 계산된다. 이 때문에 값이 크다.
- **범위**: run 안의 재시도·추가 세션·서브에이전트 호출을 포함한다(실험 품질 규칙 5절 — 실패·재시도 포함). Opus 4.8 run 48-1은 재검증 세션을, Solar Pro 4 run 1은 게이트 오검으로 이어진 세션 12개를 포함한다.

## 토큰 데이터

[usage_all_runs.csv](usage_all_runs.csv)는 133 run을 한 표로 모은 것이다(2026-10-19 기준). 대시보드 성능 매트릭스의 129 run에 프리뷰 API였던 Solar Open 2(EXP-015) 1 run과 Solar Pro 4(EXP-020) 3 run이 더해진 수다. 감사 절차와 판단은 [audit.md](audit.md)에 있다. 요약하면:

- 40 run은 기존 CSV를 원시 세션 로그로 재집계해 일치를 확인했고, 15 run은 원시 로그에서 새로 집계했으며, EXP-027 6 run은 2026-09-24에 원시 rollout을 재집계해 실험 `runs/usage.csv`와 일치를 확인했고, 6 run(EXP-019 Opus KO)은 원시 로그가 삭제돼 보고서 값을 썼다. EXP-029 9 run은 2026-09-24에 보관된 pi 세션 아카이브를 `usage_pi.py`(responseId 중복 제거)로 재집계해 실험 `runs/usage-pi.csv`와 일치를 확인했다. EXP-030 6 run은 같은 방법으로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼다. EXP-031 6 run은 2026-09-29에 원시 세션 로그(`~/ralph-exp031/sessions-sonnet55-*`)를 message.id 기준으로 다시 읽어 캐시 쓰기 TTL(전부 1시간)을 확인하고 실험 `runs/usage.csv`(`usage031.py`)와 일치를 확인했다. EXP-032 3 run은 EXP-030과 같은 방법으로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼고, 보관된 세션 아카이브에서 `cacheWrite1h`가 전부 0임을 확인했다. EXP-035 3 run은 agy transcript(`usage_agy.py`)를, EXP-036 3 run은 `usage_pi.py` 결과를 옮겼다. EXP-037 3 run은 원시 세션 로그를 message.id 기준으로 집계한 실험 `runs/usage.csv`(`usage037.py`) 값을, EXP-038·045·046·047 각 3 run은 `usage_pi.py`(responseId 중복 제거)로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼다. EXP-048 3 run은 `aggregate_tokens.py` v2(message.id 중복 제거)로 집계한 실험 `runs/usage-claude.csv` 값을 옮기고, 2026-10-18에 로컬 원시 세션(`~/experiments/ralph-exp048/sessions-flash1017-en-*`)을 message.id 기준으로 다시 읽어 네 토큰 항목과 고유 요청 수가 일치함을 확인했다. EXP-049 3 run은 `usage_pi.py`(responseId 중복 제거)로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼고, 고유 responseId 수(58·49·61)는 OpenRouter generation 기록의 호출 수와 같다. EXP-050 3 run은 `usage_pi.py`(responseId 중복 제거)로 집계한 실험 `runs/usage-pi.csv` 값을 옮겼고, 2026-10-19에 로컬 원시 세션(`~/experiments/ralph-exp050/sessions-flash1017-en-*`)과 리포 보관본 `sessions.tar.gz`를 각각 다시 집계해 같은 결과임을 확인했다.
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
