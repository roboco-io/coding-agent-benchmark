#!/usr/bin/env python3
"""실행 중 비용 가드 (EXP-042 재발 방지, 2026-10-10).

사용: python3 cost_guard.py <BASE> <HARNESS> <run|ALL> [세션 경로...]
  출력: 추정 USD 한 줄 (소수 4자리). 세션 경로를 주면 그 경로만, 없으면 sessions-<run>(ALL이면 sessions-*) 집계.
단가: 환경변수 PRICE_IN·PRICE_OUT(100만 토큰당 USD), PRICE_CACHE_READ(없으면 PRICE_IN의 10%),
      PRICE_TIERS="상한:입력:출력,..."(요청 입력 길이 구간 단가, 예: "32000:0.30:1.50,128000:0.50:2.50,256000:0.80:4.00").

배경: EXP-042에서 DashScope Anthropic 호환 엔드포인트가 tool_result 토큰을 usage에서 빼고 보고했다.
제공자 보고값만 믿으면 비용을 과소 추정하므로, claude·pi 세션은 요청마다 "그때까지 대화 기록의
UTF-8 바이트 / 3"을 입력 토큰 하한으로 함께 계산해 더 큰 쪽을 쓴다(보수적 추정).
보고값보다 바이트 추정이 크면 그 차이는 캐시 할인 없이 입력 단가로 계산한다.
codex·agy는 제공자 보고 누계만 쓴다(바이트 대조 미지원).
"""
import glob, json, os, sys

BASE, HARNESS, RUN = sys.argv[1], sys.argv[2], sys.argv[3]
PATHS = sys.argv[4:]
P_IN = float(os.environ.get("PRICE_IN", "nan"))
P_OUT = float(os.environ.get("PRICE_OUT", "nan"))
P_CR = float(os.environ.get("PRICE_CACHE_READ") or P_IN * 0.1)
TIERS = []
for t in filter(None, os.environ.get("PRICE_TIERS", "").split(",")):
    lim, pi_, po = t.split(":"); TIERS.append((int(lim), float(pi_), float(po)))
TIERS.sort()
# model-specs.json(조건별 단가)이 있으면 run 이름의 조건으로 단가를 고른다. 없으면 PRICE_* 환경변수.
SPECS = {}
_sp = os.path.join(BASE, "model-specs.json")
if os.path.exists(_sp):
    SPECS = json.load(open(_sp))
COND_MODEL = dict(c.split(":", 1) for c in os.environ.get("CONDITIONS", "").split() if ":" in c)


def use_prices(run):
    global P_IN, P_OUT, P_CR, TIERS
    model = COND_MODEL.get(run.split("-", 1)[0])
    s = SPECS.get(model) or SPECS.get((model or "").split("/", 1)[-1]) if model else None
    if s and s.get("pricing"):
        p = s["pricing"]
        P_IN, P_OUT = float(p["input"]), float(p["output"])
        P_CR = float(p["cache_read"]) if p.get("cache_read") is not None else P_IN * 0.1
        TIERS = sorted((int(a), float(b), float(c)) for a, b, c in (p.get("tiers") or []))
    if P_IN != P_IN or P_OUT != P_OUT:
        sys.exit(f"단가 없음({run}) — model-specs.json pricing 또는 PRICE_IN·PRICE_OUT 필요")
BYTES_PER_TOKEN = 3.0


def price(n_in):
    for lim, pi_, po in TIERS:
        if n_in <= lim:
            return pi_, po
    return (TIERS[-1][1], TIERS[-1][2]) if TIERS else (P_IN, P_OUT)


SKIP_KEYS = {"signature", "thinkingSignature", "encrypted_content", "id", "type", "tool_use_id", "toolCallId"}


def _strbytes(v):
    """모델 입력이 되는 문자열만 센다. 서명·암호화 추론·ID 같은 메타데이터는 제외한다(과대 추정 방지)."""
    if isinstance(v, str):
        return len(v.encode())
    if isinstance(v, list):
        return sum(_strbytes(x) for x in v)
    if isinstance(v, dict):
        return sum(_strbytes(x) for k, x in v.items() if k not in SKIP_KEYS)
    return 0


def content_bytes(msg):
    return _strbytes(msg.get("content"))


def cost_chat_jsonl(fp):
    """claude(message.id·usage) / pi(responseId·usage) 공통."""
    usd = 0.0; hist = 0; seen = {}
    for ln, line in enumerate(open(fp, errors="replace")):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        m = e.get("message") if isinstance(e.get("message"), dict) else None
        if not m:
            continue
        u = m.get("usage") or {}
        if m.get("role") == "assistant" and u:
            key = m.get("id") or m.get("responseId") or ("line", ln)  # pi는 ID가 없을 수 있다
            rin = (u.get("input_tokens") or u.get("input") or 0)
            rcw = (u.get("cache_creation_input_tokens") or u.get("cacheWrite") or 0)
            rcr = (u.get("cache_read_input_tokens") or u.get("cacheRead") or 0)
            rout = (u.get("output_tokens") or u.get("output") or 0)
            prev = seen.get(key, (0, 0, 0, 0, hist))
            seen[key] = (max(prev[0], rin), max(prev[1], rcw), max(prev[2], rcr), max(prev[3], rout), prev[4])
        hist += content_bytes(m)
    for rin, rcw, rcr, rout, h in seen.values():
        est = h / BYTES_PER_TOKEN
        rep = rin + rcw + rcr
        pi_, po = price(max(rep, est))
        usd += ((rin + rcw) * pi_ + rcr * (P_CR if not TIERS else pi_ * 0.1) + max(0.0, est - rep) * pi_ + rout * po) / 1e6
    return usd


def cost_codex(fp):
    last = None
    for line in open(fp, errors="replace"):
        if '"total_token_usage"' in line:
            info = (json.loads(line).get("payload") or {}).get("info") or {}
            last = info.get("total_token_usage") or last
    if not last:
        return 0.0
    cached = last.get("cached_input_tokens", 0) or 0
    fresh = (last.get("input_tokens", 0) or 0) - cached
    return (fresh * P_IN + cached * P_CR + (last.get("output_tokens", 0) or 0) * P_OUT) / 1e6


def cost_agy(fp):
    usd = 0.0
    for line in open(fp, errors="replace"):
        d = json.loads(line)
        if d.get("type") == "PLANNER_RESPONSE":
            usd += ((d.get("input_tokens") or 0) * P_IN + (d.get("cache_read_tokens") or 0) * P_CR
                    + (d.get("output_tokens") or 0) * P_OUT) / 1e6
    return usd


if not PATHS:
    PATHS = sorted(glob.glob(os.path.join(BASE, "sessions-*"))) if RUN == "ALL" else [os.path.join(BASE, f"sessions-{RUN}")]
total = 0.0
for root in PATHS:
    b = os.path.basename(root.rstrip("/"))
    use_prices(b[len("sessions-"):] if b.startswith("sessions-") else RUN)
    if HARNESS == "codex":
        files, fn = glob.glob(os.path.join(root, "**", "rollout-*.jsonl"), recursive=True), cost_codex
    elif HARNESS == "agy":
        files, fn = glob.glob(os.path.join(root, "**", "transcript_full.jsonl"), recursive=True), cost_agy
    else:
        files, fn = glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True), cost_chat_jsonl
    for fp in files:
        try:
            total += fn(fp)
        except (OSError, ValueError):
            pass
print(f"{total:.4f}")
