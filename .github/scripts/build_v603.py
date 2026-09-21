#!/usr/bin/env python3
# AURISI v60.3: Institute scope on Home.
# Users who joined an institute now see ONLY their class-level stuff —
# the Language Hub card (and similar non-curriculum extras) is hidden
# for them. Everything else already scoped: AI teaches only their
# classes, Library shows only their class-level collections + the
# institute's own material.
# Base: AURISI.html v60.2. Idempotent: no-op if already v60.3.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.3"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.3 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.2"' in h, "base must be v60.2"

F1 = 'else if(p.role==="junior"){hs=["Mock Exam","Score Predictor","Exam Maker"]}\n  if(!hs.length)return;'
R1 = '''else if(p.role==="junior"){hs=["Mock Exam","Score Predictor","Exam Maker"]}
  if(ins)hs=hs.concat(["Language Hub"]);
  if(!hs.length)return;'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

F2 = 'var APP_VERSION="60.2"'
R2 = 'var APP_VERSION="60.3"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Institute Scope patches, size: %d bytes" % len(h.encode("utf-8")))
