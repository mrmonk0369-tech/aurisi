#!/usr/bin/env python3
# AURISI v60.24: AURISI WORD + JAI SHREE RAM GREETING.
#  1) WELCOME = JUST THE WORD: the chat home shows only a big gradient
#     "Aurisi" (the old h2 gradient style) - all vandana/Om/chaupais
#     removed from the welcome screen.
#  2) GREETING MOVES INTO THE CHAT: when someone starts a brand-new chat,
#     Aurisi's FIRST reply opens with "Jai Shree Ram \U0001F64F", then a one-line
#     intro, then asks what they'd like to do (learn/quiz/homework/exam
#     prep). Added as an OPENING GREETING rule in SYS_PROMPT - fires only
#     on the first reply of a new conversation, never repeated later.
#  3) Cleanup: theme list in the app self-knowledge prompt no longer
#     mentions the removed Medium Grey theme.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.23 (1855834). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.24"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.24 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.23"' in h, "base must be v60.23"

# P1: welcome shows only the word "Aurisi" (big gradient h2 style returns)
F1 = '<div class="vandana"><span class="vd-flag">\U0001F549\ufe0f</span><span class="vd-jai">\u091c\u092f \u0936\u094d\u0930\u0940 \u0930\u093e\u092e</span><span class="vd-shlok">\u092d\u0942\u0924 \u092a\u093f\u0936\u093e\u091a \u0928\u093f\u0915\u091f \u0928\u0939\u093f\u0902 \u0906\u0935\u0948\u0964 \u092e\u0939\u093e\u092c\u0940\u0930 \u091c\u092c \u0928\u093e\u092e \u0938\u0941\u0928\u093e\u0935\u0948\u0965<br>\u0928\u093e\u0938\u0948 \u0930\u094b\u0917 \u0939\u0930\u0948 \u0938\u092c \u092a\u0940\u0930\u093e\u0964 \u091c\u092a\u0924 \u0928\u093f\u0930\u0902\u0924\u0930 \u0939\u0928\u0941\u092e\u0924 \u092c\u0940\u0930\u093e\u0965</span></div>'
R1 = '<h2>Aurisi</h2>'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: opening greeting rule in SYS_PROMPT
F2 = 'return profileLine()+toneLine+"You are Aurisi \u2014 created'
R2 = 'return profileLine()+toneLine+"OPENING GREETING: when this is the first reply of a brand-new conversation (no earlier turns), you MUST begin with \'Jai Shree Ram \U0001F64F\' as the very first line, then give a one-line warm introduction of yourself as their all-in-one AI teacher, then ask what they would like to do today (e.g. learn a topic, quiz, homework help, exam prep). Keep it to 3 short lines maximum, then fully answer whatever they asked. Never repeat this greeting in later replies of the same conversation. "+"You are Aurisi \u2014 created'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: drop removed Medium Grey theme from the app self-knowledge list
F3 = 'Themes: Lofi Coffee, Medium Grey, Peaches, Pure Black.'
R3 = 'Themes: Lofi Coffee, Peaches, Pure Black.'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.23"'
R4 = 'var APP_VERSION="60.24"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Aurisi Word + Greeting, size: %d bytes" % len(h.encode("utf-8")))
