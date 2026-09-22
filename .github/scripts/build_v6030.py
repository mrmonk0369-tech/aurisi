#!/usr/bin/env python3
# AURISI v60.30: CLEAN SPLASH — super minimal (Google/Notion style).
#  Replaces the v60.27 cinematic splash override with a minimal one:
#  flat near-black screen, aurora blobs + vignette + dots + ring/glow
#  gone, logo smaller with no shadow, plain spaced wordmark (no per-
#  letter stagger, no gradient/glow), tag + loading bar hidden, one
#  gentle fade for the whole core, and 2600ms -> 1500ms timing.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.29 (1862008). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.30"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.30 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.29"' in h, "base must be v60.29"

# P1: replace the whole v60.27 cinematic override block with minimal styles
F1 = Q('/* v60.27: cinematic splash upgrades */\n.boot-splash::after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 42%,rgba(0,0,0,.30) 100%);z-index:1}\n.sp-core{z-index:2}\n.sp-aurora i:nth-child(1){opacity:.52;width:380px;height:380px}\n.sp-aurora i:nth-child(2){opacity:.46;width:340px;height:340px}\n.sp-logo{width:126px;height:126px}\n.sp-logo img{width:116px;height:116px;border-radius:28px;box-shadow:0 18px 44px rgba(0,0,0,.45),0 4px 12px rgba(0,0,0,.3)}\n.splash-name{font-size:35px;letter-spacing:7px;filter:drop-shadow(0 2px 16px color-mix(in srgb,var(--accent) 38%,transparent))}\n.splash-tag{font-size:13px;letter-spacing:.6px}\n.splash-bar{width:210px}\n.splash-foot{font-size:10.5px}')
R1 = Q('/* v60.30: minimal splash (clean style) */\n.boot-splash{background:#070709}\n.boot-splash::after{content:none}\n.sp-aurora{display:none}\n.sp-dots{display:none}\n.sp-ring,.sp-glow{display:none}\n.sp-core{z-index:2;animation:spFade .5s ease both}\n.sp-logo{width:84px;height:84px}\n.sp-logo img{width:84px;height:84px;border-radius:21px;box-shadow:none}\n.splash-name{font-size:21px;letter-spacing:9px;font-weight:600;color:#dcdce0;background:none;-webkit-text-fill-color:#dcdce0;filter:none;animation:none;opacity:1;transform:none}\n.splash-name span{animation:none;opacity:1;transform:none}\n.splash-tag{display:none}\n.splash-bar{display:none}\n.splash-foot{font-size:10px;opacity:.5}')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: faster splash timing 2600 -> 1500, fade 650 -> 450
F2 = 'checkLogin();\n  },2600);'
R2 = 'checkLogin();\n  },1500);'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'setTimeout(function(){try{s.style.display="none"}catch(e2){}},650)}'
R3 = 'setTimeout(function(){try{s.style.display="none"}catch(e2){}},450)}'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.29"'
R4 = 'var APP_VERSION="60.30"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Clean Splash, size: %d bytes" % len(h.encode("utf-8")))
