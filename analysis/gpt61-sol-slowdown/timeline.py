"""세션 원자료를 모델 대기 시간(요청→응답 기록)과 도구 실행 시간(도구 호출→결과 기록)으로 분해한다.
usage: timeline.py codex|pi <session.jsonl>...  → CSV 한 줄/세션
구간 정의: 직전 이벤트 시각부터 다음 이벤트 시각까지를, 다음 이벤트가 모델 산출물이면 model, 도구 결과면 tool로 귀속."""
import json, sys, re
from datetime import datetime

def ts(s): return datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

def codex(path):
    ev = []  # (t, kind, extra)
    outs = []
    for l in open(path):
        d = json.loads(l); p = d.get('payload', {}) or {}; t = ts(d['timestamp'])
        ty, pt = d.get('type'), p.get('type')
        if ty == 'event_msg' and pt == 'task_started': ev.append((t, 'start', None))
        elif ty == 'response_item' and pt in ('custom_tool_call', 'function_call', 'reasoning', 'message') and p.get('role') not in ('developer', 'user'):
            ev.append((t, 'model', None))
        elif ty == 'response_item' and pt in ('custom_tool_call_output', 'function_call_output'):
            txt = json.dumps(p.get('output'))
            m = re.search(r'Wall time ([\d.]+) seconds', txt)
            ev.append((t, 'tool', float(m.group(1)) if m else None))
        elif ty == 'event_msg' and pt == 'token_count':
            u = (p.get('info') or {}).get('last_token_usage') or {}
            outs.append(u.get('output_tokens', 0))
        elif ty == 'event_msg' and pt == 'task_complete': ev.append((t, 'end', None))
    return ev, len(outs), sum(outs)

def pi(path):
    ev = []; calls = 0; out = 0
    for l in open(path):
        d = json.loads(l)
        if d.get('type') == 'session': ev.append((ts(d['timestamp']), 'start', None)); continue
        m = d.get('message') or {}
        if d.get('type') != 'message': continue
        t = ts(d['timestamp'])
        if m.get('role') == 'assistant':
            calls += 1; out += (m.get('usage') or {}).get('output', 0); ev.append((t, 'model', None))
        elif m.get('role') == 'toolResult': ev.append((t, 'tool', None))
    return ev, calls, out

def split(ev):
    ev.sort(key=lambda x: x[0]); model = tool = 0.0; prev = ev[0][0]; tools = []
    for t, k, x in ev[1:]:
        g = t - prev
        if k == 'model': model += g
        elif k == 'tool': tool += g; tools.append(g)
        prev = t
    return ev[-1][0] - ev[0][0], model, tool, tools

kind = sys.argv[1]
print('session,wall_s,model_s,tool_s,model_calls,output_tokens,s_per_call,out_tok_per_model_s,tool_calls,max_tool_s')
for f in sys.argv[2:]:
    ev, calls, out = (codex if kind == 'codex' else pi)(f)
    wall, model, tool, tools = split(ev)
    print(f"{f.split('/')[-2]},{wall:.0f},{model:.0f},{tool:.0f},{calls},{out},{model/max(calls,1):.1f},{out/max(model,1):.1f},{len(tools)},{max(tools or [0]):.0f}")
