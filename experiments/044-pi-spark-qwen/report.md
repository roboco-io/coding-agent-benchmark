# EXP-044 결과 보고: pi × DGX Spark 탑재 가능 Qwen 3종 (중단)

- 실험일: 2026-10-10 (18:46–18:53 KST, 첫 run의 iteration 1 진행 중 중단)
- 가설: [M-37](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DashScope OpenAI 호환 엔드포인트의 Qwen 3종(`dashscope/qwen3.8-flash`·`dashscope/qwen3-coder-next`·`dashscope/qwen3.8-27b`, thinking pi 기본값, 사용자 정의 `models.json`)을 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 클라이언트: pi 0.87.1
- **판정: 보류(실험 중단)** — 사용자가 결과 정리를 위해 중단을 결정해 9 run 중 0 run이 끝났다. flash-en-1의 iteration 1을 7분 실행한 뒤 중단했고, 그 시점 상태를 실험자가 채점한 결과는 3/13·요청 81건이었다(커밋 없음). 가설은 판정하지 않는다.

> 설계는 [README.md](README.md)에 실행 전 고정했다. 상한(20분·정체 300초)은 기동 전에 EXP-043 D-1·D-2 변경을 반영했다.

## 실행 기록

| run | 상태 | 실행 시간 | 응답 수 | 입력 / 캐시 읽기 / 출력 | 중단 시점 채점(실험자) |
|---|---|---|---|---|---|
| flash-en-1 | iteration 1 중 중단 | 18:46:04–18:53:05 (7분) | 35 | 59K / 863K / 21.8K | 3/13 · 요청 81 |
| 나머지 8 run | 미실행 | — | — | — | — |

- 응답 `model` 필드와 usage는 pi 세션 기록([runs/usage-pi.csv](runs/usage-pi.csv))에서 집계했다. 환산 비용은 qwen3.8-flash 공개 단가(입력 $0.15 / 출력 $0.47, 100만 토큰당, 캐시 읽기는 입력의 10% 가정)로 약 $0.03이다.
- pi는 DashScope OpenAI 호환 엔드포인트를 쓰며, 이 엔드포인트는 EXP-042 D-1의 usage 결함이 없다는 것을 Phase 0 재현에서 확인했다. 이 실험에서는 캐시 읽기가 정상 기록됐다.
- Phase 0의 입력 한도 확인 요청(flash·27b 300K 입력)은 실험 metering 밖에서 약 $0.1이 과금됐다.

## 결론 및 후속 실험

- 결론: 판정 없음. DashScope OpenAI 호환 경로가 pi에서 정상 동작하고 usage가 정상 기록된다는 것만 확인했다.
- 후속: Spark 등급 Qwen 3종의 pi 측정이 필요하면 같은 설계(20분 상한)로 재기동한다. 하네스와 `models.json`은 `~/experiments/ralph-exp044`와 [runs/pi-models.json](runs/pi-models.json)에 남아 있다.
