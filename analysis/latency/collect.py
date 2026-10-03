"""usage_all_runs.csv의 EN run별 세션 원자료를 찾아 timeline.analyze로 분해하고 runs.csv를 만든다.
tar.gz는 임시 디렉터리에 풀어 읽는다(리포에 풀지 않음). usage: collect.py <scratch_dir> [--list]"""
import csv, os, sys, glob, tarfile, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline as T

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
scratch = sys.argv[1]; LIST = '--list' in sys.argv

def ts_first(f):
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        if d.get('timestamp'): return d['timestamp']
    return ''

def resolve(path, run_id):
    """source_path → (main session files in time order, subagent files)"""
    paths = path.split(';')
    files = []
    for p in paths:
        if not os.path.isabs(p): p = os.path.join(ROOT, p)
        if p.endswith('.tar.gz'):
            d = os.path.join(scratch, 'x', p.replace('/', '_')); 
            if not os.path.isdir(d):
                os.makedirs(d); tarfile.open(p).extractall(d)
            p = d
        if os.path.isfile(p): files.append(p)
        else: files += glob.glob(p + '/**/*.jsonl', recursive=True)
    return files

def kind_of(harness):
    return 'codex' if harness.startswith('codex') else 'pi' if harness.startswith('pi') else 'claude'

def runfiles(row):
    k = kind_of(row['harness']); fs = resolve(row['source_path'], row['run_id'])
    rid = row['run_id']
    if row['source_path'].endswith('.tar.gz') and '/' not in row['source_path'].split('runs/')[-1].replace('sessions/', ''):
        # 단일 tar에 여러 run이 들어 있음: run 디렉터리 이름으로 거른다
        suffix = rid.split('-en-')[-1] if '-en-' in rid else rid.split('en-')[-1]
        fs = [f for f in fs if f"en-{suffix}" in f.split('x/')[-1]]
    main = [f for f in fs if '/subagents/' not in f]
    sub = [f for f in fs if '/subagents/' in f]
    main.sort(key=ts_first); sub.sort(key=ts_first)
    return k, main, sub

def rowkey(r):
    return ('pi × ' + r['model']) if r['harness'].startswith('pi') else r['model']

# 대시보드 iter 표기가 2(Solar Open 2)이고 시간 근접도만으로는 2·3개가 모호한 경우의 고정값
FORCE_N = {('EXP-015', 'solar-1'): 2}

def select(k, main, sub, time_min, force=None):
    """기록된 소요 시간(report/대시보드)에 가장 가까운 앞쪽 iteration 묶음을 고른다(완주 iteration까지의 합)."""
    best = None; acc = 0.0
    for n in range(1, len(main) + 1):
        acc += T.analyze(k, [main[n - 1]])['wall']
        d = abs(acc / 60 - time_min)
        if best is None or d < best[0]: best = (d, n)
    n = force or best[1]; inc = main[:n]
    stems = [os.path.basename(f)[:-6] for f in inc]
    sb = [f for f in sub if any(('/' + s_ + '/') in f for s_ in stems)]
    return inc, sb

if __name__ == '__main__':
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, 'analysis/cost/usage_all_runs.csv'))) if r['lang'] == 'en']
    out = []
    for r in rows:
        k, main, sub = runfiles(r)
        if LIST:
            print(r['model'], r['exp'], r['run_id'], r['time_min'], 'main', [round(T.analyze(k, [f])['wall']) for f in main], 'sub', len(sub)); continue
        inc, sb = select(k, main, sub, float(r['time_min']), FORCE_N.get((r['exp'], r['run_id'])))
        a = T.analyze(k, inc + sb)
        wall_main = T.analyze(k, inc)['wall']
        out.append(dict(exp=r['exp'], row=rowkey(r), run=r['run_id'], wall_s=round(wall_main), model_s=round(a['model']), tool_s=round(a['tool']),
            model_calls=a['calls'], output_tokens=a['out'], s_per_call=round(a['model'] / max(a['calls'], 1), 1),
            out_per_model_s=round(a['out'] / max(a['model'], 1), 1), model_share=round(a['model'] / max(a['model'] + a['tool'], 1), 3),
            sessions=len(inc), subagent_sessions=len(sb), recorded_min=r['time_min'], harness=k))
    if not LIST:
        w = csv.DictWriter(open(os.path.join(ROOT, 'analysis/latency/runs.csv'), 'w', newline=''), fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)
        for o in out: print(o['row'], o['run'], o['wall_s'], round(o['wall_s']/60 - float(o['recorded_min']), 2), o['sessions'], o['subagent_sessions'], o['s_per_call'], o['model_share'])
