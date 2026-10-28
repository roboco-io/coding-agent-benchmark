# Roadmap

우선 목표(2026-09-20 사용자 확정): **실무에서 사용할 모델·에이전트 조합 선택**. 계측 정정을 기반으로 작업 유형별 합격률·비용·시간·사람의 개입량을 비교하는 파일럿을 우선한다. 모델·도구의 원인 분리와 공개 벤치마크 확장은 후속으로 둔다.

## 현재 우선순위 (2026-09-21)

- [x] Claude 메시지 집계 중복 수정 및 중복·누계 거부·누락 회귀 검증
- [x] EXP-001~004 재집계와 판정 재검토, 보고서·카탈로그·README 4개 언어·번역 정정
- [x] 프로젝트 목적·공통 과제 완료 기준 정리
- [ ] 외부 Claude Artifact를 기존 URL로 정정 재배포 — 저장소 밖 배포물, 현재 도구에 편집 기능 없음. README에 미반영 표시
- [ ] EXP-024: Fable 5.1×Claude Code / Astra×Codex, 기존 구독만, 4과제×3회×2조합 파일럿 — 설계·schedule 작성, Fable fallback으로 Phase 0 차단(0/24)
- [ ] 공통 실행기·환경 manifest·보호된 채점기 및 정상/오류 채점 검증
- [ ] 작업별 선택표: 예산 내 합격률·실패 포함 시간·비용 상태·개입량

초기 전략 비교는 아래 연구 이력으로 보존한다. 완료 체크는 수행 이력이며 일반 효율 우위의 확정을 뜻하지 않는다.

## 연구 이력 1 — Claude Code 워크플로 전략 비교

- [x] EXP-001: Ralph loop vs Plan-then-execute (RealWorld 백엔드, Opus 고정) — S-01 관측 범위 한정 기각(대리지표 8.27배), [보고서](experiments/001-ralph-vs-plan-then-execute/report.md)
- [x] EXP-002: 한국어 vs 영어 파이프라인 토큰 비교 (L-01, KO/EN × n=2) — 보류 판정, [보고서](experiments/002-korean-vs-english/report.md)
- [x] EXP-003: PTE + 스킬식 점진 공개 (S-02) — 기준 미달(정정 -22.45%), [보고서](experiments/003-pte-skills/report.md)
- [x] EXP-004: Ralph + 스킬 구조 (S-03) — 보류(효과 없음 해석 철회), [보고서](experiments/004-ralph-skills/report.md)
- [ ] 측정 파이프라인 정리 (tokenhabit + ccusage 래퍼)

## 후속 후보 — 토큰 습관(H축) 실험

- [ ] tokenhabit H-코드 중 낭비 추정치가 큰 패턴부터 A/B 검증
- [ ] 습관 교정 가이드(전역 CLAUDE.md 규칙)의 실효성 정량화

## 연구 이력 2 — 타 도구·타 모델 비교

