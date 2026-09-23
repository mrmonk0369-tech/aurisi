#!/usr/bin/env python3
# AURISI v60.34: CREATOR PATH — Science Lab teaches by BUILDING, not by
#  subject. Physics + Chemistry + Math are woven MIXED into what the
#  student wants to create (car, bike, robot, drone, gadget), just-in-
#  time, never as separate subjects; builds are real and scaled from
#  household/scrap materials to real affordable local-market parts;
#  milestones become a BUILD PORTFOLIO. Level 4 renamed Pro -> Creator.
#  scienceLab() activation now asks what they want to CREATE.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.33 (1866589). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.34"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.34 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.33"' in h, "base must be v60.33"

# P1: prompt — CREATOR INTEGRATION rules (after ZERO TO PRO JOURNEY)
F1 = 'celebrate level-ups in one line and tell them what they unlocked. "+"You are Aurisi'
R1 = 'celebrate level-ups in one line and tell them what they unlocked. CREATOR INTEGRATION: never teach Physics, Chemistry and Math as separate subjects inside the lab - teach them MIXED through what the student wants to CREATE: (i) first ask what they want to build (RC car, robot arm, drone, electric bike, smart gadget, or a long-term dream like a powered suit of armor); (ii) break that build into stages (frame, power, motion, control, sensors, finishing) and for each stage teach exactly the physics, chemistry and math the build needs at that moment, just-in-time, woven into the build steps - never as separate chapters and never with subject labels; (iii) Math is the invisible thread connecting everything: every build step includes a real calculation (gear ratio, battery life, current draw, material cost, frame geometry); (iv) scale builds to reality: early milestones from household and scrap materials (cardboard buggy, bottle rocket car, salt-dough circuit), later milestones use real affordable parts from the local market (DC motors, batteries, switches, sensors, basic microcontroller boards); (v) keep a BUILD PORTFOLIO: each milestone ends with something that actually works, and the debrief names every concept used across all three fields together; (vi) the end goal of the zero-to-pro journey is a real CREATOR who can design and make cars, bikes, robots, gadgets and beyond with real parts and real physics - not just pass exams. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: scienceLab activation — creator framing
F2 = 'quick("SCIENCE LAB ON. My zero-to-pro journey: Level "+lv.n+" ("+lv.name+"), "+j.xp+" XP, "+j.done.length+" concepts mastered"+(j.done.length?(" - last ones: "+j.done.slice(-3).join(", ")):" - starting from zero")+". Continue my roadmap from exactly where I am. Teach me Physics, Chemistry or Math the practical applied way - real experiments, everyday examples, formulas behind them, and where the real world uses it. Ask me the topic/subject first if needed.");'
R2 = 'quick("SCIENCE LAB ON. I learn by BUILDING. My journey so far: Level "+lv.n+" ("+lv.name+"), "+j.xp+" XP, "+j.done.length+" concepts mastered"+(j.done.length?(" - last ones: "+j.done.slice(-3).join(", ")):" - starting from zero")+". Continue from exactly where I am. Ask me WHAT I WANT TO CREATE (RC car, robot, drone, gadget, bike...) and teach me the physics, chemistry and math MIXED inside that build - never as separate subjects.");'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: level 4 renamed Pro -> Creator
F3 = 'var SCI_LEVELS=[[0,"Spark"],[100,"Foundation"],[300,"Builder"],[600,"Engineer"],[1000,"Pro"]];'
R3 = 'var SCI_LEVELS=[[0,"Spark"],[100,"Foundation"],[300,"Builder"],[600,"Engineer"],[1000,"Creator"]];'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: agent card subtitle — creator framing
F4 = Q('<b>Science Lab</b><small>Physics, Chemistry & Math \u2014 practical, applied, real world</small>')
R4 = Q('<b>Science Lab</b><small>Learn by building \u2014 cars, robots, gadgets, real creations</small>')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.33"'
R5 = 'var APP_VERSION="60.34"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Creator Path, size: %d bytes" % len(h.encode("utf-8")))
