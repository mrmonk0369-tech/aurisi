#!/usr/bin/env python3
# AURISI v60.43: SPLASH WORDMARK CASE FIX
#  Owner: splash shows AURISI in all caps - should be Aurisi.
#  The splash wordmark is 6 letter-spans; lower-case all but the first.
#  No other changes. Base: AURISI.html v60.42 (1879844). Idempotent.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.43"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.43 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.42"' in h, "base must be v60.42"

F1 = '<div class="splash-name"><span>A</span><span>U</span><span>R</span><span>I</span><span>S</span><span>I</span></div>'
R1 = '<div class="splash-name"><span>A</span><span>u</span><span>r</span><span>i</span><span>s</span><span>i</span></div>'
assert h.count(F1) == 1, "splash wordmark anchor not found"
h = h.replace(F1, R1)

F2 = 'var APP_VERSION="60.42"'
R2 = 'var APP_VERSION="60.43"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied splash wordmark fix, size: %d bytes" % len(h.encode("utf-8")))
