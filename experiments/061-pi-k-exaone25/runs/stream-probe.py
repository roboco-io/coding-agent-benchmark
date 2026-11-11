import json,os,sys,time,urllib.request,glob
key=os.environ['K']; hurl=sorted(glob.glob(os.path.expanduser('~/experiments/ralph-exp061/app-kexaone-en-1/api/hurl/*.hurl')))
txt='\n\n'.join(f'##### {os.path.basename(p)}\n'+open(p).read() for p in hurl)
prompt=open(os.path.expanduser('~/experiments/ralph-exp061/PROMPT-en.md')).read()+'\n\nHere are all the Hurl test files:\n'+txt+'\n\nNow write the complete implementation plan and then the full source of src/app.ts.'
body={"model":"k-exaone_v2.5","stream":True,"stream_options":{"include_usage":True},"chat_template_kwargs":{"preserve_thinking":True},"max_tokens":65536,"messages":[{"role":"user","content":prompt}]}
req=urllib.request.Request('https://api.exaone.ai/v1/chat/completions',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
t0=time.time(); last=t0; first=None; n=0; rc=0; cc=0; maxgap=0; out=open(sys.argv[1],'w')
try:
  with urllib.request.urlopen(req,timeout=600) as r:
    for line in r:
      now=time.time(); line=line.decode().strip()
      if not line.startswith('data:'): continue
      d=line[5:].strip()
      if d=='[DONE]': break
      j=json.loads(d); n+=1
      if first is None: first=now-t0
      maxgap=max(maxgap,now-last); last=now
      for ch in j.get('choices',[]):
        dl=ch.get('delta',{}); rc+=len(dl.get('reasoning_content') or ''); cc+=len(dl.get('content') or '')
        if ch.get('finish_reason'): out.write(f'finish {ch["finish_reason"]}\n')
      if j.get('usage'): out.write('usage '+json.dumps(j['usage'])+'\n')
      if n%200==0: out.write(f'{now-t0:.0f}s chunks={n} reasoning_chars={rc} content_chars={cc} maxgap={maxgap:.1f}\n'); out.flush()
except Exception as e: out.write(f'EXC {type(e).__name__}: {e}\n')
out.write(f'END {time.time()-t0:.0f}s first_chunk={first} chunks={n} reasoning_chars={rc} content_chars={cc} maxgap={maxgap:.1f}\n')
