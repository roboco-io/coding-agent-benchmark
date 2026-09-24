#!/bin/bash
cd ~/ralph-exp030
echo "run,try,result,time" > recheck.csv
for r in opus-en-1 sol-en-1 opus-en-2 sol-en-2 opus-en-3 sol-en-3; do
  for t in 1 2; do echo "$r,$t,\"$(bash measure.sh ~/ralph-exp030/app-$r)\",$(date '+%F %T')" >> recheck.csv; done
done
python3 usage_pi.py ~/ralph-exp030 opus-en-1 opus-en-2 opus-en-3 sol-en-1 sol-en-2 sol-en-3 > usage-pi.csv 2>&1
touch recheck-done
