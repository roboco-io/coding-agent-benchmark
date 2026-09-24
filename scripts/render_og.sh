#!/bin/bash
# dashboard/index.html의 데이터(M)로 SNS 공유용 Open Graph 카드(dashboard/og.png, 1200×630)를 렌더링한다.
# GitHub Pages 배포 워크플로가 업로드 직전에 실행한다(og.png는 커밋하지 않는 빌드 산출물). 로컬 미리보기용으로도 실행 가능.
# 필요: node, Google Chrome(또는 Chromium). CHROME 환경변수로 실행 파일을 지정할 수 있다.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -z "${CHROME:-}" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome google-chrome-stable chromium chromium-browser; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then CHROME="$c"; break; fi
  done
fi
[ -n "${CHROME:-}" ] || { echo "Chrome not found (set CHROME)" >&2; exit 1; }
EXTRA=()
[ "$(uname)" = "Linux" ] && EXTRA+=(--no-sandbox)  # CI 러너용
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
node - "$ROOT" "$TMP/card.html" <<'JS'
const fs = require("fs"), [root, out] = process.argv.slice(2);
const html = fs.readFileSync(`${root}/dashboard/index.html`, "utf8");
const js = html.split("<script>")[1].split("/* raw table")[0];
const M = new Function(js + "; return M;")();
const med = a => { const s = [...a].sort((x, y) => x - y), k = s.length >> 1; return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2; };
let runs = 0, latest = 0;
for (const m of M) for (const k of ["en", "ko"]) if (m[k]) {
  runs += m[k].t.length;
  for (const n of m[k].exp.match(/\d+/g)) latest = Math.max(latest, +n);
}
const rows = M.map(m => [m.name, m.stack, +med(m.en.t).toFixed(1), !!m.preview]).sort((a, b) => a[2] - b[2]);
const data = { runs, models: new Set(M.map(m => m.base || m.name)).size, latest: "EXP-" + String(latest).padStart(3, "0"), rows };
fs.writeFileSync(out, fs.readFileSync(`${root}/scripts/og/og-card.html`, "utf8").replace("const D = __DATA__;", "const D = " + JSON.stringify(data) + ";"));
console.log(`runs ${runs} · models ${data.models} · ${data.latest}`);
JS
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=8000 ${EXTRA[@]+"${EXTRA[@]}"} \
  --screenshot="$ROOT/dashboard/og.png" "file://$TMP/card.html" 2>/dev/null
[ -s "$ROOT/dashboard/og.png" ] || { echo "og.png was not produced" >&2; exit 1; }
echo "wrote dashboard/og.png"
