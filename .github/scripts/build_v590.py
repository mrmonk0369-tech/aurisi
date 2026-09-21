#!/usr/bin/env python3
# AURISI v59.0: Institute Mode (B2B).
# A school/tuition/coaching owner creates their institute (name + classes +
# optional exams + 4-digit owner PIN), gets a 6-character code, and shares it
# with their students. When a student joins with that code, Aurisi becomes
# THEIR app: their name on Home, AI teaches only their class range, and the
# Library shows only their class-level collections + the owner's own material
# (notes/papers) synced from the owner's cloud (Supabase).
# Base: AURISI.html v58.6. Idempotent: no-op if already v59.0.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="59.0"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v59.0 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.6"' in h, "base must be v58.6"

# Patch 1: institute core JS + all UI functions, inserted before profileCats
F1 = 'function profileCats(){'
R1 = r'''var SB_URL="https://ehbdvjkguungjccaaqsm.supabase.co/rest/v1",SB_KEY="sb_publishable_ip0uOdOcSplrTkOIw5MDnA_jwSe6jDa";
function getInst(){try{return JSON.parse(localStorage.getItem(STORAGE+"inst"))}catch(e){return null}}
function instCats(cls,exams){
  var lo=6,hi=12;var m=/^\s*(\d+)\D+(\d+)\s*$/.exec((cls||"").trim());
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
}
function instCloseModals(){try{document.querySelectorAll(".modal-back.open").forEach(function(x){x.remove()})}catch(e){}}
function instRenderBox(){
  var el=$("instBox");if(!el)return;
  var ins=getInst();
  if(!ins){
    el.innerHTML='<button class="lib-chip" onclick="instJoin()">🔑 Join my institute (I have a code)</button> <button class="lib-chip" onclick="instCreate()">🏫 Create an institute (owner)</button>';
    return;
  }
  el.innerHTML='<div class="feat-row"><b>🏫 '+escH(ins.name)+'</b><small>Classes '+escH(ins.cls)+(ins.exams?' · '+escH(ins.exams):'')+'</small></div><div style="margin-top:8px"><button class="lib-chip" onclick="instShowCode()">🔑 Show code</button> <button class="lib-chip" onclick="openInstLib()">📚 Material</button> <button class="lib-chip" onclick="instAdd()">➕ Add</button></div><button class="lib-chip" style="margin-top:8px" onclick="instLeave()">✖ Leave institute</button>';
}
async function instJoin(){
  var code=(prompt("Enter your institute's 6-character code (get it from your teacher):")||"").trim().toUpperCase();
  if(!code)return;
  if(!/^[A-Z0-9]{6}$/.test(code)){toast("That code looks wrong — it is exactly 6 letters/digits");return}
  toast("Checking your code…");
  try{
    var r=await fetch(SB_URL+"/inst_public?select=code,name,cls,exams&code=eq."+encodeURIComponent(code),{headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY}});
    var rows=await r.json();
    if(!rows||!rows.length){toast("No institute found with that code — check with your teacher");return}
    var d=rows[0];
    localStorage.setItem(STORAGE+"inst",JSON.stringify({code:d.code,name:d.name,cls:d.cls,exams:d.exams||""}));
    saveProfile("student","");
    toast("Welcome to "+d.name+"! 🏫");
    instCloseModals();renderDash();
  }catch(e){toast("Could not reach the server — check your internet")}
}
async function instCreate(){
  var name=(prompt("Institute name (your students will see this):\nExample: Vaheka Tuition Classes","Vaheka Tuition Classes")||"").trim();
  if(!name)return;
  var cls=(prompt("Which classes do you teach?\nExample: 6-12, 6-8, 9-10, 11-12","6-12")||"").trim();
  if(!cls)return;
  var exams=(prompt("Any exams you prepare students for? (optional)\nExample: NEET, SSC — leave blank for school only","")||"").trim();
  var pin=(prompt("Set a 4-digit owner PIN (you will need it to add material):","")||"").trim();
  if(!/^[0-9]{4}$/.test(pin)){toast("Owner PIN must be exactly 4 digits");return}
  var chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789",code="";
  for(var t=0;t<5;t++){
    code="";for(var i=0;i<6;i++)code+=chars[Math.floor(Math.random()*chars.length)];
    try{
      var r=await fetch(SB_URL+"/institutes",{method:"POST",headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({code:code,name:name,cls:cls,exams:exams,pin:pin})});
      if(r.ok)break;
      var j=null;try{j=await r.json()}catch(e){}
      if(!j||!j.message||String(j.message).indexOf("duplicate")<0){toast("Could not create — please try again");return}
    }catch(e){toast("Could not reach the server — check your internet");return}
  }
  localStorage.setItem(STORAGE+"inst",JSON.stringify({code:code,name:name,cls:cls,exams:exams}));
  saveProfile("student","");
  toast("Created! Your institute code is "+code);
  instShowCode();
}
function instLeave(){
  if(!confirm("Leave this institute? Your own data stays on this device."))return;
  try{localStorage.removeItem(STORAGE+"inst")}catch(e){}
  instRenderBox();renderDash();toast("Back to regular Aurisi");
}
function instShowCode(){
  var ins=getInst();if(!ins)return;
  var old=document.getElementById("instModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="instModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>🏫 '+escH(ins.name)+'</h2><div class="sub">Classes '+escH(ins.cls)+(ins.exams?' · '+escH(ins.exams):'')+'</div>'+
  '<div class="feat-sec"><b>YOUR INSTITUTE CODE</b><div class="feat-row" style="font-size:28px;font-weight:700;letter-spacing:4px;text-align:center">'+ins.code+'</div><small>Share this code with your students — when they join, Aurisi shows only your classes and your material.</small></div>'+
  '<div class="feat-sec"><b>MATERIAL</b><small>Students see everything you add under My Library → Institute material. Add notes, solved papers, chapter text — anything.</small><div style="margin-top:8px"><button class="lib-chip" onclick="instAdd()">➕ Add material</button> <button class="lib-chip" onclick="openInstLib()">📚 Institute material</button></div></div>';
  b.appendChild(m);document.body.appendChild(b);
}
async function instAdd(){
  var ins=getInst();if(!ins)return;
  var pin=(prompt("Owner PIN:")||"").trim();
  if(!pin)return;
  var title=(prompt("Material title:\nExample: Class 8 Science — Chapter 1 notes","")||"").trim();
  if(!title)return;
  var body=(prompt("Paste the material text (notes, questions, anything):","")||"").trim();
  if(!body)return;
  toast("Saving…");
  try{
    var r=await fetch(SB_URL+"/rpc/add_inst_content",{method:"POST",headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({p_code:ins.code,p_title:title,p_body:body,p_pin:pin})});
    var ok=await r.json();
    if(ok!==true){toast("Wrong PIN or server error");return}
    toast("✅ Material added to "+ins.name);
  }catch(e){toast("Could not reach the server")}
}
async function openInstLib(){
  var ins=getInst();if(!ins)return;
  var old=document.getElementById("instModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="instModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>📚 Institute material</h2><div class="sub">From '+escH(ins.name)+'</div><div id="instList" class="feat-sec"><small>Loading…</small></div>';
  b.appendChild(m);document.body.appendChild(b);
  try{
    var r=await fetch(SB_URL+"/inst_content?select=id,title&code=eq."+encodeURIComponent(ins.code)+"&order=created_at.desc",{headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY}});
    var rows=await r.json();
    var box=$("instList");if(!box)return;
    if(!rows||!rows.length){box.innerHTML='<small>Nothing added yet.</small>';return}
    var hh="";
    rows.forEach(function(x){hh+='<div class="feat-row" style="cursor:pointer" onclick="openInstItem('+x.id+')"><b>'+escH(x.title)+'</b><small>tap to read</small></div>'});
    box.innerHTML=hh;
  }catch(e){var bx=$("instList");if(bx)bx.innerHTML='<small>Could not load — check internet</small>'}
}
async function openInstItem(id){
  try{
    var r=await fetch(SB_URL+"/inst_content?select=title,body&id=eq."+id,{headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY}});
    var rows=await r.json();
    if(!rows||!rows.length){toast("Could not open");return}
    var d=rows[0];
    var old=document.getElementById("instModalBack");if(old)old.remove();
    var b=document.createElement("div");b.className="modal-back open";b.id="instModalBack";
    b.onclick=function(e){if(e.target===b)b.remove()};
    var m=document.createElement("div");m.className="modal feat-modal";
    m.innerHTML='<h2>📖 '+escH(d.title)+'</h2><div style="max-height:60vh;overflow:auto;white-space:pre-wrap;line-height:1.55">'+escH(d.body)+'</div>';
    b.appendChild(m);document.body.appendChild(b);
  }catch(e){toast("Could not load — check internet")}
}
async function instDel(id){
  var ins=getInst();if(!ins)return;
  var pin=(prompt("Owner PIN to delete this material:")||"").trim();if(!pin)return;
  try{
    var r=await fetch(SB_URL+"/rpc/del_inst_content",{method:"POST",headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({p_code:ins.code,p_id:id,p_pin:pin})});
    var ok=await r.json();
    if(ok===true){toast("Deleted");openInstLib()}else toast("Wrong PIN");
  }catch(e){toast("Could not reach the server")}
}
function profileCats(){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: profileLine - institute override
F2 = 'function profileLine(){\n  var p=getProfile();if(!p)return "";'
R2 = '''function profileLine(){
  var ins=getInst();
  if(ins)return "INSTITUTION MODE: your user studies at "+ins.name+" (a real school/tuition running classes "+ins.cls+(ins.exams?"; they also prepare for "+ins.exams:"")+"). Teach ONLY within this class range, keep everything age-appropriate for those classes, and never bring in content above or below their classes. ";
  var p=getProfile();if(!p)return "";'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: profileCats - institute override
F3 = 'function profileCats(){\n  var p=getProfile();if(!p)return null;'
R3 = '''function profileCats(){
  var ins=getInst();if(ins)return instCats(ins.cls,ins.exams);
  var p=getProfile();if(!p)return null;'''
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: applyProfileHome - institute banner on Home
F4 = 'function applyProfileHome(el){\n  var p=getProfile();if(!p||!el)return;'
R4 = '''function applyProfileHome(el){
  var ins=getInst();
  if(ins&&el){
    try{
      var bn=document.createElement("div");
      bn.style.cssText="margin:2px 2px 10px;padding:12px 14px;border-radius:16px;border:1px solid rgba(255,106,61,.4);background:linear-gradient(120deg,rgba(255,106,61,.14),rgba(255,183,77,.10));display:flex;flex-wrap:wrap;gap:8px;align-items:center";
      bn.innerHTML='<b style="font-size:15px">🏫 '+escH(ins.name)+'</b><span class="sub" style="margin:0">Classes '+escH(ins.cls)+(ins.exams?' · '+escH(ins.exams).toUpperCase():'')+' · powered by Aurisi</span><button class="lib-chip" style="margin-left:auto" onclick="instShowCode()">ℹ️ Institute</button>';
      el.insertBefore(bn,el.firstChild);
    }catch(e){}
  }
  var p=getProfile();if(!p||!el)return;'''
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# Patch 5: Settings - Institute Mode section after the profile field
F5 = '''<div class="hint">Aurisi adapts the Home screen and teaching style to who is using it. Tuition owners: pick the classes you teach.</div>
      </div>'''
R5 = '''<div class="hint">Aurisi adapts the Home screen and teaching style to who is using it. Tuition owners: pick the classes you teach.</div>
      </div>

      <div class="field">
        <label>🏢 Institute Mode</label>
        <div id="instBox"></div>
        <div class="hint">School or tuition owner? Create your institute, get a code and share it with your students — they will see only your classes and your material, synced from your cloud.</div>
      </div>'''
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# Patch 6: openSettings - render the institute box
F6 = 'function openSettings(){updateAcctUI();'
R6 = 'function openSettings(){updateAcctUI();instRenderBox();'
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

# Patch 7: Library - institute material shortcut above collections
F7 = "html+='<div class=\"studio-lbl\" style=\"margin:16px 2px 0\">📁 Your Collections</div>';"
R7 = '''if(getInst()){html+='<button class="lib-open" style="margin-top:12px" onclick="openInstLib()">🏫 Institute material from '+escH(getInst().name)+'</button>';}
  html+='<div class="studio-lbl" style="margin:16px 2px 0">📁 Your Collections</div>';'''
assert h.count(F7) == 1, "P7 anchor not found"
h = h.replace(F7, R7)

# Patch 8: version bump
F8 = 'var APP_VERSION="58.6"'
R8 = 'var APP_VERSION="59.0"'
assert h.count(F8) == 1
h = h.replace(F8, R8)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Institute Mode patches, size: %d bytes" % len(h.encode("utf-8")))
