#!/usr/bin/env python3
# AURISI v60.31: ORIGINAL LOGO SPLASH — user wants the original gold
#  logo (AURISI_LOGO_DATA_URL, circular metallic render) back on the
#  splash + login instead of the v60.27 vector A-mark. Minimal clean
#  layout from v60.30 stays (flat black, wordmark, no drama); logo
#  shown slightly larger (104px) since the original is circular.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.30 (1861934). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.31"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.31 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.30"' in h, "base must be v60.30"

# P1: splash + login use the ORIGINAL logo again
F1 = '$("splashLogo").src=AURISI_MARK_URL;$("loginLogo").src=AURISI_MARK_URL'
R1 = '$("splashLogo").src=AURISI_LOGO_DATA_URL;$("loginLogo").src=AURISI_LOGO_DATA_URL'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: logo a bit larger for the circular original
F2 = '.sp-logo{width:84px;height:84px}\n.sp-logo img{width:84px;height:84px;border-radius:21px;box-shadow:none}'
R2 = '.sp-logo{width:104px;height:104px}\n.sp-logo img{width:104px;height:104px;border-radius:26px;box-shadow:none}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'var APP_VERSION="60.30"'
R3 = 'var APP_VERSION="60.31"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Original Logo Splash, size: %d bytes" % len(h.encode("utf-8")))
