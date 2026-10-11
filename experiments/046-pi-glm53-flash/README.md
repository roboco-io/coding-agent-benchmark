# EXP-046: pi × GLM-5.3-Flash (Z.ai 내장 provider) 랄프 루프 완주 검증 (EN n=3)

> 상태: **완료** (2026-10-11, 판정 검증 3/3). 결과: [report.md](report.md).

## 가설

- 가설 코드·문장: [M-39](../../hypotheses/catalog.md) — pi coding agent(`pi -p` 0.87.1)로 Z.ai의 `zai/glm-5.3-flash`(pi 내장 provider, Coding Plan 엔드포인트, thinking pi 기본값)를 돌리면 격리·무개입 랄프 루프로 RealWorld 백엔드(Hurl 13/13·154/154)를 상한 30 iteration·20분 안에 완주할 수 있다 (EN n=3, 완주율 판정·과금 배제).
- 질문 유형: **완주 가능성**. GLM 계열은 이 리포에서 처음 측정한다. 다른 실험과의 시간·토큰 차이는 모델·하네스·실행 시점·CLI 버전 조합 전체의 차이로만 서술한다.
- 판정: 게이트 통과와 독립 재검증 2회 일치(13/13·154/154)를 함께 충족한 run을 완주로 센다. **검증**은 3/3, **부분 검증**은 1–2/3, **기각**은 0/3이다. 모델 외적 장애(제공자 장애·쿼터 소진·하네스 결함)로 끝난 run은 **run 단위 보류**로 둔다.

## 조건

| 조건 | pi 모델 ID | contextWindow / maxTokens | reasoning |
|---|---|---|---|
| g53f | `zai/glm-5.3-flash` | 1,000,000 / 131,072 | true (끌 수 없음) |

- pi 0.87.1 내장 provider `zai`를 그대로 쓴다(사용자 정의 models.json 없음). 엔드포인트는 `https://api.z.ai/api/coding/paas/v4`다.
- 키는 `~/.zsh_secrets`의 `GLM_API_KEY` 값을 `ZAI_API_KEY` 이름으로만 노출한다(`PI_KEYMAP`). 다른 비밀값은 에이전트 환경에서 제거한다.
- 사양·단가 출처는 [runs/model-specs.json](runs/model-specs.json)에 있다. 공식 문서(2026-10-11 확인)와 pi 내장 데이터가 일치한다. 이 모델은 thinking을 끌 수 없다(`thinking.type=disabled` 요청 시 오류 1210, 2026-10-11 직접 확인).
- 과금: Coding Plan 엔드포인트는 플랜 쿼터에서 차감한다(https://docs.z.ai/devpack/faq). 비용 상한은 보수적으로 종량제 단가(입력 $0.15, 출력 $0.50, 캐시 읽기 $0.03 / 100만 토큰)로 추정한다.

## 과제·예산·계측

- 과제, 정본, 채점기, 완료 기준은 EXP-045와 같다(EN 정본, Hurl 13파일, 30 iteration).
- 상한은 run당 20분(`MAX_SEC=1200`), 정체 감시 300초(`STALL_SEC`)다. 반복은 3 run이며 순차로 실행한다.
- 비용 상한은 run당 추정 $2, 실험 전체 $6이다(사용자 승인 2026-10-11, [preflight-report](runs/preflight-report.md)).
- usage는 `usage_pi.py`로 집계한다(responseId dedup). 이 값은 토큰 대리지표이며 청구 비용이 아니다.

## Phase 0 기록

- [x] preflight 보고서·사용자 승인 (2026-10-11)
- [x] 스모크 PASS — [runs/phase0.md](runs/phase0.md)
