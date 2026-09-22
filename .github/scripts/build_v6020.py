#!/usr/bin/env python3
# AURISI v60.20: TRULY CLEAN WELCOME.
#  1) MEDIUM GREY THEME REMOVED: the "grey" theme (the flat metallic-looking
#     medium grey) is deleted from the theme picker (both the topbar popup
#     and the tiles). Anyone who had grey selected is auto-migrated to
#     Lofi Coffee on next boot. Remaining themes: Lofi, Peaches, Pure Black.
#  2) WELCOME = CLEAN: the starter-suggestion grid is removed from the chat
#     home entirely - every feature already lives on home (topbar + menus),
#     so nothing is shown separately there. Welcome keeps only the greeting,
#     subtitle and the tour button.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.19 (1854948). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.20"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.20 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.19"' in h, "base must be v60.19"

# P1: remove Medium Grey from theme popup
F1 = '<div class="theme-pop-row" data-th="grey" onclick="themePick(\'grey\')"><span class="th-cap" style="background:linear-gradient(to right,#B7BCC4,#4A5462)"></span>\U0001F32B️ Medium Grey</div>\n    '
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, "")

# P2: remove Medium Grey from theme tiles
F2 = '<button class="theme-tile" data-th="grey" onclick="themePick(\'grey\')"><span class="th-prev" style="background:linear-gradient(135deg,#B7BCC4 55%,#4A5462)"></span>Medium Grey</button>\n          '
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, "")

# P3: migrate grey users to lofi
F3 = 'if(t==="lofidark")t="grey";'
R3 = 'if(t==="lofidark"||t==="grey")t="lofi";'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: grey no longer a valid theme
F4 = 'if(t!=="lofi"&&t!=="grey"&&t!=="peachlight"&&t!=="pureblack")t="pureblack";'
R4 = 'if(t!=="lofi"&&t!=="peachlight"&&t!=="pureblack")t="pureblack";'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: theme toggle cycle skips grey
F5 = 'const order=["lofi","grey","peachlight","pureblack"];'
R5 = 'const order=["lofi","peachlight","pureblack"];'
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: welcome stays clean - no starter grid (features already on home)
F6 = '.starter-pill .ac-text small{display:block;color:var(--muted);font-size:10.5px;font-weight:600;line-height:1.3}'
R6 = F6 + "\n" + Q('/* v60.20: starters removed from welcome - every feature already lives on home */\n.snap-stage{display:none!important}')
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.19"'
R7 = 'var APP_VERSION="60.20"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Truly Clean Welcome, size: %d bytes" % len(h.encode("utf-8")))
