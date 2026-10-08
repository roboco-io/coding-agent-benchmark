# 호출당 관측 대기 시간·세션 시간 분해 (2026-10-03)

대시보드 성능 매트릭스의 "호출당 관측 대기"와 "세션 중 모델 대기 비중" 열, 원 수치 표의 모델 대기·도구 시간·모델 호출·모델 대기 1초당 output 열의 근거다. 모델 속도 측정이 아니라, 각 실험 run의 세션 기록에서 관측한 대기 시간이다.

## 정의

- 세션 기록을 시간순으로 읽는다. 직전 이벤트부터 다음 이벤트까지의 구간을, 다음 이벤트가 모델 산출물(응답·도구 호출·reasoning·메시지)이면 **모델 대기**, 도구 결과이면 **도구 실행**으로 귀속한다.
- **모델 호출 수**는 서로 다른 모델 응답의 수다. Codex는 `last_token_usage`가 있는 `token_count` 이벤트 수, pi는 assistant 메시지 수, Claude Code는 assistant 레코드의 고유 `message.id` 수다. Claude Code는 스트리밍 때문에 같은 `message.id`가 여러 줄로 기록되므로 한 번만 세고, output 토큰은 `message.id`별 최댓값으로 중복을 제거해 합산한다.
- **호출당 대기** = 모델 대기 / 모델 호출 수(run 단위). **모델 대기 비중** = 모델 대기 /(모델 대기 + 도구 실행). **모델 대기 1초당 output** = output 토큰 / 모델 대기.
- 대상 세션은 run의 소요 시간으로 기록된 iteration까지다. run에 세션이 여러 개이면(iteration 재시작) 앞쪽부터 기록된 소요 시간에 가장 가까운 개수까지를 합산한다(`collect.py`의 `select`). 완주 뒤에 추가된 재검증 세션(예: EXP-010 48-1의 두 번째 세션 84초)은 제외한다. Solar Open 2(EXP-015)는 대시보드 iter 표기(2)에 맞춰 2개로 고정했다. 세션 시간 합은 기록된 소요 시간과 -0.7분 이내(EXP-015 -0.67, gpt-5.6-sol sol-2 -0.53, pi × qwen3.8-max run 1 -0.72, 나머지 대부분 0.5분 이내)로 맞는다.
- Claude Code 서브에이전트 세션(`<세션 id>/subagents/*.jsonl`, EXP-028 en-2, EXP-015 solar-1, EXP-020 pro4-2)은 별도 세션으로 분해해 run에 합산한다. 부모 세션이 서브에이전트를 기다리는 시간은 부모 쪽에서도 도구 실행으로 잡히므로 이 run들의 도구 시간과 `wall_s`(부모 세션 합)에는 겹침이 있다. `wall_s`는 부모 세션만의 합이고, `model_s`·`model_calls`·`output_tokens`에는 서브에이전트가 포함된다.

## 방법과 검증

- `timeline.py`: Codex·pi·Claude Code 세션 파서와 구간 귀속(`analyze`). 기존 `analysis/gpt61-sol-slowdown/timeline.py`는 이 스크립트를 호출하는 래퍼이며 같은 출력(codex, pi)을 낸다.
- `collect.py`: `analysis/cost/usage_all_runs.csv`의 EN run과 `source_path`로 세션을 찾아 `runs.csv`를 만든다. tar.gz는 임시 디렉터리에 풀어서 읽는다. 실행: `python3 analysis/latency/collect.py <임시 디렉터리>`.
- `build_dashboard_data.py`: `runs.csv`를 `dashboard/index.html`의 `LAT` 상수로 반영한다.
- **2026-10-08 추가 (EXP-035/036 gemini-3.8-flash)**: 두 실험은 대시보드 반영 때 이 분석에 추가되지 않아 해당 열이 비어 있었다. EXP-036(pi)은 기존 pi 파서로, EXP-035(Antigravity CLI)는 새 `agy` 파서로 분해해 `runs.csv`에 6 run을 추가했다.
  - `agy` 파서: `transcript_full.jsonl`의 도구 결과 단계(GENERIC) 본문 `Created At`(도구 시작 = 직전 모델 응답 완료)을 모델 이벤트로, `Completed At`(도구 종료)을 도구 이벤트로 쓴다. 백그라운드 작업 대기(`schedule` 타이머)는 결과에 `Completed At`이 없으므로, 타이머 만료를 알리는 SYSTEM_MESSAGE 시각을 도구 이벤트로 써서 대기를 도구 쪽에 넣는다(이 처리를 빼면 EXP-035 run 2의 모델 대기가 54초 많게 잡혔다).
  - 한계: agy 시각은 초 단위이고, 도구 호출이 없는 마지막 응답의 생성 시간은 완료 시각이 없어 빠진다. 세션 시간 합은 기록된 소요 시간과 -0.5분 이내로 맞는다(17.3/17.5, 15.3/15.5, 22.0/22.4분).
  - 교차 확인: 같은 모델을 밀리초 단위로 기록하는 pi(EXP-036)의 호출당 대기 6.1–7.7초·모델 대기 비중 86–94%가 agy(EXP-035)의 6.5–8.1초·88–95%와 같은 범위다.
- 검증: Codex EXP-033은 기존 분석(587/557/31초, 31호출, 16.2K)과 일치했다. 전체 73 run에서 `wall_s`가 대시보드 소요 시간과 거의 일치했다(대부분 -0.2분 이내). Claude Code는 EXP-026 en-1이 494초(기록 8.35분), output 28,166으로 대시보드의 28.2K와 일치했고 EXP-023 fable-1은 408초(6.9분), 31,102 토큰이었다.

