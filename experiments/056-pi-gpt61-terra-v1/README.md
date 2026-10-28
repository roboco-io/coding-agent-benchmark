# EXP-056: pi × gpt-6.1-terra 재실험 — PROMPT v1 (EXP-032·034와 동일 조건)

> [실험 품질 규칙](../../docs/experiment-quality-rules.md)을 적용한다. 설계 확정: 2026-10-28 (실행 전).

## 배경과 질문

[EXP-055](../055-pi-gpt61-terra/README.md)(pi 0.87.1 × gpt-6.1-terra, PROMPT v2)는 3/3 완주했지만 완주까지 iteration 6·5·7회가 걸렸다. 세션 기록상 모델은 iteration마다 기능 묶음 하나를 구현·커밋하고 `stopReason: stop`으로 스스로 종료했다. 같은 pi 0.87.1·같은 격리 플래그에서 Sonnet 5.5(EXP-032)와 gpt-6.1-sol(EXP-034)은 3/3 모두 iteration 1에 완주했다. 실행 조건에서 남은 차이는 PROMPT 버전(EXP-032·034는 v1, EXP-055는 v2 — `PORT` 안내 한 줄 추가)이다.

사용자 지시(2026-10-28): EXP-032·034의 pi와 같은 조건으로 재실험하고, 그래도 여러 iteration으로 나뉘면 지속 실행 지침을 추가한 조건으로 다시 실험한다. 이 실험은 그 첫 단계다.

- 가설 코드·문장: [M-49](../../hypotheses/catalog.md) — PROMPT를 v1(EXP-032·034와 byte-identical)로 되돌리면 pi × gpt-6.1-terra도 iteration 1에 완주한다. 즉 EXP-055의 다회 iteration은 PROMPT v2 차이 때문이다.
- 사전 예측(기록용): 원인으로 보이는 문장("pick the single most important remaining piece of work … and do it")은 v1에도 있으므로, 다회 iteration이 재현될 가능성이 높다고 본다.
- 주 지표: run별 게이트 pass iteration. 보조 지표: 완주 수, 세션 시간, iteration별 `stopReason`, 토큰 대리지표(`usage_pi.py`).

## 조건

EXP-055와 같다(pi 0.87.1 `-nc -ns -ne -np -na`, `openai-codex/gpt-6.1-terra` 사용자 정의 항목 contextWindow 272,000, thinking medium, ChatGPT 구독 OAuth, 30 iteration·20분·정체 300초, EN n=3). **유일한 변경은 PROMPT**: 스킬 `assets/PROMPT-en.v1.md`(md5 `2c28ea6b7f16125d9b3105f5ee00b126`, EXP-034 하네스 사본과 같은 해시)를 setup 후 하네스의 `PROMPT-en.md`에 덮어쓴다. 포트는 하네스가 계속 `PORT`로 주입하지만 v1 PROMPT는 이를 안내하지 않는다(EXP-032·034와 같음).

## 판정 기준 (실행 전 고정)

- 3/3 run이 iteration 1에 게이트 pass → M-49 **검증**(다회 iteration은 v2 영향). 지속 실행 지침 실험은 하지 않는다.
- 1–2/3 run이 iteration 1에 pass → **부분 검증**. 지속 실행 지침 실험(EXP-057)을 진행한다.
- 0/3 → **반증**(PROMPT 버전과 무관). 지속 실행 지침 실험(EXP-057)을 진행한다.
- 완주 여부 자체(게이트 pass + 재검증 2회 13/154)는 별도로 기록한다. 인증·가용성 장애 run은 보류 후 새 run 번호로 재실행.

## 계측

usage는 토큰 대리지표이며 청구 비용이 아니다(구독 OAuth). 응답 model·thinking·stopReason을 세션 기록에서 전수 확인한다.
