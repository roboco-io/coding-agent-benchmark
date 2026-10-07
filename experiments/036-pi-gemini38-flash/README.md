# EXP-036: pi coding agent × gemini-3.8-flash 완주 검증

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-07 (실행 전).

## 가설

- 가설 코드·문장: [M-29](../../hypotheses/catalog.md) — pi coding agent(`pi -p`, 0.87.1)로 `google/gemini-3.8-flash`(thinking high, Gemini API 키 인증)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다.
- 질문 유형: **완주 가능성** (탐색, n=3).
- 주 지표: 완주 수. 보조 지표: 완주 iteration, 세션 시간, 토큰 대리지표(`usage_pi.py`, responseId dedup, `input + output + cacheWrite`).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구 | 연결 | 원자료 |
|---|---|---|---|---|
| flash38 | `google/gemini-3.8-flash`, `--thinking high` | pi 0.87.1 | pi 내장 `google` provider, `GEMINI_API_KEY` (`~/.zsh_secrets`) | `runs/` |

- 키: pi google provider는 `GOOGLE_API_KEY`와 `GEMINI_API_KEY`가 함께 있으면 `GOOGLE_API_KEY`를 쓴다(Phase 0 스모크 경고로 확인). `PI_KEYMAP`으로 `GOOGLE_API_KEY`에 `GEMINI_API_KEY` 값을 넣어 Gemini API 키로 통일한다.
- pi 0.87.1 내장 모델 목록에 `google/gemini-3.8-flash`(컨텍스트 1.0M, 출력 65.5K)가 있어 사용자 정의 항목이 필요 없다.
- thinking은 EXP-035의 agy `--effort high`와 맞추기 위해 `high`로 고정한다. 두 클라이언트가 high를 Gemini API의 같은 설정값으로 보내는지는 확인하지 못했다.
- 지침 노출 차단: `-nc -ns -ne -np -na`로 상위 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 템플릿을 끈다(EXP-029와 동일). 따라서 사용자가 설치한 pi-clm 확장은 로드되지 않는다(`-ne`는 settings.json `packages` 확장도 제외함을 pi 소스 `resource-loader.js`에서 확인).

## 과제·완료 기준

- EXP-035와 동일 (정본 PROMPT-en.md md5 `2c28ea6b7f16125d9b3105f5ee00b126`, Hurl 13파일·154 요청, `/opt/homebrew/bin/hurl`, 게이트 `pass` + 독립 재검증 2회 `13,154`).

## 반복·실행 순서·예산

- 반복: EN n=3, 순차 실행. EXP-035(agy) 3 run 종료 후 실행한다. 다른 실험과 동시 실행 금지.
- 상한: 30 iteration, run당 wall-clock 4시간(14,400초). Gemini API 종량 과금으로 실제 지출이 생긴다.
- 사람 개입·실패 규칙·판정 기준: EXP-035와 동일 (3/3 **검증**, 1–2/3 **부분 검증**, 0/3 **반증**, 장애 run **보류**).

## 환경 주의 (실행 전 확인, 2026-10-07)

- 모델 ID 확인: EXP-035와 같은 Gemini API 모델 목록에서 확인했다.
- 기준선: EXP-035(agy, 같은 모델)와 EXP-029/030/032/034(pi, 다른 모델). 시점·모델·하네스 교락이 있으므로 차이는 조합 전체의 차이로만 서술한다.

## 계측

- usage는 토큰 대리지표이며 청구 비용이 아니다. 시간은 driver 로그의 run start부터 마지막 iteration end까지.
- 응답 모델 필드가 조건과 일치하는지 세션 기록을 전수 확인한다.
