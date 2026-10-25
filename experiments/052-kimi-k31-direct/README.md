# EXP-052: Claude Code × Kimi K3.1 Pro·Pro Highspeed 직결 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-25, 판정 부분 검증 — highspeed 3/3, pro 2/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-45](../../hypotheses/catalog.md) — Claude Code를 Moonshot Anthropic 호환 엔드포인트(`https://api.moonshot.ai/anthropic`)로 `kimi-k3.1-pro`·`kimi-k3.1-pro-highspeed`에 직결하면(thinking 기본값) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (조건별 EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. 같은 두 모델을 같은 날 pi 하네스로 측정한 EXP-051, 같은 엔드포인트로 kimi-k3를 측정한 EXP-014/016과 관측값을 나란히 놓되 우열은 판정하지 않는다(하네스·API 형식·시점 교락).
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. 조건별로 **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | 모델 ID | 컨텍스트 / 최대 출력 | thinking |
|---|---|---|---|
| k31pro | `kimi-k3.1-pro` | 1,048,576 / 131,072 | Claude Code 기본값 |
| k31hs | `kimi-k3.1-pro-highspeed` | 1,048,576 / 131,072(highspeed는 미확인) | Claude Code 기본값 |

- 연결: `ANTHROPIC_BASE_URL`·`ANTHROPIC_AUTH_TOKEN`(`KIMI_API_KEY`)·`ANTHROPIC_MODEL` 3요소 직결. 변환 계층 없음. 미인식 모델 200k 창 제한 해제 env 포함(스킬 기본).
- 격리: 전용 `CLAUDE_CONFIG_DIR`, run별 세션 디렉터리.
- 사양·단가는 [runs/model-specs.json](runs/model-specs.json)(EXP-051과 같은 값, 2026-10-25 확인).
- 실행 순서: 순차, run-all이 조건을 교차한다(k31pro-en-1 → k31hs-en-1 → …).

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-051과 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초다.
- 비용 상한: `RUN_BUDGET_USD=4`, `EXP_BUDGET_USD=20`. preflight 추정과 사용자 승인은 Phase 0에 기록한다.
- usage는 `scripts/aggregate_tokens.py`(message.id dedup)로 집계한다. 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-25, "진행 (Recommended)")
- [x] 스모크 PASS(usage_probe 포함, 1차는 잔액 부족으로 FAIL → 충전 후 PASS) — [runs/phase0.md](runs/phase0.md)
