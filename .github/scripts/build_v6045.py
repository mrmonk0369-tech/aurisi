#!/usr/bin/env python3
# AURISI v60.45: INSTITUTE COURSES + NETFLIX-STYLE PLAYER + COMMISSION
# All patch strings live in sibling .txt files (zero escaping tricks):
#   f1p.txt/r1p.txt  - instRenderBox Courses chip (plain/with chip)
#   f2p.txt          - home anchor (end of Language Hub section)
#   v6045_home.txt   - home Institute Courses card insert
#   newblock.txt     - full courses+player JS block (before instCloseModals)
# Commission: course_codes.price_at_sale feeds portal Earnings (institute v2);
# percentage lives in app_config (commission_pct).
# Base: v60.44 (1936649). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))

def rf(name):
    return io.open(os.path.join(D, name), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.45"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.45 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.44"' in h, "base must be v60.44"

# P1: Courses chip in the institute box
F1 = rf("f1p.txt"); R1 = rf("r1p.txt")
assert h.count(F1) == 1, "P1 anchor: %d" % h.count(F1)
h = h.replace(F1, R1)

# P2: home Institute Courses section for institute students
F2 = rf("f2p.txt"); R2 = F2 + "\n" + rf("v6045_home.txt").rstrip("\n")
assert h.count(F2) == 1, "P2 anchor: %d" % h.count(F2)
h = h.replace(F2, R2)

# P3: courses browser + unlock + Netflix-style player, before instCloseModals
F3 = 'function instCloseModals(){'
NEW = rf("newblock.txt")
assert h.count(F3) == 1, "P3 anchor: %d" % h.count(F3)
h = h.replace(F3, NEW + "\n" + F3)

F4 = 'var APP_VERSION="60.44"'
R4 = 'var APP_VERSION="60.45"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied institute courses + player, size: %d bytes" % len(h.encode("utf-8")))
