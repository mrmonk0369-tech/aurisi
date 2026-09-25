#!/usr/bin/env python3
# AURISI v60.48: STUDIO PRO - self-checking builds + LIVE publish.
# Owner ask: "to phir banao" - close the gap to a real builder agent:
#   - stuCheck: syntax-checks every <script> block with new Function()
#   - auto-fix loop: up to 2 repair rounds (error message sent back to AI)
#   - Publish button: PUT to mrmonk0369-tech/aurisi-apps via GitHub API
#     (token from app_config github_publish_token, set in HQ Settings);
#     app goes live at mrmonk0369-tech.github.io/aurisi-apps/<slug>.html
# Patch strings in sibling .txt files. Base: v60.47 (1899130). Idempotent.
import sys, io, os

D = os.path.dirname(os.path.abspath(__file__))
def rf(n): return io.open(os.path.join(D, n), encoding="utf-8").read()

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.48"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.48 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.47"' in h, "base must be v60.47"

pairs = [("p48_1o.txt","p48_1n.txt"),("p48_2o.txt","p48_2n.txt"),("p48_3o.txt","p48_3n.txt"),("p48_4o.txt","p48_4n.txt"),("p48_5o.txt","p48_5n.txt")]
for fo, fn in pairs:
    old, new = rf(fo), rf(fn)
    assert h.count(old) == 1, fo + " anchor: %d" % h.count(old)
    h = h.replace(old, new)

F2 = 'function instCloseModals(){'
NEW = rf("newblock48.txt")
assert h.count(F2) == 1, "engine anchor"
assert chr(92)+chr(34) not in NEW, "newblock48 contains backslash-quote"
h = h.replace(F2, NEW + "\n" + F2)

F3 = 'var APP_VERSION="60.47"'
R3 = 'var APP_VERSION="60.48"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied studio pro, size: %d bytes" % len(h.encode("utf-8")))
