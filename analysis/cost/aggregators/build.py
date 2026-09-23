import sys,os,csv,glob,json
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
from agg_claude import agg
H=os.path.expanduser('~'); R='/Users/dohyunjung/Workspace/roboco-io/research/vibecoding-token-experiments'
def jl(d): return sorted(glob.glob(os.path.join(d,'**','*.jsonl'),recursive=True))
NAT='claude-code-native'; 
def DIR(p): return f'claude-code-direct({p})'
CODEX='codex-cli'
# (model, exp, lang, run_id, harness, time, kind, source, existing_csv_values or None)
runs=[]
def C(model,exp,lang,rid,har,t,src,csvv=None,note=''): runs.append((model,exp,lang,rid,har,t,'claude',src,csvv,note))
def X(model,exp,lang,rid,har,t,files,csvv=None,note=''): runs.append((model,exp,lang,rid,har,t,'codex',files,csvv,note))
e9=f'{R}/experiments/009-opus5-ralph-en/runs'; e10=f'{R}/experiments/010-opus48-vs-opus5/runs'
for rid,t in zip(['48-1','48-2','48-3'],[8.70,8.30,7.80]):
    C('Opus 4.8','EXP-010','en',rid,NAT,t,f'{e10}/{rid}/logs',note='iter1 true completion; iter2 re-verify session after harness false-reject INCLUDED (dashboard output 37.1K incl. both; time is iter1 only)' if rid=='48-1' else '')
for rid in ['48ko-1','48ko-2','48ko-3']: pass
for rid,t in zip(['opus5-1','opus5-2','opus5-3'],[12.2,11.6,8.9]): C('Opus 5','EXP-009','en',rid,NAT,t,f'{e9}/{rid}/logs')
for rid,t in zip(['5-1','5-2','5-3'],[13.8,17.6,9.4]): C('Opus 5','EXP-010','en',rid,NAT,t,f'{e10}/{rid}/logs')
for i,t in zip([1,2,3],[6.90,7.77,6.15]): C('Fable 5.1','EXP-023','en',f'fable-{i}',NAT,t,f'{H}/.claude/projects/-Users-dohyunjung-ralph-exp023-app-fable-{i}','csv')
for lang,ts in [('en',[8.35,3.98,4.20]),('ko',[4.00,4.22,3.95])]:
    for i,t in zip([1,2,3],ts): C('Opus 5.5','EXP-026',lang,f'{lang}-{i}',NAT,t,f'{H}/.claude/projects/-Users-dohyunjung-ralph-exp026-app-{lang}-{i}','csv')
for m,k,tt in [('DeepSeek V4.1-Flash','flash',{'en':[4.57,5.98,4.82],'ko':[8.42,6.32,4.23]}),('DeepSeek V4-Pro','pro',{'en':[13.33,12.08,15.83],'ko':[13.37,13.35,13.72]})]:
    for lang in ['en','ko']:
        for i,t in zip([1,2,3],tt[lang]): C(m,'EXP-025',lang,f'{k}-{lang}-{i}',DIR('DeepSeek'),t,f'{H}/ralph-exp025/claude-config-projects-{k}-{lang}-{i}','csv')
for i,(exp,t) in enumerate(zip(['EXP-014','EXP-016','EXP-016'],[21.30,7.62,7.87]),1): C('kimi-k3',exp,'en',f'kimi-{i}',DIR('Moonshot'),t,f'{H}/ralph-exp014/claude-config-projects-kimi-{i}','csv')
for i,t in zip([1,2,3],[15.88,13.67,10.60]): C('kimi-k3','EXP-017','ko',f'kimi-ko-{i}',DIR('Moonshot'),t,f'{H}/ralph-exp017k/claude-config-projects-kimi-ko-{i}','csv')
for i,(exp,t) in enumerate(zip(['EXP-013','EXP-016','EXP-016'],[15.08,15.58,14.62]),1): C('qwen3.8-max',exp,'en',f'qwen-{i}',DIR('DashScope'),t,f'{H}/ralph-exp013/claude-config-projects-qwen-{i}','csv')
for i,t in zip([1,2,3],[22.78,22.32,23.50]): C('qwen3.8-max','EXP-017','ko',f'qwen-ko-{i}',DIR('DashScope'),t,f'{H}/ralph-exp017q/claude-config-projects-qwen-ko-{i}','csv')
C('Solar Open 2','EXP-015','en','solar-1',DIR('Upstage'),58.25,f'{H}/ralph-exp015/claude-config-projects-solar-1','csv',
  'includes aborted iter-3 session dc547653 (17 req: input 627342, output 3356) that started after gate false-reject; report 252.3K includes it')
