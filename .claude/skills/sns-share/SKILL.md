---
name: sns-share
description: Use when the user asks to write an SNS/social post (SNS 공유 문구, 홍보 문구, 트윗, 링크드인 글) summarizing this repo's latest Ralph loop benchmark experiment results, usually copied to the clipboard with the dashboard link.
---

# 실험 결과 SNS 공유 문구

## 대상 실험

사용자가 실험 번호를 지정하지 않으면 가장 최근에 끝난 실험(같은 날 함께 끝난 실험 묶음 포함)을 대상으로 한다. `experiments/NNN-*/report.md` 헤더의 `- 가설:`·`- **판정:` 줄과 run별 결과 표에서 수치를 가져온다. 필요하면 대시보드 첫 화면 수치(누적 완주 run 수 등)를 `dashboard/index.html`에서 확인한다.

## 작성 규칙

- 분량: 한국어 **300자 내외**의 서술형 한 문단. 글머리표·해시태그는 사용자가 요청할 때만 쓴다. 언어 지정이 있으면 그 언어로 쓴다.
- 포함할 내용: ① 무엇을 했는지(모델 × 하네스, 과제 = 사람 개입 없는 랄프 루프로 RealWorld 백엔드 API 구현, 채점 = 공식 Hurl 테스트 154건) ② 결과(반복 수 대비 완주 수, 완주 iteration) ③ 핵심 관측 수치(세션 시간 등) ④ 교락이 있는 비교라면 "단정하지 않는다"는 한계 한 문장 ⑤ 대시보드 안내.
- 보고서의 판정과 한계를 넘는 표현 금지: 우열 단정, "재현성 확정", 토큰 대리지표를 청구 비용처럼 쓰는 표현을 하지 않는다.
- 범위 표기는 `-`(예: `6-10분`)를 쓰고 `~`는 쓰지 않는다.
- 내부 약어(EXP-NNN, M-26 등)는 넣지 않거나, 넣더라도 설명 없이 의미가 통하게 쓴다.

## 링크와 클립보드

- 기본 링크: 라이브 대시보드 `https://roboco.io/coding-agent-benchmark/` (본문 마지막 줄에 따로 둔다).
- 사용자가 요청하면 보고서 링크 `https://github.com/roboco-io/coding-agent-benchmark/blob/main/experiments/<dir>/report.md`를 추가한다.
- 본문+링크를 `pbcopy`로 복사한다(heredoc 사용, `LANG=en_US.UTF-8`으로 한글 깨짐 방지). 이후 `pbpaste`로 내용이 일치하는지 확인한다.
- 채팅에는 복사한 문구 전문과 글자 수(공백 포함, 링크 제외)를 보여 준다.
