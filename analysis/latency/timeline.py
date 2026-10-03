"""세션 원자료(Codex rollout / pi / Claude Code jsonl)를 모델 대기 시간과 도구 실행 시간으로 분해한다.
usage: timeline.py codex|pi|claude <session.jsonl>...  → CSV 한 줄/세션
구간 정의: 직전 이벤트 시각부터 다음 이벤트 시각까지를, 다음 이벤트가 모델 산출물이면 model, 도구 결과면 tool로 귀속.
모델 호출 수: Codex=last_token_usage가 있는 token_count 수, pi=assistant 메시지 수,
              Claude Code=assistant 레코드의 고유 message.id 수(스트리밍으로 같은 id가 여러 줄이므로 1회로 계산, usage는 id별 최댓값).
함수 analyze(kind, paths)는 여러 세션(iteration)을 합산한다."""
import json, sys, re
from datetime import datetime

def ts(s): return datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

def codex(path):
    ev = []; outs = []; seen = None
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

def claude(path):
    ev = []; ids = {}
    for l in open(path):
        try: d = json.loads(l)
        except Exception: continue
        ty = d.get('type'); m = d.get('message') or {}
        if ty not in ('user', 'assistant') or 'timestamp' not in d: continue
        t = ts(d['timestamp'])
        if ty == 'assistant':
            if m.get('model') == '<synthetic>': continue
            ev.append((t, 'model', None))
            mid = m.get('id') or d.get('uuid')
            ids[mid] = max(ids.get(mid, 0), (m.get('usage') or {}).get('output_tokens', 0) or 0)
        else:
            c = m.get('content')
            if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
                ev.append((t, 'tool', None))
            else:
                ev.append((t, 'start', None))  # 사용자 프롬프트: 시각만 기준점으로 사용, 구간 귀속 없음
    return ev, len(ids), sum(ids.values())

PARSERS = {'codex': codex, 'pi': pi, 'claude': claude}

def split(ev):
    ev.sort(key=lambda x: x[0]); model = tool = 0.0; prev = ev[0][0]; tools = []
    for t, k, x in ev[1:]:
        g = t - prev
        if k == 'model': model += g
        elif k == 'tool': tool += g; tools.append(g)
        prev = t
    return ev[-1][0] - ev[0][0], model, tool, tools

def analyze(kind, paths):
    """여러 세션 파일(iteration, 서브에이전트)을 세션별로 분해한 뒤 합산한다."""
    wall = model = tool = 0.0; calls = out = ntool = 0; mx = 0.0
    for f in paths:
        ev, c, o = PARSERS[kind](f)
        if len(ev) < 2: continue
        w, m, t, tools = split(ev)
        wall += w; model += m; tool += t; calls += c; out += o; ntool += len(tools); mx = max(mx, max(tools or [0]))
    return dict(wall=wall, model=model, tool=tool, calls=calls, out=out, ntool=ntool, max_tool=mx)

if __name__ == '__main__':
    kind = sys.argv[1]
    print('session,wall_s,model_s,tool_s,model_calls,output_tokens,s_per_call,out_tok_per_model_s,tool_calls,max_tool_s')
    for f in sys.argv[2:]:
        r = analyze(kind, [f])
        print(f"{f.split('/')[-2]},{r['wall']:.0f},{r['model']:.0f},{r['tool']:.0f},{r['calls']},{r['out']},{r['model']/max(r['calls'],1):.1f},{r['out']/max(r['model'],1):.1f},{r['ntool']},{r['max_tool']:.0f}")
