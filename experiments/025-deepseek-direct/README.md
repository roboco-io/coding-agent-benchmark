# EXP-025: Claude Code × DeepSeek V4.1-Flash·V4-Pro 직결 랄프 루프 완주 검증 (EN·KO 각 n=3)

> 상태: **진행중** (2026-09-21 기동). 설계 형식은 새 실험 설계 템플릿(작성 시점에 main 미커밋 상태인 `templates/experiment-readme.md`·`docs/experiment-quality-rules.md`)을 따른다. 링크는 해당 작업이 main에 병합된 뒤 유효해진다.

## 가설

- 가설 코드·문장: [M-18](../../hypotheses/catalog.md) — Claude Code를 DeepSeek Anthropic 호환 엔드포인트로 `deepseek-flash`(DeepSeek-V4.1-Flash)·`deepseek-v4-pro`(DeepSeek-V4-Pro-0813)에 직결하면(thinking 기본값) 격리·무교란 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·4시간 안에 무개입 완주할 수 있다 — EN 정본·KO 정본 각 n=3, 완주율 판정·과금 배제.
- 질문 유형: **완주 가능성**(스모크). 실무 조합 효율·요인 효과 분리는 목적이 아니며, 사후에 효율 우위 실험으로 바꾸지 않는다.
- 실무 선택 질문: DeepSeek 최신 세대(V4.1)가 기존 직결 3사(qwen·kimi·solar)와 같은 하네스에서 후보 조합으로 성립하는가.
- 실험 단계: 탐색(조건당 n=3 완주 스모크).
- 주 지표와 사전 판정 기준: 조건(모델×언어)별 예산 내(30 iter·4h) 게이트 + 독립 재검증 2회 일치 완주 수. **검증**: 4조건 모두 3/3. **부분 검증**: 조건별 3/3 여부를 사실 보고. **run 단위 보류**: 모델 외적 장애(제공자 5xx·429 지속, 하네스 결함)로 run 불가.
- 보조 지표: 완주 iteration, wall-clock, git 커밋 수, usage(비캐시 입력·캐시 읽기/쓰기·출력), 언어 준수(KO 조건 커밋·README 언어), 실제 응답 model 필드. 기존 직결 조건(EXP-013/014/016/017/020)과 분포 병치·방향성 기록만.

## 과제·완료 기준

- 과제 정의: [realworld-backend](../../tasks/realworld-backend/) 신규 구현 1종.
- 초기 코드·DB: run별 빈 git 리포(`~/ralph-exp025/app-<run>/`), PROMPT.md만 존재.
- 프롬프트 정본·해시: EN `PROMPT-en.md` md5 `2c28ea6b7f16125d9b3105f5ee00b126`(EXP-010 EN 정본), KO `PROMPT-ko.md` md5 `fa75275f335b1552ad1baedb630c522a`(EXP-017 KO 정본). 조건 간 차이는 프롬프트 언어뿐.
- 채점 정본·예상 테스트 수: `harness-hurl/` 공식 Hurl 13파일·154요청(EXP-020/023과 diff 무차이), 실험 대상 리포 밖(`~/ralph-exp025/`)에 보관.
- 완료 기준: 에이전트의 `.ralph-done` 신고 → 하네스 게이트(measure v4) 13/13 → 완료 후 실험자 독립 재검증 2회 일치. 자기 완료 선언만으로 완주로 보지 않는다.
- 평가 과제 분리: 미적용 — 완주 스모크이므로 조정용/최종 과제 분리와 숨긴 테스트를 두지 않는다(사유: 과제 1종, 기존 직결 실험과 동일 조건 유지).

## 조건

| 조건 | 모델·리비전·추론 설정 | 실행 도구·버전 | 작업 전략 | 제공자·연결 계층 | 원자료 |
|------|--------------------|--------------|----------|----------------|--------|
| flash-en | `deepseek-flash` (DeepSeek-V4.1-Flash, 2026-09-10 출시), thinking 기본 ON(effort high) | Claude Code 2.1.273, `claude -p --dangerously-skip-permissions` | 랄프 루프, EN 정본 | DeepSeek `https://api.deepseek.com/anthropic` 직결(Bearer) | `runs/` metrics·usage·로그 |
| flash-ko | 동일 | 동일 | 랄프 루프, KO 정본 | 동일 | 동일 |
| pro-en | `deepseek-v4-pro` (DeepSeek-V4-Pro-0813), thinking 기본 ON | 동일 | 랄프 루프, EN 정본 | 동일 | 동일 |
| pro-ko | 동일 | 동일 | 랄프 루프, KO 정본 | 동일 | 동일 |

## 환경·비교 범위

