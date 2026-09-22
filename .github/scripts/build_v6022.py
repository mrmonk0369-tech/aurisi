#!/usr/bin/env python3
# AURISI v60.22: RAM RAM WELCOME (devotional greeting).
#  When anyone opens AURISI for chatting, the FIRST thing they see is a
#  devotional greeting, Neem Karoli Baba style:
#    - a gently pulsing 🚩 flag
#    - the classic Hanuman vandana shloka (Sundarkand):
#      "Manojavam marutatulyavegam jitendriyam buddhimatam varishtham |
#       vatatmajam vanarayoothamukhyam shreeramadootam sharanam prapadye ||"
#    - and a warm "Ram Ram 🙏" greeting line in the accent color
#  It sits above the "Hi, I'm Aurisi" heading, fades in gently, and is
#  fully theme-adaptive (uses --muted / --accent variables).
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.21 (1855059). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.22"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.22 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.21"' in h, "base must be v60.21"

# P1: vandana markup - the greeting before everything else
F1 = '<div id="welcome" class="welcome">\n        <h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>'
R1 = '<div id="welcome" class="welcome">\n        <div class="vandana"><span class="vd-flag">\U0001F6A9</span><span class="vd-shlok">\u092e\u0928\u094b\u091c\u0935\u0902 \u092e\u093e\u0930\u0941\u0924\u0924\u0941\u0932\u094d\u092f\u0935\u0947\u0917\u0902 \u091c\u093f\u0924\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u092f\u0902 \u092c\u0941\u0926\u094d\u0927\u093f\u092e\u0924\u093e\u0902 \u0935\u0930\u093f\u0937\u094d\u0920\u092e\u0965<br>\u0935\u093e\u0924\u093e\u0924\u094d\u092e\u091c\u0902 \u0935\u093e\u0928\u0930\u092f\u0942\u0925\u092e\u0941\u0916\u094d\u092f\u0902 \u0936\u094d\u0930\u0940\u0930\u093e\u092e\u0926\u0942\u0924\u0902 \u0936\u0930\u0923\u0902 \u092a\u094d\u0930\u092a\u0926\u094d\u092f\u0947 \u0965</span><span class="vd-ram">\U0001F64F Ram Ram</span></div>\n        <h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: vandana styles - gentle, premium, theme-adaptive
F2 = '.welcome p{color:var(--muted);margin:0 auto 14px;font-size:14px;max-width:480px;line-height:1.5}'
R2 = F2 + "\n" + Q('.vandana{display:flex;flex-direction:column;align-items:center;gap:7px;margin:0 0 16px;animation:fadeUp .6s ease}\n.vandana .vd-flag{font-size:24px;line-height:1;animation:vdGlow 2.8s ease-in-out infinite}\n.vandana .vd-shlok{font-size:12.5px;line-height:1.8;color:var(--muted);max-width:440px;text-align:center}\n.vandana .vd-ram{font-size:15px;font-weight:800;letter-spacing:.6px;color:var(--accent)}\n@keyframes vdGlow{0%,100%{opacity:.7;transform:scale(1)}50%{opacity:1;transform:scale(1.1)}}')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'var APP_VERSION="60.21"'
R3 = 'var APP_VERSION="60.22"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Ram Ram Welcome, size: %d bytes" % len(h.encode("utf-8")))
