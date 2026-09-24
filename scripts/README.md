# scripts

측정·집계용 최소 래퍼 스크립트 디렉토리.

## 집계 v2 (2026-09-21)

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/aggregate_tokens.py --json experiments/00[1-4]-*/runs/*/logs
python3 scripts/update_readme_results.py
```

각 디렉터리는 하나의 run이며 최상위 JSONL만 읽는다. run 내 `message.id`가 같고 usage가 같으면 한 번만 센다. 같은 ID의 다른 usage, ID 누락, 잘못된 JSON, 빈 입력 및 Codex 누계 형식은 오류다. 누락 필드는 `null`, 실제 0은 `0`으로 남는다. 일부 메시지의 usage가 없으면 전체 토큰 총계는 미측정으로 처리한다.

출력 `messages`는 고유 usage 메시지 수, `usage_rows`는 중복 포함 행 수다. `duplicates`, `missing_usage`, 필드별 `missing_fields`를 함께 기록한다. `sessions`는 로그 파일 수이며 누락된 세션의 존재를 검증하지 않는다. 동일 usage의 서로 다른 ID는 별도 요청이다.

`billable` 출력은 `token_proxy`로 대체했다. input + output + cache creation을 더한 대리지표이며 실제 청구 비용이 아니다. 캐시 읽기는 별도 보존하고 reasoning 세부값을 output에 추가하지 않는다. Codex는 별도 누계 어댑터가 필요하다.

[정정 기록](../docs/2026-09-21-corrections.md)과 [재집계 JSON](../docs/2026-09-21-usage-corrections.json)에 범위·명령·원자료 해시를 기록했다.

## 도구 원칙

원칙: 직접 구현하지 않고 기존 도구를 래핑한다.

- 토큰 집계: [ccusage](https://github.com/ryoppippi/ccusage)
- 습관 패턴 스캔: [tokenhabit](https://github.com/epoko77-ai/tokenhabit) `habit_scan.py`

여기에는 "실험 구간의 세션 로그 추출"과 "조건 간 비교 표 생성"처럼 위 도구가 직접 제공하지 않는 접착 코드만 둔다.

## 파일럿 사전 점검

`python3 scripts/pilot_preflight.py experiments/024-practical-combinations/manifest.json`

오프라인 검사이며 모델을 호출하지 않는다. 모델 전환, 실패·usage 누락, 구독 overage 및 남은 준비 항목이 있으면 종료 코드 2다. Astra의 compact stdout은 served model을 증명하지 못하므로 별도 검증 전 통과시키지 않는다. `schedule()`은 seed를 고정해 과제별 두 조합을 연속 배치하고 전체 선행 순서를 균형화한다. 이 도구는 공통 실행기를 대신하지 않는다.
