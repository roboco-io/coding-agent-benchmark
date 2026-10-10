# EXP-042: Claude Code × DGX Spark 탑재 가능 Qwen 3종 직결 랄프 루프 완주 검증 (EN n=3)

> 상태: **중단** (2026-10-10 15:41, 사용자 결정). 4/9 run 완료 후 중단. 원인: DashScope Anthropic 호환 엔드포인트의 usage 과소 보고로 자동 압축이 일어나지 않아 coder 조건이 입력 한도에 닿음 — [runs/deviations.md](runs/deviations.md). 같은 모델은 [EXP-044](../044-pi-spark-qwen/README.md)(pi)로 측정한다. 설계 고정 2026-10-10. 후보 선정 근거: [로컬 실행 가능 오픈 웨이트 모델 조사](../../docs/2026-10-10-local-runnable-open-weight-models.md).

## 가설

- 가설 코드·문장: [M-35](../../hypotheses/catalog.md) — Claude Code(`claude -p` 2.1.296)를 DashScope Anthropic 호환 엔드포인트로 DGX Spark 1대(128GB)에 올릴 수 있는 크기의 오픈 웨이트 Qwen 3종(`qwen3.8-flash`, `qwen3-coder-next`, `qwen3.8-27b`, thinking 기본값)에 직결하면, 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 완주할 수 있다 — EN n=3, 완주율 판정·과금 배제.
- 질문 유형: **완주 가능성**(스모크). 실무 조합 효율·요인 효과 분리는 목적이 아니며 사후에 바꾸지 않는다.
- 실무 선택 질문: 로컬 장비 한 대(DGX Spark)에 올릴 수 있는 크기의 공개 가중치 모델이 이 과제를 무개입으로 끝낼 수 있는가. 이 실험은 클라우드 API로 실행하므로 로컬 서빙의 속도·양자화 품질 저하는 측정하지 않는다.
- 실험 단계: 탐색(조건당 n=3).
- 주 지표와 사전 판정 기준: 조건별 예산 내(30 iter·4h) 게이트 + 독립 재검증 2회 일치 완주 수. **검증**: 3조건 모두 3/3. **부분 검증**: 일부 조건만 3/3 또는 1–2/3 — 조건별로 사실 보고. **기각**: 3조건 모두 0/3. **run 단위 보류**: 모델 외적 장애(제공자 5xx·429 지속, 하네스 결함)로 run 불가.
- 보조 지표: 완주 iteration, 세션 시간, 커밋 수, usage(비캐시 입력·캐시 읽기/쓰기·출력), 실제 응답 `message.model`. 기존 직결 조건(EXP-013 qwen3.8-max, EXP-025 DeepSeek)과는 방향성 병치만 한다.

## 과제·완료 기준

- 과제: [realworld-backend](../../tasks/realworld-backend/) 신규 구현 1종. run별 빈 git 리포, PROMPT.md만 존재.
- 프롬프트 정본: `ralph-model-benchmark` 스킬 `assets/` EN 정본(setup.sh가 해시 검증). KO 미실행(2026-10-03 사용자 지시: 기본 EN만).
- 채점 정본: 스킬 `assets/` Hurl 13파일·154요청, 실험 대상 리포 밖(`~/experiments/ralph-exp042/`)에 보관. 채점기 `/opt/homebrew/bin/hurl` 8.0.1.
- 완료 기준: `.ralph-done` 신고 → 하네스 게이트 13/13 → 실험자 독립 재검증 2회 `13,154` 일치.

## 조건

| 조건 | 모델 ID (DashScope) | 공개 가중치 (HF) | 실행 도구 | 제공자·연결 |
|------|------|------|------|------|
| flash | `qwen3.8-flash`, thinking 기본값 | `Qwen/Qwen3.8-Flash-Next` 125B/활성 6B (+51B n-gram 임베딩), Qwen Community 1.0 | Claude Code 2.1.296 `claude -p --dangerously-skip-permissions` | DashScope `https://dashscope-intl.aliyuncs.com/apps/anthropic` 직결 |
| coder | `qwen3-coder-next`, thinking 기본값 | `Qwen/Qwen3-Coder-Next` 79.7B/활성 3B, Apache-2.0 | 동일 | 동일 |
| q27 | `qwen3.8-27b`, thinking 기본값 | `Qwen/Qwen3.8-27B` 27.8B dense, Apache-2.0 | 동일 | 동일 |

- API 모델과 공개 가중치의 동일성: `qwen3-coder-next`·`qwen3.8-27b`는 이름이 공개 가중치와 일치한다. `qwen3.8-flash`가 `Qwen3.8-Flash-Next`와 같은 가중치인지는 공식 확인되지 않았다(2차 자료 1건). 결과는 "DashScope가 서비스하는 해당 ID"의 결과로 기록한다.
- Spark 탑재 판정은 조사 문서의 추정이다. `qwen3.8-flash`(NVFP4 약 99GiB + 임베딩)는 빠듯하다.

## 환경·비교 범위

- 바꾸는 요인: 모델. 고정: 하네스·엔드포인트·채점기·프롬프트. 차이는 "DashScope 직결 Qwen 조합 간 차이"로만 해석한다.
- OS·런타임: macOS Darwin 25.6.0, Node 24.14.0, Hurl 8.0.1.
- 격리: 스킬 setup.sh의 `claude-direct` 하네스(전용 `CLAUDE_CONFIG_DIR`, onboarding 우회, `env -u ANTHROPIC_API_KEY`, `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`, `API_TIMEOUT_MS=600000`, 빈 포트 `PORT` 주입). 실제 노출된 지침·스킬·MCP는 Phase 0에 기록.
- 과금: DashScope 종량 API. 공개 단가로 환산 추정만 하며 청구액은 미측정. 단가는 보고 시점에 출처와 함께 확인한다.
- 기준선: 동시기 재측정 없음(완주 스모크라 불필요).

## 반복·실행 순서·예산

- 반복: 조건당 3 run, 총 9 run. 실행 순서는 회차 교차(flash-1 → coder-1 → q27-1 → … → q27-3), 단일 오케스트레이터 순차, 다른 실험과 동시 실행 금지.
- 상한: run당 30 iteration 또는 4시간(`MAX_SEC=14400`, iteration 중에도 적용), 정체 900초(`STALL_SEC`).
- 비용 상한: 9 run 합계 환산 $20 초과 시 중단 검토(사후 집계).
- 사람 개입: 없음. 하네스 수준 복구만 허용하며 발생 시 `runs/deviations.md`에 기록.
- 제외·재실행: 제공자 장애로 iteration이 API 호출 0건으로 끝나면 run 보류(재실행 없음). 게이트 기각은 채점기 로그 부검 후 확정.

## Ralph 정책

- 매 iteration 새 `claude -p` 세션, 코드·git 유지, 고정 PROMPT만 재투입(게이트 결과 미전달).

## 계측·분석 계획

- usage: `python3 scripts/aggregate_tokens.py --json sessions-<run>/*/` (message.id dedup v2). 토큰 대리지표이며 청구 비용 아님.
- 시간: iteration 세션 시간 합과 run wall-clock 병기.
- 분석: 조건별 완주 수/3, 완주 iteration, 시간·output 분포. 동등성·우위 주장 없음.

## Phase 0 기록

- [ ] 제공자 스모크(3모델 `/v1/messages` 200·응답 model 일치·usage 필드)
- [ ] 프롬프트·채점 해시, 채점기 정상/오류 사례
- [ ] 클라이언트 버전, 노출 지침·스킬·MCP
- 증거: [runs/phase0.md](runs/phase0.md)