for i,t in zip([1,2,3],[258.38,171.40,118.67]): C('Solar Pro 4','EXP-020','en',f'pro4-{i}',DIR('Upstage'),t,f'{H}/ralph-exp020/claude-config-projects-pro4-{i}',None,
  {1:'12 iteration sessions (iters 3-11 gate false-rejects) all included',2:'2 iterations',3:''}[i])
def cx(d): return sorted(glob.glob(f'{d}/**/rollout-*.jsonl',recursive=True))
X('gpt-5.6-sol','EXP-011','en','sol-1',CODEX,5.77,[f for f in cx(f'{H}/ralph-exp011/codex-sessions-sol-1') if '07-41-02' not in f],'csv11',
  'excluded pre-run smoke rollout 07-41-02 ("Reply with exactly: OK", 13264 in/9984 cached/5 out) that existing usage-sol-1.csv included')
X('gpt-5.6-sol','EXP-016','en','sol-2',CODEX,10.0,cx(f'{H}/ralph-exp011/codex-sessions-sol-2'),'csv','2 iteration rollouts summed')
X('gpt-5.6-sol','EXP-016','en','sol-3',CODEX,5.28,cx(f'{H}/ralph-exp011/codex-sessions-sol-3'),'csv')
for i,t in zip([1,2,3],[7.53,8.72,6.90]): X('gpt-5.6-sol','EXP-019','ko',f'solko-{i}',CODEX,t,cx(f'{H}/ralph-exp019/codex-sessions-solko-{i}'),'csv')
for i,t in zip([1,2,3],[7.60,7.10,7.08]): X('gpt-6-astra','EXP-021','en',f'astra-{i}',CODEX,t,cx(f'{H}/ralph-exp021/codex-sessions-astra-{i}'),'csv')
# existing CSV comparison values (input,cache_create,cache_read,output) for verification
def load_existing(model,rid):
    E=f'{R}/experiments'
    if model=='Fable 5.1':
        for r in csv.DictReader(open(f'{E}/023-fable51-ralph/runs/usage.csv')):
            if r['run']==rid: return tuple(int(r[k]) for k in ['input','cache_create','cache_read','output']),f'{E}/023-fable51-ralph/runs/usage.csv'
    if model=='Opus 5.5':
        for r in csv.DictReader(open(f'{E}/026-opus55-ralph/runs/usage.csv')):
            if r['run']==rid: return tuple(int(r[k]) for k in ['input','cache_create','cache_read','output']),f'{E}/026-opus55-ralph/runs/usage.csv'
    if model.startswith('DeepSeek'):
        for r in csv.DictReader(open(f'{E}/025-deepseek-direct/runs/usage.csv')):
            if r['run']==rid: return tuple(int(r[k]) for k in ['input','cache_create','cache_read','output']),f'{E}/025-deepseek-direct/runs/usage.csv'
    g=glob.glob(f'{E}/*/runs/{rid}/usage-{rid}.csv')
    if g:
        last=open(g[0]).read().strip().splitlines()[-1].split(',')
        if last[0]=='TOTAL': return ('codex',int(last[1]),int(last[2]),int(last[3])),g[0]
        return tuple(int(x) for x in last[1:5]),g[0]
    if rid.startswith('solko'):
        for r in csv.DictReader(open(f'{E}/019-ko-native-codex/runs/usage-codex.csv')):
            if r['run']==rid: return ('codex',int(r['input']),int(r['cached']),int(r['output'])),f'{E}/019-ko-native-codex/runs/usage-codex.csv'
    if rid.startswith('astra'):
        f=f'{E}/021-gpt6-astra-codex/runs/usage-{rid}.csv'; last=open(f).read().strip().splitlines()[-1].split(',')
        return ('codex',int(last[1]),int(last[2]),int(last[3])),f
    return None,None
