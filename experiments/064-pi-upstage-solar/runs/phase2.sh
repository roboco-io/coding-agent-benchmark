#!/bin/bash
# EXP-064: mini45 종료 후 pro4c 조건 추가 재설정 → 재승인 → smoke → run-all (2026-11-24 사용자 지시)
B=~/experiments/ralph-exp064; R=~/Workspace/roboco-io/research/vibecoding-token-experiments
until [ -f $B/done-all ]; do sleep 15; done
echo "phase2 start $(date '+%F %T')"
rm -f $B/done-all $B/done-pro4-en-1
cd $R && bash .claude/skills/ralph-model-benchmark/scripts/setup.sh experiments/064-pi-upstage-solar/runs/bench.env > $B/phase2-setup.log 2>&1 || { echo "SETUP-FAIL"; exit 1; }
bash $B/approve.sh "둘 다 진행하고 공개할때는 soalr pro 4 요금 기준으로 공개해줘. Contributor 모델이 일반 모델과 성능차이가 나지 않을지에 대한 확인도 하고싶어 / 진행시켜 (2026-11-24, pro4c 추가·EXP_BUDGET_USD 5)" >/dev/null || { echo "APPROVE-FAIL"; exit 1; }
bash $B/smoke.sh > $B/phase2-smoke.log 2>&1
grep -E "^(PASS|FAIL)" $B/phase2-smoke.log
[ $(grep -c '^PASS' $B/phase2-smoke.log) -eq 3 ] && ! grep -q '^FAIL' $B/phase2-smoke.log || { echo "SMOKE-FAIL"; exit 1; }
nohup caffeinate -is bash $B/run-all.sh >/dev/null 2>&1 &
echo "run-all relaunched $(date '+%F %T')"
