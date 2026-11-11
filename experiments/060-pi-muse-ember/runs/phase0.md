# EXP-060 Phase 0

## 1차 (2026-11-10 KST) — FAIL, 기동 안 함

- smoke.sh: `FAIL openrouter/meta/muse-ember` — 지속 지침 탐침 요청이 OpenRouter → 제공자 Meta에서 HTTP 404 `model_not_found`.
- 직접 진단: 같은 키·같은 Meta 제공자로 `meta/muse-spark-1.3`은 정상 응답, `meta/muse-ember`·`meta/muse-ember-20261109`는 404. 키·pi 설정이 아니라 제공자 쪽 미서빙으로 판단해 중단했다.
- 하위 에이전트의 Exa 조사(2026-11-10): Meta 블로그·TechCrunch·VentureBeat 기준 2026-11-09 정식 출시, 대기열 언급 없음, Meta API ID `muse-ember-1.0`. ember 전용 404 장애 보고는 찾지 못했다.

## 2차 (2026-11-11 11:19 KST) — PASS

- OpenRouter 목록·endpoints 재확인: `meta/muse-ember` 단가·컨텍스트 변화 없음. 제공자 Google Vertex(최대 출력 524,288)가 추가됐으나 status -5·가동률 0이었다. 하네스는 Meta 고정이라 영향 없음.
- 직접 호출 1건 정상("OK", provider Meta). `bench.env`·`model-specs.json` 변경 없음 → 1차 승인 유지.
- smoke.sh: `PASS openrouter/meta/muse-ember` — 지속 지침 탐침이 지침 고유 문장을 완성해 주입 확인.
- 클라이언트: pi 0.87.1. hurl: `/opt/homebrew/bin/hurl`. 격리 플래그 `-nc -ns -ne -np -na`, `PI_KEEP_ENV=OPENROUTER_API_KEY`만 노출.
- 외부 포트: DeepSRT 127.0.0.1:3003 LISTEN(종료하지 않음, 하네스는 빈 포트 주입).
