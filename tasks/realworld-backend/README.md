# 공통 과제: RealWorld App 백엔드

모델·하네스 조합의 신규 구현 능력을 확인하는 기본 과제. 기존 코드 변경 과제는 별도 task ID와 시작 상태로 관리한다.

## 과제 정의

[RealWorld](https://github.com/gothinkster/realworld) 스펙("Medium 클론")의 백엔드 API를 구현한다.

- **스펙**: [RealWorld API 스펙](https://realworld-docs.netlify.app/specifications/backend/endpoints/) — 인증(JWT), 유저/프로필, 아티클 CRUD, 코멘트, 즐겨찾기, 태그, 피드
- **기술 스택**: TypeScript (Node.js) + Fastify + Prisma + SQLite — 모든 조건에 동일 적용
  - 선정 근거(2026-07 Perplexity 조사): Stack Overflow 2025 설문에서 Node.js 백엔드 1위, AI 스택 가이드들이 Node+Prisma 조합으로 수렴, LLM 학습 데이터가 풍부해 에이전트 코딩 오류율이 낮다고 평가됨. 차점 후보는 Python+FastAPI(AI 특화 백엔드용)였으나 본 과제는 일반 REST API이므로 제외.
  - DB는 조사 1위인 PostgreSQL 대신 **SQLite** 사용: DB 서버 기동·설정 없이 파일 기반으로 즉시 실행 가능해 실험 반복이 빠르고, 환경 설정 토큰(교란 변수)을 줄임. SQLite 선택이 PostgreSQL의 동시성·운영 특성을 대표한다는 뜻은 아니다.
- **시작 상태**: 빈 저장소에서 시작 (스캐폴딩 없음)

## 완료 기준 (Definition of Done)

- [ ] 실험별로 고정한 Hurl 정본 13파일·154요청 전체 통과(파일 해시·실행 경로·버전 고정, 종료 코드 0 확인)
- [ ] 채점 정본은 실험 대상이 수정할 수 없는 환경에서 실행하며 빈 테스트·오류 바이너리의 허위 통과를 거부
- [ ] 로컬에서 단일 명령으로 서버 기동 가능

## 통제 조건

- 모델·하네스·추론 설정·제공자는 실험별 조합 manifest에 기록. 전략 효과 분리 실험에서만 모델을 고정
- 동일한 초기 프롬프트 자료(이 과제 스펙)를 조건별로 동일하게 제공
- 실험자 개입 규칙은 각 실험 README에 명시

과거 EXP-001 PTE의 Newman 311 assertion과 Hurl 154요청은 서로 다른 채점 정본이다. 과거 완료 관측은 보존하지만 동일 품질의 비교 근거로 섞지 않는다. Hurl 정본 파일은 현재 저장소에 포함돼 있지 않으므로 새 실행 전 확보·버전 고정·정상/오류 사례 검증이 필요하다.
