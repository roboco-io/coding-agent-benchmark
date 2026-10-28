# EXP-055 결과 보고: pi × gpt-6.1-terra 랄프 루프 완주 검증 (EN n=3)

- 실험일: 2026-10-28 (08:45–08:59 KST, 순차 3 run)
- 가설: [M-48](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 `openai-codex/gpt-6.1-terra`(ChatGPT 구독 OAuth, thinking medium, 사용자 정의 모델 항목, PROMPT v2)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3).
- 클라이언트: pi 0.87.1
- **판정: 검증** — 3/3 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 model 필드 168건 전부 `gpt-6.1-terra`, thinking 전 iteration `medium`). 단, 완주까지 iteration 6·5·7회가 걸렸다. 모델이 iteration마다 기능 묶음 하나만 구현·커밋하고 스스로 턴을 끝냈기 때문이다(아래 "루프 기여"). 세션 4분 3초–4분 44초.

## 사전 기준 대조

| 모델 | 사전 기준 | 관측 | 판정 |
|---|---|---|---|
| gpt-6.1-terra (pi) | 3/3 완주 = 검증 | 3/3 완주 (iter 6·5·7) | 검증 |

## run별 결과

세션 시간은 로그의 iteration 1 start부터 마지막 iteration end까지(iteration 사이 채점 포함)다. usage는 `usage_pi.py`(responseId dedup) 합계이며 input은 캐시 제외, reasoning은 output에 포함된다. 환산 비용은 공개 API 단가(EXP-054와 같음)로 계산한 값이며 실제 청구액이 아니다.

| run | 완주 iteration | 세션 시간 | input(비캐시) | cache read | output (reasoning) | 커밋 | 재검증 ×2 | API 환산 |
|---|---|---|---|---|---|---|---|---|
| terra61-en-1 | 6/30 | 4분 21초 | 73.1K | 276.4K | 11.0K (0.4K) | 6 | 13/154 ×2 | $0.142 |
| terra61-en-2 | 5/30 | 4분 3초 | 50.6K | 255.5K | 9.1K (0.3K) | 5 | 13/154 ×2 | $0.109 |
| terra61-en-3 | 7/30 | 4분 44초 | 77.7K | 311.2K | 11.4K (0.4K) | 7 | 13/154 ×2 | $0.150 |

통과 파일 수 추이(iteration별): en-1 2→4→7→10→13→13(완료 선언), en-2 4→7→10→13→13(완료 선언), en-3 2→4→6→9→10→12→13(완료 선언).

## 루프 기여 — iteration마다 기능 묶음 하나

세션 기록 18개 전부에서 각 iteration은 `stopReason: stop`으로 끝났다. API 오류·출력 한도 초과는 없었다. 모델은 매 iteration에 기능 묶음 하나(인증 → 프로필 → 게시글·태그 → 댓글 → 즐겨찾기·피드 → 전체 검증)를 구현하고 해당 Hurl 파일로 확인한 뒤 커밋했다. 마지막 메시지는 "나머지는 미구현이므로 `.ralph-done`을 만들지 않았다"는 진행 보고였다. 정본 PROMPT의 "pick the single most important remaining piece of work toward the completion criteria and do it" 문장을 한 번 실행에 작업 하나로 해석한 것으로 보인다. 랄프 루프는 이 해석에서도 매 iteration의 진척을 이어 받아 20분 상한 안에 완주시켰다.

같은 모델이 Codex CLI(EXP-054)에서는 3/3 iteration 1에 완주했다. Codex 세션 기록의 기본 지침(약 21K자)에는 "Autonomy and persistence" 절("persist until the user's intended goal is complete" 등)이 있고, pi 0.87.1 기본 시스템 프롬프트(`dist/core/system-prompt.js`)에는 해당 지침이 없다. 같은 pi에서 Sonnet 5.5(EXP-032)와 gpt-6.1-sol(EXP-034)은 3/3 iteration 1에 완주했다. 후속 [EXP-056](../056-pi-gpt61-terra-v1/report.md)(PROMPT v1)에서 같은 행동이 재현됐고, [EXP-057](../057-pi-gpt61-terra-persist/report.md)(지속 실행 지침 추가)에서 3/3 iteration 1 완주로 바뀌었다.

## 한계와 교란 변수

- 과제 1개·n=3. 3/3은 이 조건의 관측값이다.
- EXP-034(pi × gpt-6.1-sol)는 PROMPT v1이었다. 행동 차이에 PROMPT 버전이 기여했을 가능성은 EXP-056 run 1(v1에서도 iteration 1 미완주)로 낮아졌으나 n=1이다.
- 실행 중 VS Code가 3000·3001을 점유했다. 하네스가 빈 포트를 `PORT`로 주입했고 거짓 음성은 관측되지 않았다.

## 재현 자료

`runs/`의 `bench.env`, `model-specs.json`, `pi-models.json`, `preflight-report.md`·`preflight-approved`, 스크립트 사본, `phase0.md`/`phase0.log`, `metrics-*.csv`, `cost-guard.csv`, `recheck.csv`, `usage-pi.csv`, 로그(gz), `sessions.tar.gz`. 보관 전 `redact_keys.py` 마스킹 0건.
