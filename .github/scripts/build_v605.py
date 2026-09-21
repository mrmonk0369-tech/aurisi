#!/usr/bin/env python3
# AURISI v60.5: House AI — zero-setup chat for every user.
# When a user has no key of their own, the app silently uses the owner's
# Gemini key from app_config (ai_house_key, set in the Admin panel).
# Covering both callGeminiStream and callGeminiFast covers every
# Gemini call site (chat, lessons, quick calls) in one chokepoint each.
# Users who add their own key still use their own; Puter stays as the
# last-resort fallback when no house key is configured.
# Base: AURISI.html v60.4. Idempotent: no-op if already v60.5.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.5"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.5 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.4"' in h, "base must be v60.4"

# P1: callGeminiStream - house key fallback
F1 = 'async function callGeminiStream(apiKey, history, onDelta, signal, sysPrompt){\n  apiKey=(apiKey||"").trim();'
R1 = 'async function callGeminiStream(apiKey, history, onDelta, signal, sysPrompt){\n  apiKey=((apiKey||"").trim()||(cfgGet("ai_house_key")||"").trim());'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: callGeminiFast - house key fallback
F2 = 'function callGeminiFast(apiKey, history, jsonMode, sysPrompt) {\n  apiKey=(apiKey||"").trim();'
R2 = 'function callGeminiFast(apiKey, history, jsonMode, sysPrompt) {\n  apiKey=((apiKey||"").trim()||(cfgGet("ai_house_key")||"").trim());'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

F3 = 'var APP_VERSION="60.4"'
R3 = 'var APP_VERSION="60.5"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied House AI patches, size: %d bytes" % len(h.encode("utf-8")))
