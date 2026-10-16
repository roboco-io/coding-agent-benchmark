"""pi 세션 기록에서 모델 호출 단위 대기·토큰을 뽑아 gemini-4-argon(EXP-047)과 gemini-3.8-flash(EXP-036)를 비교한다.
대기 = assistant 메시지 시각 - 직전 이벤트(세션 시작·도구 결과·직전 assistant) 시각 (analysis/latency/timeline.py의 귀속 규칙과 같음).
사용: python3 percall.py <라벨>=<세션 jsonl> ... > percall.csv ; python3 percall.py --summary percall.csv"""
import json, sys, csv
from datetime import datetime
ts = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

def calls(label, path):
    prev = None; k = 0
    for l in open(path):
        d = json.loads(l)
        if d.get('type') == 'session': prev = ts(d['timestamp']); continue
        if d.get('type') != 'message': continue
        m = d.get('message') or {}; t = ts(d['timestamp'])
        if m.get('role') == 'assistant':
            u = m.get('usage') or {}; k += 1
            tools = sum(1 for c in (m.get('content') or []) if isinstance(c, dict) and c.get('type') == 'toolCall')
            yield [label, k, round(t - prev, 2), u.get('input', 0) + u.get('cacheRead', 0), u.get('output', 0), u.get('reasoning', 0), tools]
        prev = t

def fit(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    r2 = 1 - sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)
    return a, b, r2

def med(v): v = sorted(v); h = len(v) // 2; return v[h] if len(v) % 2 else (v[h - 1] + v[h]) / 2

if sys.argv[1] == '--summary':
    rows = list(csv.reader(open(sys.argv[2])))[1:]
    w = csv.writer(sys.stdout)
    w.writerow(['group', 'calls', 'wait_med_s', 'prompt_med', 'out_med', 'reason_share', 'tools_per_call', 'fit_intercept_s', 'fit_s_per_1k_out', 'r2'])
    for g in sorted({r[0].rsplit('-', 1)[0] for r in rows}):
        R = [r for r in rows if r[0].rsplit('-', 1)[0] == g]
        wt = [float(r[2]) for r in R]; out = [int(r[4]) for r in R]
        a, b, r2 = fit(out, wt)
        w.writerow([g, len(R), round(med(wt), 1), int(med([int(r[3]) for r in R])), int(med(out)),
                    round(sum(int(r[5]) for r in R) / sum(out), 2), round(sum(int(r[6]) for r in R) / len(R), 2),
                    round(a, 1), round(b * 1000, 1), round(r2, 2)])
else:
    w = csv.writer(sys.stdout); w.writerow(['run', 'call', 'wait_s', 'prompt_tokens', 'output', 'reasoning', 'tool_calls'])
    for a in sys.argv[1:]:
        lab, p = a.split('=', 1)
        for r in calls(lab, p): w.writerow(r)
