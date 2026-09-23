#!/usr/bin/env python3
# AURISI v60.39: NO BIOGRAPHY + SVG FENCE FIX + CLEAN ROOM START
#  Owner feedback: (1) no need to tell about owner/creator of concepts -
#     remove the PERSON section; also never volunteer app-creator info in
#     the greeting; (2) from screenshots: [[SVG]] token sometimes emitted
#     inside a markdown code fence -> renders as literal code instead of a
#     diagram (data-svslot leak) - unwrap fenced SVG tokens before parsing;
#     (3) room activation messages (SCIENCE LAB ON... etc) are internal -
#     hide them like the video lesson does (HIDE_SEND), fixes the clipped
#     first-bubble under the room banner.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.38 (1869686). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.39"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.39 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.38"' in h, "base must be v60.38"

# P1: deep-dive - drop PERSON, forbid biography
F1 = '(a) PERSON - one line on the human behind it, who discovered or invented it and one vivid detail from their story; (b) PICTURE - MANDATORY, NO EXCEPTIONS: every important concept MUST include at least one [[SVG]] diagram placed immediately after the PERSON line and before any long explanation - a concept taught without a diagram is a failed teaching; draw the intuition, whenever possible as three panels in one canvas: BEFORE (the simple everyday case), THE IDEA (an arrow or transform showing what changes), AFTER (the resulting effect), every part labeled; (c) NOTATION - the clean formal math or chemistry notation in text, shown only after the picture is understood; (d) ESSENCE - one single line capturing the entire concept (example: the Jacobian matrix records how a smooth map locally distorts area).'
R1 = '(a) PICTURE - MANDATORY, NO EXCEPTIONS: every important concept MUST include at least one [[SVG]] diagram before any explanation - a concept taught without a diagram is a failed teaching; draw the intuition, whenever possible as three panels in one canvas: BEFORE (the simple everyday case), THE IDEA (an arrow or transform showing what changes), AFTER (the resulting effect), every part labeled; (b) NOTATION - the clean formal math or chemistry notation in text, shown only after the picture is understood; (c) ESSENCE - one single line capturing the entire concept (example: the Jacobian matrix records how a smooth map locally distorts area). Never talk about who discovered or invented the concept - no owner, no creator, no biography, no history: the student is here to master the idea itself.'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: greeting - never volunteer creator info
F2 = 'then give a one-line warm introduction of yourself as their all-in-one AI teacher, then ask'
R2 = 'then give a one-line warm introduction of yourself as their all-in-one AI teacher (never mention who built you, your creator, owner or developer in this introduction - reveal that only if explicitly asked later), then ask'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: unwrap [[SVG]] tokens wrapped in markdown code fences
F3 = '    let svData=null;'
R3 = '    txt=String(txt).replace(/```[a-zA-Z]*~B~s*(~B~[~B~[~B~s*SVG[~B~s~B~S]*?~B~]~B~])~B~s*```/gi,function(m,t){return t});\n    let svData=null;'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, Q(R3))

# P4: hide science lab activation message
F4 = 'function scienceLab(){\n  var lv=sciLevel(),j=sciGet();\n  roomStart("\U0001F52C","Science Lab");\n  quick("SCIENCE LAB ON.'
R4 = 'function scienceLab(){\n  var lv=sciLevel(),j=sciGet();\n  roomStart("\U0001F52C","Science Lab");\n  HIDE_SEND=true;try{quick("SCIENCE LAB ON.'
assert h.count(F4) == 1, "P4a anchor not found"
h = h.replace(F4, R4)
F4b = ' MIXED inside, never as separate subjects.");\n}'
R4b = ' MIXED inside, never as separate subjects.");}catch(e){}finally{HIDE_SEND=false}\n}'
assert h.count(F4b) == 1, "P4b anchor not found"
h = h.replace(F4b, R4b)

# P5: hide situation room activation message
F5 = 'function situationRoom(){\n  roomStart("\U0001F3AD","Situation");\n  quick("SITUATION MODE ON.'
R5 = 'function situationRoom(){\n  roomStart("\U0001F3AD","Situation");\n  HIDE_SEND=true;try{quick("SITUATION MODE ON.'
assert h.count(F5) == 1, "P5a anchor not found"
h = h.replace(F5, R5)
F5b = 'play it out scene by scene with decision points.");\n}'
R5b = 'play it out scene by scene with decision points.");}catch(e){}finally{HIDE_SEND=false}\n}'
assert h.count(F5b) == 1, "P5b anchor not found"
h = h.replace(F5b, R5b)

# P6: hide daily brief activation message
F6 = 'function dailyBrief(){\n  roomStart("~B~u2600~B~uFE0F","Daily Brief");\n  quick("Today'
R6 = 'function dailyBrief(){\n  roomStart("~B~u2600~B~uFE0F","Daily Brief");\n  HIDE_SEND=true;try{quick("Today'
assert h.count(Q(F6)) == 1, "P6a anchor not found"
h = h.replace(Q(F6), Q(R6))
F6b = 'no | inside the question or answer). Keep it tight.");\n}'
R6b = 'no | inside the question or answer). Keep it tight.");}catch(e){}finally{HIDE_SEND=false}\n}'
assert h.count(F6b) == 1, "P6b anchor not found"
h = h.replace(F6b, R6b)

F7 = 'var APP_VERSION="60.38"'
R7 = 'var APP_VERSION="60.39"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied no-biography + svg fence fix + hidden activations, size: %d bytes" % len(h.encode("utf-8")))
