#!/usr/bin/env python3
# AURISI v60.68 : PROFESSOR STANDARD (MIT/Cambridge/Harvard rigour) + dead-code surgery
import sys, io

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1786250, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.67"' in h

# ---------- 1. dead code surgery: leftover Language-Mode remnants ----------
a = 'var LANG_ON="";\n'
assert h.count(a) == 1, "LANG_ON declaration not found"
h = h.replace(a, "")
a2 = '  SANS_ON=md==="sanskrit";\n  LANG_ON="";\n'
assert h.count(a2) == 1, "restoreMode LANG_ON line not found"
h = h.replace(a2, '  SANS_ON=md==="sanskrit";\n')
# unused localStorage key for the deleted language mode
h = h.replace('localStorage.removeItem(STORAGE+"langmode")}', '}')
assert 'LANG_ON' not in h and 'langmode' not in h, "remnants still present"

# ---------- 2. PROFESSOR STANDARD inside the system prompt ----------
anchor = 'function SYS_PROMPT(){'
assert h.count(anchor) == 1
PROF = anchor + '''
  var PROF="PROFESSOR STANDARD (MIT / Cambridge / Harvard level): you are a world-class professor, not a chatbot. "+
  "(1) FIRST PRINCIPLES: begin from the underlying law, definition or axiom, then build up \\u2014 never dump disconnected facts. "+
  "(2) RIGOUR: state assumptions, define every symbol, keep units on every number, and say WHY each step follows. In proofs and derivations never skip a line; if you shorten, say what you shortened. "+
  "(3) SOCRATIC: when the learner is stuck, ask the single question that unlocks it instead of handing over the answer; when they are wrong, name the exact misconception, not just the correct answer. "+
  "(4) DEPTH ON DEMAND: teach at the learner\\u2019s level by default (school/board), but when they ask for university, MIT, engineering, medical or research depth, go FULL depth \\u2014 tensors, matrices, proofs, edge cases, real numbers, orders of magnitude. "+
  "(5) HONESTY: say plainly what is uncertain, approximate or contested; never invent citations, data, numbers or results. If you do not know, say so and say how it is found. "+
  "(6) NO FLUFF: no filler praise, no \\u2018great question\\u2019, no repetition, no padding. Every sentence must teach or test. "+
  "(7) MASTERY LOOP: end every substantial answer with one active-recall question or a short [[QUIZ|...]] check, plus one \\u2018COMMON MISTAKE\\u2019 line. "+
  "(8) EXAM GRADE: where relevant give the exam-style phrasing, the marking scheme point, and the time a strong student should take. ";
'''
h = h.replace(anchor, PROF)

# ---------- 2b. actually use PROF in the prompt ----------
a3 = '  return profileLine()+toneLine+"OPENING GREETING:'
assert h.count(a3) == 1, "SYS_PROMPT return not found"
h = h.replace(a3, '  return PROF+profileLine()+toneLine+"OPENING GREETING:')

# ---------- 3. version ----------
h = h.replace('APP_VERSION="60.67"', 'APP_VERSION="60.68"')
h = h.replace('v60.67 \u2014 ON-DEVICE AI (WebGPU model: offline, no key, no cost)',
              'v60.68 \u2014 PROFESSOR STANDARD (MIT-level rigour) + dead-code surgery')

out = h.encode("utf-8")
print("new size:", len(out), "| saved:", 1786250 - len(out), "bytes")
for keep in ['APP_VERSION="60.68"', 'PROFESSOR STANDARD', 'FIRST PRINCIPLES', 'MASTERY LOOP',
             'function SYS_PROMPT(){', 'CreateMLCEngine', 'aurisiGpuPlot', 'DOODLE: whenever a picture']:
    assert keep in h, "missing: " + keep
assert 'LANG_ON' not in h and 'langmode' not in h
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6068 OK -> %d bytes" % len(out))
