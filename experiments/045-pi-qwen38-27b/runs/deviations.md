# EXP-045 이탈 기록

## D-1: 비용 가드가 실행 내내 추정 비용 0을 기록했다 (하네스 결함, 판정 무관)

- 관측: `cost-guard.csv` 63행이 모두 run 추정 비용 `0`이었다. 실행이 끝난 뒤 수정본으로 다시 계산한 run 추정 비용은 $0.23–0.25다.
- 원인: `bench.env`는 `MODEL_SPECS`로 단가를 줄 때 `PRICE_IN=""`처럼 예비 단가를 빈 값으로 둔다. `cost_guard.py`는 `float(os.environ.get("PRICE_IN", "nan"))`로 읽어, 변수가 빈 문자열이면 `float("")` 예외로 종료했다. `driver.sh`의 `budget_check`는 이 실패를 `|| cur=0`으로 삼켜 0으로 기록했다(fail-open). 따라서 이 실험에서 run당 $4·실험 $12 상한은 실제로 강제되지 않았다.
- 영향: 3 run 모두 약 9–12분, 추정 $0.22–0.24로 끝나 상한에 가까이 가지 않았다. 판정에는 영향이 없다. 비용 가드는 2026-10-10 도입 후 이 실험에서 처음 쓰였으므로 이전 실험에는 영향이 없다.
- 조치(2026-10-11, 스킬 `scripts/`): `cost_guard.py`는 빈 값을 미지정으로 처리한다. `driver.sh`는 추정 실패 시 0으로 보지 않고 사유를 출력해 iteration·run을 멈춘다(fail-closed, `cost-guard.err`에 오류 기록). `smoke.sh`는 조건마다 `cost_guard.py`를 한 번 실행해 오류가 나면 FAIL한다. 수정본이 기존 결함을 FAIL로 잡고 수정 후 통과하는 것을 이 실험의 하네스로 확인했다.
