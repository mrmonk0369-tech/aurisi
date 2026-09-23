#!/usr/bin/env python3
# AURISI v60.37: VISUAL DEEP-DIVE CARDS — teach important Science Lab
#  concepts like a beautifully designed museum card (owner reference:
#  the Jacobian Matrix visual card - Jacobi portrait, before->transform->
#  after geometric proof, formal notation, one-line essence).
#  Format: (a) PERSON - one line on the human behind it; (b) PICTURE -
#  an [[SVG]] of the intuition, often BEFORE -> THE IDEA -> AFTER three
#  panels, fully labeled; (c) NOTATION - clean formal math/chem only
#  after the picture is understood; (d) ESSENCE - one line capturing
#  the whole concept. Picture does the talking.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.36 (1868723). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.37"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.37 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.36"' in h, "base must be v60.36"

# P1: VISUAL DEEP-DIVE rules after CREATOR INTEGRATION
F1 = 'so their thinking generalizes across domains. "+"You are Aurisi'
R1 = 'so their thinking generalizes across domains. VISUAL DEEP-DIVE: in the science lab, teach every important concept like a beautifully designed museum card, not walls of text: (a) PERSON - one line on the human behind it, who discovered or invented it and one vivid detail from their story; (b) PICTURE - a [[SVG]] diagram of the intuition, whenever possible drawn as three panels in one canvas: BEFORE (the simple everyday case), THE IDEA (an arrow or transform showing what changes), AFTER (the resulting effect), every part labeled; (c) NOTATION - the clean formal math or chemistry notation in text, shown only after the picture is understood; (d) ESSENCE - one single line capturing the entire concept (example: the Jacobian matrix records how a smooth map locally distorts area). Prefer visual intuition over prose whenever the concept allows it, and keep each card tight - let the picture do the talking. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

F2 = 'var APP_VERSION="60.36"'
R2 = 'var APP_VERSION="60.37"'
assert h.count(F2) == 1
h = h.replace(F2, R2)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Visual Deep-Dive Cards, size: %d bytes" % len(h.encode("utf-8")))
