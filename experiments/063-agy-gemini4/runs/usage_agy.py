#!/usr/bin/env python3
"""agy(Antigravity CLI) usage 집계 (EXP-035).
사용: python3 usage_agy.py <BASE> <run>...
- 정본: <BASE>/sessions-<run>/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript_full.jsonl
  의 PLANNER_RESPONSE 스텝 usage 합계. 대화(conversation) 1개 = agy -p 호출 1회(iteration).
  강제 종료돼 결과 JSON이 없는 iteration도 포함된다 (EXP-035 D-1).
- 대조: driver 로그(ralph-run-<run>.log)의 결과 JSON usage 합계. 결과 JSON이 있는 대화는 값이 일치해야 한다
  (EXP-035 전 대화 일치 확인). json_* 열로 함께 출력한다.
- input_tokens는 cache_read를 제외한 값이다(total_tokens = input + output 검산).
  output_tokens는 thinking을 포함한다. proxy = input + output → 토큰 대리지표, 청구 비용 아님.
"""
import glob, json, os, sys
base, runs = sys.argv[1], sys.argv[2:]
print("run,conversations,planner_steps,input,output,cache_read,proxy,json_results,json_errors,json_proxy,json_thinking")
for run in runs:
    pat = os.path.join(base, f"sessions-{run}", ".gemini", "antigravity-cli", "brain", "*",
                       ".system_generated", "logs", "transcript_full.jsonl")
    conv = steps = i = o = c = 0
    for fp in sorted(glob.glob(pat)):
        conv += 1
        for line in open(fp):
            d = json.loads(line)
            if d.get("type") != "PLANNER_RESPONSE":
                continue
            steps += 1
            i += d.get("input_tokens", 0) or 0
            o += d.get("output_tokens", 0) or 0
            c += d.get("cache_read_tokens", 0) or 0
    n = err = jp = jt = 0
    for line in open(os.path.join(base, f"ralph-run-{run}.log"), errors="replace"):
        line = line.strip()
        if not line.startswith('{"conversation_id"'):
            continue
        d = json.loads(line); u = d.get("usage", {}); n += 1
        if d.get("status") != "SUCCESS": err += 1
        jp += (u.get("input_tokens", 0) or 0) + (u.get("output_tokens", 0) or 0)
        jt += u.get("thinking_tokens", 0) or 0
    print(f"{run},{conv},{steps},{i},{o},{c},{i + o},{n},{err},{jp},{jt}")
