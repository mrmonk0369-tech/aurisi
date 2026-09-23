#!/usr/bin/env python3
# AURISI v60.32: SCIENCE LAB — practical applied Physics + Chemistry + Math.
#  1) SYS_PROMPT gets an APPLIED SCIENCE MODE section: teach one concept
#     at a time in the HOOK -> EVERYDAY ANCHOR -> DO IT (safe hands-on
#     experiment / real calculation) -> THE SCIENCE (formula, first
#     principles, Socratic) -> PREDICT ([[Q]]) -> REAL WORLD -> choose
#     next ([[OPTIONS]]) loop, Oxford/Harvard + science-movie style.
#  2) scienceLab() feature room (chat reset + activation message).
#  3) Science Lab agent card after the Situation card in the grid.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.31 (1861948). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.32"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.32 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.31"' in h, "base must be v60.31"

# P1: APPLIED SCIENCE MODE rules in SYS_PROMPT (after SITUATION MODE)
F1 = 'end with a suggestion for the next scenario. "+"You are Aurisi'
R1 = 'end with a suggestion for the next scenario. "+"APPLIED SCIENCE MODE: when the user starts with SCIENCE LAB ON, taps the Science Lab card, or asks to learn Physics, Chemistry or Mathematics practically / applied / the real way, teach like the best of Oxford, Harvard and a science movie, one concept at a time in this loop: (1) HOOK - open with a real-world phenomenon or movie-grade scenario that uses the concept (rocket launch, arc reactor, cricket ball swing, cooking, mobile screens, UPI payments); (2) EVERYDAY ANCHOR - explain it with things from their daily life (cricket, kitchen, kirana shop bills, vehicles, water tank) in the user\'s language; (3) DO IT - for Physics and Chemistry give a SAFE hands-on experiment with common household materials: exact steps, what to observe, the expected result; never suggest dangerous chemicals, flames near the face, or mixing cleaning agents; for Mathematics give a small real calculation they can actually do (split a bill, measure a wall, count score patterns); include a [[SVG]] diagram of the setup or figure when it helps; (4) THE SCIENCE - now name the exact concept, formula or theorem, and explain WHY it works from first principles, Socratic style: ask one why question and wait for their reply; (5) PREDICT - one applied [[Q]] question: what happens if one variable changes (thinking, not memorization); (6) REAL WORLD - where it is used in engineering, ISRO, rockets, phones, medicine, cryptography or daily life; (7) then ask via [[OPTIONS]] to continue to the next concept, take a 5-question practical exam, or stop. Show every formula only after they have seen the situation it describes, and tie Math to real quantities they can touch (money, distance, time, speed). Keep each loop tight and exciting like a lab demo video. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: scienceLab() before situationRoom()
F2 = 'function situationRoom(){'
R2 = 'function scienceLab(){\n  roomStart("\U0001F52C","Science Lab");\n  quick("SCIENCE LAB ON. Teach me Physics, Chemistry or Math the practical applied way - real experiments, everyday examples, formulas behind them, and where the real world uses it. Ask me the topic first if needed.");\n}\nfunction situationRoom(){'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2, 1)

# P3: agent card after the Situation card
F3 = Q("  html+='<button class=\"agent-card\" onclick=\"switchView(~B~'chat~B~');situationRoom()\"><span class=\"agent-ico\">\U0001F3AD</span><span><b>Situation</b><small>You are the hero \u2014 live the story, decide under pressure</small></span></button>';\n")
R3 = F3 + Q("  html+='<button class=\"agent-card\" onclick=\"switchView(~B~'chat~B~');scienceLab()\"><span class=\"agent-ico\">\U0001F52C</span><span><b>Science Lab</b><small>Physics, Chemistry & Math \u2014 practical, applied, real world</small></span></button>';\n")
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.31"'
R4 = 'var APP_VERSION="60.32"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Science Lab (PCM), size: %d bytes" % len(h.encode("utf-8")))
