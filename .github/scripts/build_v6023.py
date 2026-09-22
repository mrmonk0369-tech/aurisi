#!/usr/bin/env python3
# AURISI v60.23: SHRI RAM WELCOME (pure devotional).
#  ALL "Aurisi" branding removed from the chat welcome (heading, subtitle,
#  tour button). What opens the app now is ONLY:
#    - a gently pulsing Om symbol (replaces the flag)
#    - a big gradient "जय श्री राम"
#    - Hanuman Chalisa's most powerful chaupais (24 & 25, adjacent pair):
#        भूत पिशाच निकट नहिं आवै। महाबीर जब नाम सुनावै॥
#        नासै रोग हरै सब पीरा। जपत निरंतर हनुमत बीरा॥
#  (chaupai 24 = fear/evil removal + protection, chaupai 25 = disease/pain
#   removal - the pair most widely cited as Chalisa's most powerful verses)
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.22 (1855992). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.23"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.23 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.22"' in h, "base must be v60.22"

# P1: welcome = ONLY Om + Jai Shri Ram + Chalisa chaupais (Aurisi branding removed)
F1 = '<div class="vandana"><span class="vd-flag">\U0001F6A9</span><span class="vd-shlok">\u092e\u0928\u094b\u091c\u0935\u0902 \u092e\u093e\u0930\u0941\u0924\u0924\u0941\u0932\u094d\u092f\u0935\u0947\u0917\u0902 \u091c\u093f\u0924\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u092f\u0902 \u092c\u0941\u0926\u094d\u0927\u093f\u092e\u0924\u093e\u0902 \u0935\u0930\u093f\u0937\u094d\u0920\u092e\u0965<br>\u0935\u093e\u0924\u093e\u0924\u094d\u092e\u091c\u0902 \u0935\u093e\u0928\u0930\u092f\u0942\u0925\u092e\u0941\u0916\u094d\u092f\u0902 \u0936\u094d\u0930\u0940\u0930\u093e\u092e\u0926\u0942\u0924\u0902 \u0936\u0930\u0923\u0902 \u092a\u094d\u0930\u092a\u0926\u094d\u092f\u0947 \u0965</span><span class="vd-ram">\U0001F64F Ram Ram</span></div>\n        <h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>\n        <p data-i18n="welcomeSub">Your all-in-one teacher. Ask me anything \u2014 any subject, taught the way a great teacher would.</p>\n        <button class="feat-tour" onclick="showFeatures()">\u2728 What\'s inside AURISI?</button>'
R1 = '<div class="vandana"><span class="vd-flag">\U0001F549\ufe0f</span><span class="vd-jai">\u091c\u092f \u0936\u094d\u0930\u0940 \u0930\u093e\u092e</span><span class="vd-shlok">\u092d\u0942\u0924 \u092a\u093f\u0936\u093e\u091a \u0928\u093f\u0915\u091f \u0928\u0939\u093f\u0902 \u0906\u0935\u0948\u0964 \u092e\u0939\u093e\u092c\u0940\u0930 \u091c\u092c \u0928\u093e\u092e \u0938\u0941\u0928\u093e\u0935\u0948\u0965<br>\u0928\u093e\u0938\u0948 \u0930\u094b\u0917 \u0939\u0930\u0948 \u0938\u092c \u092a\u0940\u0930\u093e\u0964 \u091c\u092a\u0924 \u0928\u093f\u0930\u0902\u0924\u0930 \u0939\u0928\u0941\u092e\u0924 \u092c\u0940\u0930\u093e\u0965</span></div>'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: Om symbol styling (bigger, keeps the gentle pulse)
F2 = '.vandana .vd-flag{font-size:24px;line-height:1;animation:vdGlow 2.8s ease-in-out infinite}'
R2 = '.vandana .vd-flag{font-size:34px;line-height:1;animation:vdGlow 3.2s ease-in-out infinite}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: big gradient Jai Shri Ram heading (replaces the Ram Ram line style)
F3 = '.vandana .vd-ram{font-size:15px;font-weight:800;letter-spacing:.6px;color:var(--accent)}'
R3 = Q('.vandana .vd-jai{font-size:clamp(30px,8.5vw,44px);font-weight:800;letter-spacing:.5px;line-height:1.25;background:linear-gradient(92deg,var(--text) 30%,var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: chaupais slightly larger, a touch more breathing room
F4 = '.vandana{display:flex;flex-direction:column;align-items:center;gap:7px;margin:0 0 16px;animation:fadeUp .6s ease}'
R4 = '.vandana{display:flex;flex-direction:column;align-items:center;gap:10px;margin:0 0 10px;animation:fadeUp .6s ease}'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = '.vandana .vd-shlok{font-size:12.5px;line-height:1.8;color:var(--muted);max-width:440px;text-align:center}'
R5 = '.vandana .vd-shlok{font-size:13.5px;line-height:1.9;color:var(--muted);max-width:460px;text-align:center}'
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

F6 = 'var APP_VERSION="60.22"'
R6 = 'var APP_VERSION="60.23"'
assert h.count(F6) == 1
h = h.replace(F6, R6)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Shri Ram Welcome, size: %d bytes" % len(h.encode("utf-8")))
