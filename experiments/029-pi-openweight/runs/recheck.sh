#!/bin/bash
cd ~/ralph-exp029
echo "run,try,result,time" > recheck.csv
for r in kimi-en-1 qwen-en-1 flash-en-1 kimi-en-2 qwen-en-2 flash-en-2 kimi-en-3 qwen-en-3 flash-en-3; do
  for t in 1 2; do echo "$r,$t,\"$(bash measure.sh ~/ralph-exp029/app-$r)\",$(date '+%F %T')" >> recheck.csv; done
done
rm -rf rescore-qwen-en-1-iter1; cp -R app-qwen-en-1 rescore-qwen-en-1-iter1
git -C rescore-qwen-en-1-iter1 checkout -q -f c53937d
echo "rescore,commit c53937d,\"$(bash measure.sh ~/ralph-exp029/rescore-qwen-en-1-iter1)\",$(date '+%F %T')" >> recheck.csv
echo "rescore,commit c53937d try2,\"$(bash measure.sh ~/ralph-exp029/rescore-qwen-en-1-iter1)\",$(date '+%F %T')" >> recheck.csv
python3 usage_pi.py ~/ralph-exp029 kimi-en-1 kimi-en-2 kimi-en-3 qwen-en-1 qwen-en-2 qwen-en-3 flash-en-1 flash-en-2 flash-en-3 > usage-pi.csv 2>&1
touch recheck-done
