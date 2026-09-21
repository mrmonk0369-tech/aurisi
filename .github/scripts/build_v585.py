#!/usr/bin/env python3
# AURISI v58.5: User Profiles - serve each user by their requirement.
# Tuition owner (e.g. classes 6-8) gets a teaching-focused Home and
# classroom-ready AI content; coaching institutes get batch-exam focus;
# junior students get simple mode; students keep the full app (default).
# Base: AURISI.html v58.4. Idempotent: no-op if already v58.5.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.5"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.5 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.4"' in h, "base must be v58.4"

# Patch 1: Settings - profile picker field before the tone field
F1 = '      <div class="field">\n        <label>🎭 AI teaching tone</label>'
R1 = (
'      <div class="field">\n'
'        <label>👤 Who uses Aurisi?</label>\n'
'        <select class="select" id="profileSel" style="width:100%" onchange="profileSelChange()">\n'
'          <option value="student">🎓 Student — full app</option>\n'
'          <option value="teacher">👨\u200d🏫 Teacher / Tuition — teaching tools only</option>\n'
'          <option value="institute">🏫 Coaching Institute — batch & exam focus</option>\n'
'          <option value="junior">🧒 Junior student (classes 6-8) — simple mode</option>\n'
'        </select>\n'
'        <select class="select" id="profileDetailSel" style="width:100%;margin-top:6px;display:none"></select>\n'
'        <div class="hint">Aurisi adapts the Home screen and teaching style to who is using it. Tuition owners: pick the classes you teach.</div>\n'
'      </div>\n\n'
'      <div class="field">\n        <label>🎭 AI teaching tone</label>')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: openSettings - init profile selects
F2 = 'try{$("toneSel").value=localStorage.getItem(STORAGE+"tone")||"auto"}catch(e){}'
R2 = F2 + '\n  try{$("profileSel").value=(getProfile()||{}).role||"student";fillProfileDetail()}catch(e){}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: saveSettings - persist profile
F3 = 'localStorage.setItem(STORAGE+"curriculum",$("curriculumSel").value||"auto");'
R3 = F3 + '\n  try{saveProfile($("profileSel").value||"student",(($("profileDetailSel")||{}).value)||"")}catch(e){}'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: profile functions before renderStudio
F4 = 'function renderStudio(){'
HUB = '''function getProfile(){try{return JSON.parse(localStorage.getItem(STORAGE+"profile")||"null")}catch(e){return null}}
function saveProfile(role,detail){
  role=role||"student";
  if(role==="student")localStorage.removeItem(STORAGE+"profile");
  else localStorage.setItem(STORAGE+"profile",JSON.stringify({role:role,detail:detail||""}));
  try{renderDash()}catch(e){}
}
function fillProfileDetail(){
  var d=$("profileDetailSel");if(!d)return;
  var role=($("profileSel")||{}).value||"student";
  var opts={teacher:["Classes 6-8","Classes 9-10","Classes 11-12","Other classes"],institute:["SSC & Govt exams","NEET","JEE","Board exams","Other exams"]};
  var list=opts[role]||[];
  if(!list.length){d.style.display="none";return}
  d.style.display="block";
  d.innerHTML=list.map(function(x){return '<option value="'+escAttr(x)+'">'+escH(x)+'</option>'}).join("");
  var cur=(getProfile()||{}).detail;
  if(cur){try{for(var i=0;i<d.options.length;i++)if(d.options[i].value===cur)d.selectedIndex=i}catch(e){}}
}
function profileSelChange(){try{fillProfileDetail()}catch(e){}}
function profileLine(){
  var p=getProfile();if(!p)return "";
  if(p.role==="teacher")return "USER PROFILE: your user is a school tuition/coaching teacher"+(p.detail?" for "+p.detail:"")+". Make all content classroom-ready and age-appropriate for their students (lesson plans, worksheets, simple quizzes); skip competitive-exam current affairs. ";
  if(p.role==="institute")return "USER PROFILE: your user runs a coaching institute"+(p.detail?" focused on "+p.detail:"")+". Focus on batch-test workflows: question papers, mock tests, performance analysis, printable student material. ";
  if(p.role==="junior")return "USER PROFILE: your user is a young school student (roughly classes 6-8). Use very simple English (or their language), short sentences, everyday examples, no jargon. ";
  return "";
}
function applyProfileHome(el){
  var p=getProfile();if(!p||!el)return;
  var hs=[];
  if(p.role==="teacher"){hs=["Daily Brief","Score Predictor","Mistake Drill","Spaced Review","Full Analytics"];if(p.detail==="Classes 6-8")hs.push("Mock Exam")}
  else if(p.role==="junior"){hs=["Mock Exam","Score Predictor","Exam Maker"]}
  if(!hs.length)return;
  var cards=el.querySelectorAll(".agent-card");
  for(var i=0;i<cards.length;i++){var b=cards[i].querySelector("b");if(b&&hs.indexOf(b.textContent)>=0)cards[i].style.display="none"}
}
'''
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, HUB + F4)

# Patch 5: SYS_PROMPT gets the profile line
F5 = 'return toneLine+"You are Aurisi'
R5 = 'return profileLine()+toneLine+"You are Aurisi'
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# Patch 6: renderDash applies the profile filter
F6 = '  el.innerHTML=html;\n}\nfunction searchLocker('
R6 = '  el.innerHTML=html;\n  try{applyProfileHome(el)}catch(e){}\n}\nfunction searchLocker('
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

# Patch 7: version bump
F7 = 'var APP_VERSION="58.4"'
R7 = 'var APP_VERSION="58.5"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied profile patches, size: %d bytes" % len(h.encode("utf-8")))
