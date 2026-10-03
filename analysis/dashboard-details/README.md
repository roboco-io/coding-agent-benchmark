# 대시보드 실험 상세 데이터

대시보드 성능 매트릭스에서 모델 행을 클릭하면 펼쳐지는 아코디언의 원자료다. `scripts/build_dashboard_details.py`가 이 디렉터리의 `EXP-NNN.json`(수작업 추출)과 다음 자료를 합쳐 `dashboard/details.js`를 만든다.

- 판정·가설(섹션 1): 한국어는 `experiments/*/report.md` 헤더(가설·판정 줄, 클라이언트 줄은 섹션 헤더 표기용), 영·일·중은 `scripts/readme_i18n.json`
- run별 토큰·비용(섹션 2·3): `analysis/cost/cost_all_runs.csv`
- 실험 조건·편차·행동 특징·run별 iteration/커밋(섹션 2·4·5·6): 이 디렉터리의 `EXP-NNN.json`

## EXP-NNN.json 스키마

```json
{
  "exp": "EXP-031",
  "date": "2026-09-29",
  "report": "experiments/031-sonnet55-ralph/report.md",
  "client": "Claude Code 2.1.284",
  "runs": { "<cost_all_runs.csv의 run_id>": { "iter": 1, "commits": 2 } },
  "conditions": { "ko": [["항목", "값"]], "en": [], "ja": [], "zh": [] },
  "deviations": { "ko": ["문장"], "en": [], "ja": [], "zh": [] },
  "behavior":   { "ko": ["문장"], "en": [], "ja": [], "zh": [] }
}
```

- `client`: 에이전트 클라이언트·버전. 해당 `report.md`의 `- 클라이언트:` 줄과 글자까지 같아야 하며(빌더가 불일치를 오류로 처리), 영·일·중 표기에서는 빌더가 `scripts/readme_i18n.json`의 `client_terms`로 "미기록" 등만 번역한다. 실험 간 시간 비교에 클라이언트 버전 차이가 섞이므로 필수다. 기록이 없으면 `미기록`.
- `runs`: 값을 보고서에서 확인할 수 없으면 `null`로 둔다(추정 금지).
- `conditions`: 날짜, 에이전트·CLI 버전, 연결 방식, 모델 ID, thinking/effort, 격리 여부, 상한(iteration·시간), 프롬프트 언어를 `[항목, 값]`으로. 보고서에 없는 항목은 넣지 않는다.
- `deviations`: 게이트 반려, 재실행, 보류, 포트·채점 교란, 비격리 노출 등 해석에 영향을 준 사건. 없으면 "기록된 편차 없음" 한 문장.
- `behavior`: 선택 스택, 사용 도구, iteration 분할, 서브에이전트 사용 등 보고서에 기록된 행동. 기록이 없으면 빈 배열.
- 여러 모델을 다루는 실험은 모델별 문장 앞에 모델명을 붙인다(예: "Flash: …").
- 네 언어 배열의 항목 수와 순서는 같아야 한다. 마크다운 본문에 `~`를 쓰지 않는다.

새 실험을 대시보드에 반영할 때 이 파일을 추가하고 `python3 scripts/build_dashboard_details.py`를 실행한다.
