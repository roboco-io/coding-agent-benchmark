#!/usr/bin/env python3
"""~/.zsh_secrets의 비밀값(길이 12 이상)을 파일들에서 <REDACTED:NAME>으로 치환한다 (EXP-036 D-3).
사용: python3 scripts/redact_keys.py <dir_or_file>...   → 제자리 수정, 치환 건수 출력
에이전트가 `env` 등으로 셸 환경을 출력하면 세션 로그에 키가 남으므로, 원자료를 리포에 보관하기 전에 반드시 실행한다.
"""
import os, re, sys
vals = {}
for line in open(os.path.expanduser("~/.zsh_secrets")):
    m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)", line)
    if m:
        v = m.group(2).strip().strip('"').strip("'")
        if len(v) >= 12 and not v.startswith("$"): vals[v] = m.group(1)   # 변수 참조 제외
total = 0
def fix(p):
    global total
    try: s = open(p, encoding="utf-8", errors="surrogateescape").read()
    except (IsADirectoryError, PermissionError): return
    n = 0
    for v, k in vals.items():
        c = s.count(v)
        if c: s = s.replace(v, f"<REDACTED:{k}>"); n += c
    if n:
        open(p, "w", encoding="utf-8", errors="surrogateescape").write(s); total += n
        print(f"{p}: {n}")
for a in sys.argv[1:]:
    if os.path.isdir(a):
        for r, _, fs in os.walk(a):
            for f in fs: fix(os.path.join(r, f))
    else: fix(a)
print(f"redacted total: {total}")
