#!/usr/bin/env python3
# Institute Portal v2 builder: applies earnings/commission patches to
# build_institute_v1.py source and generates institute.html.
# Patch pairs: g1..g6 (globals PCT, earnings panel, loadDash pct+price_at_sale,
# codes select, renderDash earnings, guide fee line). All strings in txt files.
# Output size: 19629 bytes. Idempotent (output is deterministic).
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))

def rf(name):
    return io.open(os.path.join(D, name), encoding="utf-8").read()

src = rf("build_institute_v1.py")
pairs = [("g1_old","g1_new"),("g2_old","g2_new"),("g3_old","g3_new"),("g4_old","g4_new"),("g5_old","g5_new"),("g6_old","g6_new")]
for fo, fn in pairs:
    old, new = rf(fo), rf(fn)
    assert src.count(old) == 1, fo + " anchor count != 1"
    src = src.replace(old, new)

out = sys.argv[1] if len(sys.argv) > 1 else "institute.html"
g = {"__name__": "__main__", "__file__": os.path.join(D, "build_institute_v1.py")}
import io as _io, sys as _sys
_argv = _sys.argv[:]
try:
    _sys.argv = ["builder", out]
    exec(compile(src, "build_institute_v1_patched", "exec"), g)
finally:
    _sys.argv = _argv
