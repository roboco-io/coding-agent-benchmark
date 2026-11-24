# EXP-064 이탈 기록

- **D-1 mini45 요청 한도 초과(429) 100건 (12:18–12:26)**: `solar-mini-4-5-preview` run의 세션 기록에 `429: You've reached your API request limit` 오류 응답이 100건 있다. 1–2건씩 연속으로 나타났고 pi가 재시도해 작업을 이어 갔다. 오류 응답 직후부터 다음 응답까지의 시간 합계는 약 305초이며, 이 값에는 다음 요청의 생성 시간도 들어 있으므로 대기 시간의 상한이다. 세션 시간 11:34에는 이 대기가 포함된다. pro4·pro4c run에는 429가 없었다. 실행 중 모니터는 metrics·비용 가드만 보았기 때문에 run이 끝난 뒤 세션 점검에서 발견했다.
- **D-2 실행 중 조건 추가와 재설정 (12:26–12:27)**: mini45 run 중 사용자 지시로 `solar-pro-4-contributor` 조건(pro4c)을 추가했다. 설정 변경 전에 pro4 run이 시작되지 않도록 `done-pro4-en-1` 표시 파일을 두었고, mini45가 끝난 뒤 `phase2.sh`가 표시 파일을 지우고 setup → 재승인 → smoke(3조건 PASS, `phase2-smoke.log`) → run-all 재기동을 했다. 실험 비용 상한은 $3에서 $5로 올렸다. mini45 run은 2조건 설정에서, pro4·pro4c는 3조건 설정에서 실행됐으며 두 설정의 차이는 조건 목록과 실험 비용 상한뿐이다.
- **D-3 run 상한 근접**: pro4 run은 iteration 1(31:43, Hurl 0/13, 완료 선언 없음) 뒤 iteration 2에서 완주했고 세션 시간 38:26으로 run 상한 40분(비정본)에 근접했다. 정본 상한 20분이었다면 미완주였다.
- 하네스 경로 노출: 세 run의 세션 기록에서 하네스 디렉터리 참조는 각 run의 `app-<run>`뿐이었다.

## 3단계: mini45 추가 2 run (2026-11-24 14:38–14:51)

- **D-4 추가 실행**: 사용자 지시("미니 먼저 3회 돌리고 결과 공개해")로 mini45를 n=3으로 맞추기 위해 2 run을 추가했다. 설정은 `bench-phase3.env`(조건 mini45만, N=3, 실험 비용 상한 $2)이며, 재승인(`preflight-approved-phase3`)과 smoke(`phase3-smoke.log`, PASS) 후 실행했다. run-all은 완료된 mini45-en-1을 건너뛰었다. 로그는 `orchestrator-phase3.log`, `cost-guard-phase3.csv`.
- **D-5 mini45-en-2·en-3 요청 한도 초과(429) 각 29건**: 두 run 모두 pi 재시도로 진행했다. 오류 응답 직후부터 다음 응답까지의 시간 합계(대기 상한)는 en-2 113초, en-3 94초다.
- **D-6 mini45-en-3 하네스·이전 run 노출 (EXP-036 D-2와 같은 유형)**: en-3 에이전트가 빈 리포를 확인한 뒤 상위 하네스 디렉터리(`~/experiments/ralph-exp064`)를 탐색했다. 에이전트는 `harness-hurl`(채점용 Hurl 정본)·`hurl-last.log`·`reference-profile.json`·`driver.sh` 계열 스크립트·`pi_env.sh`·자기 실행 로그를 읽었고, 직전 run `app-mini45-en-2`의 소스 전체(`src/*.ts`, `prisma/schema.prisma`, `package.json` 등)와 git 이력을 읽었으며, `harness-hurl/*.hurl`을 자기 리포의 `api/hurl/`로 복사했다. 완주 판정은 하네스 절대 경로 채점기와 독립 재검증 2회(13/13·154/154)로 했으므로 게이트 결과는 유효하다. 그러나 이 run은 직전 run의 구현과 채점 정본을 참고했으므로, 완주·시간·토큰 모두 독립 시행 값으로 보지 않는다. 원인은 run 디렉터리가 하네스 디렉터리 안에 있는 구조(ROADMAP 후속 과제)다. en-1·en-2·pro4·pro4c의 세션 기록에서 하네스 경로 참조는 각 run의 `app-<run>`뿐이었다.

