#!/usr/bin/env python3
# AURISI v60.25: PERSONAL WELCOME ("Hi Kavi, let's get into it").
#  ChatGPT/Gemini-style: the chat home greeting uses the student's own
#  name. userName() (cloud login / local account name) is the source:
#    - "Kavi" (or kavi@... -> "Kavi")  -> "Hi Kavi, let's get into it"
#    - no name set                      -> "Hi, let's get into it"
#  Name is title-cased, email prefix stripped. The greeting refreshes at
#  boot and on every login/logout (updateAcctUI hook).
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.24 (1855929). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.25"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.25 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.24"' in h, "base must be v60.24"

# P1: welcome h2 becomes a live, name-aware greeting
F1 = '<h2>Aurisi</h2>'
R1 = '<h2 id="welcomeHi">Aurisi</h2>'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: welcomeGreet() + refresh on login/logout (updateAcctUI) and at boot
F2 = 'function updateAcctUI(){'
R2 = Q('function welcomeGreet(){try{var el=$("welcomeHi");if(!el)return;var n=userName();if(n&&n.indexOf("@")>-1)n=n.split("@")[0];n=(n||"").trim();if(n){n=n.charAt(0).toUpperCase()+n.slice(1);el.textContent="Hi "+n+", let\'s get into it"}else{el.textContent="Hi, let\'s get into it"}}catch(e){}}\nfunction updateAcctUI(){   try{welcomeGreet()}catch(e0){}')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: run once at boot too
F3 = '/* v60.19: carousel removed */updateTopTitle();'
R3 = '/* v60.19: carousel removed */updateTopTitle();welcomeGreet();'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.24"'
R4 = 'var APP_VERSION="60.25"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Personal Welcome, size: %d bytes" % len(h.encode("utf-8")))
