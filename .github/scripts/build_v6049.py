#!/usr/bin/env python3
# AURISI v60.49: STUDIO PRO 2 - runtime testing + multi-turn memory.
#   - stuRunTest: runs the app in a hidden sandboxed iframe, catches
#     window.onerror + unhandledrejection via postMessage, 2.6s watch
#   - runtime auto-fix loop: up to 2 repair rounds on real errors
#   - STU.hist: conversation memory across Improve rounds (last 6
#     requests) so the AI remembers every change request
# Patch strings in sibling .txt files. Base: v60.48 (1901395). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.49"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.49 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.48"' in h, "base must be v60.48"

pairs = [("p49_1o.txt","p49_1n.txt"),("p49_2o.txt","p49_2n.txt"),("p49_3o.txt","p49_3n.txt"),("p49_4o.txt","p49_4n.txt"),("p49_5o.txt","p49_5n.txt"),("p49_6o.txt","p49_6n.txt"),("p49_7o.txt","p49_7n.txt")]
for fo, fn in pairs:
    old, new = rf(fo), rf(fn)
    assert h.count(old) == 1, fo + " anchor: %d" % h.count(old)
    h = h.replace(old, new)

F2 = 'function instCloseModals(){'
NEW = rf("newblock49.txt")
assert h.count(F2) == 1, "engine anchor"
assert chr(92)+chr(34) not in NEW, "newblock49 contains backslash-quote"
assert "</scr"+"ipt>" not in NEW, "newblock49 contains literal script closer"
h = h.replace(F2, NEW + "\n" + F2)

F3 = 'var APP_VERSION="60.48"'
R3 = 'var APP_VERSION="60.49"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied studio pro 2, size: %d bytes" % len(h.encode("utf-8")))
