#!/usr/bin/env python3
# AURISI v60.29: SITUATION MODE — cinematic situational learning.
#  1) SYS_PROMPT gets a SITUATION MODE section: cast the student as the
#     hero of a movie-style scenario that secretly tests their studies;
#     cinematic scenes, decision points via [[OPTIONS]], realistic
#     consequences + Mind Spark lessons, finale debrief with Mind Rating.
#  2) situationRoom() feature room (chat reset + activation message).
#  3) Situation agent card in the Agents grid (after New Lesson).
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.28 (1860216). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.29"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.29 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.28"' in h, "base must be v60.28"

# P1: SITUATION MODE rules in SYS_PROMPT (after OPENING GREETING block)
F1 = 'Never repeat this greeting in later replies of the same conversation. "+"You are Aurisi'
R1 = 'Never repeat this greeting in later replies of the same conversation. "+"SITUATION MODE: when the user starts with SITUATION MODE ON, asks for situation mode / a scenario / to be the hero, you run an immersive movie-style learning adventure: (1) cast the student as the HERO of a dramatic, age-appropriate scenario that secretly tests their studies — e.g. a scientist racing a lab crisis, a detective cracking a case, a young ruler, an engineer, a doctor, an explorer; if the subject or topic is unclear, ask with 3 exciting setting options using [[OPTIONS|...]]; (2) play in short cinematic scenes of 2-4 sentences (sights, sounds, stakes, a ticking clock), each ending on a decision point with 3-4 choices via [[OPTIONS|...]] — mix smart, risky and tempting-but-wrong; (3) the student may type their own move instead of picking — treat it as a real choice and judge it fairly; (4) never just say wrong answer: show realistic consequences — smart moves advance the story, weak moves create setbacks to recover from — and after each consequence add a one-line Mind Spark naming the concept that mattered; (5) stay fully in character until the finale, then give a cinematic ending plus a short debrief: what the hero did great, which concepts were exercised, and a Mind Rating out of 5 stars with one line why; (6) keep it tight — 4 to 6 scenes total, end with a suggestion for the next scenario. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: situationRoom() before dailyBrief()
F2 = Q('function dailyBrief(){\n  roomStart("~B~u2600~B~uFE0F","Daily Brief");')
R2 = Q('function situationRoom(){\n  roomStart("🎭","Situation");\n  quick("SITUATION MODE ON. Cast me as the hero of a movie-style scenario that secretly tests my studies — play it out scene by scene with decision points.");\n}\nfunction dailyBrief(){\n  roomStart("~B~u2600~B~uFE0F","Daily Brief");')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: agent card after the New Lesson card
F3 = Q("  html+='<button class=\"agent-card\" onclick=\"switchView(~B~'chat~B~');roomStart(~B~'\u2728~B~',~B~'New Lesson~B~')\"><span class=\"agent-ico\">\u2728</span><span><b>New Lesson</b><small>Start a fresh chat on any subject or topic</small></span></button>';\n")
R3 = Q("  html+='<button class=\"agent-card\" onclick=\"switchView(~B~'chat~B~');situationRoom()\"><span class=\"agent-ico\">🎭</span><span><b>Situation</b><small>You are the hero — live the story, decide under pressure</small></span></button>';\n") + F3
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.28"'
R4 = 'var APP_VERSION="60.29"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Situation Mode, size: %d bytes" % len(h.encode("utf-8")))
