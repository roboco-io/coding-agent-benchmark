import json,glob,sys,collections,re
def run_stats(run):
    ids={};models=collections.Counter();tools=collections.Counter();think=0;n_msgs=0;dups=0
    for p in glob.glob(f"claude-config-projects-{run}/**/*.jsonl",recursive=True):
        for line in open(p):
            try:d=json.loads(line)
            except:continue
            m=d.get('message') or {}
            if d.get('type')=='assistant' and m.get('id') and m.get('usage'):
                n_msgs+=1
                if m['id'] in ids: dups+=1
                ids[m['id']]=m['usage']; models[m.get('model')]+=1
                for c in m.get('content',[]):
                    if isinstance(c,dict):
                        if c.get('type')=='tool_use': tools[c['name']]+=1
                        if c.get('type')=='thinking': think+=1
    u={'input':0,'cache_create':0,'cache_read':0,'output':0}
    for x in ids.values():
        u['input']+=x.get('input_tokens',0) or 0; u['cache_create']+=x.get('cache_creation_input_tokens',0) or 0
        u['cache_read']+=x.get('cache_read_input_tokens',0) or 0; u['output']+=x.get('output_tokens',0) or 0
    return len(ids),n_msgs-len(ids),u,dict(models),dict(tools),think
def secs(run):
    t=open(f"ralph-run-{run}.log").read()
    s=re.search(r'iteration 1 start: (\S+ \S+)',t).group(1); e=re.search(r'iteration 1 end \(exit \d+\): (\S+ \S+)',t).group(1)
    from datetime import datetime as D
    return (D.fromisoformat(e)-D.fromisoformat(s)).total_seconds()
price={'flash':(0.30,0.006,0.30,1.20),'pro':(1.32,0.044,1.32,3.96)}  # miss, hit, create(=miss), out per 1M
print("run,api,dups,input,cache_create,cache_read,output,thinking_blocks,models,tools,sec,commits,est_usd")
for run in ["flash-en-1","pro-en-1","flash-ko-1","pro-ko-1","flash-en-2","pro-en-2","flash-ko-2","pro-ko-2","flash-en-3","pro-en-3","flash-ko-3","pro-ko-3"]:
    api,dups,u,models,tools,think=run_stats(run)
    import subprocess
    commits=subprocess.run(['git','-C',f'app-{run}','log','--oneline'],capture_output=True,text=True).stdout.count('\n')
    pm=price['flash' if run.startswith('flash') else 'pro']
    usd=(u['input']*pm[0]+u['cache_read']*pm[1]+u['cache_create']*pm[2]+u['output']*pm[3])/1e6
    print(f"{run},{api},{dups},{u['input']},{u['cache_create']},{u['cache_read']},{u['output']},{think},{models},{tools},{secs(run):.0f},{commits},{usd:.3f}".replace("'",""))
