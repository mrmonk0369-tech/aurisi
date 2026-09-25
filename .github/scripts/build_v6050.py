#!/usr/bin/env python3
# AURISI v60.50: STUDIO OMNI - every task, not just single-file apps.
#   - stuParse: routes AI output to 3 formats:
#     (A) single-file HTML app (as before)
#     (B) multi-file project (===FILE: name=== blocks) -> stuInline
#         merges CSS/JS into preview; ZIP download; subfolder publish
#     (C) document JSON {title, blocks} -> stuRenderDoc (A4 print HTML);
#         PDF export via hand-rolled stuPdf (Latin text)
#   - stuZip/stuCrc32: STORE-method ZIP writer, no libraries
#   - Project locker: studio_projects table (save/load/resume)
# Patch strings in sibling .txt files. Base: v60.49 (1903174). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.50"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.50 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.49"' in h, "base must be v60.49"

pairs = [("p50_1o.txt","p50_1n.txt"),("p50_2o.txt","p50_2n.txt"),("p50_3o.txt","p50_3n.txt"),("p50_4o.txt","p50_4n.txt"),("p50_5o.txt","p50_5n.txt"),("p50_6o.txt","p50_6n.txt"),("p50_7o.txt","p50_7n.txt"),("p50_8o.txt","p50_8n.txt"),("p50_9o.txt","p50_9n.txt"),("p50_10o.txt","p50_10n.txt")]
for fo, fn in pairs:
    old, new = rf(fo), rf(fn)
    assert h.count(old) == 1, fo + " anchor: %d" % h.count(old)
    h = h.replace(old, new)

F2 = 'function instCloseModals(){'
NEW = rf("nb50_part1.txt") + rf("nb50_part2.txt") + rf("nb50_part3.txt")
assert h.count(F2) == 1, "engine anchor"
assert chr(92)+chr(34) not in NEW, "newblock50 contains backslash-quote"
assert "</scr"+"ipt>" not in NEW, "newblock50 contains literal script closer"
h = h.replace(F2, NEW + "\n" + F2)

F3 = 'var APP_VERSION="60.49"'
R3 = 'var APP_VERSION="60.50"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied studio omni, size: %d bytes" % len(h.encode("utf-8")))
