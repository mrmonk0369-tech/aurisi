#!/usr/bin/env python3
# AURISI v60.26: PWA INSTALL FIX (correct manifest + logo on live site).
#  BUG: a legacy boot block injected a SECOND manifest <link> (a data: URL)
#  plus duplicate favicon/apple-touch-icon links on EVERY protocol - including
#  the live site. On iOS, apple-touch-icons served as data: URLs are not
#  supported -> "no logo" when adding to Home Screen; on Android the second
#  manifest (data: URL, 448px icons, start_url ".") is invalid for install.
#  FIX: that whole injection block now runs ONLY on file:// (standalone file
#  copies, where it was needed). On the live site the real manifest.json +
#  icon-192/512/apple-touch-icon.png links are the only ones the browser sees.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.25 (1856279). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.26"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.26 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.25"' in h, "base must be v60.25"

# P1: gate the data-URL manifest + favicon/apple-touch-icon injection to
#     file:// only (standalone copies). Live https site keeps the real ones.
F1 = '    try{\n      var man={name:'
R1 = '    if(location.protocol==="file:")try{\n      var man={name:'
assert h.count(F1) == 1, "P1 anchor not found (count=%d)" % h.count(F1)
h = h.replace(F1, R1)

F2 = 'var APP_VERSION="60.25"'
R2 = 'var APP_VERSION="60.26"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied PWA Install Fix, size: %d bytes" % len(h.encode("utf-8")))
