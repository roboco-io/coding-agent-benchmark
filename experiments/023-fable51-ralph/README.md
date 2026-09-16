# EXP-023 설계: Claude Code × Fable 5.1 네이티브 랄프 루프 완주 검증 (n=3)

## 배경

Anthropic의 Claude 5 세대 최상위 공개 모델 **Fable 5.1**(`claude-fable-5-1`, Mythos-class 티어)이 Claude Code에서 기본 사용 가능해졌다. 리포의 네이티브 기준선은 Opus 4.8·Opus 5(EXP-009/010, EN 정본, 각 n=3)까지이며, EXP-010은 Opus 5가 4.8 대비 **산출량 확대 프로파일**(output +37%·커밋 4–8회, 시간 9–18분)을 갖는다는 것을 확정했다. 본 실험은 같은 하네스·같은 EN 정본으로 Fable 5.1의 무개입 완주를 검증하고, 프로파일(output·커밋·시간)이 Opus 5 대비 어느 방향으로 이동하는지 병치 기록한다.

## 가설

[M-17](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Fable 5.1(`claude-fable-5-1`, thinking 기본값)은 EN 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration 안에 무개입 완주할 수 있다 (n=3, 완주율 판정·과금 배제).

## 조건 (사전 고정)

- **PROMPT**: EXP-010 EN 정본 byte-identical (md5 `2c28ea6b7f16125d9b3105f5ee00b126`)
- **하네스**: EXP-019 `driver-opus.sh`(EXP-010 이식본) 이식 — 치환은 BASE 경로(`~/ralph-exp023`)와 주석뿐, 모델은 인자(`claude-fable-5-1`). 상한 10 iter, `.ralph-done` 게이트, `--dangerously-skip-permissions`, 개입 금지
- **비격리(기본 `~/.claude`)** — EXP-009/010/019 네이티브 기준선과 동일 조건 (OAuth 키체인 제약, EXP-009 한계 절 계승). 글로벌 CLAUDE.md·플러그인이 노출되는 것도 기준선과 동일하게 수용
- **채점**: measure v4 게이트 (EXP-021판 이식, `HURL_BIN=/opt/homebrew/bin/hurl` 절대 경로 고정) + 완료 후 독립 재검증 2회
- **실행**: 순차 3 run (fable-1 → fable-2 → fable-3), 단일 오케스트레이터(caffeinate + nohup). 동시 실행 금지
- **usage**: `~/.claude/projects/-Users-dohyunjung-ralph-exp023-app-fable-N/` 세션 jsonl에서 assistant `message.id` dedup 후 합산. 스모크 세션(`-Users-dohyunjung-ralph-exp023`)은 제외
- **판정 기준 (사전 등록)**: 검증(3/3 완주) / 부분 검증(1–2/3 — run별 사실 보고) / run 단위 보류(모델 외적 장애)
- **보조 지표 (사전 등록)**: output 토큰·git 커밋·wall-clock을 EXP-010 Opus 5(n=3: output 41.1–47.9K·커밋 4–8·9.4–17.6분) 및 Opus 4.8과 병치. 분포 비겹침이면 "프로파일 이동"으로 서술, 겹치면 "동급"으로 서술. 시점 차이(약 7주)로 원인 분해는 불가 — 방향성 기록만
- **과금 배제**: 완주율 단일 판정. 구독 플랜 경유라 달러 산출 없음

## 리스크

- Fable 5.1은 상위 티어 — 구독 사용량 한도 도달(rate limit) 시 iteration 로그에 기록, 루프 복원력으로 흡수. run 단위 장애만 보류
- 실험 조율 세션(이 리포 작업)도 동일 계정·동일 모델을 사용 중 — 사용량 한도를 공유하므로 run 중 조율 세션의 활동은 최소화
- 비격리 조건이라 기준선과 동일하게 글로벌 CLAUDE.md 규칙(간결 출력 등)이 노출됨 — 기준선(EXP-010 당시 글로벌 설정)과 내용이 달라졌을 수 있어 완전 동형은 아님(명기)

## Phase 0 (기동 전 스모크)

- `claude -p ... --model claude-fable-5-1` 스모크 SMOKE-OK 정확 출력 → [runs/phase0.md](runs/phase0.md)
- PROMPT md5 대조 일치, driver/measure diff는 주석·BASE 경로뿐, 포트 8000 비점유, metrics 3개 사전 생성

## 후속

- 완주 시 대시보드 아티팩트(랄프 루프 모델별 완주 비교, `137de971-…`)에 fable 조건 추가 — 기존 URL 재배포
- README 실험 결과 재생성(`scripts/update_readme_results.py`), catalog·ROADMAP 갱신
