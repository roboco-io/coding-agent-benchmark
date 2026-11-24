# EXP-064 이탈 기록

- **D-1 mini45 요청 한도 초과(429) 100건 (12:18–12:26)**: `solar-mini-4-5-preview` run의 세션 기록에 `429: You've reached your API request limit` 오류 응답이 100건 있다. 1–2건씩 연속으로 나타났고 pi가 재시도해 작업을 이어 갔다. 오류 응답 직후부터 다음 응답까지의 시간 합계는 약 305초이며, 이 값에는 다음 요청의 생성 시간도 들어 있으므로 대기 시간의 상한이다. 세션 시간 11:34에는 이 대기가 포함된다. pro4·pro4c run에는 429가 없었다. 실행 중 모니터는 metrics·비용 가드만 보았기 때문에 run이 끝난 뒤 세션 점검에서 발견했다.
- **D-2 실행 중 조건 추가와 재설정 (12:26–12:27)**: mini45 run 중 사용자 지시로 `solar-pro-4-contributor` 조건(pro4c)을 추가했다. 설정 변경 전에 pro4 run이 시작되지 않도록 `done-pro4-en-1` 표시 파일을 두었고, mini45가 끝난 뒤 `phase2.sh`가 표시 파일을 지우고 setup → 재승인 → smoke(3조건 PASS, `phase2-smoke.log`) → run-all 재기동을 했다. 실험 비용 상한은 $3에서 $5로 올렸다. mini45 run은 2조건 설정에서, pro4·pro4c는 3조건 설정에서 실행됐으며 두 설정의 차이는 조건 목록과 실험 비용 상한뿐이다.
- **D-3 run 상한 근접**: pro4 run은 iteration 1(31:43, Hurl 0/13, 완료 선언 없음) 뒤 iteration 2에서 완주했고 세션 시간 38:26으로 run 상한 40분(비정본)에 근접했다. 정본 상한 20분이었다면 미완주였다.
- 하네스 경로 노출: 세 run의 세션 기록에서 하네스 디렉터리 참조는 각 run의 `app-<run>`뿐이었다.

## 3단계: mini45 추가 2 run (2026-11-24 14:38–14:51)

- **D-4 추가 실행**: 사용자 지시("미니 먼저 3회 돌리고 결과 공개해")로 mini45를 n=3으로 맞추기 위해 2 run을 추가했다. 설정은 `bench-phase3.env`(조건 mini45만, N=3, 실험 비용 상한 $2)이며, 재승인(`preflight-approved-phase3`)과 smoke(`phase3-smoke.log`, PASS) 후 실행했다. run-all은 완료된 mini45-en-1을 건너뛰었다. 로그는 `orchestrator-phase3.log`, `cost-guard-phase3.csv`.
- **D-5 mini45-en-2·en-3 요청 한도 초과(429) 각 29건**: 두 run 모두 pi 재시도로 진행했다. 오류 응답 직후부터 다음 응답까지의 시간 합계(대기 상한)는 en-2 113초, en-3 94초다.
- **D-6 mini45-en-3 하네스·이전 run 노출 (EXP-036 D-2와 같은 유형)**: en-3 에이전트가 빈 리포를 확인한 뒤 상위 하네스 디렉터리(`~/experiments/ralph-exp064`)를 탐색했다. 에이전트는 `harness-hurl`(채점용 Hurl 정본)·`hurl-last.log`·`reference-profile.json`·`driver.sh` 계열 스크립트·`pi_env.sh`·자기 실행 로그를 읽었고, 직전 run `app-mini45-en-2`의 소스 전체(`src/*.ts`, `prisma/schema.prisma`, `package.json` 등)와 git 이력을 읽었으며, `harness-hurl/*.hurl`을 자기 리포의 `api/hurl/`로 복사했다. 완주 판정은 하네스 절대 경로 채점기와 독립 재검증 2회(13/13·154/154)로 했으므로 게이트 결과는 유효하다. 그러나 이 run은 직전 run의 구현과 채점 정본을 참고했으므로, 완주·시간·토큰 모두 독립 시행 값으로 보지 않는다. 원인은 run 디렉터리가 하네스 디렉터리 안에 있는 구조(ROADMAP 후속 과제)다. en-1·en-2·pro4·pro4c의 세션 기록에서 하네스 경로 참조는 각 run의 `app-<run>`뿐이었다.
