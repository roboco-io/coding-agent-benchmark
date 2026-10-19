# EXP-050: pi × DeepSeek V4.1-Flash-1017 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-19, 판정 검증 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-43](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 DeepSeek OpenAI 호환 엔드포인트의 `deepseek-flash`(2026-10-17부터 DeepSeek-V4.1-Flash-1017, pi 내장 provider, thinking high)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. 같은 별칭을 9월 가중치로 pi에서 측정한 EXP-029 flash 조건, 같은 1017 가중치를 Claude Code 직결로 측정한 EXP-048과 관측값을 나란히 놓되 우열은 판정하지 않는다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. **검증** 3/3, **부분 검증** 1–2/3, **기각** 0/3. 모델 외적 장애(제공자 장애·하네스 결함·비용 상한 도달)로 끝난 run은 **run 단위 보류**.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | thinking |
|---|---|---|---|
| flash1017 | `deepseek/deepseek-flash` | 1,000,000 / 384,000 (pi 내장 카탈로그) | high |

- pi 0.87.1 내장 deepseek provider(api `openai-completions`, thinkingFormat `deepseek`, `requiresReasoningContentOnAssistantMessages`)를 그대로 쓴다. 사용자 정의 models.json은 없다.
- thinking high 고정 이유: EXP-029 flash 세션 기록에서 pi 기본값(medium)이 high로 조정되어 실행된 것을 확인했다(`thinking_level_change` → `high`). 같은 수준을 명시해 EXP-029와 맞춘다.
- 날짜가 붙은 모델 ID는 API에 없다. 2026-10-19 시점 별칭 `deepseek-flash`가 1017을 가리킨다는 근거는 EXP-048과 같다(제공자 changelog·가격 페이지, 2026-10-18 확인).
- 키는 `~/.zsh_secrets`의 `DEEPSEEK_API_KEY`만 노출한다(`PI_KEEP_ENV`).
- 사양·단가는 [runs/model-specs.json](runs/model-specs.json): 100만 토큰당 입력 $0.30, 출력 $1.20, 캐시 읽기 $0.006(피크, EXP-048과 같은 값).

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-049와 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초다.
- 비용 상한: `RUN_BUDGET_USD=1`, `EXP_BUDGET_USD=3`, 최악 총액 $3. preflight 추정(캐시 할인 없음) run당 p50 $0.70. 사용자 승인 2026-10-19("진행 (Recommended)").
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-19)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
