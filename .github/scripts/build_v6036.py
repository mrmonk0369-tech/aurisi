#!/usr/bin/env python3
# AURISI v60.36: FIELD PATHS — specialized branches named explicitly.
#  The student's field can be ANY specialty (robotics engineering,
#  mechanical, electrical, aerospace, nanotechnology, biotech, civil...)
#  and the AI now presents a FIELD PATH: the sub-fields and skills
#  that specialty needs, mapped onto the Spark->Creator levels; from
#  Engineer level, builds specialize toward their chosen field.
#  Activation examples updated to name the specialized branches.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.35 (1868432). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.36"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.36 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.35"' in h, "base must be v60.35"

# P1: field list + FIELD PATH rule
F1 = '(i) first ask their GOAL or FIELD - what they want to become or work in (medicine, engineering, agriculture, coding, business, design, sports science, teaching, anything) - then choose builds and experiments that train exactly the thinking that field needs; a build is a training ground for the mind, never the destination'
R1 = '(i) first ask their GOAL or FIELD - what they want to become or work in (medicine, robotics engineering, mechanical, electrical, aerospace, nanotechnology, biotech, civil, agriculture, coding, business, design, sports science, teaching, anything) - then present their FIELD PATH: name the sub-fields and skills that specialty needs (e.g. robotics = mechanics + electronics + control systems + programming) mapped onto the Spark to Creator levels; from Engineer level onward, builds should specialize toward their chosen field; a build is a training ground for the mind, never the destination'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: activation examples include specialized branches
F2 = 'Ask me MY GOAL OR FIELD (medicine, engineering, farming, coding, business, design...)'
R2 = 'Ask me MY GOAL OR FIELD (medicine, robotics engineer, mechanical, nanotech, aerospace, coding, business...)'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'var APP_VERSION="60.35"'
R3 = 'var APP_VERSION="60.36"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Field Paths, size: %d bytes" % len(h.encode("utf-8")))
