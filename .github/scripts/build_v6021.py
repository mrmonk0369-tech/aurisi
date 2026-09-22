#!/usr/bin/env python3
# AURISI v60.21: GEMINI-STYLE WELCOME (no box).
#  1) BOX REMOVED: the welcome greeting sat inside a bordered, shadowed
#     design-system card (.welcome,.lock-pdf rule). ".welcome" is taken out
#     of that rule - the greeting now sits directly on the page background,
#     exactly like ChatGPT / Gemini welcome screens.
#  2) BIG BEAUTIFUL HEADING: "Hi, I'm Aurisi" is now a large bold heading
#     with a smooth text-color -> accent gradient (Gemini-style), sized
#     responsively with clamp().
#  3) SUBTITLE RESTORED: the welcomeSub line ("Your all-in-one teacher...")
#     now renders under the heading (it existed in every language's i18n
#     dictionary but was never shown). data-i18n keeps it translated.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.20 (1854677). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.21"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.21 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.20"' in h, "base must be v60.20"

# P1: welcome OUT of the boxed design-system card rule (box removed)
F1 = '.welcome,.lock-pdf{border-radius:var(--ds-r-lg);border:1px solid var(--line);box-shadow:var(--ds-shadow-1);transition:box-shadow var(--ds-tr),transform var(--ds-tr),border-color var(--ds-tr)}'
R1 = '.lock-pdf{border-radius:var(--ds-r-lg);border:1px solid var(--line);box-shadow:var(--ds-shadow-1);transition:box-shadow var(--ds-tr),transform var(--ds-tr),border-color var(--ds-tr)}'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: big premium gradient heading (ChatGPT/Gemini style)
F2 = '.welcome h2{margin-top:18px;font-size:23px}'
R2 = Q('.welcome h2{margin:0 0 8px;font-size:clamp(26px,6.4vw,34px);font-weight:800;letter-spacing:-.6px;line-height:1.15;background:linear-gradient(92deg,var(--text) 30%,var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: subtitle tweak (was margin-top:8px on .welcome p)
F3 = '.welcome p{color:var(--muted);margin-top:8px;font-size:14px}'
R3 = '.welcome p{color:var(--muted);margin:0 auto 14px;font-size:14px;max-width:480px;line-height:1.5}'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: render the subtitle (welcomeSub exists in every language's i18n)
F4 = '<h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>\n        <button class="feat-tour"'
R4 = '<h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>\n        <p data-i18n="welcomeSub">Your all-in-one teacher. Ask me anything — any subject, taught the way a great teacher would.</p>\n        <button class="feat-tour"'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.20"'
R5 = 'var APP_VERSION="60.21"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Gemini Welcome, size: %d bytes" % len(h.encode("utf-8")))