- 바꾸는 요인: 모델(flash/pro)·프롬프트 언어(EN/KO). 고정: 하네스·엔드포인트·채점기·프롬프트 본문. 모델 간 차이는 "DeepSeek 조합 간 차이"로만 해석하며 기존 직결 3사와는 시점·CLI 버전이 달라 방향성 병치만 한다.
- OS·런타임: macOS Darwin 25.6.0, Node 24.14.0, Hurl 8.0.1 (`/opt/homebrew/bin/hurl` 절대 경로 고정), Claude Code 2.1.273.
- 설정 스냅샷: 전용 `CLAUDE_CONFIG_DIR=~/ralph-exp025/claude-config`에 `.claude.json`(hasCompletedOnboarding 우회, EXP-020 사본)만 둠 — 글로벌 CLAUDE.md·스킬·MCP·훅 노출 없음. `env -u ANTHROPIC_API_KEY`로 실 계정 키 제거. run별 `projects/`를 `claude-config-projects-<run>`으로 격리 이동.
- 실제 노출 확인: Phase 0 스모크 세션 jsonl에 MCP·스킬 로드 흔적 없음(격리 config에 settings 파일 없음).
- 실제 응답 모델: 세션 jsonl assistant `message.model`을 run별 전수 집계해 요청 ID와 일치 확인. 불일치 발견 시 해당 run 보류.
- 과금: API 종량(구독 아님). 공개 단가(2026-09-21 `api-docs.deepseek.com/quick_start/pricing`, 피크 기준 1M당 flash 캐시 히트 $0.006·미스 $0.30·출력 $1.20 / v4-pro $0.044·$1.32·$3.96)로 **환산 추정치**만 기록, 실제 청구액은 미측정.
- DeepSeek 공식 Claude Code 권장 설정(`deepseek-flash[1m]` 접미사, `CLAUDE_CODE_EFFORT_LEVEL=max`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW=786432`)은 **적용하지 않음** — 기존 직결 하네스(env 3요소 치환 + `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`)와의 동등성 우선. 이탈로 기록.
- 캐시·공유 한도: DeepSeek 자동 컨텍스트 캐시(usage에 cache_read/creation 계상 확인). 동시성 한도 flash 2500·pro 500 — 순차 실행이라 영향 없음. 통제 불가 항목: 제공자 서빙 상태·피크/오프피크 단가.
- 기준선: 직결 3사(EXP-013/014/016/017/020)는 2026-08 실행·CLI 구버전 — 동시기 재측정 없음(완주 스모크라 불필요, 명기).

## 반복·실행 순서·예산

- 반복 수: 조건당 3 run(총 12) — 완주 가능성 탐색용. 효과 크기 추정 목적 아님.
- 실행 순서(교차): flash-en-1 → pro-en-1 → flash-ko-1 → pro-ko-1 → (2회차) → (3회차). 단일 오케스트레이터 순차, 동시 실행 금지.
- run 초기화: 빈 리포·빈 세션(projects 이동)·포트 정리(measure cleanup).
- 상한: run당 30 iteration 또는 wall-clock 4시간(먼저 도달하는 쪽, driver가 iteration 경계에서 판정). 비용 상한: 6 run 합계 환산 추정 $20 초과 시 캠페인 중단 검토(사후 집계).
- 사람 개입: 없음. 하네스 수준 복구(프로세스 종료 등)만 허용하며 발생 시 로그·보고서에 기록.
- 실패·제외·재실행: 제공자 장애로 iteration이 0 API 호출로 끝나면 run 보류(재실행 없음). 게이트 기각은 채점기 로그 부검 후 확정. 재채점은 원 기록을 덮어쓰지 않는다.

## Ralph 정책

- iteration 세션: 매 iteration 새 `claude -p` 세션, 코드·git은 유지, 세션 메모리 없음.
- 피드백: 고정 PROMPT만 재투입(게이트 결과 미전달, 기존 실험과 동일).
- 최종 채점: 완료 후 실험자가 measure.sh로 독립 재검증 2회.
- 지표: 첫 iteration 합격 여부, 후속 iteration 합격, 소요.

## 계측·분석 계획

- usage 원자료: `claude-config-projects-<run>/**/*.jsonl` (run당 세션 1개 이상). 서브에이전트 호출 포함(같은 projects 디렉토리), 실패·재시도 포함.
- 집계기: `runs/parse_usage.py`(EXP-013 계열 — assistant `message.id` 단위 dedup, 같은 id 재등장 시 마지막 기록). 고유 메시지 수·usage 합산을 보고.
- 토큰 정의: input(비캐시)·cache_read·cache_creation·output(DeepSeek는 thinking 토큰을 output에 포함 — 별도 가산 없음).
- 비용 정의: 공개 단가 환산 추정(피크 기준), 실제 청구 미측정.
- 시간 정의: iteration start~end(claude -p 프로세스) 합 + 게이트 채점 시간은 별도. 보고서에 세션 시간·run 전체 wall-clock 병기.
- 분석: 조건별 완주 수/3, 완주 iteration, 시간·커밋·output 분포를 기존 직결 조건과 병치. 동등성·우위 주장 없음.

## Phase 0 기록

- [x] 제공자 스모크: `/anthropic/v1/messages` Bearer·x-api-key 모두 200, 응답 content에 thinking 블록 존재, usage 캐시 필드 계상. `claude -p` 격리 config 스모크 양 모델 SMOKE-OK, 세션 jsonl `message.model`이 요청 ID와 일치(flash 2/2, pro 2/2).
- [x] 프롬프트·초기 상태·설정: md5 대조 일치, 격리 config `.claude.json`만 존재.
- [x] 채점기: measure.sh(EXP-021 v4, BASE만 치환), 정상 사례(EXP-023 app-fable-1) 13,154 / 오류 사례(빈 디렉토리) 0,0 확인. Hurl 13파일.
- [x] 원자료 경로: `~/ralph-exp025/` → 종료 후 `runs/`로 이식(metrics·usage CSV·로그 gz·orchestrator/driver 로그).
- 증거: [runs/phase0.md](runs/phase0.md)