- [x] EXP-005: Claude Code × Upstage Solar Pro 3 백엔드 (M-01) — 보류(solar-1 미완주·조기중단), [보고서](experiments/005-solar-pro3-backend/report.md)
- [x] EXP-006: Claude Code × Upstage Solar Open 2 백엔드 (M-02) — 보류(0/2 완주, 자율 TDD 루프는 확립·병목은 수렴 속도), [보고서](experiments/006-solar-open2-backend/report.md)
- [x] EXP-007: Solar Open 2 미완주 원인 부검 (M-03) — 검증(계측 3배 과대·환경 오염·모델 결함 3계층 분해, EXP-006 비용 서사 정정), [보고서](experiments/007-solar-open2-autopsy/report.md)
- [x] EXP-008: Solar Open 2 무오염 클린 run (M-04, EXP-007 Phase B) — 검증(**iteration 10에서 완주** 13/13·154/154, 오염 제거가 결정 변수, 커밋 4회 이행), [보고서](experiments/008-solar-open2-clean-run/report.md)
- [x] EXP-009: Opus 5 랄프 루프 (M-05, EXP-002 en 조건) — 부분 검증(n=3, 3/3 iteration 1 완주·9–12분, 시간 증가는 변동 아닌 산출량 +62% 프로파일), [보고서](experiments/009-opus5-ralph-en/report.md)
- [x] EXP-010: Opus 4.8 vs 5 순수 A/B (M-06, 동시점 교차 각 n=3) — 검증(6/6 완주, output·커밋 분포 비겹침으로 프로파일 실재 확정), [보고서](experiments/010-opus48-vs-opus5/report.md)
- [x] EXP-011: Codex CLI × gpt-5.6-sol 완주 검증 (M-07, n=1) — 검증(iteration 1 완주·독립 재검증 일치, 5분 46초·커밋 3회), [보고서](experiments/011-codex-gpt56-sol/report.md)
- [x] EXP-012: Claude Code 백엔드 × gpt-5.6-sol (ccr, M-08, n=1) — 검증(iteration 11 완주·58분·커밋 11회, 스톨 1건 하네스 복구), [보고서](experiments/012-ccr-gpt56-sol/report.md)
- [x] EXP-013: Claude Code × qwen3.8-max 직결(ANTHROPIC_BASE_URL) 완주 검증 (M-09, n=1) — 검증(iteration 1 완주·15분 5초·커밋 4회, 직결 트러블슈팅 0건·usage 정상 기록), [보고서](experiments/013-qwen38max-direct/report.md)
- [x] EXP-014: Claude Code × kimi-k3 직결(ANTHROPIC_BASE_URL) 완주 검증 (M-10, n=1) — 검증(iteration 1 완주·21분 18초·커밋 4회, EXP-013 하네스 env 치환만으로 동작), [보고서](experiments/014-kimi-k3-direct/report.md)
- [x] EXP-015: Claude Code × solar-open2 직결(ANTHROPIC_BASE_URL) 완주 검증 (M-11, n=1, EXP-008 직결 완주의 정본 조건 재현) — 검증(iteration 2 완주·58분 15초, 게이트 오검 1건 v4 수정·재채점 일치), [보고서](experiments/015-solar-open2-direct/report.md)
- [x] EXP-016: n=1 완주 조건 3종(EXP-011/013/014) 재현성 확충, 각 n=3 (M-12) — 검증(추가 6 run 전부 완주, 합산 9/9·8/9 iter 1, 완주 외 지표는 변동 큼), [보고서](experiments/016-n3-replication/report.md)
- [x] EXP-017: qwen3.8-max·kimi-k3 한국어 조건 완주 검증 (L-02, 각 n=3) — 검증(6/6 iter 1, 언어 준수 전수, qwen ko +48% 시간은 방향성 기록), [보고서](experiments/017-ko-condition/report.md)
- [x] EXP-018: solar-open2 직결 재현성 확충, n=3 (M-13, EXP-015 +2 run) — 보류(제공자 엔드포인트 회수로 검증 불가, EXP-015가 마지막 시점 기록), [보고서](experiments/018-solar-n3-replication/report.md)
- [x] EXP-019: 네이티브 Opus 4.8·5 + Codex×gpt-5.6-sol 한국어 조건, 각 n=3 (L-03) — 검증(9/9 iter 1, 언어 준수 전수·EN 분포와 겹침, 언어 반전 누적 15/15), [보고서](experiments/019-ko-native-codex/report.md)
- [x] EXP-020: Claude Code × solar-pro4 직결 완주 검증, n=3 (M-14, 엔드포인트 복구 확인 후) — 검증(3/3 완주, 신고 iter 3→2→1, 게이트 오검 1건 소급 재채점으로 유효 완주 확정, 캐시 0·유효 119–258분 최장 프로파일), [보고서](experiments/020-solar-pro4-direct/report.md)
- [x] EXP-021: Codex CLI × gpt-6-astra 완주 검증 (M-15, n=3, GPT-6 출시 대응 — Anthropic 호환 엔드포인트 부재로 Codex 하네스 경로) — 검증(3/3 iter 1 완주·세션 7분대·오검 0건, sol 대비 +23–32% 시간으로 "1.9x 고속" 미재현), [보고서](experiments/021-gpt6-astra-codex/report.md)
- [x] EXP-023: Claude Code × Fable 5.1 네이티브 완주 검증 (M-17, n=3, EN 정본) — 검증(3/3 iter 1 완주·6–8분 네이티브 최속, output은 Opus 4.8 수준으로 Opus 5 확대 프로파일 미재현), [보고서](experiments/023-fable51-ralph/report.md)
- [x] EXP-025: Claude Code × DeepSeek V4.1-Flash·V4-Pro 직결 완주 검증 (M-18, EN·KO 각 n=3, 총 12 run) — 검증(12/12 iter 1 완주, Flash EN 4.6–6.0분 전 조건 최속 대역·run당 약 $0.1, Pro 12–16분, 모델 유지 12/12), [보고서](experiments/025-deepseek-direct/report.md)
- [x] EXP-026: Claude Code × Opus 5.5 네이티브 완주 검증 (M-19, EN·KO 각 n=3, 총 6 run) — 검증(6/6 iter 1 완주, 5/6 run이 약 4분·output 약 20K로 네이티브 최단·최저 대역, Opus 5 확대 프로파일 미재현), [보고서](experiments/026-opus55-ralph/report.md)
- [x] EXP-027: Codex CLI × gpt-6-sol·gpt-6-luna 완주 검증 (M-20, 각 n=3, `ralph-model-benchmark` 스킬 첫 적용) — 검증(6/6 iter 1 완주, sol 약 5분·output 약 11K로 산포 작음, luna 5.4–10.0분, 채점기 행 결함 D-1 수정), [보고서](experiments/027-gpt6-sol-luna-codex/report.md)
- [x] EXP-028: Claude Code × Sonnet 5 네이티브 완주 검증 (M-21, EN·KO 각 n=3, 스킬 `claude-native` 첫 적용) — 검증(6/6 완주, 5 run iter 1·en-1 iter 3, 세션 11.2–16.8분·output 57.6–73.7K), [보고서](experiments/028-sonnet5-ralph/report.md)
- [x] EXP-029: pi coding agent × kimi-k3·qwen3.8-max·deepseek-flash OpenAI 호환 직결 완주 검증 (M-22, EN 각 n=3, 스킬 `pi` 하네스 첫 적용) — 검증(9/9 완주, 8 run iter 1·qwen-en-1은 채점 포트 외부 점유(D-1)로 iter 5, 세션 flash 1.9–4.1분(D-3 재실행 반영)·kimi 9.5–9.9분·qwen 15.6–29.0분, Claude Code 직결과는 하네스·API 형식 교락), [보고서](experiments/029-pi-openweight/report.md)
- [x] EXP-030: pi coding agent × Opus 5.5(Anthropic API 키)·gpt-6-sol(ChatGPT OAuth) 완주 검증 (M-23, EN 각 n=3) — 검증(6/6 iter 1 완주, 세션 opus 3.1–4.9분·sol 4.2–5.6분, output opus 16.6–19.8K·sol 7.0–8.6K. 네이티브 기준선 EXP-026·EXP-027과는 에이전트·API 경로 교락), [보고서](experiments/030-pi-frontier/report.md)
- [x] EXP-031: Claude Code × Sonnet 5.5 네이티브 완주 검증 (M-24, EN·KO 각 n=3, 하네스 빈 포트 `PORT` 주입 첫 적용) — 검증(6/6 iter 1 완주, 세션 2.5–4.2분·output 15.2–20.9K·API 호출 16–24, Bash만 사용), [보고서](experiments/031-sonnet55-ralph/report.md)
- [x] EXP-032: pi coding agent × Sonnet 5.5(Anthropic API 키, 사용자 정의 모델 항목) 완주 검증 (M-25, EN n=3) — 검증(3/3 iter 1 완주, 세션 1.8–3.2분·output 10.9–14.7K, 리포 최단 세션 1분 49초), [보고서](experiments/032-pi-sonnet55/report.md)
- [x] EXP-033: Codex CLI × gpt-6.1-sol 완주 검증 (M-26, EN n=3) — 검증(3/3 iter 1 완주, 세션 6.2–9.8분·output 10.0–16.2K, Codex 로컬 메타데이터 없음(fallback)), [보고서](experiments/033-gpt61-sol-codex/report.md)
- [x] EXP-034: pi coding agent × gpt-6.1-sol(ChatGPT OAuth, 사용자 정의 모델 항목) 완주 검증 (M-27, EN n=3) — 검증(3/3 iter 1 완주, 세션 8.3–9.2분·output 12.5–13.3K), [보고서](experiments/034-pi-gpt61-sol/report.md)
- [x] EXP-035: Antigravity CLI(agy 1.3.1) × gemini-3.8-flash(effort high, Gemini API 키) 완주 검증 (M-28, EN n=3) — 검증(3/3 완주, run 3은 하네스 채점기에 의한 강제 종료로 iter 2, 세션 15.5–22.4분), [보고서](experiments/035-agy-gemini38-flash/report.md)
- [x] EXP-036: pi coding agent × gemini-3.8-flash(thinking high, Gemini API 키) 완주 검증 (M-29, EN n=3) — 검증(3/3 iter 1 완주, 세션 13.1–15.6분), [보고서](experiments/036-pi-gemini38-flash/report.md)
- [x] EXP-037: Claude Code × Haiku 5.5 네이티브 완주 검증 (M-30, EN n=3) — 검증(3/3 완주, run 1만 iter 2, 세션 5.1–7.9분, 환산 $0.06–0.16), [보고서](experiments/037-haiku55-ralph/report.md)
- [x] EXP-038: pi coding agent × Haiku 5.5 완주 검증 (M-31, EN n=3) — 검증(3/3 iter 1 완주, 세션 5.4–5.9분, 환산 $0.05–0.09), [보고서](experiments/038-pi-haiku55/report.md)
- [x] EXP-042: Claude Code × DGX Spark 탑재 가능 Qwen 3종 DashScope 직결 (M-35, EN n=3) — 보류(5/9 run 후 중단: flash 2/2·q27 1/1·coder 1/2 완주, DashScope Anthropic 엔드포인트 usage 누락으로 coder 400 반복), [보고서](experiments/042-spark-qwen-direct/report.md)
- [x] EXP-043: pi × gpt-oss-120b (Amazon Bedrock) 완주 검증 (M-36, EN n=3) — 기각(20분 상한 0/3, 포그라운드 서버 정체 반복), [보고서](experiments/043-pi-gptoss120b-bedrock/report.md)
- [x] EXP-044: pi × DGX Spark 탑재 가능 Qwen 3종 DashScope OpenAI 호환 (M-37, EN n=3) — 보류(첫 run에서 중단), [보고서](experiments/044-pi-spark-qwen/report.md)
- [x] EXP-045: pi × qwen3.8-27b DashScope OpenAI 호환 (M-38, EN n=3, 30분 상한) — 검증(3/3 iter 1 완주, 세션 8.8–12.1분, 환산 $0.22–0.24, 비용 가드 결함 D-1 수정), [보고서](experiments/045-pi-qwen38-27b/report.md)
- [x] EXP-046: pi × glm-5.3-flash Z.ai 내장 provider (M-39, EN n=3, 20분 상한) — 검증(3/3 iter 1 완주, 세션 7.1–11.0분, 환산 $0.04–0.07), [보고서](experiments/046-pi-glm53-flash/report.md)
- [x] EXP-047: pi × gemini-4-argon Gemini API, 사용자 정의 모델 항목 (M-40, EN n=3, 20분 상한, 1 run 비용 측정 선행) — 검증(3/3 iter 1 완주, 세션 12.2–16.2분, 환산 $0.85–0.89). agy는 구독 전용이라 미측정, [보고서](experiments/047-pi-gemini4-argon/report.md)
- [x] EXP-048: Claude Code × DeepSeek V4.1-Flash-1017 직결 (M-41, EN n=3, 20분 상한) — 검증(3/3 iter 1 완주, 세션 3.0–4.9분, 환산 $0.06–0.08). 별칭 `deepseek-flash`가 2026-10-17 1017로 갱신된 뒤 측정, [보고서](experiments/048-deepseek-flash-1017/report.md)
- [x] EXP-049: pi × Muse Spark Open OpenRouter, Together 고정 (M-42, EN n=3, 20분 상한) — 검증(3/3 iter 1 완주, 세션 5.2–6.7분, 청구 기록 $0.45–0.67), [보고서](experiments/049-pi-muse-spark-open/report.md)
- [x] EXP-050: pi × DeepSeek V4.1-Flash-1017 (M-43, EN n=3, 20분 상한) — 검증(3/3 iter 1 완주, 세션 4.4–4.9분, 환산 $0.05–0.07), [보고서](experiments/050-pi-deepseek-flash-1017/report.md)
- [x] EXP-051: pi × Kimi K3.1 Pro·Pro Highspeed (M-44, 조건별 EN n=3, 20분 상한) — 검증(두 조건 각 3/3 iter 1 완주, 세션 pro 7.3–10.2분·highspeed 3.7–5.2분, 환산 pro $0.45–0.60·highspeed $0.57–0.98), [보고서](experiments/051-pi-kimi-k31/report.md)
- [x] EXP-052: Claude Code × Kimi K3.1 Pro·Pro Highspeed 직결 (M-45, 조건별 EN n=3, 20분 상한) — 부분 검증(highspeed 3/3, pro 2/3 — 포트 8000 가정 대기·완료 후 백그라운드 서버 잔존으로 정체 종료 3/6 run, 환산 pro $0.67–0.93·highspeed $1.00–1.40), [보고서](experiments/052-kimi-k31-direct/report.md)
- [x] EXP-053: pi × GLM-5.3·GLM-5.3-Prime via OpenRouter (M-46, 조건별 EN n=3, 20분 상한, PROMPT v2 첫 적용) — 검증(두 조건 각 3/3 iter 1, 세션 glm-5.3 6.1–7.6분·prime 5.8–8.1분, 환산=청구 glm-5.3 $0.41–0.50·prime $0.92–1.95), [보고서](experiments/053-pi-glm53/report.md)
- [x] EXP-054: Codex × gpt-6.1-terra (M-47, EN n=3, 20분 상한, PROMPT v2) — 검증(3/3 iter 1 완주, 세션 1분 40초–2분 10초, 환산 $0.09–0.12·구독 OAuth로 청구 없음), [보고서](experiments/054-gpt61-terra-codex/report.md)
- [x] EXP-055: pi × gpt-6.1-terra (M-48, EN n=3, 20분 상한, PROMPT v2) — 검증(3/3 완주, iteration 6·5·7 — iteration마다 기능 묶음 하나, 세션 4분 3초–4분 44초, 환산 $0.11–0.15), [보고서](experiments/055-pi-gpt61-terra/report.md)
- [x] EXP-056: pi × gpt-6.1-terra PROMPT v1 재실험 (M-49) — 보류(run 1 iteration 3까지 미완주 후 사용자 지시로 중단, 반증 방향 n=1), [보고서](experiments/056-pi-gpt61-terra-v1/report.md)
- [x] EXP-057: pi × gpt-6.1-terra + 지속 실행 지침 (M-50, EN n=3, 비정본 스택) — 검증(3/3 iteration 1, 세션 1분 38초–1분 47초, 환산 $0.05–0.07), [보고서](experiments/057-pi-gpt61-terra-persist/report.md)
- [ ] 지속 실행 지침(EXP-057 `persistence.md`)이 다른 pi 모델에서도 iteration 수를 줄이는지, 정본 조건에 넣을지 검토 (EXP-055–057)
- [ ] DashScope Anthropic 호환 엔드포인트 usage 누락(EXP-042 D-1)이 EXP-013·016·017(qwen3.8-max) 토큰 수치에 준 영향 재점검
- [ ] driver가 iteration마다 `bench.env`의 상한(`MAX_SEC`)을 다시 읽도록 개선 — 실행 중 상한 변경 적용 실패 사례(EXP-043 D-3)
- [ ] DGX Spark 등급 후속: Qwen pi 재측정 중 flash·coder 남음(27b는 EXP-045 완료), Nemotron-3.5-Lightning(HF 크레딧 필요). 256GB·512GB 등급 중 GLM-5.3-Flash는 Z.ai API로 EXP-046 완료(로컬 실행은 미측정), MiniMax-M3는 키 확보 후 — [후보 조사](docs/2026-10-10-local-runnable-open-weight-models.md)
- [ ] 에이전트 실행 격리(별도 사용자·컨테이너) — 에이전트가 `ps`/`pgrep`으로 같은 머신의 다른 프로세스 비밀값을 읽은 사례(EXP-038 D-1)
- [ ] 하네스 디렉터리와 run 디렉터리 분리 — 에이전트가 채점기·이전 run 기록에 접근한 사례(EXP-035 D-1, EXP-036 D-2, EXP-029 3개 세션) 재발 방지
- [ ] Codex, Cursor 등 동일 과제 기반 도구 간 토큰 효율 비교
- [ ] 도구별 측정 방법 표준화
