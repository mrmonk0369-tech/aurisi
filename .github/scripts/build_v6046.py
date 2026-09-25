#!/usr/bin/env python3
# AURISI v60.46: SPLASH REVERT - back to the clean bold sans wordmark
# Owner verdict: the Great Vibes script font splash does not look good.
# This removes the embedded 42.8KB script font and restores the exact
# v60.43 splash: per-letter gold wordmark (27px, weight 800, spaced,
# staggered pop-in). Everything else from v60.45 stays (institute courses,
# Netflix-style player, commission plumbing).
# Patch strings live in sibling .txt files (zero escaping tricks):
#   s1_old/s1_new      - wordmark HTML (single span -> per-letter spans)
#   old_splash_css.txt - the v60.43 .splash-name rule (replaces the
#                        @font-face block + script .splash-name rule; the
#                        font b64 is cut out by index surgery, not matched)
#   s3_old/s3_new      - keyframes -> per-letter span css + keyframes
# Base: v60.45 (1947341). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.46"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.46 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.45"' in h, "base must be v60.45"

# P1: wordmark back to per-letter spans
F1, R1 = rf("s1_old.txt"), rf("s1_new.txt")
assert h.count(F1) == 1, "P1 anchor: %d" % h.count(F1)
h = h.replace(F1, R1)

# P2: cut @font-face 'Aurisi Script' + script .splash-name rule, restore v60.43 css
i = h.find("@font-face{font-family:'Aurisi Script'")
assert i > 0, "font-face block not found"
ns = h.find(".splash-name{", i)
assert ns > i, "script splash-name rule not found"
j = h.find("}", ns) + 1
h = h[:i] + rf("old_splash_css.txt").rstrip("\n") + h[j:]

# P3: per-letter span css + original keyframes
F3, R3 = rf("s3_old.txt").rstrip("\n"), rf("s3_new.txt").rstrip("\n")
assert h.count(F3) == 1, "P3 anchor: %d" % h.count(F3)
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.45"'
R4 = 'var APP_VERSION="60.46"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied splash revert, size: %d bytes" % len(h.encode("utf-8")))
