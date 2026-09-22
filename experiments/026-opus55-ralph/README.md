# EXP-026: Claude Code × Opus 5.5 네이티브 랄프 루프 완주 검증 (EN·KO 각 n=3)

> 상태: **완료** (2026-09-23 07:05–07:35 KST, 판정: 검증 — [보고서](report.md)). 설계 형식은 새 실험 설계 템플릿(작성 시점에 main 미커밋 상태인 `templates/experiment-readme.md`·`docs/experiment-quality-rules.md`)을 따른다. 이 브랜치는 main에 병합되지 않은 `exp-025-deepseek-direct`에서 분기했다.

## 가설

- 가설 코드·문장: [M-19](../../hypotheses/catalog.md) — Claude Code 네이티브 하네스에서 Opus 5.5(`claude-opus-5-5`, thinking 기본값)는 EN 정본·KO 정본 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 10 iteration·4시간 안에 무개입 완주할 수 있다 (EN·KO 각 n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**(스모크). 효율 우위·요인 분리 실험으로 사후 전환하지 않는다.
- 실무 선택 질문: 신규 출시된 Opus 5.5가 기존 네이티브 조합(Opus 4.8·Opus 5·Fable 5.1)과 같은 하네스에서 후보 조합으로 성립하는가, 한국어 지시 조건에서도 성립하는가.
- 실험 단계: 탐색(조건당 n=3 완주 스모크).
- 주 지표와 사전 판정 기준: 조건(언어)별 예산 내(10 iter·4h) 게이트 + 독립 재검증 2회 일치 완주 수. **검증**: EN·KO 모두 3/3. **부분 검증**: 조건별 결과를 사실 보고. **run 단위 보류**: 모델 외적 장애(서비스 5xx·레이트 리밋 지속, 하네스 결함)로 run 불가.
- 보조 지표: 완주 iteration, 세션 시간, git 커밋 수, usage(비캐시 입력·캐시 읽기/쓰기·출력), 언어 준수(KO 조건 커밋·README 언어), 응답 `message.model`. Opus 5(EXP-009/010/019)·Fable 5.1(EXP-023)과 분포 병치·방향성 기록만 한다.

## 과제·완료 기준

- 과제: [realworld-backend](../../tasks/realworld-backend/) 신규 구현 1종. run별 빈 git 리포(`~/ralph-exp026/app-<run>/`)에 PROMPT.md만 둔다.
- 프롬프트 정본: EN `PROMPT-en.md` md5 `2c28ea6b7f16125d9b3105f5ee00b126`(EXP-010/023 EN 정본), KO `PROMPT-ko.md` md5 `fa75275f335b1552ad1baedb630c522a`(EXP-017/019 KO 정본). 조건 간 차이는 프롬프트 언어뿐이다.
- 채점 정본: `harness-hurl/` 공식 Hurl 13파일·154요청(EXP-023과 diff 무차이), 실험 대상 리포 밖(`~/ralph-exp026/`)에 보관.
- 완료 기준: 에이전트의 `.ralph-done` 신고 → 하네스 게이트(measure v4) 13/13 → 완료 후 실험자 독립 재검증 2회 일치.
- 평가 과제 분리: 미적용(완주 스모크, 과제 1종 — 기존 네이티브 실험과 동일 조건 유지).

## 조건

| 조건 | 모델·추론 설정 | 실행 도구·버전 | 작업 전략 | 연결 | 원자료 |
|------|--------------|--------------|----------|------|--------|
| en | `claude-opus-5-5`, thinking 기본값 | Claude Code 2.1.280, `claude -p --model claude-opus-5-5 --dangerously-skip-permissions` | 랄프 루프, EN 정본 | Anthropic 네이티브(OAuth 구독) | `runs/` |
| ko | 동일 | 동일 | 랄프 루프, KO 정본 | 동일 | 동일 |

## 환경·비교 범위

- 바꾸는 요인: 프롬프트 언어. 고정: 모델·하네스·채점기.
- OS·런타임: macOS Darwin 25.6.0, Node 24.14.0, Hurl 8.0.1(`/opt/homebrew/bin/hurl` 절대 경로), Claude Code 2.1.280.
- 격리: **비격리**(기본 `~/.claude`) — EXP-009/010/019/023 네이티브 기준선과 동일 조건(OAuth 키체인 제약). 따라서 사용자 글로벌 CLAUDE.md·MCP(EXP-023에서 context7 확인)·언어 설정이 run에 노출된다. 실제 노출은 세션 jsonl로 사후 확인해 보고서에 기록한다.
- 과금: 구독(OAuth). 토큰은 대리지표로만 보고하며 청구 비용으로 표현하지 않는다.
- 기준선: Opus 5·Fable 5.1 결과는 시점·CLI 버전이 다르다(동시기 재측정 없음 — 완주 스모크라 병치만).

## 반복·실행 순서·예산

- 조건당 3 run(총 6), 교차 순서 en-1 → ko-1 → en-2 → ko-2 → en-3 → ko-3, 단일 오케스트레이터 순차.
- 상한: run당 10 iteration 또는 wall-clock 4시간(iteration 경계 판정). 사람 개입 없음.
- 제외·재실행: 서비스 장애로 iteration이 API 호출 0으로 끝나면 run 보류. 게이트 기각은 채점 로그 부검 후 확정. 재채점은 원 기록을 덮어쓰지 않는다.

## 계측·분석 계획

- usage 원자료: `~/.claude/projects/-Users-dohyunjung-ralph-exp026-app-<run>/*.jsonl`(서브에이전트 포함).
- 집계: assistant `message.id` 단위 dedup(같은 ID의 usage가 다르면 오류로 보고). 고유 메시지 수·중복 수·usage 합을 보고.
- 시간: iteration start–end(claude -p 프로세스) 합.
- 분석: 조건별 완주 수/3, 시간·커밋·output 분포를 Opus 5·Fable 5.1과 병치. 동등성·우위 주장 없음.

## Phase 0 기록

- [x] 스모크: `claude -p --model claude-opus-5-5` 응답 정상, `modelUsage` 키 `claude-opus-5-5` 확인(2026-09-23).
- [x] 프롬프트 md5 대조 일치(위 해시).
- [x] 채점기: measure.sh(v4, BASE만 치환), 정상 사례(EXP-023 app-fable-1) `13,154` / 오류 사례(빈 디렉토리) `0,0`.
