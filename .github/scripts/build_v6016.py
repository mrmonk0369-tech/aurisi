#!/usr/bin/env python3
# AURISI v60.16: TOP TIER CORE - KaTeX math engine EMBEDDED in the file.
#  - KaTeX 0.16.8 css + js + auto-render + all 20 woff2 fonts (base64) are
#    inlined into AURISI.html. Math now renders instantly, fully OFFLINE.
#  - No more CDN flash of raw "$x^2$" text, no jsdelivr/unpkg dependency.
#  - File grows ~650KB (1.2MB -> ~1.85MB) - worth it, still fast.
# Determinism: downloads pinned katex@0.16.8 from jsdelivr (immutable), caches
# in ./katex_cache/. Base: AURISI.html v60.15 (1203044). Idempotent.
import sys, io, os, re, base64, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "katex_cache")
DIST = "https://cdn.jsdelivr.net/npm/katex@0.16.8/dist"

def fetch(path):
    """Download (with local cache) a katex dist file; return bytes."""
    local = os.path.join(CACHE, path.replace("/", "__"))
    if os.path.exists(local):
        return open(local, "rb").read()
    os.makedirs(CACHE, exist_ok=True)
    req = urllib.request.Request(DIST + "/" + path,
                                 headers={"User-Agent": "aurisi-build"})
    data = urllib.request.urlopen(req, timeout=60).read()
    open(local, "wb").write(data)
    return data

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.16"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.16 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.15"' in h, "base must be v60.15"

# --- 1) build embedded CSS (fonts inlined as base64 woff2) ---
css = fetch("katex.min.css").decode("utf-8")
fonts = sorted(set(re.findall(r"fonts/([A-Za-z0-9_\-]+\.woff2)", css)))
assert len(fonts) == 20, "expected 20 woff2 fonts, got %d" % len(fonts)
for f in fonts:
    b64 = base64.b64encode(fetch("fonts/" + f)).decode("ascii")
    css = css.replace("fonts/" + f, "data:font/woff2;base64," + b64)
# strip woff/ttf fallbacks (relative urls would 404; woff2 data URIs win)
css = re.sub(r",url\(fonts/[^)]+\.woff\) format\(\"woff\"\),"
             r"url\(fonts/[^)]+\.ttf\) format\(\"truetype\"\)", "", css)
assert css.count("url(fonts/") == 0, "leftover font refs in css"

js = fetch("katex.min.js").decode("utf-8")
ar = fetch("contrib/auto-render.min.js").decode("utf-8")
assert "</script" not in js and "</script" not in ar and "</style" not in css

# --- 2) replace the 3 CDN tags with inline embeds ---
F1 = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">\n'
      '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>\n'
      '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>')
assert h.count(F1) == 1, "katex CDN tags not found"
R1 = ('<style id="katexCss">/* KaTeX 0.16.8 embedded - instant offline math */\n'
      + css + '\n</style>\n'
      '<script id="katexJs">/* KaTeX 0.16.8 embedded */\n' + js + '</script>\n'
      '<script>/* auto-render 0.16.8 embedded */\n' + ar + '</script>')
h = h.replace(F1, R1)

F2 = 'var APP_VERSION="60.15"'
R2 = 'var APP_VERSION="60.16"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("embedded KaTeX (css %dB, js %dB, auto-render %dB, fonts %d), size: %d bytes"
      % (len(css), len(js), len(ar), len(fonts), len(h.encode("utf-8"))))
