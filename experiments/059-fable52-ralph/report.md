# EXP-059 결과 보고: Claude Code × Fable 5.2 네이티브 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-11-10 (10:06–10:20 KST, 순차 3 run)
- 가설: [M-51](../../hypotheses/catalog.md) — Claude Code 네이티브(`claude -p` 2.1.321)에서 Fable 5.2(`claude-fable-5-2`, thinking 기본값)는 EN 정본(PROMPT v2) 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 run 상한 20분·30 iteration 안에 무개입 완주할 수 있다 (EN n=3).
- 클라이언트: Claude Code 2.1.321
- **판정: 검증** — 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 모델 필드 56건 전부 `claude-fable-5-2`). 세션 4분 12초–4분 47초, output 23.3–25.7K, API 단가 환산 run당 $2.37–2.47이다(구독 실행, 청구액 아님).

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| claude-fable-5-2 | 3/3 완주 = 검증 | 3/3 iter 1 완주 | 검증 |

## run별 결과

세션 시간은 세션 jsonl의 첫·마지막 기록 시각 차이다(채점 제외). usage는 `scripts/aggregate_tokens.py` v2로 `message.id` 중복을 제거한 값이다. 서브에이전트 jsonl은 3 run 모두 없었다. 환산 비용은 아래 "usage·집계 검증"의 공개 API 단가로 계산한 값이며 실제 청구액이 아니다.

| run | 완주 | 세션 시간 | API 호출 | cache read | cache write(1h) | output | 요청별 최대 프롬프트 | 커밋 | 재검증 ×2 | API 환산 |
|---|---|---|---|---|---|---|---|---|---|---|
| fable52-en-1 | iter 1/30 | 4분 47초 | 19 | 1.13M | 75.8K | 25.7K | 87.5K | 4 | 13/154 ×2 | $2.47 |
| fable52-en-2 | iter 1/30 | 4분 38초 | 19 | 1.17M | 76.2K | 23.7K | 87.8K | 5 | 13/154 ×2 | $2.40 |
| fable52-en-3 | iter 1/30 | 4분 12초 | 18 | 1.13M | 75.7K | 23.3K | 87.3K | 4 | 13/154 ×2 | $2.37 |

세 run 모두 도구는 Bash만 18회 썼다. 노출된 MCP·스킬·서브에이전트는 호출하지 않았다. 세션 기록에서 하네스 파일(`measure.sh`, 다른 run 디렉터리 등)을 참조한 호출은 없었다.

## 모델 유지·루프 기여

응답 `message.model`은 3 run 56건 모두 `claude-fable-5-2`였다. 세 run 모두 첫 iteration에서 합격했으므로 루프의 복구 기여는 관측되지 않았다. 정체 종료(exit 124)·run 상한(125)·비용 상한(126)은 발생하지 않았다.

세 에이전트 모두 완료 보고에서 "업스트림 Hurl 스위트가 현재 157 요청이며 PROMPT의 154와 다르다"고 적었다. 에이전트는 업스트림 최신 `specs/api/hurl`(커밋 `2558884`)을 받아 자체 확인에 썼다. 판정은 하네스가 고정한 13파일·154 요청 정본으로만 했고, 그 결과 13/13·154/154였다. 업스트림 스위트 변경은 이후 실험에서 에이전트의 자체 확인 기준이 달라질 수 있는 요인이므로 기록한다.

## 같은 네이티브 하네스의 Claude 모델과 비교 (관측값, 우열 판정 아님)

| 조건 | 세션 시간 범위 | output 범위 | API 환산 범위 |
|---|---|---|---|
| Fable 5.2 (이번, CC 2.1.321, PROMPT v2) | 4.2–4.8분 | 23.3–25.7K | $2.37–2.47 |
| Fable 5.1 (EXP-023, 2026-09, PROMPT v1) | 6.2–7.8분 | 28.7–35.8K | $3.23–4.07 |
| Opus 5.5 EN (EXP-026, PROMPT v1) | 4.0–8.4분 | 18.6–28.2K | $1.18–1.72 |
| Sonnet 5.5 EN (EXP-031, PROMPT v1) | 2.9–4.2분 | 15.2–20.0K | $0.60–0.76 |

이번 3 run은 Fable 5.1보다 세션 시간이 짧고 output이 약 20% 적었다. 단가도 20% 낮아(입력 $10→$8, 출력 $50→$40) API 환산은 약 30% 낮았다. output 규모는 Opus 5.5와 같은 대역이다. 그러나 실험 시점, Claude Code 버전, PROMPT 버전(v1 → v2, PORT 안내 한 줄 추가), 글로벌 설정 노출 내용이 함께 달라졌다. 따라서 이 차이를 모델 차이로 단정하지 않고 조합 전체의 차이로만 기록한다.

## usage·집계 검증

- 원자료: run별 `sessions-<run>/` 최상위 jsonl 1개, usage 누락 0, 중복 제거 17–19행.
- 인증: smoke init `"apiKeySource":"none"`(구독 OAuth), `overageStatus: rejected`(유료 추가 사용 비활성). 캐시 쓰기는 전부 1시간 TTL이었다.
- 비용: 구독 실행이라 run별 실제 지출은 없다. 하네스 비용 가드는 단가 0으로 동작했다. 2026-11-10 [pricing 페이지](https://platform.claude.com/docs/en/about-claude/pricing)의 공개 단가(1M 토큰당 입력 $8, 출력 $40, 캐시 읽기 $0.20, 캐시 쓰기 1h $16, 200K 초과 구간 단가 없음)를 적용했다. 이 단가는 하위 에이전트가 페이지에서 읽은 값이다.
- 재현 자료: `runs/`의 `bench.env`, `model-specs.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage.csv`, 로그(gz), `sessions.tar.gz`. 보관 전 `redact_keys.py` 마스킹 결과 0건.

## 한계와 교란 변수

- 과제 1개·n=3이다. 3/3은 이 조건의 관측값이며 일반적인 성공률을 확정하지 않는다.
- 비격리 `~/.claude` 조건이라 글로벌 CLAUDE.md·플러그인·MCP가 노출되었다(`runs/phase0.md`). 과거 네이티브 실험과 노출 내용이 같지 않다.
- 조율 세션(Opus 5.5)이 같은 구독 계정을 동시에 썼다. 사용량 한도 경고나 rate limit 오류는 관측되지 않았다.
- 실행 중 외부 프로세스(DeepSRT)가 3003을 점유했다. driver가 run별 빈 포트를 주입했고 3 run 모두 첫 채점에서 13/13이어서 거짓 음성은 발생하지 않았다.

## 결론 및 후속 실험

- 결론: Fable 5.2는 Claude Code 네이티브 하네스에서 이 과제를 iteration 1에 완주했다(n=3).
- 후속: Fable 5.1·Opus 5.5를 CC 2.1.321·PROMPT v2로 같은 시기에 재측정하면, 이번 output·시간 차이 중 모델이 차지하는 부분을 분리할 수 있다.
