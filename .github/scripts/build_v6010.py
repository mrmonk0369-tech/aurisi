#!/usr/bin/env python3
# AURISI v60.10: theme cleanup trace.
# The UI (topbar popup + Settings > More tab) already shows only the 4
# themes since v60.9. This fixes the LAST remaining reference: the AI
# system prompt still listed the old themes (Pure Black, Tangerine Sky,
# Peach Horizon, Lavender) — the AI would have described deleted themes
# to students. Now it lists the real 4.
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.9. Idempotent: no-op if already v60.10.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.10"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.10 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.9"' in h, "base must be v60.9"

# P1: AI system prompt — correct theme list
F1 = 'Themes: Pure Black, Tangerine Sky, Peach Horizon, Lavender.'
R1 = 'Themes: Lofi Coffee, Dark Roast, Peaches Dark, Pure Black.'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# sanity: no other visible old-theme text remains
for dead in ['Tangerine Sky,', 'Peach Horizon,', 'Lavender,']:
    assert h.count(dead) == 0, "unexpected leftover: " + dead

F2 = 'var APP_VERSION="60.9"'
R2 = 'var APP_VERSION="60.10"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied theme trace cleanup, size: %d bytes" % len(h.encode("utf-8")))
