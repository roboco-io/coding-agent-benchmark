# EXP-049 Phase 0

- 일시: 2026-10-18 23:3x–23:41 KST
- 모델 확인: OpenRouter `GET /api/v1/models`에 `meta/muse-spark-open`("Meta: Muse Spark Open", 2026-10-16 등록, context 1,048,576). 엔드포인트 5곳(Modal·Together·Nebius fp4·Fireworks·BaseTen fp4), 단가 동일. pi 0.87.1 내장 목록에는 없음(muse-spark-1.1–1.3·contributor·glimmer-30b만) → 사용자 정의 `pi-models.json`
- 라우팅: `openRouterRouting {only: ["together"], allow_fallbacks: false}`. run 1 첫 응답 generation 기록 provider_name Together, model `meta/muse-spark-open-20261015`. 사후 전수 대조(3 run 168 호출) 모두 Together·같은 스냅샷
- preflight: musespark 적합(1,048,576), 3 run, 상한 run당 $3·실험 $6, 최악 총액 $6. 사용자 승인 "바로 3 run (Recommended)" (approve.sh 기록)
- smoke: PASS (SMOKE-OK). smoke는 세션 기록을 남기지 않아 라우팅은 run 1에서 확인
- 클라이언트: pi 0.87.1 (`pi --version`)
- 노출: pi `-nc -ns -ne -np -na`, 환경 키는 `OPENROUTER_API_KEY`만(`PI_KEEP_ENV`)
- 채점기: `/opt/homebrew/bin/hurl` 8.0.1
- 외부 포트: DeepSRT 127.0.0.1:3003 LISTEN(종료하지 않음)
