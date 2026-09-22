#!/usr/bin/env python3
# AURISI v60.19: CLEAN WELCOME (chat interface polish).
#  1) SCROLL CAROUSEL REMOVED: the swipeable "snap-stage" carousel of
#     starter suggestions on the chat home is gone. Starters now sit in a
#     simple static 2-column grid - nothing to scroll, swipe or drag.
#  2) LIGHT METALLIC REMOVED: starter pills were hard-coded dark (#26262e)
#     with a mirror "box-reflect" sheen and inset highlights - that shiny
#     metallic look is deleted.
#  3) THEME-ADAPTIVE: pills now use the app's own theme variables
#     (--surface / --line / --text / --muted), so they automatically match
#     every theme (lofi, grey, peachlight, pureblack). Subtitles are shown
#     under each title, flat and friendly.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.18 (1853928). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.19"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.19 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.18"' in h, "base must be v60.18"

# P1: CSS overrides - static flat grid, theme colors, no metallic sheen
F1 = ".snap-hint{text-align:center;font-size:10px;font-weight:800;letter-spacing:1.2px;color:rgba(255,255,255,.45);margin-top:10px;text-transform:uppercase}"
R1 = F1 + "\n" + Q('''/* v60.19: welcome starters - static flat grid, theme-adaptive (carousel + metallic look removed) */
.snap-stage{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;position:static;overflow:visible;touch-action:auto;cursor:default;background:transparent;border-radius:0;perspective:none;box-shadow:none;margin-top:22px}
.snap-item{position:static!important;transform:none!important;opacity:1!important;width:calc(50% - 5px);min-width:158px;transition:none;will-change:auto;backface-visibility:visible;border-color:transparent;box-shadow:none}
.snap-item.on{border-color:transparent;box-shadow:none}
.starter-pill{-webkit-box-reflect:none;box-reflect:none;border:1.5px solid var(--line);background:var(--surface);color:var(--text)}
.starter-pill:hover{border-color:var(--accent)}
.starter-pill .ac-ico{background:var(--surface2);box-shadow:none}
.starter-pill .ac-text b{color:var(--text)}
.starter-pill .ac-text small{display:block;color:var(--muted);font-size:10.5px;font-weight:600;line-height:1.3}''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: never start the carousel
F2 = "initSnapCarousel();updateTopTitle();"
R2 = "/* v60.19: carousel removed */updateTopTitle();"
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'var APP_VERSION="60.18"'
R3 = 'var APP_VERSION="60.19"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Clean Welcome, size: %d bytes" % len(h.encode("utf-8")))
