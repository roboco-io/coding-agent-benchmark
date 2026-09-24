# Vibecoding Token Experiments

🌐 [English](README.md) · **한국어** · [日本語](README.ja.md) · [中文](README.zh-CN.md)

이 프로젝트는 **Ralph loop를 사용하는 모델·하네스 조합의 백엔드 구현 성능**을 비교한다. 목표는 작업별 품질·예산 조건에 맞는 실무 조합 선택이다. 초기 Ralph 대 Plan-then-execute 실험은 연구 이력으로 보존한다.

## 실험 방법론

- 평가 단위: **모델 × 하네스 × 추론 설정 × 제공자·연결 환경**. Claude Code와 Codex를 포함하며 조합 차이를 모델 단독 효과로 단정하지 않는다.
- 기본 과제: [RealWorld 백엔드](tasks/realworld-backend/). 신규 구현에 이어 기존 코드의 버그 수정·기능 추가·DB 마이그레이션을 평가할 계획이다.
- 주 지표: **예산 내 합격률·실패 포함 비용·시간·사람 개입량**. 토큰은 진단용이며 청구 비용과 구분한다.
- 기준: [실험 품질 규칙](docs/experiment-quality-rules.md), [정정 기록](docs/2026-09-21-corrections.md), [ROADMAP](ROADMAP.md).
- 다음 파일럿: Claude Code + Fable 5.1 대 Codex + Astra. [설계](experiments/024-practical-combinations/README.md).

## 연구 축

현재 우선순위는 모델·하네스 조합과 작업 유형별 성능이다. 전략(S)·토큰 습관(H)·언어(L)는 후속 진단 축이며 [가설 카탈로그](hypotheses/catalog.md)에 이력을 보관한다.

## 실험 결과

> 아래 표와 실험별 요약은 [`scripts/update_readme_results.py`](scripts/update_readme_results.py)가 각 실험의 `report.md`에서 자동 생성한다(영·일·중 README는 [`scripts/readme_i18n.json`](scripts/readme_i18n.json)의 번역을 사용). 실험이 끝나 `report.md`가 커밋될 때 pre-commit 훅이 자동 실행한다 (수동 실행: `python3 scripts/update_readme_results.py`).

