#!/usr/bin/env python3
# AURISI v60.27: CINEMATIC SPLASH 2.0.
#  The old splash used the AI-rendered 3D gold logo (soft edges, cursive
#  "Aurisi" text baked inside, inconsistent lighting = amateur look).
#  NEW: a crisp inline-SVG brand mark - sharp geometric gold "A" (crossbar
#  tucked behind the legs, 4-point sparkle at the top-right shoulder) on a
#  deep warm squircle - used on the splash + login screens only (topbar
#  brand unchanged for now). Plus polish: cinematic vignette, richer
#  aurora blobs, bigger logo with drop-shadow, bigger AURISI wordmark with
#  accent glow, wider loading bar, 2200ms -> 2600ms breathing room.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.26 (1856310). Idempotent.
import sys, io, base64

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.27"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.27 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.26"' in h, "base must be v60.26"

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 448">'
 '<defs>'
 '<linearGradient id="au" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FBE29B"/><stop offset=".45" stop-color="#F2B44A"/><stop offset="1" stop-color="#C9741F"/></linearGradient>'
 '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A1D12"/><stop offset="1" stop-color="#140D07"/></linearGradient>'
 '<radialGradient id="hl" cx=".5" cy=".28" r=".75"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".14"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
 '</defs>'
 '<rect width="448" height="448" rx="112" fill="url(#bg)"/>'
 '<rect width="448" height="448" rx="112" fill="url(#hl)"/>'
 '<g fill="none" stroke="url(#au)" stroke-linecap="round" stroke-linejoin="round">'
 '<path d="M172 258 h104" stroke-width="30"/>'
 '<path d="M136 338 L224 118 L312 338" stroke-width="34"/>'
 '</g>'
 '<path d="M298 88 l8 20 20 8 -20 8 -8 20 -8 -20 -20 -8 20 -8 z" fill="#FFF4D9"/>'
 '</svg>')
MARK = "data:image/svg+xml;base64," + base64.b64encode(SVG.encode("utf-8")).decode("ascii")

# P1: define AURISI_MARK_URL right after the old logo const line
key = 'const AURISI_LOGO_DATA_URL='
idx = h.find(key)
assert idx > -1, "logo const not found"
eol = h.find("\n", idx)
assert eol > -1
ins = '\nconst AURISI_MARK_URL="' + MARK + '";'
h = h[:eol] + ins + h[eol:]

# P2: splash + login screens use the new crisp mark
F2 = 'function bootSplash(){\n  try{$("splashLogo").src=AURISI_LOGO_DATA_URL;$("loginLogo").src=AURISI_LOGO_DATA_URL}catch(e){}'
R2 = 'function bootSplash(){\n  try{$("splashLogo").src=AURISI_MARK_URL;$("loginLogo").src=AURISI_MARK_URL}catch(e){}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: cinematic CSS upgrades (appended after the last splash keyframes)
F3 = '@keyframes spFade{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}'
R3 = F3 + "\n" + Q('/* v60.27: cinematic splash upgrades */\n.boot-splash::after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 42%,rgba(0,0,0,.30) 100%);z-index:1}\n.sp-core{z-index:2}\n.sp-aurora i:nth-child(1){opacity:.52;width:380px;height:380px}\n.sp-aurora i:nth-child(2){opacity:.46;width:340px;height:340px}\n.sp-logo{width:126px;height:126px}\n.sp-logo img{width:116px;height:116px;border-radius:28px;box-shadow:0 18px 44px rgba(0,0,0,.45),0 4px 12px rgba(0,0,0,.3)}\n.splash-name{font-size:35px;letter-spacing:7px;filter:drop-shadow(0 2px 16px color-mix(in srgb,var(--accent) 38%,transparent))}\n.splash-tag{font-size:13px;letter-spacing:.6px}\n.splash-bar{width:210px}\n.splash-foot{font-size:10.5px}')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: a touch more breathing room
F4 = 'checkLogin();\n  },2200);'
R4 = 'checkLogin();\n  },2600);'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.26"'
R5 = 'var APP_VERSION="60.27"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Cinematic Splash, size: %d bytes" % len(h.encode("utf-8")))
