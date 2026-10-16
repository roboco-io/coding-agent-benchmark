# EXP-047 Phase 0

- 일시: 2026-10-16 10:21–10:31 KST
- preflight: argon 적합(1,048,576), 1 run, 최악 총액 $5. 사용자 승인 "진행" (approve.sh 기록). 이후 키 환경변수 이름만 고쳐 같은 승인을 다시 기록했다(승인 범위 변경 없음)
- 시도 경위(모두 API 호출 전 실패, 비용 0):
  1. agy 1.3.2 + `--effort high` → `--effort is not supported for model "gemini-4-argon"`
  2. agy, effort 미지정 → `model gemini-4-argon is not recognized as a known model or custom model in settings`. `agy update` 결과 최신 1.3.6이며 모델 목록에 argon 없음. agy 시도 하네스는 `~/experiments/ralph-exp047.agy-attempt`로 보존
  - 사용자 확인(대화형 agy 1.3.6 `/model`): "Gemini 4 Argon — Unavailable · currently available to Ultra and paid Pro plan subscribers" (계정 등급 Antigravity Starter Quota)
  3. pi, `PI_KEYMAP="GOOGLE_API_KEY=GEMINI_API_KEY"`(EXP-036 방식) → `No API key found for google`
  4. pi, `PI_KEEP_ENV="GEMINI_API_KEY"` → PASS (SMOKE-OK)
- 클라이언트: pi 0.87.1 (`pi --version`)
- 모델 정의: 사용자 정의 `pi-models.json`(google provider, `google-generative-ai`, maxTokens 32,768), thinking high
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1
- 노출: pi `-nc -ns -ne -np -na`로 상위 AGENTS.md/CLAUDE.md·스킬·확장·프롬프트 비노출, 환경 키는 `GEMINI_API_KEY`만(`PI_KEEP_ENV`)
