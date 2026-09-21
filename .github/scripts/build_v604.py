#!/usr/bin/env python3
# AURISI v60.4: Pure Scope for ALL B2B users.
# 1) Exam-only institutes: a coaching that teaches NO school classes can
#    leave "classes" blank at creation -> app shows ONLY their exam
#    content (no class cats, no Sanskrit), AI locks to their exams.
# 2) Home extras hidden for institute users: "Your Teachers" (Feynman
#    Mode, Sanskrit Mode) and the Language Hub card no longer show.
# 3) Features modal: Language Hub entry hidden for institute users.
# 4) Home banner: handles institutes with no classes (exam coaching).
# Base: AURISI.html v60.3. Idempotent: no-op if already v60.4.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.4"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.4 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.3"' in h, "base must be v60.3"

# P1a: wrap "Your Teachers" + Language Hub card in if(!getInst()){
F1a = "html+='<div class=\"ws-h\">🧑‍🏫 Your Teachers</div><div class=\"teacher-row\">';"
R1a = "if(!getInst()){html+='<div class=\"ws-h\">🧑‍🏫 Your Teachers</div><div class=\"teacher-row\">';"
assert h.count(F1a) == 1, "P1a anchor not found"
h = h.replace(F1a, R1a)

# P1b: close the wrap after the Language Hub card
F1b = "onclick=\"openLangLab()\">🌍 Open the Language Hub</button></div>';"
R1b = "onclick=\"openLangLab()\">🌍 Open the Language Hub</button></div>';}"
assert h.count(F1b) == 1, "P1b anchor not found"
h = h.replace(F1b, R1b)

# P2: institute creation - classes now optional (exam-only coaching)
F2 = '  var cls=(prompt("Which classes do you teach?\\nExample: 6-12, 6-8, 9-10, 11-12","6-12")||"").trim();\n  if(!cls)return;'
R2 = '  var cls=(prompt("Which classes do you teach?\\nExample: 6-12, 6-8, 9-10, 11-12\\nLeave blank for exam-only coaching (SSC, NEET, UPSC…)","")||"").trim();'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: instCats - exam-only mode when no classes
F3 = """function instCats(cls,exams){
  var lo=6,hi=12;var m=/^\\s*(\\d+)\\D+(\\d+)\\s*$/.exec((cls||"").trim());
  if(m){lo=parseInt(m[1],10);hi=parseInt(m[2],10)}else if((cls||"").indexOf("11")===0){lo=11;hi=12}
  if(!(lo>=1&&lo<=12))lo=6;if(!(hi>=lo&&hi<=12))hi=12;
  var cats=["other","english","sanskrit"];
  function _a(x){if(cats.indexOf(x)<0)cats.push(x)}
  if(lo<=8){_a("class7");_a("class8")}
  if(lo<=9&&hi>=9)_a("class9");
  if(lo<=10&&hi>=10)_a("class10");
  if(hi>=11)_a("class11");
  (exams||"").toLowerCase().split(/[,; ]+/).forEach(function(t){
    if(["ssc","hssc","dsssb","neet","jee","upsc"].indexOf(t)>=0)_a(t)});
  return cats;
}"""
R3 = """function instCats(cls,exams){
  var t=(cls||"").trim();var school=t.length>0;
  var lo=6,hi=12;var m=/^\\s*(\\d+)\\D+(\\d+)\\s*$/.exec(t);
  if(m){lo=parseInt(m[1],10);hi=parseInt(m[2],10)}else if(t.indexOf("11")===0){lo=11;hi=12}
  if(school){if(!(lo>=1&&lo<=12))lo=6;if(!(hi>=lo&&hi<=12))hi=12}
  var cats=["other","english"];
  function _a(x){if(cats.indexOf(x)<0)cats.push(x)}
  if(school){
    _a("sanskrit");
    if(lo<=8){_a("class7");_a("class8")}
    if(lo<=9&&hi>=9)_a("class9");
    if(lo<=10&&hi>=10)_a("class10");
    if(hi>=11)_a("class11");
  }
  (exams||"").toLowerCase().split(/[,; ]+/).forEach(function(t){
    if(["ssc","hssc","dsssb","neet","jee","upsc"].indexOf(t)>=0)_a(t)});
  return cats;
}"""
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: profileLine - exam-only institutes lock AI to exams only
F4 = '  if(ins)return "INSTITUTION MODE: your user studies at "+ins.name+" (a real school/tuition running classes "+ins.cls+(ins.exams?"; they also prepare for "+ins.exams:"")+"). Teach ONLY within this class range, keep everything age-appropriate for those classes, and never bring in content above or below their classes. ";'
R4 = '''  if(ins){var _ic=(ins.cls||"").trim();
    if(_ic)return "INSTITUTION MODE: your user studies at "+ins.name+" (a real school/tuition running classes "+_ic+(ins.exams?"; they also prepare for "+ins.exams:"")+"). Teach ONLY within this class range, keep everything age-appropriate for those classes, and never bring in content above or below their classes. ";
    return "INSTITUTION MODE: your user studies at "+ins.name+" (an exam-coaching institute"+(ins.exams?" preparing students for "+ins.exams:"")+"). Teach ONLY their exam subjects and exam-relevant material. Never school-class subjects, foreign languages (Spanish, French, Japanese etc.) or anything outside their coaching focus. ";
  }'''
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: Home banner handles no-classes institutes
F5 = """>Classes '+escH(ins.cls)+(ins.exams?' · '+escH(ins.exams).toUpperCase():'')+' · powered by Aurisi</span>"""
R5 = """>'+(ins.cls?'Classes '+escH(ins.cls):'')+(ins.exams?((ins.cls?' · ':'')+escH(ins.exams).toUpperCase()):'')+((ins.cls||ins.exams)?' · ':'')+'powered by Aurisi</span>"""
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: features modal - hide Language Hub entry for institute users
F6 = "  var html='<h2>✨ Everything inside AURISI</h2>"
R6 = """  if(getInst())secs[0][1]=secs[0][1].filter(function(f){return f[0].indexOf("Language Hub")<0});
  var html='<h2>✨ Everything inside AURISI</h2>"""
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.3"'
R7 = 'var APP_VERSION="60.4"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Pure Scope patches, size: %d bytes" % len(h.encode("utf-8")))
