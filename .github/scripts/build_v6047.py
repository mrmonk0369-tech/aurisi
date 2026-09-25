#!/usr/bin/env python3
# AURISI v60.47: AURISI STUDIO - the app builder inside the app.
# Owner ask: "Aurisi bhi app/website/software bana sake jaise tumne banaya."
# Flow: describe -> callGeminiFast (house key, same AI as chat, with Groq/
# Puter/Pollinations fallbacks) -> single-file HTML app extracted -> live
# preview in sandboxed iframe -> download .html + Improve iterations.
# Patch strings live in sibling .txt files (zero escaping tricks):
#   a47_old/a47_new    - Study Tools card anchor (after PDF to Video) + card
#   newblock47.txt     - Studio JS + CSS block (before instCloseModals)
# Base: v60.46 (1890536). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.47"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.47 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.46"' in h, "base must be v60.46"

# P1: Studio card in Study Tools
F1, R1 = rf("a47_old.txt"), rf("a47_new.txt")
assert h.count(F1) == 1, "P1 anchor: %d" % h.count(F1)
h = h.replace(F1, R1)

# P2: Studio engine, before instCloseModals
F2 = 'function instCloseModals(){'
NEW = rf("newblock47.txt")
assert h.count(F2) == 1, "P2 anchor: %d" % h.count(F2)
assert chr(92)+chr(34) not in NEW, "newblock47 contains backslash-quote"
h = h.replace(F2, NEW + "\n" + F2)

F3 = 'var APP_VERSION="60.46"'
R3 = 'var APP_VERSION="60.47"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied aurisi studio, size: %d bytes" % len(h.encode("utf-8")))
