#!/usr/bin/env python3
# AURISI v60.33: ZERO TO PRO JOURNEY — Science Lab becomes a progression.
#  1) XP + level system persisted in localStorage (sciJ): Spark (0),
#     Foundation (100), Builder (300), Engineer (600), Pro (1000 XP);
#     10 XP per mastered concept, dedup, toast on mastery.
#  2) [[MASTERED|concept]] token: the AI emits it after the student
#     passes a concept's PREDICT question; mdRefresh strips it and
#     awards XP. sciGet/sciLevel/sciMaster helpers.
#  3) scienceLab() activation now injects the student's current
#     journey state so the AI continues the roadmap where they left.
#  4) SYS_PROMPT: ZERO TO PRO roadmap rules added to APPLIED SCIENCE
#     MODE (assess level, prerequisites-first roadmap, milestone
#     mini-projects, real-world-only, MASTERED token discipline).
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.32 (1864204). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.33"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.33 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.32"' in h, "base must be v60.32"

# P1: prompt — ZERO TO PRO roadmap rules
F1 = 'Keep each loop tight and exciting like a lab demo video. "+"You are Aurisi'
R1 = 'Keep each loop tight and exciting like a lab demo video. ZERO TO PRO JOURNEY: science lab is a journey from zero to pro - (a) when the student is new, quickly assess their current level (2-3 tiny questions or their class/standard) and lay out a short roadmap of 5-6 milestones from absolute foundations to real builds, naming what they will be able to DO at the end of each; (b) never teach an advanced idea before its prerequisites - if a gap appears, fix the gap first; (c) after they pass the PREDICT question of a concept, you MUST end that reply with exactly one line containing only the token [[MASTERED|short concept name]] so the app awards XP and levels them up (never emit it when they failed or guessed right without reason); (d) at the end of every milestone give a real mini-project buildable with actual materials (lemon battery, pulley, water rocket with math prediction, cabbage pH indicator, budget project) and evaluate their result; (e) real world only - every experiment, example and project must be physically possible with real materials and real physics, chemistry or math - real scientists and engineers as role models, zero imaginary sci-fi tech; (f) celebrate level-ups in one line and tell them what they unlocked. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: XP system + enhanced scienceLab()
F2 = 'function scienceLab(){\n  roomStart("\U0001F52C","Science Lab");\n  quick("SCIENCE LAB ON. Teach me Physics, Chemistry or Math the practical applied way - real experiments, everyday examples, formulas behind them, and where the real world uses it. Ask me the topic first if needed.");\n}'
R2 = 'var SCI_LEVELS=[[0,"Spark"],[100,"Foundation"],[300,"Builder"],[600,"Engineer"],[1000,"Pro"]];\nfunction sciGet(){try{var j=JSON.parse(localStorage.getItem(STORAGE+"sciJ")||"{}");j.xp=j.xp||0;j.done=j.done||[];return j}catch(e){return{xp:0,done:[]}}}\nfunction sciLevel(){var j=sciGet(),n=0;for(var i=0;i<SCI_LEVELS.length;i++)if(j.xp>=SCI_LEVELS[i][0])n=i;return{n:n,name:SCI_LEVELS[n][1],xp:j.xp}}\nfunction sciMaster(c){c=String(c||"").trim().slice(0,60);if(!c)return;var j=sciGet();var isNew=j.done.indexOf(c)<0;if(isNew){j.done.push(c);j.xp+=10;try{localStorage.setItem(STORAGE+"sciJ",JSON.stringify(j))}catch(e){}}var lv=sciLevel();toast((isNew?"\u26A1 Mastered: "+c+" (+10 XP)":"Already mastered: "+c)+" \u00b7 Level "+lv.n+" "+lv.name+" ("+j.xp+" XP)")}\nfunction scienceLab(){\n  var lv=sciLevel(),j=sciGet();\n  roomStart("\U0001F52C","Science Lab");\n  quick("SCIENCE LAB ON. My zero-to-pro journey: Level "+lv.n+" ("+lv.name+"), "+j.xp+" XP, "+j.done.length+" concepts mastered"+(j.done.length?(" - last ones: "+j.done.slice(-3).join(", ")):" - starting from zero")+". Continue my roadmap from exactly where I am. Teach me Physics, Chemistry or Math the practical applied way - real experiments, everyday examples, formulas behind them, and where the real world uses it. Ask me the topic/subject first if needed.");\n}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: [[MASTERED|...]] parsing before mdRefresh
F3 = 'mdRefresh(md,txt);\n    if(optData&&optData.length>1){'
R3 = 'try{var mM=null;var mRe=/\\[\\[\\s*MASTERED\\s*\\|([^\\]|]+)\\]\\]/gi;while((mM=mRe.exec(txt))){try{sciMaster(mM[1])}catch(eM){}}txt=txt.replace(mRe,"").trim()}catch(eMZ){}\n    ' + F3
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.32"'
R4 = 'var APP_VERSION="60.33"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Zero to Pro Journey, size: %d bytes" % len(h.encode("utf-8")))
