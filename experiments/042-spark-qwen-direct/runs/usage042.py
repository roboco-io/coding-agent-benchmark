# EXP-042 usage: DashScope Anthropic 엔드포인트는 같은 message.id에 message_start(과소)·message_delta 값이 섞여 기록된다(D-1).
# message.id별 각 필드의 최대값을 취한다 — 하한 추정치이며 tool_result 누락분은 복원되지 않는다.
import json,glob,os,sys
H=sys.argv[1]; print('run,requests,input_max,cache_read_max,cache_write_max,output_max,model')
for r in sys.argv[2:]:
    best={}; models=set()
    for f in glob.glob(f'{H}/sessions-{r}/**/*.jsonl',recursive=True):
        for l in open(f):
            try:e=json.loads(l)
            except:continue
            m=e.get('message') or {}; u=m.get('usage'); i=m.get('id')
            if not u or not i or m.get('model')=='<synthetic>': continue
            models.add(m.get('model'))
            k=('input_tokens','cache_read_input_tokens','cache_creation_input_tokens','output_tokens')
            p=best.get(i,(0,0,0,0)); best[i]=tuple(max(p[j],u.get(k[j],0) or 0) for j in range(4))
    s=[sum(v[j] for v in best.values()) for j in range(4)]
    print(r,len(best),*s,'|'.join(sorted(x for x in models if x)),sep=',')