import agg_codex_mod as AC
rows=[]; audit={}
for model,exp,lang,rid,har,t,kind,src,csvflag,note in runs:
    ex,exp_path=load_existing(model,rid) if csvflag else (None,None)
    if kind=='claude':
        r=agg(jl(src)); s=r['res']; mf=r['missing_field_count']
        split= mf['cw5m']==0 and mf['cw1h']==0
        think = None if mf['thinking']>0 or s['thinking']==0 and 'claude' not in str(r['models']) else s['thinking']
        n=[]
        if r['resolved_stream']: n.append(f"{r['resolved_stream']} ids had preliminary(message_start,output=0,no cache dict)+final rows; final used")
        if r['prelim_only']: n.append(f"{len(r['prelim_only'])} ids have ONLY preliminary usage (final unknown) -> excluded; prelim input est {sum(x[1][0] for x in r['prelim_only'])}")
        if r['unresolved']: n.append(f"{len(r['unresolved'])} UNRESOLVED conflicts excluded")
        if r['sub_files']: n.append(f"{r['sub_files']} subagent transcripts included")
        if think: n.append(f"thinking_tokens(subset of output)={think}")
        if note: n.append(note)
        mine=(s['input'],s['cache_write'],s['cache_read'],s['output'])
        if ex is not None:
            if ex==mine: method='csv_verified'; n.append(f'matches {os.path.relpath(exp_path,R)} (last-wins dedup script)')
            else: method='reaggregated'; n.append(f'existing {os.path.relpath(exp_path,R)} differs {ex} (last-wins kept prelim-only rows)')
        else: method='reaggregated'
        rea='yes'
        rows.append(dict(model=model,exp=exp,lang=lang,run_id=rid,harness=har,time_min=t,input_uncached=s['input'],cache_read=s['cache_read'],
            cache_write_5m=s['cw5m'] if split else '',cache_write_1h=s['cw1h'] if split else '',cache_write_unsplit='' if split else s['cache_write'],
            output=s['output'],reasoning_in_output=rea,unique_requests=r['unique']-len(r['prelim_only'])-len(r['unresolved']),dup_removed=r['dup_rows'],
            source_path=src,method=method,notes='; '.join(n)))
    else:
        tot=dict(input=0,cached=0,out=0,reason=0,req=0,dup=0,cw=None)
        for f in src:
            x=AC.sess(f); fi=x['final']; assert fi==dict((k,v) for k,v in x['sum_last'].items()) or all(fi[k]==x['sum_last'][k] for k in x['sum_last'])
            tot['input']+=fi['input_tokens']; tot['cached']+=fi['cached_input_tokens']; tot['out']+=fi['output_tokens']; tot['reason']+=fi.get('reasoning_output_tokens',0)
            tot['req']+=x['requests']; tot['dup']+=x['dup_events']
            if 'cache_write_input_tokens' in fi: tot['cw']=(tot['cw'] or 0)+fi['cache_write_input_tokens']
        n=[f"rollout total_token_usage (session-cumulative, last event) summed over {len(src)} session(s); equals sum of per-request last_token_usage",
           f"input_uncached=input_tokens-cached_input_tokens ({tot['input']}-{tot['cached']})", f"reasoning_output_tokens(subset of output)={tot['reason']}"]
        if tot['cw'] is None: n.append('no cache-write field in rollout')
        if note: n.append(note)
        method='reaggregated'
        if ex:
            if ex[1:]==(tot['input'],tot['cached'],tot['out']): method='csv_verified'; n.append(f'matches {os.path.relpath(exp_path,R)}')
            else: n.append(f'existing {os.path.relpath(exp_path,R)} differs {ex[1:]}')
        rows.append(dict(model=model,exp=exp,lang=lang,run_id=rid,harness=har,time_min=t,input_uncached=tot['input']-tot['cached'],cache_read=tot['cached'],
            cache_write_5m='',cache_write_1h='',cache_write_unsplit='' if tot['cw'] is None else tot['cw'],output=tot['out'],reasoning_in_output='yes',
            unique_requests=tot['req'],dup_removed=tot['dup'],source_path=';'.join(src),method=method,notes='; '.join(n)))
# EXP-019 Opus: raw purged -> archived CSV
E19=f'{R}/experiments/019-ko-native-codex/runs/usage-opus.csv'
tm={'48ko-1':8.48,'48ko-2':7.12,'48ko-3':8.30,'5ko-1':11.15,'5ko-2':11.07,'5ko-3':9.92}
for r in csv.DictReader(open(E19)):
    model='Opus 4.8' if r['run'].startswith('48') else 'Opus 5'
    rows.append(dict(model=model,exp='EXP-019',lang='ko',run_id=r['run'],harness=NAT,time_min=tm[r['run']],input_uncached=r['input'],cache_read=r['cache_read'],
        cache_write_5m='',cache_write_1h='',cache_write_unsplit=r['cache_create'],output=r['output'],reasoning_in_output='yes',unique_requests='',dup_removed='',
        source_path=E19,method='report_value',notes='raw session jsonl purged from ~/.claude/projects (30-day cleanup); README says message.id dedup but aggregator not archived (conflict handling unknown); 5m/1h split unavailable (EXP-009/010 same harness were 100% 1h)'))
order=['Opus 4.8','Opus 5','Fable 5.1','Opus 5.5','DeepSeek V4.1-Flash','DeepSeek V4-Pro','kimi-k3','qwen3.8-max','gpt-5.6-sol','gpt-6-astra','Solar Open 2','Solar Pro 4']
rows.sort(key=lambda x:(order.index(x['model']),x['lang'],x['exp'],x['run_id']))
cols='model,exp,lang,run_id,harness,time_min,input_uncached,cache_read,cache_write_5m,cache_write_1h,cache_write_unsplit,output,reasoning_in_output,unique_requests,dup_removed,source_path,method,notes'.split(',')
w=csv.DictWriter(open(f'{S}/usage_all_runs.csv','w'),fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows))
