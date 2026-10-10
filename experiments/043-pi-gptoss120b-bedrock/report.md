# EXP-043 결과 보고: pi × gpt-oss-120b (Amazon Bedrock) 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-10 (15:41–18:44 KST, 단일 오케스트레이터 순차 3 run)
- 가설: [M-36](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DGX Spark 1대(128GB)에 올릴 수 있는 오픈 웨이트 `gpt-oss-120b`(Amazon Bedrock `amazon-bedrock/openai.gpt-oss-120b-1:0`, us-west-2, thinking pi 기본값, Bedrock API 키)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분(실행 중 4시간에서 변경, D-1·D-2) 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 클라이언트: pi 0.87.1
- **판정: 기각** — 3 run 모두 20분 상한 안에 완주하지 못했다(0/3). 상한 안의 모든 iteration이 Hurl 0/13이었고, 상한 밖까지 실행된 구간(oss-en-1 약 100분, oss-en-2 60분)에서도 게이트 통과는 없었다. 주된 실패 양상은 에이전트가 `npm run dev`를 포그라운드로 실행해 도구 호출이 반환되지 않는 정체였다. 상한이 실행 중 두 번 바뀌었으므로 "20분 안 완주 실패"로만 해석한다.

> 설계는 [README.md](README.md)에 실행 전 고정했고, 상한 변경은 [runs/deviations.md](runs/deviations.md) D-1–D-3에 기록했다.

## 사전 기준 대조

| 주 지표·사전 기준 | 관측값 | 충족 여부 | 판정 범위 |
|---|---|---|---|
| 3/3 → 검증, 1–2/3 → 부분 검증, 0/3 → 기각 | 0/3 (20분 상한 기준). 4시간 상한이었던 oss-en-1의 100분 실행에서도 0/13 | 기각 | 완주 가능성 (20분 상한) |
| run 단위 보류(Bedrock 5xx·스로틀 지속, 하네스 결함) | 해당 없음 — 세션 기록상 오류 응답(stopReason error) 0건. 상한 적용 실패(D-3)는 판정 구간에 영향 없음 | — | — |

## run별 결과

| run | 판정 구간 | 판정 구간 iteration | 정체 종료(exit 124) | 최고 채점(판정 구간) | 실제 실행 | 커밋 | 응답 수 | 입력 / 출력 토큰 |
|---|---|---|---|---|---|---|---|---|
| oss-en-1 | 15:41:21 시작, 20분 시점까지 | 1–3 | iter 3 | 0/13 · 요청 26 | 약 100분, 9 iteration (전부 0/13) | 2 | 148 | 2.26M / 25.5K |
| oss-en-2 | 17:23:00 시작, 17:44:38 timeout | 1–5 | iter 1·2 | 0/13 · 요청 0 | 60분, 26 iteration (최고 0/13 · 요청 26) | 5 | 451 | 10.57M / 69.0K |
| oss-en-3 | 18:23:10 시작, 18:44:40 timeout | 1–5 | iter 4 (iter 5는 상한 exit 125) | 0/13 · 요청 0 | 21분 | 0 | 125 | 1.35M / 20.5K |

- 토큰은 pi 세션 기록(responseId dedup, [runs/usage-pi.csv](runs/usage-pi.csv))이며 상한 밖 구간을 포함한다. oss-en-2의 판정 구간(iteration 1–5)만 보면 응답 24건, 입력 0.14M이다. Bedrock은 캐시를 보고하지 않았다(cacheRead·cacheWrite 0).
- CloudWatch `AWS/Bedrock`(us-west-2, 2026-10-10) 합계: 호출 728회, 입력 14,221,977, 출력 115,345 토큰. 세션 집계(입력 14.18M)와 차이는 스모크와 사전 확인 호출로 본다.
- 환산 비용: AWS Price List API의 us-west-2 표준 온디맨드 단가(입력 $0.15 / 출력 $0.60, 100만 토큰당)로 약 **$2.20**. 청구액은 Cost Explorer 반영 지연으로 확인하지 못했다(2026-10-10 조회 시 $0).

## 모델 유지·루프 기여

- 응답 `model` 필드는 전수 `openai.gpt-oss-120b-1:0`(724건), thinking level `medium`(pi 기본값)이었다.
- 반복 실패 양상: (1) `npm run dev`를 포그라운드로 실행해 정체 감시가 iteration을 종료, (2) 존재하지 않는 모듈을 import한 상태로 커밋해 서버가 기동하지 않음(oss-en-1 마지막 채점: `Cannot find module src/routes/articles`), (3) oss-en-3은 커밋을 하나도 만들지 못했다.
- 새 세션 재시작이 진전을 만들지 못했다. 상한 밖까지 26 iteration을 실행한 oss-en-2도 최고 결과는 요청 26건 실행·성공 파일 0이었다.

## usage·집계 검증

- 집계: `runs/usage_pi.py`(responseId dedup). CloudWatch 지표와 세션 집계가 0.3% 이내로 일치했다.
- 인증: 전용 IAM 사용자 `ralph-bench-bedrock`의 Bedrock API 키. `~/.aws` 관리자 자격증명은 `AWS_CONFIG_FILE=/dev/null` 등으로 차단했다. 키와 사용자는 실험 종료 후 2026-10-10에 삭제했다.
- 재현 자료: `bench.env`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, 로그(gz), `sessions.tar.gz`(마스킹 점검, 검출 0건). 완주 run이 없어 `recheck.csv`는 없다.

## 한계와 교란 변수

- 상한이 실행 중 4시간 → 1시간 → 20분으로 바뀌었다. oss-en-1은 4시간 상한으로 시작했고, oss-en-2는 20분 적용 스크립트가 driver 본체를 멈추지 못해 60분까지 실행됐다(D-3). 판정은 모든 run에 20분 기준을 적용했다.
- 20분은 최근 완주 실험(5–25분)에 근거한 값이며, 25분 걸린 정상 완주 사례도 있다. 따라서 이 결과는 "더 긴 시간을 주면 완주할 수 없다"를 뜻하지 않는다. 다만 20분을 넘겨 실행된 약 120분(oss-en-1 80분, oss-en-2 40분) 동안 진전이 없었다는 관측이 있다.
- Bedrock 서빙 정밀도와 로컬 서빙(MXFP4)의 차이는 확인하지 않았다. pi의 기본 시스템 프롬프트·도구가 gpt-oss에 맞춰진 것인지도 확인하지 않았다.

## 결론 및 후속 실험

- 결론: pi × Bedrock gpt-oss-120b는 이 과제를 20분 안에 완주하지 못했다(0/3). 포그라운드 서버 실행에 따른 정체와 미완성 코드 커밋이 반복됐다.
- 후속: gpt-oss를 다시 측정한다면 Codex CLI 등 gpt-oss용 도구 형식을 쓰는 하네스와 비교가 필요하다. 하네스 개선 후보로 driver가 iteration마다 `bench.env`의 상한을 다시 읽게 하는 변경을 남긴다(D-3).
