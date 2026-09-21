#!/usr/bin/env python3
# AURISI v58.1 hotfix: tolerant token parsing ([[CARDS | ...]], lowercase, etc.)
# Root cause of "Daily Brief flashcard flip nahi hota": when the model writes the
# token with a space before the pipe (or lowercase), the strict regex never matches,
# so the flashcard UI is never built and the raw token text shows instead.
# Base: AURISI.html v58.0. Idempotent: exits 0 untouched if already v58.1.
import sys, io

BS = chr(92)

def Q(s):
    return s.replace('~B~', BS)

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.1"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.1 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.0"' in h, "base must be v58.0"

PATCHES = []

def P(name, find, repl, count=1):
    PATCHES.append((name, find, repl, count))

# 1. Version bump
P("version",
  'var APP_VERSION="58.0"',
  'var APP_VERSION="58.1"')

# 2. OPTIONS token tolerant
P("opt-rx",
  Q('const om=txt.match(/~B~[~B~[OPTIONS~B~|([^~B~]]+)~B~]~B~]/);'),
  Q('const om=txt.match(/~B~[~B~[~B~s*OPTIONS~B~s*~B~|([^~B~]]+)~B~]~B~]/i);'))

# 3. QUIZ token tolerant
P("quiz-rx",
  Q('const qm=txt.match(/~B~[~B~[QUIZ~B~|([^~B~]]+)~B~]~B~]/);'),
  Q('const qm=txt.match(/~B~[~B~[~B~s*QUIZ~B~s*~B~|([^~B~]]+)~B~]~B~]/i);'))

# 4. VIDEO token tolerant
P("video-rx",
  Q('const vTok=txt.match(/~B~[~B~[VIDEO~B~|([^~B~]]+)~B~]~B~]/g);'),
  Q('const vTok=txt.match(/~B~[~B~[~B~s*VIDEO~B~s*~B~|([^~B~]]+)~B~]~B~]/gi);'))

# 5. VIDEO slice fix (slice(8,-2) assumed strict prefix; strip via regex now)
P("video-slice",
  Q('vData=vTok.map(tk=>tk.slice(8,-2).trim()).filter(Boolean)'),
  Q('vData=vTok.map(function(tk){return tk.replace(/~B~[~B~[~B~s*VIDEO~B~s*~B~|/i,"").replace(/~B~]~B~]~B~s*$/,"").trim()}).filter(Boolean)'))

# 6. REPORT token tolerant
P("report-rx",
  Q('const rTok=txt.match(/~B~[~B~[REPORT~B~|([^~B~]]+)~B~]~B~]/);'),
  Q('const rTok=txt.match(/~B~[~B~[~B~s*REPORT~B~s*~B~|([^~B~]]+)~B~]~B~]/i);'))

# 7. CARDS token tolerant (the flashcard fix)
P("cards-rx",
  Q('const cTok=txt.match(/~B~[~B~[CARDS~B~|([^~B~]]+)~B~]~B~]/);'),
  Q('const cTok=txt.match(/~B~[~B~[~B~s*CARDS~B~s*~B~|([^~B~]]+)~B~]~B~]/i);'))

# 8. DOODLE token tolerant
P("doodle-rx",
  Q('const dRe=/~B~[~B~[DOODLE~B~|([^|~B~]]+)~B~|([~B~s~B~S]+?)~B~]~B~]/g;'),
  Q('const dRe=/~B~[~B~[~B~s*DOODLE~B~s*~B~|([^|~B~]]+)~B~|([~B~s~B~S]+?)~B~]~B~]/gi;'))

# 9. PODCAST token tolerant
P("podcast-rx",
  Q('const pdTok=txt.match(/~B~[~B~[PODCAST~B~|([~B~s~B~S]+?)~B~]~B~]/);'),
  Q('const pdTok=txt.match(/~B~[~B~[~B~s*PODCAST~B~s*~B~|([~B~s~B~S]+?)~B~]~B~]/i);'))

# 10. MAP token tolerant
P("map-rx",
  Q('const mpTok=txt.match(/~B~[~B~[MAP~B~|([~B~s~B~S]+?)~B~]~B~]/);'),
  Q('const mpTok=txt.match(/~B~[~B~[~B~s*MAP~B~s*~B~|([~B~s~B~S]+?)~B~]~B~]/i);'))

# 11. GRAPH token tolerant
P("graph-rx",
  Q('const gRe=/~B~[~B~[GRAPH~B~|([^|~B~]]+)~B~|(-?[~B~d.]+)~B~|(-?[~B~d.]+)~B~]~B~]/g;'),
  Q('const gRe=/~B~[~B~[~B~s*GRAPH~B~s*~B~|([^|~B~]]+)~B~|(-?[~B~d.]+)~B~|(-?[~B~d.]+)~B~]~B~]/gi;'))

# 12. SLIDES token tolerant
P("slides-rx",
  Q('const slTok=txt.match(/~B~[~B~[SLIDES~B~|([~B~s~B~S]+?)~B~]~B~]/);'),
  Q('const slTok=txt.match(/~B~[~B~[~B~s*SLIDES~B~s*~B~|([~B~s~B~S]+?)~B~]~B~]/i);'))

# 13. Daily Brief prompt: insist on exact token shape
P("db-prompt",
  'then 1 active-recall flashcard as [[CARDS|question|answer]]. Keep it tight.',
  'then 1 active-recall flashcard exactly as [[CARDS|question|answer]] (write CARDS in capitals, no space before the pipe, no | inside the question or answer). Keep it tight.')

applied = 0
for (name, find, repl, count) in PATCHES:
    c = h.count(find)
    assert c == count, "PATCH %s: found %d occurrences (expected %d) of %r" % (name, c, count, find[:80])
    h = h.replace(find, repl)
    applied += 1

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied %d patches, size: %d bytes" % (applied, len(h.encode("utf-8"))))
