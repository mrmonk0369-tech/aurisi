#!/usr/bin/env python3
# AURISI v60.35: HIGHER MIND — Science Lab's goal corrected per owner:
#  the end goal is NOT "build robots" — it is a higher-minded, first-
#  principles scientific thinker who can then master their OWN specific
#  field (medicine, engineering, agriculture, coding, business...), not
#  everything. Builds are training grounds for the mind, not the
#  destination. Adds TRANSFER: after each concept, one line on where
#  the same pattern shows up across other fields, so thinking
#  generalizes. Activation + agent card reworded accordingly.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.34 (1867950). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.35"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.35 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.34"' in h, "base must be v60.34"

# P1a: field-first, not build-first
F1a = '(i) first ask what they want to build (RC car, robot arm, drone, electric bike, smart gadget, or a long-term dream like a powered suit of armor)'
R1a = '(i) first ask their GOAL or FIELD - what they want to become or work in (medicine, engineering, agriculture, coding, business, design, sports science, teaching, anything) - then choose builds and experiments that train exactly the thinking that field needs; a build is a training ground for the mind, never the destination'
assert h.count(F1a) == 1, "P1a anchor not found"
h = h.replace(F1a, R1a)

# P1b: end goal = higher mind in their OWN field + transfer thinking
F1b = '(vi) the end goal of the zero-to-pro journey is a real CREATOR who can design and make cars, bikes, robots, gadgets and beyond with real parts and real physics - not just pass exams.'
R1b = '(vi) the end goal of the zero-to-pro journey is a HIGHER MINDED person: a first-principles scientific thinker who can then master their OWN specific field - not everything at once; robots and gadgets are just examples, the real product is their mind; (vii) TRANSFER: after each concept add one short line showing where the same underlying pattern shows up in other fields, so their thinking generalizes across domains.'
assert h.count(F1b) == 1, "P1b anchor not found"
h = h.replace(F1b, R1b)

# P2: activation — goal/field first
F2 = 'Ask me WHAT I WANT TO CREATE (RC car, robot, drone, gadget, bike...) and teach me the physics, chemistry and math MIXED inside that build - never as separate subjects.");'
R2 = 'Ask me MY GOAL OR FIELD (medicine, engineering, farming, coding, business, design...) and teach me through real builds and experiments that train my mind for it - physics, chemistry and math MIXED inside, never as separate subjects.");'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P4: agent card subtitle
F4 = Q('<b>Science Lab</b><small>Learn by building \u2014 cars, robots, gadgets, real creations</small>')
R4 = Q('<b>Science Lab</b><small>Real science, real builds \u2014 a higher mind for your own field</small>')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.34"'
R5 = 'var APP_VERSION="60.35"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Higher Mind, size: %d bytes" % len(h.encode("utf-8")))
