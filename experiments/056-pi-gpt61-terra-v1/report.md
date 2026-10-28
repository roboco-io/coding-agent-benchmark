# EXP-056 결과 보고: pi × gpt-6.1-terra 재실험 — PROMPT v1 (중단)

- 실험일: 2026-10-28 (09:03–09:07 KST, run 1 도중 중단)
- 가설: [M-49](../../hypotheses/catalog.md) — PROMPT를 v1(EXP-032·034와 동일)로 되돌리면 pi × gpt-6.1-terra도 iteration 1에 완주한다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 보류** — run 1이 iteration 1에 완주하지 못했고(0/13), iteration 2(3/13)·3(10/13)으로 EXP-055와 같은 기능 묶음 단위 진행을 보였다. 사용자 지시로 09:07에 중단해 run 2·3은 실행하지 않았다. 관측은 반증 방향(n=1)이다.

## 관측

| run | iteration별 통과 파일 | 결과 |
|---|---|---|
| terra61-en-1 | 0 → 3 → 10 → (iteration 4 진행 중 중단) | 미완주·중단 |

iteration 1–3은 모두 `stopReason: stop`으로 끝났다. PROMPT는 스킬 `assets/PROMPT-en.v1.md`(md5 `2c28ea6b7f16125d9b3105f5ee00b126`, EXP-034 하네스 사본과 같은 해시)로 교체했고, 그 밖의 조건은 EXP-055와 같다. usage(중단 시점까지, 세션 4개): input 73.4K(비캐시), cache read 321.2K, output 10.6K.

## 해석

v1에서도 iteration 1에 완료를 선언하지 않았으므로, EXP-055의 다회 iteration이 PROMPT v2(`PORT` 안내 한 줄)에서 비롯됐을 가능성은 낮다. 원인으로 본 문장("pick the single most important remaining piece of work … and do it")은 v1·v2에 모두 있다. n=1이며 중단했으므로 확정 판정은 내리지 않는다. 이후 원인 가설(pi 시스템 프롬프트에 지속 실행 지침 부재)은 [EXP-057](../057-pi-gpt61-terra-persist/report.md)에서 시험했다.

## 이탈

[runs/deviations.md](runs/deviations.md) D-1: 사용자 지시("루프 중단시키고 단일 이터레이션에서 완료하도록 지시할 수 있는 방법을 찾아줘")로 run-all·driver·앱 서버를 PID 지정으로 종료했다.

## 재현 자료

`runs/`의 `bench.env`, `model-specs.json`, `pi-models.json`, `PROMPT-en.md`(v1), preflight 보고서·승인, 스크립트 사본, `phase0.md`, `metrics-terra61-en-1.csv`, `usage-pi.csv`, 로그(gz), `sessions.tar.gz`. 보관 전 마스킹 0건.
