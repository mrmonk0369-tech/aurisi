#!/usr/bin/env python3
# AURISI HQ builder: concatenates hq_part1/2/3.txt into admin.html.
# Total size: 22598 bytes. Deterministic and idempotent.
import sys, io, os
D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()
out = sys.argv[1] if len(sys.argv) > 1 else "admin.html"
s = rf("hq_part1.txt") + rf("hq_part2.txt") + rf("hq_part3.txt")
assert len(s.encode("utf-8")) == 22598, "HQ size mismatch: %d" % len(s.encode("utf-8"))
io.open(out, "w", encoding="utf-8").write(s)
print("admin.html written: %d bytes" % len(s.encode("utf-8")))
