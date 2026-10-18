#!/usr/bin/env python3
"""claude-direct usage 정확도 점검 (EXP-042 D-1 재발 방지, 2026-10-10).

사용: python3 usage_probe.py <BASE_URL> <model> <키 환경변수 이름>
약 6,000토큰 tool_result를 넣은 스트리밍 요청 1회를 보내고, message_start·message_delta가 보고한
입력 토큰(input + cache_read + cache_creation)이 기대치(UTF-8 바이트/4)의 50% 이상인지 확인한다.
Claude Code는 이 보고값으로 컨텍스트 크기를 판단해 자동 압축을 시작한다. 보고가 누락되면 압축이 일어나지 않아
컨텍스트가 입력 한도까지 커지고 비용이 급증한다(EXP-042 coder: 2 run 약 $92).
종료 코드 0 = 통과, 1 = 과소 보고 또는 오류. 요청 비용은 약 6K 입력 토큰 1회분이다.
"""
import json, os, sys, urllib.error, urllib.request

base, model, key_env = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
key = os.environ.get(key_env, "")
blob = "alpha beta gamma delta epsilon zeta eta theta " * 750  # 약 36KB
expected = len(blob.encode()) / 4
body = {
    "model": model, "max_tokens": 16, "stream": True,
    "tools": [{"name": "read_file", "description": "Read a file", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}}],
    "messages": [
        {"role": "user", "content": "Read notes.txt, then reply with the single word OK."},
        {"role": "assistant", "content": [{"type": "tool_use", "id": "toolu_probe1", "name": "read_file", "input": {"path": "notes.txt"}}]},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_probe1", "content": blob}]},
    ],
}
def make_req(b):
    return urllib.request.Request(base + "/v1/messages", data=json.dumps(b).encode(), method="POST", headers={
        "content-type": "application/json", "anthropic-version": "2023-06-01",
        "x-api-key": key, "authorization": "Bearer " + key})


def open_stream(b):
    """thinking 모드에서 이전 턴의 thinking 반송을 요구하는 제공자(DeepSeek V4.1-Flash-1017, EXP-048)는
    400을 돌려준다. 그 경우에만 assistant 턴에 thinking 블록을 넣어 1회 재요청한다."""
    try:
        return urllib.request.urlopen(make_req(b), timeout=120)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if e.code != 400 or "thinking" not in detail:
            raise urllib.error.HTTPError(e.url, e.code, f"{e.msg} {detail[:300]}", e.headers, None) from None
        b["messages"][1]["content"].insert(0, {"type": "thinking", "thinking": "I should read notes.txt first.", "signature": ""})
        print("INFO usage probe: 제공자가 thinking 반송을 요구해 thinking 블록을 넣어 재요청")
        return urllib.request.urlopen(make_req(b), timeout=120)


start = delta = None
try:
    with open_stream(body) as r:
        for raw in r:
            line = raw.decode(errors="replace").strip()
            if not line.startswith("data:"):
                continue
            try:
                ev = json.loads(line[5:])
            except ValueError:
                continue
            u = (ev.get("message") or {}).get("usage") if ev.get("type") == "message_start" else ev.get("usage")
            if not u:
                continue
            tot = sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            if ev.get("type") == "message_start":
                start = tot
            elif ev.get("type") == "message_delta" and tot:
                delta = tot
except Exception as e:  # noqa: BLE001 — 점검 실패는 모두 FAIL로 처리
    detail = e.read().decode(errors="replace")[:300] if hasattr(e, "read") else ""
    print(f"FAIL usage probe {model}: 요청 오류 {type(e).__name__}: {str(e)[:120]} {detail}")
    sys.exit(1)
ok = start is not None and start >= expected * 0.5 and (delta is None or delta >= expected * 0.5)
print(f"{'PASS' if ok else 'FAIL'} usage probe {model}: 기대 입력 약 {expected:.0f} / message_start {start} / message_delta {delta}")
sys.exit(0 if ok else 1)
