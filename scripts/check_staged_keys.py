#!/usr/bin/env python3
"""커밋 대상에 API 키·토큰이 들어 있으면 커밋을 막는다 (hooks/pre-commit에서 호출).

사용:
  python3 scripts/check_staged_keys.py          # 스테이징된 내용(git index) 검사 — pre-commit
  python3 scripts/check_staged_keys.py --all    # HEAD의 추적 파일 전체 검사 — 수동 점검·CI

검사 방식 (둘 중 하나라도 걸리면 실패):
  1. 정확 일치: ~/.zsh_secrets에 있는 값(길이 12 이상)이 그대로 들어 있는지. 파일이 없으면 건너뛴다.
  2. 패턴: 알려진 키 형식(sk-proj-, sk-ant-, AIza, up_, ghp_ 등)과 `*_KEY=값`·`*_TOKEN=값` 형태의 대입.
gzip·tar.gz 파일은 압축을 풀어 내부 파일까지 검사한다(세션 아카이브에 키가 남은 EXP-029·036 사례).
출력에는 값을 찍지 않고 앞 4자만 보여 준다. 오탐이면 값을 `<REDACTED:NAME>`으로 바꾸거나
scripts/redact_keys.py로 마스킹한 뒤 다시 커밋한다. 우회 옵션은 두지 않는다.
"""
import gzip, io, os, re, subprocess, sys, tarfile

MAX_BYTES = 200 * 1024 * 1024
B = rb"(?<![A-Za-z0-9_+/-])"
E = rb"(?![A-Za-z0-9_+/=-])"
PATTERNS = [
    # 앞뒤 경계: 긴 base64 블롭(Codex encrypted reasoning 등) 안의 우연한 부분 일치를 제외한다
    ("OpenAI key", re.compile(B + rb"sk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{32,200}" + E)),
    ("Anthropic key", re.compile(B + rb"sk-ant-[A-Za-z0-9_-]{20,200}" + E)),
    ("Google API key", re.compile(B + rb"AIza[0-9A-Za-z_-]{35}" + E)),
    ("Upstage key", re.compile(rb"\bup_[A-Za-z0-9]{24,}")),
    ("GitHub token", re.compile(rb"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|github_pat_[A-Za-z0-9_]{40,}")),
    ("Slack token", re.compile(rb"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("AWS access key", re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Private key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY")),
    # NAME_KEY=값 / NAME_TOKEN: 값 — 값이 변수 참조·마스킹·자리표시자가 아니고 영문+숫자가 섞인 16자 이상일 때만
    ("Key assignment", re.compile(
        rb"\b[A-Z][A-Z0-9_]*(?:API_KEY|_KEY|_TOKEN|_SECRET|PASSWORD)\b[\"']?\s*[:=]\s*[\"']?"
        rb"(?![$<{%])([A-Za-z0-9_\-./+]{16,})")),
]
PLACEHOLDER = re.compile(rb"^(?:x+|X+|\*+|your|example|dummy|test|placeholder|changeme)", re.I)


def secret_values():
    p = os.path.expanduser("~/.zsh_secrets")
    vals = {}
    if not os.path.isfile(p):
        return vals
    for line in open(p, errors="replace"):
        m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)", line)
        if m:
            v = m.group(2).strip().strip('"').strip("'")
            if len(v) >= 12 and not v.startswith("$"):   # "$OTHER_KEY" 같은 변수 참조는 값이 아님
                vals[v.encode()] = m.group(1)
    return vals


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def targets(all_files):
    if all_files:
        names = git("ls-files", "-z").split(b"\0")
        return [(n.decode(), lambda n=n: git("show", b"HEAD:" + n)) for n in names if n]
    names = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split(b"\0")
    return [(n.decode(), lambda n=n: git("show", b":" + n)) for n in names if n]


def expand(name, data):
    """(표시 이름, 내용) 목록. gzip/tar.gz는 풀어서 내부 파일을 돌려준다."""
    if data[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(data)[:MAX_BYTES]
        except (OSError, EOFError):
            return [(name, data)]
        try:
            with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
                out = []
                for m in tf.getmembers():
                    if m.isfile():
                        f = tf.extractfile(m)
                        if f:
                            out.append((f"{name}!{m.name}", f.read(MAX_BYTES)))
                return out
        except tarfile.TarError:
            return [(name, raw)]
    return [(name, data)]


def mask(b):
    s = b.decode(errors="replace")
    return s[:4] + "…" if len(s) > 4 else "…"


def lineno(data, pos):
    return data.count(b"\n", 0, pos) + 1


def scan(name, data, vals):
    hits = []
    for v, k in vals.items():
        i = data.find(v)
        if i >= 0:
            hits.append((name, lineno(data, i), f"~/.zsh_secrets 값 일치 ({k})", mask(v)))
    for label, pat in PATTERNS:
        for m in pat.finditer(data):
            tok = m.group(1) if m.groups() else m.group(0)
            if label == "Key assignment":
                if PLACEHOLDER.match(tok) or not (re.search(rb"[A-Za-z]", tok) and re.search(rb"[0-9]", tok)):
                    continue
            hits.append((name, lineno(data, m.start()), label, mask(tok)))
    return hits


def main():
    all_files = "--all" in sys.argv[1:]
    vals = secret_values()
    hits = []
    for name, read in targets(all_files):
        try:
            data = read()
        except subprocess.CalledProcessError:
            continue
        for sub, content in expand(name, data):
            hits += scan(sub, content, vals)
    if hits:
        print("커밋 차단: API 키·토큰으로 보이는 값이 있습니다 (값은 앞 4자만 표시).", file=sys.stderr)
        for name, ln, label, preview in hits:
            print(f"  {name}:{ln}  {label}  {preview}", file=sys.stderr)
        print("조치: 값을 <REDACTED:NAME>으로 바꾸거나 `python3 scripts/redact_keys.py <경로>`로 마스킹 후 다시 스테이징하세요.",
              file=sys.stderr)
        sys.exit(1)
    if not vals:
        print("경고: ~/.zsh_secrets가 없어 정확 일치 검사는 건너뛰고 패턴 검사만 했습니다.", file=sys.stderr)


if __name__ == "__main__":
    main()