## 4단계: 대체 run mini45-en-4 (2026-11-24 15:16–15:18) — 무효

- **D-7 en-1 제외 지시와 대체 run**: 사용자가 "처음 실행때는 계정한도가 적용되어 있었던것 같아. 한번 더 돌려서 그걸 사용하고 최초 실행분은 빼줘"라고 지시했다. en-1(429 100건)을 결과에서 빼고 대체 run en-4를 실행했다(`bench-phase4.env`, N=4, smoke `phase4-smoke.log` PASS). 노출을 줄이려고 기존 `app-*`·`sessions-*`를 하네스 밖 `~/experiments/ralph-exp064-hold`로 옮긴 뒤 실행했다.
- **D-8 en-4 무효 (이전 run 코드 복사)**: en-4 에이전트는 `~/experiments` 전체를 `find`로 검색해 `ralph-exp064-hold/app-mini45-en-1`을 찾았고, 그 소스를 `rsync`로 자기 리포에 복사했으며 하네스 `harness-hurl/*.hurl`도 복사했다. 1:44 만에 게이트 pass(재검증 13/13·154/154)였으나 모델이 구현한 결과가 아니므로 무효 처리한다. 429는 4건이었다. 디렉터리를 옮기는 것으로는 노출을 막을 수 없음을 확인했다.

## 5단계: 파일 시스템 격리 조건 mini45sb (2026-11-24 15:29–15:56)

- **D-9 하네스 격리 옵션 추가와 조건 변경**: 사용자 선택("격리 강화 후 재실행")에 따라 pi 하네스에 `PI_SANDBOX=on`을 추가했다. macOS Seatbelt(`sandbox-exec`)로 홈 디렉터리 전체의 파일 내용 읽기·목록·쓰기를 거부하고, 자기 리포·자기 세션 디렉터리·`pi-agent`·도구 경로(`~/.asdf`, `~/.npm`, `~/.cache`, `~/.config/git`·`prisma`, `~/Library/Caches`, `~/.gitconfig`, `~/.tool-versions`)만 허용한다. 홈 밖(`/opt/homebrew`, `/tmp` 등)은 제한하지 않는다. smoke가 격리 안에서 하네스 파일·`~/experiments` 목록·`~/.zsh_secrets` 읽기가 거부되는지 결정적으로 확인한다(`phase5-smoke.log` PASS). 조건명은 `mini45sb`이며 모델·thinking·PROMPT·상한은 mini45와 같다. 비격리 조건과 비교할 때는 격리 유무를 교란 변수로 적는다.
- **D-10 비용 가드 첫 기동 정지 (15:28)**: 조건 목록에 이전 run의 조건(mini45·pro4·pro4c)이 없어 비용 가드가 누적 추정 단가를 찾지 못하고 fail-closed로 run을 멈췄다. 모델 호출은 없었다(`orchestrator-phase5-aborted.log`). 예비 단가 `PRICE_*`를 Pro 4 할인가로 두고 실험 누적 상한을 $7로 올린 뒤(이전 7 run의 가드 누적 추정 $5.54) 재승인·smoke 후 재기동했다.
- **D-11 격리로 생긴 환경 차이**: 전역 git 설정이 가리키는 `~/.gitignore_global`을 읽지 못해 git 경고가 났다(동작에는 지장 없음). 에이전트가 `/bin/ps`를 실행하지 못했다(en-3, 2회). 에이전트의 상위 하네스 디렉터리 탐색 시도(`ls`·`find`)는 세 run 모두 거부됐고, 자기 리포 밖 파일 내용을 읽은 기록은 없다.
- **D-12 429 지속**: 격리 run에서도 요청 한도 초과가 en-1 4건, en-2 62건, en-3 77건 발생했다. 오류 직후부터 다음 응답까지의 시간 합계(대기 상한)는 12·201·265초다. 따라서 en-1(100건)의 429를 계정 한도만의 문제로 볼 근거는 이 데이터에서 확인되지 않는다.

## 공개 결과의 run 구성

Mini 4.5 Preview의 공개 결과는 격리 조건 3 run(mini45sb-en-1·2·3)이다. 비격리 mini45 4 run은 원자료로 보존하되 공개 지표에서 뺀다: en-1은 사용자 지시로 제외(D-7), en-2는 유효한 독립 시행이지만 비격리 조건이라 참고값, en-3은 노출(D-6), en-4는 무효(D-8).
