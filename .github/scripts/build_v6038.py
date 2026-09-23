#!/usr/bin/env python3
# AURISI v60.38: EDGE-TO-EDGE CHAT + MANDATORY VISUALS
#  Owner feedback: (1) chat inside a border/card in feature rooms - remove
#  ALL inner boxes, chat must be edge-to-edge across the whole app;
#  (2) SVG visuals did not appear - make the deep-dive diagram MANDATORY.
#  Changes:
#  P1 CSS: body.room-on .bubble.ai card -> transparent, no border/radius/shadow
#  P2 CSS: user bubble - remove 2px border + hard shadow (soft flat bubble)
#  P3 CSS: user bubble tail - border transparent
#  P4 CSS: katex-display - remove boxed background/border (flat formula)
#  P5 CSS: chat-col side padding 22px -> 14px (fuller edge-to-edge feel)
#  P6 PROMPT: PICTURE clause "whenever possible" -> MANDATORY, diagram
#     immediately after PERSON line, teaching without diagram = failed.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.37 (1869587). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.38"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.38 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.37"' in h, "base must be v60.37"

# P1: room AI bubble card -> flat edge-to-edge
F1 = 'body.room-on .bubble.ai{background:var(--surface);border:1px solid var(--line);border-radius:18px;box-shadow:0 4px 16px rgba(0,0,0,.07)}'
R1 = 'body.room-on .bubble.ai{background:transparent;border:none;border-radius:0;box-shadow:none}'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: user bubble - no border, no hard shadow
F2 = '.msg-row.user .bubble{position:relative;background:var(--ai-user-bg);color:var(--ai-user-text);border:2px solid var(--text);border-radius:18px 18px 5px 18px;padding:11px 15px;white-space:pre-wrap;box-shadow:3px 3px 0 var(--line)}'
R2 = '.msg-row.user .bubble{position:relative;background:var(--ai-user-bg);color:var(--ai-user-text);border:none;border-radius:18px 18px 5px 18px;padding:11px 15px;white-space:pre-wrap;box-shadow:none}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: user bubble tail - transparent borders
F3 = '.msg-row.user .bubble::after{content:"";position:absolute;right:16px;bottom:-8px;width:12px;height:12px;background:var(--ai-user-bg);border-right:2px solid var(--text);border-bottom:2px solid var(--text);transform:rotate(45deg);border-radius:0 0 4px 0}'
R3 = '.msg-row.user .bubble::after{content:"";position:absolute;right:16px;bottom:-8px;width:12px;height:12px;background:var(--ai-user-bg);border-right:2px solid transparent;border-bottom:2px solid transparent;transform:rotate(45deg);border-radius:0 0 4px 0}'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: katex display - flat, no boxed background
F4 = '.ai-md .katex-display{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:14px 0;position:relative;cursor:zoom-in;overflow-x:auto}'
R4 = '.ai-md .katex-display{background:transparent;border:none;border-radius:0;padding:10px 2px;margin:14px 0;position:relative;cursor:zoom-in;overflow-x:auto}'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: chat column - fuller edge-to-edge
F5 = '.chat-col{max-width:780px;margin:0 auto;padding:20px 22px 26px}'
R5 = '.chat-col{max-width:780px;margin:0 auto;padding:18px 14px 26px}'
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: PICTURE clause -> MANDATORY
F6 = '(b) PICTURE - a [[SVG]] diagram of the intuition, whenever possible drawn as three panels in one canvas: BEFORE (the simple everyday case), THE IDEA (an arrow or transform showing what changes), AFTER (the resulting effect), every part labeled; (c) NOTATION'
R6 = '(b) PICTURE - MANDATORY, NO EXCEPTIONS: every important concept MUST include at least one [[SVG]] diagram placed immediately after the PERSON line and before any long explanation - a concept taught without a diagram is a failed teaching; draw the intuition, whenever possible as three panels in one canvas: BEFORE (the simple everyday case), THE IDEA (an arrow or transform showing what changes), AFTER (the resulting effect), every part labeled; (c) NOTATION'
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.37"'
R7 = 'var APP_VERSION="60.38"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied edge-to-edge chat + mandatory visuals, size: %d bytes" % len(h.encode("utf-8")))