## 범위

- 영어 프롬프트(EN) run만 분석했다. 대시보드의 EN 중앙값에 쓰인 24개 행, 73개 run 모두 원자료를 찾았다. 한국어(KO) 행은 분석하지 않아 대시보드에서 "—"로 표시한다.
- 원자료 위치: 홈 디렉터리의 `ralph-exp0NN/…`(Codex rollout, Claude Code 프로젝트 jsonl), 리포의 `experiments/*/runs`(logs 디렉터리, `sessions.tar.gz`). 사용한 파일 경로는 `usage_all_runs.csv`의 `source_path`와 같다.

## 결과 요약 (EN, 호출당 대기 run 중앙값 순)

| 행 | 하네스 | run | 호출당 대기(초) | run 범위(초) | 모델 대기 비중 | 모델 대기 1초당 output |
|---|---|---|---|---|---|---|
| DeepSeek V4.1-Flash | Claude Code 직결 | 3 | 3.6 | 3.4-4.0 | 70% | 200 |
| pi × DeepSeek V4.1-Flash | pi | 3 | 4.6 | 3.1-4.7 | 76% | 230 |
| pi × Sonnet 5.5 | pi | 3 | 4.9 | 4.5-5.5 | 58% | 151 |
| Sonnet 5.5 | Claude Code | 3 | 6.0 | 4.3-6.3 | 65% | 158 |
| Opus 5.5 | Claude Code | 3 | 6.6 | 5.9-7.2 | 67% | 113 |
| pi × gpt-6-sol | pi | 3 | 7.1 | 6.7-8.4 | 86% | 32 |
| Sonnet 5 | Claude Code | 3 | 7.2 | 5.3-7.6 | 74% | 98 |
| pi × Opus 5.5 | pi | 3 | 7.3 | 7.2-8.9 | 75% | 109 |
| gpt-6-luna | Codex | 3 | 8.3 | 5.1-8.3 | 85% | 42 |
| gpt-6-sol | Codex | 3 | 8.7 | 7.3-9.5 | 84% | 43 |
| Solar Open 2 | Claude Code 직결 | 1 | 8.7 | 8.7 | 84% | 76 |
| Opus 4.8 | Claude Code | 3 | 9.3 | 9.2-10.8 | 92% | 71 |
| gpt-5.6-sol | Codex | 3 | 9.6 | 8.9-11.9 | 88% | 45 |
| Opus 5 | Claude Code | 6 | 9.6 | 7.6-11.3 | 90% | 79 |
| kimi-k3 | Claude Code 직결 | 3 | 12.9 | 11.5-24.8 | 95% | 32 |
| Fable 5.1 | Claude Code | 3 | 13.5 | 12.1-14.8 | 89% | 88 |
| pi × kimi-k3 | pi | 3 | 14.2 | 13.5-17.7 | 93% | 34 |
| pi × gpt-6.1-sol | pi | 3 | 14.3 | 14.3-15.2 | 89% | 28 |
| DeepSeek V4-Pro | Claude Code 직결 | 3 | 15.1 | 14.2-28.4 | 94% | 83 |
| qwen3.8-max | Claude Code 직결 | 3 | 16.2 | 14.5-22.2 | 96% | 46 |
| gpt-6.1-sol | Codex | 3 | 18.0 | 16.4-23.0 | 93% | 29 |
| pi × qwen3.8-max | pi | 3 | 19.9 | 10.2-24.8 | 89% | 36 |
| gpt-6-astra | Codex | 3 | 20.4 | 18.4-20.4 | 95% | 30 |
| Solar Pro 4 | Claude Code 직결 | 3 | 34.5 | 33.3-43.4 | 97% | 11 |

(대시보드에는 실험 코드와 run별 값이 `runs.csv` 기준으로 함께 반영된다. Solar Open 2·Solar Pro 4는 프리뷰 API다.)

## 해석상 주의

- **호출당 대기는 모델 속도가 아니다.** 호출 한 번이 생성한 토큰 수(출력이 길수록 길다), 컨텍스트 크기, 하네스가 도구 호출을 묶는 방식(병렬·배치 여부로 모델 호출 수 자체가 달라진다), 제공자 엔드포인트, 측정 시간대의 서버 부하, 네트워크·대기열 시간이 모두 들어 있다. 모델 대기 1초당 output은 이 중 출력 길이 영향을 일부 덜어내지만 reasoning 토큰이 output에 포함되는지는 제공자마다 다르다.
- 구간 귀속은 기록 시각 기준 근사다. Claude Code는 한 응답의 여러 content block이 각각 다른 줄·시각에 기록되므로, 블록 사이 간격도 모델 대기에 들어간다. 병렬 도구 호출의 결과가 여러 줄로 기록되면 첫 결과까지의 구간만 도구 실행에 크게 반영된다.
- 실험은 서로 다른 날짜(2026-07-24 이후 약 10주)와 클라이언트 버전에서 수행했다(`analysis/client-versions.md`). 날짜가 다른 행 사이의 차이에는 서버 부하와 클라이언트 변경이 섞여 있다. 같은 모델의 두 하네스(Codex와 pi 등) 비교만 하네스 차이를 일부 분리해 보여 준다.
- 모델 대기 비중은 도구 실행(설치·빌드·채점 실행)과 모델 응답 시간의 상대 비율이라, 도구 시간이 긴 run은 모델이 빨라도 비중이 낮게 나온다(예: Opus 5.5 en-1은 도구 252초로 비중 49%).
