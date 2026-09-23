#!/usr/bin/env python3
"""Aggregate Claude-format session jsonl usage for one run dir (recursive, incl. subagents/).
Dedup key: assistant message.id within the run.
Same id + identical usage -> counted once.
Same id + differing usage -> resolved ONLY for the observed streaming pattern:
  exactly one 'preliminary' tuple (output_tokens==0 and no cache_creation dict = message_start snapshot)
  plus exactly one 'complete' tuple (has cache_creation dict) that appears LATER in file order -> take complete.
  Anything else -> unresolved conflict, excluded from sums and reported.
Ids with only preliminary rows -> excluded (usage final unknown), reported."""
import json,sys,glob,os,collections
def tup(u):
    cc=u.get('cache_creation')
    return (u.get('input_tokens'),u.get('cache_read_input_tokens'),u.get('cache_creation_input_tokens'),u.get('output_tokens'),
            cc.get('ephemeral_5m_input_tokens') if isinstance(cc,dict) else None,
            cc.get('ephemeral_1h_input_tokens') if isinstance(cc,dict) else None,
            (u.get('output_tokens_details') or {}).get('thinking_tokens') if isinstance(u.get('output_tokens_details'),dict) else None)
def prelim(t): return t[3]==0 and t[4] is None
def agg(paths):
    by=collections.defaultdict(list); rows=0; noid=0; sub_ids=set(); models=collections.Counter(); seq=0
    for p in paths:
        for l in open(p):
            try:o=json.loads(l)
            except Exception:continue
            m=o.get('message')
            if o.get('type')!='assistant' or not isinstance(m,dict) or not m.get('usage'): continue
            rows+=1; seq+=1
            mid=m.get('id')
            if not mid: noid+=1; continue
            by[mid].append((seq,tup(m['usage']))); models[m.get('model')]+=1
            if '/subagents/' in p: sub_ids.add(mid)
    K=['input','cache_read','cache_write','output','cw5m','cw1h','thinking']
    res=dict((k,0) for k in K); missing=dict((k,0) for k in K)
    resolved=0; unresolved=[]; prelim_only=[]
    for mid,lst in by.items():
        d=[]
        for s,t in lst:
            if t not in [x for _,x in d]: d.append((s,t))
        if len(d)==1: t=d[0][1]
        else:
            pre=[x for x in d if prelim(x[1])]; comp=[x for x in d if not prelim(x[1])]
            if len(pre)==1 and len(comp)==1 and comp[0][0]>pre[0][0]:
                t=comp[0][1]; resolved+=1
            else:
                unresolved.append((mid,[x[1] for x in d])); continue
        if prelim(t) and len(d)==1 and t[1] is None:
            prelim_only.append((mid,t)); continue
        for k,v in zip(K,t):
            if v is None: missing[k]+=1
            else: res[k]+=v
    return dict(res=res,missing_field_count=missing,unique=len(by),rows=rows,dup_rows=rows-noid-len(by),noid=noid,
                resolved_stream=resolved,unresolved=unresolved,prelim_only=prelim_only,sub_ids=len(sub_ids),
                models=dict(models),files=len(paths),sub_files=sum('/subagents/' in p for p in paths))
if __name__=='__main__':
    out={}
    for d in sys.argv[1:]:
        paths=sorted(glob.glob(os.path.join(d,'**','*.jsonl'),recursive=True))
        r=agg(paths); out[d]=r
        print(d.split('/')[-1], r['res'], 'uniq',r['unique'],'dup',r['dup_rows'],'resolved',r['resolved_stream'],'unres',len(r['unresolved']),'prelimOnly',len(r['prelim_only']),'miss',{k:v for k,v in r['missing_field_count'].items() if v},'sub',r['sub_files'],r['models'])
        for x in r['unresolved'][:3]: print('   UNRES',x)
        for x in r['prelim_only'][:3]: print('   PRELIM_ONLY',x)
    json.dump(out,open(os.environ.get('OUT','/dev/null'),'w'),indent=1)