**📊 라이브 대시보드**: [랄프 루프 모델별 완주 비교](https://roboco.io/coding-agent-benchmark/) — 최신 실험 반영: EXP-029 (2026-09-24)

> 외부 대시보드는 2026-09-21 계측 정정 미반영. 수치 판단에는 아래 보고서와 정정 기록을 사용한다.

<!-- RESULTS:BEGIN -->
<!-- 이 블록은 scripts/update_readme_results.py가 experiments/*/report.md에서 자동 생성한다. 직접 수정 금지. -->

| 실험 | 가설 | 판정 |
|------|------|------|
| [EXP-001](experiments/001-ralph-vs-plan-then-execute/report.md) Ralph loop vs Plan-then-execute | S-01: Plan-then-execute가 Ralph loop보다 동일 과제에서 토큰을 적게 쓴다 | **기각 (관측 범위 한정)** |
| [EXP-002](experiments/002-korean-vs-english/report.md) 한국어 vs 영어 파이프라인 토큰 비교 | L-01: 전 파이프라인 영어 진행이 한국어 대비 토큰 대리지표 토큰을 유의미하게 줄인다 | **보류** |
| [EXP-003](experiments/003-pte-skills/report.md) PTE + 스킬식 점진 공개 | S-02: 컨텍스트를 스킬 공식 권고(문서 200줄 이하, 스킬로 필요한 것만 로드)로 구조화하면 EXP-001 PTE 대비 토큰 대리지표 30% 이상 감소 | **기준 미달 (정정)** |
| [EXP-004](experiments/004-ralph-skills/report.md) Ralph loop + 스킬 구조 | S-03: 단일 세션 ralph에 도메인 계약 스킬을 제공하면 토큰 대리지표이 감소한다 | **보류** |
| [EXP-005](experiments/005-solar-pro3-backend/report.md) Claude Code × Upstage Solar Pro 3 백엔드 | M-01: Claude Code의 백엔드를 Solar Pro 3로 교체하면 동일 과제(RealWorld 백엔드)를 무개입 완주할 수 있고, 완주 시 총비용이 Opus 대비 유의미하게 낮다. | **보류** |
| [EXP-006](experiments/006-solar-open2-backend/report.md) Claude Code × Upstage Solar Open 2 백엔드 | M-02: Claude Code의 백엔드를 Solar Open 2로 교체하면 동일 과제(RealWorld 백엔드)를 무개입 완주할 수 있고, 완주 시 총비용이 Opus 대비 유의미하게 낮다. | **보류** |
| [EXP-007](experiments/007-solar-open2-autopsy/report.md) Solar Open 2 미완주 원인 부검 | M-03: EXP-006(Solar Open 2) 미완주는 수렴 속도 단일 병목이 아니라 복수 실패 요인(모델 행동 결함 · 실험 환경 오염 · 계측 왜곡)의 중첩이다. | **검증** |
| [EXP-008](experiments/008-solar-open2-clean-run/report.md) Solar Open 2 무오염 클린 run — 완주 검증 | M-04: 오염 제거(격리 설정)·무교란·상한 30 iter 조건에서 solar-open2는 랄프 루프로 RealWorld 백엔드(Hurl 154/154)를 무개입 완주할 수 있다 (과금 배제, 완주 여부 단일 판정). | **검증** |
| [EXP-009](experiments/009-opus5-ralph-en/report.md) Opus 5 랄프 루프 (EXP-002 en 조건, n=3) | M-05: Opus 5는 EXP-002 en 조건의 랄프 루프에서 단일 세션 완주를 재현하고, Opus 4.x 기준선(en 6–7분·API 38–54회) 대비 동등 이상의 효율을 보인다. | **부분 검증 (n=3)** |
| [EXP-010](experiments/010-opus48-vs-opus5/report.md) Opus 4.8 vs Opus 5 순수 A/B (동일 시점, 각 n=3) | M-06: 완전 동일 조건에서 Opus 5의 산출량 확대 프로파일(output·커밋 ↑)이 Opus 4.8 대비 재현되고 양 모델 모두 단일 세션 완주를 유지한다. | **검증** |
| [EXP-011](experiments/011-codex-gpt56-sol/report.md) Codex CLI × gpt-5.6-sol 리얼월드 백엔드 완주 검증 | M-07: Codex CLI(`codex exec`) 하네스에서 gpt-5.6-sol(effort medium)은 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-012](experiments/012-ccr-gpt56-sol/report.md) Claude Code × gpt-5.6-sol 백엔드(ccr) 리얼월드 백엔드 완주 검증 | M-08: Claude Code 백엔드를 ccr로 gpt-5.6-sol에 연결하면(reasoning effort medium) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-013](experiments/013-qwen38max-direct/report.md) Claude Code × qwen3.8-max 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증 | M-09: Claude Code를 DashScope Anthropic 호환 엔드포인트로 qwen3.8-max에 직결하면(thinking 기본값) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-014](experiments/014-kimi-k3-direct/report.md) Claude Code × kimi-k3 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증 | M-10: Claude Code를 Moonshot Anthropic 호환 엔드포인트로 kimi-k3에 직결하면(thinking 기본값) 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-015](experiments/015-solar-open2-direct/report.md) Claude Code × solar-open2 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증 | M-11: Claude Code를 Upstage Anthropic 호환 엔드포인트로 solar-open2에 직결하면(thinking 기본값) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-016](experiments/016-n3-replication/report.md) n=1 완주 조건 3종의 재현성 확충 (각 n=3) | M-12: EXP-011/013/014 세 조건(Codex CLI × gpt-5.6-sol, qwen3.8-max 직결, kimi-k3 직결)의 무개입 완주는 재현된다: 각 조건 추가 2 run(총 n=3)이 모두 상한 30 iteration 안에 게이트+독립 재검증 일치로 완주한다. | **검증** |
| [EXP-017](experiments/017-ko-condition/report.md) qwen3.8-max·kimi-k3 한국어 조건 랄프 루프 완주 검증 (각 n=3) | L-02: qwen3.8-max·kimi-k3(직결, thinking 기본값)는 한국어 정본 프롬프트(전 산출물 한국어 지시 포함) 조건에서도 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-018](experiments/018-solar-n3-replication/report.md) solar-open2 직결 재현성 확충 — 제공자 엔드포인트 회수로 재현 불가 | M-13: EXP-015의 solar-open2 직결 무개입 완주는 재현된다: 추가 2 run(총 n=3) 전부 30 iteration 안에 게이트(measure v4)+재검증 완주할 수 있다. | **보류** |
| [EXP-019](experiments/019-ko-native-codex/report.md) 네이티브 Opus 4.8·Opus 5·Codex×gpt-5.6-sol 한국어 조건 완주 검증 (각 n=3) | L-03: 네이티브 Opus 4.8·Opus 5(Claude Code)와 gpt-5.6-sol(Codex CLI)은 한국어 정본 프롬프트(전 산출물 한국어 지시 포함) 조건에서도 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 iteration 안에 무개입 완주할 수 있다. | **검증** |
| [EXP-020](experiments/020-solar-pro4-direct/report.md) Claude Code × solar-pro4 직결 완주 검증 (n=3) | M-14: Claude Code를 Upstage Anthropic 호환 엔드포인트로 solar-pro4에 직결하면(thinking 기본값) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다 (n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-021](experiments/021-gpt6-astra-codex/report.md) Codex CLI × gpt-6-astra 랄프 루프 완주 검증 (n=3) | M-15: Codex CLI(`codex exec`) 하네스에서 gpt-6-astra(effort medium)는 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration 안에 무개입 완주할 수 있다 (n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-023](experiments/023-fable51-ralph/report.md) Claude Code × Fable 5.1 네이티브 랄프 루프 완주 검증 (n=3) | M-17: Claude Code 네이티브 하네스에서 Fable 5.1(`claude-fable-5-1`, thinking 기본값)은 EN 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration 안에 무개입 완주할 수 있다 (n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-025](experiments/025-deepseek-direct/report.md) Claude Code × DeepSeek V4.1-Flash·V4-Pro 직결 랄프 루프 완주 검증 (EN·KO 각 n=3) | M-18: Claude Code를 DeepSeek Anthropic 호환 엔드포인트로 `deepseek-flash`(DeepSeek-V4.1-Flash)·`deepseek-v4-pro`(DeepSeek-V4-Pro-0813)에 직결하면(thinking 기본값) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 무개입 완주할 수 있다 (EN·KO 정본 각 n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-026](experiments/026-opus55-ralph/report.md) Claude Code × Opus 5.5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3) | M-19: Claude Code 네이티브 하네스에서 Opus 5.5(`claude-opus-5-5`, thinking 기본값)는 EN 정본·KO 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration·4시간 안에 무개입 완주할 수 있다 (EN·KO 각 n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-027](experiments/027-gpt6-sol-luna-codex/report.md) Codex CLI × gpt-6-sol·gpt-6-luna 랄프 루프 완주 검증 (각 n=3) | M-20: Codex CLI(`codex exec`) 하네스에서 gpt-6-sol·gpt-6-luna(effort medium)는 각각 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iter·4h 안에 완주할 수 있다 (각 n=3). | **검증** |
| [EXP-028](experiments/028-sonnet5-ralph/report.md) Claude Code × Sonnet 5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3) | M-21: Claude Code 네이티브 하네스에서 Sonnet 5(`claude-sonnet-5`, thinking 기본값)는 EN·KO 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration·4h 안에 무개입 완주할 수 있다 (EN·KO 각 n=3, 완주율 판정·과금 배제). | **검증** |
| [EXP-029](experiments/029-pi-openweight/report.md) pi coding agent × kimi-k3·qwen3.8-max·deepseek-flash 랄프 루프 완주 검증 (EN 각 n=3) | M-22: pi coding agent(`pi -p` v0.87.1)를 제공자 OpenAI 호환 엔드포인트에 직결해 `kimi-k3`·`qwen3.8-max`·`deepseek-flash`(thinking pi 기본값)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iter·4h 안에 완주할 수 있다 (EN 각 n=3, 완주율 판정·과금 배제). | **검증** |

**EXP-001 — Ralph loop vs Plan-then-execute** (기각 (관측 범위 한정))  
보관 로그의 토큰 대리지표는 PTE 1,128,420, Ralph 136,506으로 약 8.27배. 동일 품질의 비용 우위로 일반화하지 않는다. → [보고서](experiments/001-ralph-vs-plan-then-execute/report.md)

**EXP-002 — 한국어 vs 영어 파이프라인 토큰 비교** (보류)  
토큰 대리지표 KO 평균 114,605.5, EN 평균 112,463.5. 평균 차 2,142가 최대 조건 내 범위 23,033보다 작아 사전 규칙 미충족. → [보고서](experiments/002-korean-vs-english/report.md)

**EXP-003 — PTE + 스킬식 점진 공개** (기준 미달 (정정))  
토큰 대리지표 1,128,420 → 875,083으로 22.45% 감소. 사전 30% 절감 기준 미달이며 기존 검증 판정을 철회한다. → [보고서](experiments/003-pte-skills/report.md)

**EXP-004 — Ralph loop + 스킬 구조** (보류)  
스킬 토큰 대리지표 117,352 / 118,311, 기준 KO 평균 대비 +2.81%. 두 스킬 run의 범위는 959이며 효과 없음·두 배 변동 주장을 철회한다. → [보고서](experiments/004-ralph-skills/report.md)

**EXP-005 — Claude Code × Upstage Solar Pro 3 백엔드** (보류)  
solar-1 미완주(테스트 실행 0회·커밋 0회, 6/15 iteration 시점 조기 중단): 연동 스택은 검증됐으나 headless 자율 루프에서 허락-대기·컨텍스트 초과 실패 모드가 반복되어 완주 궤도에 오르지 못함. → [보고서](experiments/005-solar-pro3-backend/report.md)

**EXP-006 — Claude Code × Upstage Solar Open 2 백엔드** (보류)  
0/2 완주이나 완전 프로토콜 run은 1회뿐(open2-1은 1 iter 만에 허위 완료 신고로 자체 종료): open2-2는 15 iteration을 소진하고도 독립 검증 3/13 파일(94/154 요청)에 그쳤지만, solar-pro3에서 부재했던 자율 TDD 루프를 확립하고 단조 수렴해 "행동 계층" 병목이 자율성에서 수렴 속도로 이동했다. → [보고서](experiments/006-solar-open2-backend/report.md)

**EXP-007 — Solar Open 2 미완주 원인 부검** (검증)  
3계층 실증: ① 계측 왜곡(usage 3.07배 과대 계상 — 실제 483요청·23.3M input, 추정 ~$3.8로 Opus $6.41보다 낮음), ② 환경 오염(superpowers 훅·글로벌 CLAUDE.md 주입으로 최소 3 iteration 잠식), ③ 모델 행동 결함(선언-실행 탈락으로 커밋 0회, thinking-only 잘림 25회, 과제 이탈 환각 2건). → [보고서](experiments/007-solar-open2-autopsy/report.md)

**EXP-008 — Solar Open 2 무오염 클린 run — 완주 검증** (검증)  
**iteration 10/30에서 완주**: `.ralph-done` 생성 → 하네스 게이트 13/13 파일·154/154 요청 통과 → 실험자 독립 재검증 2회 일치. wall-clock 약 2시간 53분, 무개입·무중단, git 커밋 4회(한국어)까지 이행. 완주 시점이 EXP-006의 상한(15) 안쪽이므로 결정 변수는 상한 증가가 아니라 **환경 오염 제거·무교란**이었다. → [보고서](experiments/008-solar-open2-clean-run/report.md)

**EXP-009 — Opus 5 랄프 루프 (EXP-002 en 조건, n=3)** (부분 검증 (n=3))  
완주 조항 검증: **3/3 run 모두 iteration 1 단일 세션 완주**(9분03초–12분22초, 게이트 13/13·154/154 + 독립 재검증 각 2회, 커밋 6–7개). 효율 조항 미충족 확정: 시간 분포(8.9–12.2분)가 4.x(5.8–6.9분)와 비겹침 — 단 원인은 서빙 속도가 아니라 **일관된 산출량 증가(+62%)를 동반한 행동 프로파일 변화**로 판별됨. → [보고서](experiments/009-opus5-ralph-en/report.md)

**EXP-010 — Opus 4.8 vs Opus 5 순수 A/B (동일 시점, 각 n=3)** (검증)  
완주 6/6 (전 run iteration 1, 게이트 13/13·154/154). 사전 등록 지표 모두 충족: **output 토큰 분포 비겹침**(4.8: 29.6–37.1K vs 5: 41.1–47.9K, +37% 평균) · **git 커밋 분포 비겹침**(1–2개 vs 4–8개), 방향 EXP-009와 동일(5 > 4.8). 세대 차는 시점·계측 아티팩트가 아닌 실재 프로파일로 확정. → [보고서](experiments/010-opus48-vs-opus5/report.md)

**EXP-011 — Codex CLI × gpt-5.6-sol 리얼월드 백엔드 완주 검증** (검증)  
**iteration 1에서 완주** (게이트 13/13·154/154 + 독립 재검증 2회 일치, codex exec 5분 46초·세션 1개·커밋 3회, 무개입). → [보고서](experiments/011-codex-gpt56-sol/report.md)

**EXP-012 — Claude Code × gpt-5.6-sol 백엔드(ccr) 리얼월드 백엔드 완주 검증** (검증)  
**iteration 11/30에서 완주** (게이트 13/13·154/154 + 독립 재검증 2회 일치, 총 58분·커밋 11회). 단 iteration 2에서 스트림 스톨 1건에 하네스 수준 개입(프로세스 종료로 iteration 경계 복구, 모델 산출물 불개입)이 있었다 — 아래 프로토콜 이슈 참조. → [보고서](experiments/012-ccr-gpt56-sol/report.md)

**EXP-013 — Claude Code × qwen3.8-max 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증** (검증)  
**iteration 1에서 완주** (게이트 13/13·154/154 + 독립 재검증 2회 일치, 15분 5초·커밋 4회·개입 0, 직결 스택 트러블슈팅 0건). → [보고서](experiments/013-qwen38max-direct/report.md)

**EXP-014 — Claude Code × kimi-k3 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증** (검증)  
**iteration 1에서 완주** (게이트 13/13·154/154 + 독립 재검증 2회 일치, 21분 18초·커밋 4회·개입 0, 직결 스택 트러블슈팅 0건). → [보고서](experiments/014-kimi-k3-direct/report.md)

**EXP-015 — Claude Code × solar-open2 직결(ANTHROPIC_BASE_URL) 리얼월드 백엔드 완주 검증** (검증)  
**iteration 2에서 완주** (산출물 직접 재채점 2회 모두 13/13·154/154 일치, 58분 15초·커밋 2회. 각주: 게이트 오검 1건 — measure v3 포트 탐지 결함으로 정당 완주를 기각, EXP-010 48-1 선례 적용). → [보고서](experiments/015-solar-open2-direct/report.md)

**EXP-016 — n=1 완주 조건 3종의 재현성 확충 (각 n=3)** (검증)  
**추가 6 run 전부 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0). 원 run 포함 세 조건 완주율 **각 3/3, 합산 9/9**. → [보고서](experiments/016-n3-replication/report.md)

**EXP-017 — qwen3.8-max·kimi-k3 한국어 조건 랄프 루프 완주 검증 (각 n=3)** (검증)  
**6/6 run 전부 iteration 1 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0). 언어 준수도 성립: 전 run의 커밋 메시지·README가 한국어. → [보고서](experiments/017-ko-condition/report.md)

**EXP-018 — solar-open2 직결 재현성 확충 — 제공자 엔드포인트 회수로 재현 불가** (보류)  
모델 외적 장애(사전 등록 기준): 실험 개시 시점에 Upstage가 Anthropic 호환 엔드포인트(`/v1/messages`)와 solar-open2 hosted API를 회수해 run 자체가 불가능. 가설은 기각이 아니라 **검증 불가**. → [보고서](experiments/018-solar-n3-replication/report.md)

**EXP-019 — 네이티브 Opus 4.8·Opus 5·Codex×gpt-5.6-sol 한국어 조건 완주 검증 (각 n=3)** (검증)  
**9/9 run 전부 iteration 1 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0). 언어 준수도 전수 성립: 9 run 모두 커밋 메시지·README 한국어 (영어권 모델 gpt-5.6-sol 포함). → [보고서](experiments/019-ko-native-codex/report.md)

**EXP-020 — Claude Code × solar-pro4 직결 완주 검증 (n=3)** (검증)  
**3/3 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 모델 개입 0). 단 pro4-1은 게이트 오검(하네스 귀책)으로 루프가 연장됨 — 소급 재채점으로 유효 완주 iter 3 확정. → [보고서](experiments/020-solar-pro4-direct/report.md)

**EXP-021 — Codex CLI × gpt-6-astra 랄프 루프 완주 검증 (n=3)** (검증)  
**3/3 run 전부 iteration 1 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 세션 7분대·커밋 3–4회). → [보고서](experiments/021-gpt6-astra-codex/report.md)

**EXP-023 — Claude Code × Fable 5.1 네이티브 랄프 루프 완주 검증 (n=3)** (검증)  
**3/3 run 전부 iteration 1 완주** (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 세션 6–8분·커밋 2–4회). 보조 지표는 Opus 5(EXP-009/010) 대비 **시간·output 분포 비겹침으로 하향**(6.2–7.8분 vs 8.9–17.6분, 28.7–35.8K vs 41.1–48.4K) — Opus 5의 산출량 확대 프로파일이 Fable 5.1에서는 4.8 수준으로 되돌아감. → [보고서](experiments/023-fable51-ralph/report.md)

**EXP-025 — Claude Code × DeepSeek V4.1-Flash·V4-Pro 직결 랄프 루프 완주 검증 (EN·KO 각 n=3)** (검증)  
**12/12 run 전부 iteration 1 완주** (4조건 각 3/3, 게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 응답 model 필드 전수 일치). Flash는 EN 4.6–6.0분으로 전 조건 최속·run당 환산 약 $0.1, Pro는 12–16분·약 $0.5. 관측 범위의 사실이며 일반적 성공률·효율 우위의 확정이 아니다. → [보고서](experiments/025-deepseek-direct/report.md)

**EXP-026 — Claude Code × Opus 5.5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3)** (검증)  
**6/6 run 전부 iteration 1 완주** (EN 3/3·KO 3/3, 게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 응답 model 필드 전수 `claude-opus-5-5`). 세션 4.0–8.4분(6 run 중 5개가 4.0–4.2분)·output 18.6–28.2K로 네이티브 Claude 조건 중 최단·최저 대역이며, Opus 5(8.9–17.6분·39–49K)와 Fable 5.1(6.2–7.8분·28.7–35.8K) 분포 아래에 놓인다. 관측값이며 우위 확정이 아니다. → [보고서](experiments/026-opus55-ralph/report.md)

**EXP-027 — Codex CLI × gpt-6-sol·gpt-6-luna 랄프 루프 완주 검증 (각 n=3)** (검증)  
sol 3/3·luna 3/3 모두 iteration 1 완주 (게이트 pass + 독립 재검증 2회 13/13·154/154 일치, 응답 모델 필드 전수 일치). 채점 인프라 결함 1건(D-1)은 에이전트 개입 없이 처리했고 판정에 영향 없음. → [보고서](experiments/027-gpt6-sol-luna-codex/report.md)

**EXP-028 — Claude Code × Sonnet 5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3)** (검증)  
EN 3/3·KO 3/3 완주 (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 응답 model 필드 전수 `claude-sonnet-5`). 5 run은 iteration 1, en-1은 에이전트가 작업을 3개 iteration으로 나눠 iteration 3에 완주했다. 세션 11.2–16.8분·output 57.6–73.7K로 같은 하네스의 Opus 5.5(EXP-026)·Fable 5.1(EXP-023)보다 길고 많은 대역에 놓인다. 관측값이며 우열 확정이 아니다. → [보고서](experiments/028-sonnet5-ralph/report.md)

**EXP-029 — pi coding agent × kimi-k3·qwen3.8-max·deepseek-flash 랄프 루프 완주 검증 (EN 각 n=3)** (검증)  
세 조건 모두 3/3 완주 (게이트 pass + 독립 재검증 각 2회 13/13·154/154 일치, 개입 0, 응답 model 필드 전수 일치). 8 run은 iteration 1에 완주했고, qwen-en-1은 채점 포트가 외부 프로세스와 충돌해 iteration 5에 완주로 기록됐다(iteration 1 코드도 재채점에서 통과). 세션 시간은 flash 1.9–7.7분, kimi 9.5–9.9분, qwen 15.6–29.0분이다. 관측값이며 우열 확정이 아니다. → [보고서](experiments/029-pi-openweight/report.md)

<!-- RESULTS:END -->

### 종합 인사이트 (2026-09-21 정정 반영)

- EXP-001의 PTE/Ralph 토큰 대리지표 비율은 정정 후 8.27배다. 채점 정본이 달라 동일 품질의 비용 비교로 해석하지 않는다.
- EXP-003은 22.45% 감소로 사전 30% 기준 미달이다. EXP-004의 두 배 변동 및 효과 없음 해석은 철회했다.
- 최근 첫 iteration 완주는 해당 조건의 구현 가능성 증거다. 반복 루프의 추가 기여와 실무 유지보수 성능은 별도 평가가 필요하다.
- n=3 성공·다른 시점의 시간 차이로 일반 순위나 모델·하네스의 인과 효과를 확정하지 않는다. 구독 실행의 비용 미측정은 무료를 뜻하지 않는다.

9. **DeepSeek V4.1-Flash는 직결 표준을 무조정으로 통과하며 전 조건 최속 대역·최저 비용 프로파일을 보였다 (EXP-025).** env 3요소 치환만으로 Flash·V4-Pro 모두 EN·KO 각 3/3, 총 12/12 iter 1 완주(응답 model 필드 전수 유지). Flash EN 4.6–6.0분·run당 환산 약 $0.1(캐시 히트 입력 $0.006/M)로 Codex×sol(5.3–10.0분)보다 아래 대역이고, Pro는 12–16분·약 $0.5로 output이 1.5배. 시점·하네스 교락으로 속도·비용 우위는 확정하지 않으며, 직결 재사용성 사례(4사째)와 프로파일 기록으로 남긴다.
10. **Opus 5.5는 네이티브 하네스를 모델 ID 교체만으로 통과하며 네이티브 Claude 조건 중 최단·최저 산출 프로파일을 보였다 (EXP-026).** EN·KO 각 3/3, 총 6/6 iter 1 완주(재검증 각 2회 일치). 6 run 중 5개가 4.0–4.2분·output 약 20K로 Fable 5.1(6.2–7.8분·28.7–35.8K)과 Opus 5(8.9–17.6분·39–49K) 분포 아래에 있고, KO에서도 같은 대역을 유지했다. 8항의 해석(산출량 확대는 Opus 5 고유 특성)과 부합한다. 단 시점·CLI 버전이 다른 기준선과의 병치이며 n=3 관측이므로 속도 우위는 동시기 교차 재측정 전까지 확정하지 않는다.
11. **GPT-6 계열 3개 모델(astra·sol·luna) 모두 Codex 하네스에서 모델 ID 치환만으로 완주했다 (EXP-021·027).** sol·luna 각 3/3 iter 1 완주(응답 model 필드 전수 일치). sol은 3 run 모두 4.8–5.2분·output 약 11K로 산포가 작았고, luna는 5.4–10.0분·output 13.4–21.5K로 "fast" 포지셔닝과 달리 이 과제에서 sol보다 짧은 run이 없었다. astra(EXP-021, 7분대)와는 시점·CLI 버전이 달라 모델 차이로 단정하지 않는다. EXP-027은 신규 모델 벤치마크 절차를 묶은 `ralph-model-benchmark` 스킬의 첫 적용이다.
12. **Sonnet 5도 네이티브 하네스에서 EN·KO 모두 완주했지만, 같은 하네스의 상위 모델보다 느리고 출력이 많았다 (EXP-028).** EN 3/3·KO 3/3 완주(응답 model 필드 전수 `claude-sonnet-5`). 5 run은 iteration 1에 끝났고, en-1은 에이전트가 스캐폴딩·테스트 준비·구현을 3개 iteration으로 나눠 iteration 3에 완주했다(반려 없음). 세션 11.2–16.8분·output 57.6–73.7K로 Opus 5.5(EXP-026, 4.0–8.4분·18.6–28.2K)·Fable 5.1(EXP-023)의 관측 범위보다 위다. 측정일·Claude Code 버전이 달라 모델 단독 차이로 단정하지 않는다.
13. **제3의 하네스 pi도 변환 계층 없이 오픈웨이트 계열 3개 모델로 완주했다 (EXP-029).** pi coding agent를 각 제공자의 OpenAI 호환 엔드포인트에 직결해 kimi-k3·qwen3.8-max·deepseek-flash 각 EN 3/3, 총 9/9 완주했다(응답 model 필드 전수 일치, 하네스 트러블슈팅 0건). 8 run은 iteration 1에 끝났고, qwen-en-1은 채점 포트를 외부 프로세스가 점유해 iteration 5로 기록됐다(iteration 1 코드도 재채점 통과). 세션은 flash 1.9–7.7분, kimi 9.5–9.9분, qwen 15.6–29.0분이다. 같은 모델의 이전 Claude Code 직결 run(EXP-013·014·025)과는 하네스와 API 형식(Anthropic 호환 대 OpenAI 호환)이 함께 달라 차이를 pi의 효과로 분리하지 않는다. 이로써 랄프 루프 벤치마크는 Claude Code·Codex·pi 세 하네스에서 같은 절차로 재현된다.

## 실험 라이프사이클

1. `templates/experiment-readme.md`를 복사해 `experiments/NNN-이름/README.md`에 실험 설계 작성 (가설, 조건, 측정 방법, 성공 기준)
2. 조건별로 세션 수행, 세션 로그·측정 결과를 `runs/<조건명>/`에 저장
3. `report.md`에 토큰 차이 분석과 결론 작성 — 헤더에 `- 가설: [코드](...) — ...`와 `- **판정: ...** — <핵심 요약>` 형식을 지킨다 (README 자동 생성이 이 두 줄을 파싱)
4. `hypotheses/catalog.md`의 상태 갱신 (미실험 → 진행중 → 검증/기각)
5. `scripts/readme_i18n.json`에 새 실험의 영·일·중 번역(제목·가설·판정·요약)을 추가한다 — 누락 시 해당 언어 README에는 한국어 원문이 들어가고 스크립트가 경고한다
6. `report.md` 커밋 시 pre-commit 훅이 4개 README(ko/en/ja/zh-CN)의 실험 결과 섹션을 자동 갱신한다. 새로 클론했다면 최초 1회 `git config core.hooksPath hooks` 실행 (수동 갱신: `python3 scripts/update_readme_results.py`)

## 디렉토리 구조

```
├── ideation.md            # 최초 아이디에이션 (원본 유지)
├── ROADMAP.md             # 단계별 로드맵
├── hypotheses/catalog.md  # 가설 카탈로그 + 실험 상태 표
├── experiments/           # 실험 단위 디렉토리 (NNN-이름/)
│   └── 001-ralph-vs-plan-then-execute/
├── tasks/                 # 공통 과제 스펙 (조건 간 재사용)
│   └── realworld-backend/
├── templates/             # 실험 설계·보고서 템플릿
├── scripts/               # 측정·집계 래퍼 스크립트
└── docs/specs/            # 설계 문서
```
