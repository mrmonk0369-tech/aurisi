#!/usr/bin/env python3
# AURISI v60.44: SPLASH WORDMARK IN SCRIPT FONT
#  Owner wants: Aurisi on splash in a script (handwritten) font.
#  - Great Vibes (latin subset, 42800 bytes woff2) embedded as base64
#    @font-face Aurisi Script - fully offline, no CDN
#  - wordmark becomes ONE span (cursive letters must join, so the
#    per-letter flex spans would break the script connections)
#  - whole-word reveal animation, gradient fill kept, bigger size
# Font source: local greatvibes-latin.woff2, or pinned gstatic URL.
# Base: AURISI.html v60.43 (1879844). Idempotent.
import sys, io, os, base64, urllib.request

FONT_URL = "https://fonts.gstatic.com/s/greatvibes/v21/RWmMoKWR9v4ksMfaWd_JN9XFiaQ.woff2"
FONT_LEN = 42800

def get_font():
    if os.path.exists("greatvibes-latin.woff2"):
        b = open("greatvibes-latin.woff2", "rb").read()
        if len(b) == FONT_LEN:
            return b
    req = urllib.request.Request(FONT_URL, headers={"User-Agent": "Mozilla/5.0"})
    b = urllib.request.urlopen(req, timeout=60).read()
    assert len(b) == FONT_LEN, "unexpected font size: %d" % len(b)
    open("greatvibes-latin.woff2", "wb").write(b)
    return b

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.44"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.44 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.43"' in h, "base must be v60.43"

fb64 = base64.b64encode(get_font()).decode()

# P1: wordmark HTML - one span so cursive letters connect
F1 = '<div class="splash-name"><span>A</span><span>u</span><span>r</span><span>i</span><span>s</span><span>i</span></div>'
R1 = '<div class="splash-name"><span>Aurisi</span></div>'
assert h.count(F1) == 1, "wordmark anchor not found"
h = h.replace(F1, R1)

# P2: embed font + script style on the wordmark
F2 = '.splash-name{display:flex;gap:1px;font-size:27px;font-weight:800;letter-spacing:5px;margin-top:6px;background:linear-gradient(100deg,var(--text) 35%,var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}'
R2 = ("@font-face{font-family:'Aurisi Script';font-style:normal;font-weight:400;"
      "src:url(data:font/woff2;base64," + fb64 + ") format('woff2');font-display:block}\n"
      ".splash-name{font-family:'Aurisi Script',cursive;font-size:46px;font-weight:400;"
      "letter-spacing:1px;line-height:1.25;margin-top:2px;"
      "animation:spLetter .7s cubic-bezier(.2,1.2,.3,1) .35s backwards;"
      "background:linear-gradient(100deg,var(--text) 35%,var(--accent));"
      "-webkit-background-clip:text;background-clip:text;color:transparent}")
assert h.count(F2) == 1, "splash-name css anchor not found"
h = h.replace(F2, R2)

# P3: drop per-letter spans css, single whole-word keyframes
F3 = ('.splash-name span{display:inline-block;animation:spLetter .55s cubic-bezier(.2,1.2,.3,1) backwards}\n'
      '.splash-name span:nth-child(1){animation-delay:.35s}\n'
      '.splash-name span:nth-child(2){animation-delay:.42s}\n'
      '.splash-name span:nth-child(3){animation-delay:.49s}\n'
      '.splash-name span:nth-child(4){animation-delay:.56s}\n'
      '.splash-name span:nth-child(5){animation-delay:.63s}\n'
      '.splash-name span:nth-child(6){animation-delay:.7s}\n'
      '@keyframes spLetter{0%{transform:translateY(20px) scale(.6);opacity:0}100%{transform:translateY(0) scale(1);opacity:1}}')
R3 = '@keyframes spLetter{0%{transform:translateY(14px);opacity:0}100%{transform:translateY(0);opacity:1}}'
assert h.count(F3) == 1, "per-letter css anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.43"'
R4 = 'var APP_VERSION="60.44"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied script font splash, size: %d bytes" % len(h.encode("utf-8")))
