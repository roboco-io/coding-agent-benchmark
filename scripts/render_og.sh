#!/bin/bash
# dashboard/index.html의 데이터(M)로 SNS 공유용 Open Graph 카드(dashboard/og.png, 1200×630)를 렌더링한다.
# 새 실험을 대시보드에 반영한 뒤 실행하고 og.png를 함께 커밋한다. 필요: node, Google Chrome.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
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
const data = { runs, models: M.length, latest: "EXP-" + String(latest).padStart(3, "0"), rows };
fs.writeFileSync(out, fs.readFileSync(`${root}/scripts/og/og-card.html`, "utf8").replace("const D = __DATA__;", "const D = " + JSON.stringify(data) + ";"));
console.log(`runs ${runs} · models ${M.length} · ${data.latest}`);
JS
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=5000 \
  --screenshot="$ROOT/dashboard/og.png" "file://$TMP/card.html" 2>/dev/null
echo "wrote dashboard/og.png"
