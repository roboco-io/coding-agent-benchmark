# CLAUDE.md

이 리포는 토큰 사용 실험 관리 리포다. 구조·방법론은 [README.md](README.md), 가설 상태는 [hypotheses/catalog.md](hypotheses/catalog.md) 참조.

## 실험 종료 시 필수 절차

실험이 끝나 `experiments/*/report.md`를 작성·수정했다면 반드시:

1. report.md 헤더에 파싱 가능한 두 줄을 유지한다: `- 가설: [코드](...) — <문장>`, `- **판정: <판정>** — <핵심 요약 한 문장>`
2. `scripts/readme_i18n.json`에 새 실험의 영·일·중 번역(name·hypothesis·verdict·summary)을 추가한 뒤 `python3 scripts/update_readme_results.py` 실행 → 4개 README(README.ko.md 원문 / README.md 영어 / README.ja.md / README.zh-CN.md)의 실험 결과 섹션이 재생성된다. 번역 누락 시 한국어 원문이 들어가고 경고가 출력되므로 반드시 채운다 (pre-commit 훅도 동일 작업을 수행하지만, 훅 미설정 환경에 대비해 직접 실행 후 커밋).
3. README의 `### 종합 인사이트` 절은 자동 생성 대상이 아니다 — 새 실험이 기존 결론을 바꾸면 이 절을 4개 README 모두에서 직접 갱신한다(README.ko.md를 먼저 쓰고 en/ja/zh-CN에 번역 반영).
4. `hypotheses/catalog.md` 상태와 `ROADMAP.md` 체크박스를 갱신한다.
5. **대시보드 갱신 + README 링크 동기화**: 대시보드 정본은 `dashboard/index.html`이며 main에 push되면 GitHub Actions(`.github/workflows/pages.yml`)가 GitHub Pages(https://roboco.io/coding-agent-benchmark/)로 배포한다. 새 실험을 반영할 때는 이 파일을 수정해 커밋하고, 배포 워크플로 성공과 Pages 반영을 확인한다. 4개 README의 `## 실험 결과` 절 상단 "라이브 대시보드" 링크가 Pages URL을 가리키는지, "최신 실험 반영: EXP-NNN (날짜)" 표기를 이번 실험으로 갱신했는지 확인한다. 대시보드는 4개 언어(EN 기본·KO·JA·ZH-CN)를 내장하므로 새 실험을 반영할 때 네 언어 사전(`T.en/ko/ja/zh`)의 카드·원 수치 표·문구를 함께 갱신한다. SNS 공유용 섬네일(`dashboard/og.png`, 1200×630)은 배포 워크플로가 `scripts/render_og.sh`로 매번 대시보드 데이터에서 자동 생성하므로 커밋하지 않는다(모델 수·run 수·최신 실험 번호와 모델별 중앙값 막대가 자동으로 채워진다). 배포 후 섬네일이 새 데이터를 반영했는지 확인한다. 2026-09-23 이전에 쓰던 claude.ai 아티팩트(`137de971-...`)는 Pages 이전 안내 페이지로 바뀌었으므로 더 이상 데이터를 갱신하지 않는다.

## 랄프 루프 벤치마크 하네스 규칙 (2026-08-04 확정)

서드파티 모델을 Claude Code에 연결하는 실험(M축)은 다음을 따른다:

1. **ccr(claude-code-router) 등 변환 계층은 사용하지 않는다.** 변환 계층은 실패 모드를 구조적으로 추가한다 — tool call 인자 훼손(EXP-006 멀티 델타 유실 버그: `python3`→`3`), usage 유실(EXP-012 Phase 0 ④), transformer 체인 수동 조정(모델마다 커스텀 코드 필요), 스트림 스톨(EXP-012 iter 2), max_tokens/컨텍스트 한도 미조정 크래시(EXP-005). 완주 소요 비교는 모델 교락으로 판단 유보 — 직결도 모델에 따라 길다(EXP-008 solar-open2 직결 173분). 금지 근거는 속도가 아니라 **실패 모드와 계측 왜곡**이다.
2. **기본 연결은 제공자의 Anthropic 호환 엔드포인트 직결**(`ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`)이다. 검증된 제공자: Upstage(EXP-006 open2-2·EXP-008에서 최초 사용, EXP-015 — Bearer만 수용. **단 2026-08-05 엔드포인트 회수됨** — EXP-018 보류 참조, 재사용 전 스모크 필수), DashScope(EXP-013), Moonshot(EXP-014). 템플릿은 직전 실험 하네스에서 env 3요소(엔드포인트/키/모델 ID)만 치환한다.
3. Anthropic 호환 엔드포인트가 없는 모델은 벤치마크 대상에서 제외하거나, 부득이 변환 계층을 쓸 경우 설계 문서에 **사유와 계측 한계를 사전 등록**하고 결과 비교에서 별도 스택으로 표기한다.
4. 격리(`CLAUDE_CONFIG_DIR` 전용 + `hasCompletedOnboarding` 우회)·PROMPT 정본 byte-identical·세션 jsonl usage(message.id dedup) 계측은 기존 원칙(EXP-007/008) 그대로 유지한다.

## 환경 주의

- 새로 클론한 환경에서는 `git config core.hooksPath hooks` 1회 실행 (pre-commit 훅 활성화).
- 4개 README(README.ko.md·README.md·README.ja.md·README.zh-CN.md)의 `<!-- RESULTS:BEGIN/END -->` 마커 사이는 직접 수정 금지 (스크립트가 덮어씀). README.ko.md가 한국어 원문이며 README.md는 영어판이다.
