#!/usr/bin/env python3
# AURISI v60.0: Student Pro (owner-controlled paywall).
# Students use Aurisi free while the Aurisi team keeps it free
# (server config student_pro_enabled = false). The moment the team flips
# it to true, every student without a Pro code gets locked out by a
# full-screen Pro gate - only a valid Pro activation code (sold by the
# team, kind='pro' in activation_codes) unlocks the app for X days.
# Institute functionality is untouched.
# Base: AURISI.html v59.1. Idempotent: no-op if already v60.0.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.0"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.0 - no-op")
    sys.exit(0)

assert 'APP_VERSION="59.1"' in h, "base must be v59.1"

# Patch 1: Pro system JS, inserted before profileCats + startup check
F1 = 'function profileCats(){'
R1 = r'''function getAppCfg(){try{return JSON.parse(localStorage.getItem(STORAGE+"appcfg")||"{}")}catch(e){return{}}}
function cfgGet(k){var c=getAppCfg();return c[k]||""}
async function fetchAppConfig(){
  var now=Date.now();
  try{
    var c=getAppCfg();
    if(c._ts&&now-c._ts<3600000)return c;
  }catch(e){}
  try{
    var r=await fetch(SB_URL+"/app_config?select=key,value",{headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY}});
    var rows=await r.json();
    var o={_ts:Date.now()};
    if(rows&&rows.forEach){rows.forEach(function(x){o[x.key]=x.value})}
    try{localStorage.setItem(STORAGE+"appcfg",JSON.stringify(o))}catch(e){}
    return o;
  }catch(e){return getAppCfg()}
}
function isPro(){try{var p=JSON.parse(localStorage.getItem(STORAGE+"pro"));return !!(p&&p.until&&p.until>Date.now())}catch(e){return false}}
function proCheckGate(){
  if(cfgGet("student_pro_enabled")!=="true")return;
  if(isPro())return;
  var old=document.getElementById("proGateBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="proGateBack";b.style.zIndex="99999";
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>✨ Aurisi Pro</h2><div class="sub">Aurisi is now a Pro app. Enter your Pro code to continue — you get it from the Aurisi team.</div>'+
  '<div class="feat-sec"><input id="proCodeIn" placeholder="Your Pro code" style="width:100%;box-sizing:border-box;padding:10px 13px;border:1px solid var(--line);border-radius:12px;font:inherit;font-size:13px;background:var(--surface);color:var(--text)">'+
  '<div style="margin-top:10px"><button class="lib-open" style="width:100%" onclick="proActivate()">🔓 Unlock Aurisi</button></div></div>';
  b.appendChild(m);document.body.appendChild(b);
}
async function proActivate(){
  var v="";
  var e1=document.getElementById("proCodeIn");var e2=document.getElementById("proCodeIn2");
  if(e1&&e1.value)v=e1.value;else if(e2&&e2.value)v=e2.value;
  v=(v||"").trim();
  if(!v){toast("Enter your Pro code");return}
  toast("Checking your code…");
  try{
    var r=await fetch(SB_URL+"/rpc/activate_pro",{method:"POST",headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({p_act:v})});
    var days=await r.json();
    if(!days||days<1){toast("Invalid or already-used Pro code");return}
    var until=Date.now()+days*86400000;
    try{localStorage.setItem(STORAGE+"pro",JSON.stringify({until:until}))}catch(e){}
    toast("✅ Aurisi Pro active!");
    var g=document.getElementById("proGateBack");if(g)g.remove();
    try{proRenderBox()}catch(e){}
  }catch(e){toast("Could not reach the server — check your internet")}
}
function proRenderBox(){
  var el=$("proBox");if(!el)return;
  if(isPro()){
    var p={};try{p=JSON.parse(localStorage.getItem(STORAGE+"pro")||"{}")}catch(e){}
    var d=new Date(p.until||0);
    el.innerHTML='<div class="feat-row"><b>✨ Aurisi Pro active</b><small>until '+d.toLocaleDateString()+'</small></div>';
  }else{
    el.innerHTML='<input id="proCodeIn2" placeholder="Pro code (if you have one)" style="width:100%;box-sizing:border-box;padding:10px 13px;border:1px solid var(--line);border-radius:12px;font:inherit;font-size:13px;background:var(--surface);color:var(--text)"><div style="margin-top:8px"><button class="lib-chip" onclick="proActivate()">🔓 Activate Pro</button></div>';
  }
}
setTimeout(function(){try{fetchAppConfig().then(function(){try{proCheckGate()}catch(e){}})}catch(e){}},1200);
function profileCats(){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: Settings - Aurisi Pro section after Institute Mode field
F2 = 'Institutes need a paid activation code from the Aurisi team. Create your institute with it, then share your 6-character code with your students — they see only your classes and your material.</div>\n      </div>'
R2 = '''Institutes need a paid activation code from the Aurisi team. Create your institute with it, then share your 6-character code with your students — they see only your classes and your material.</div>
      </div>

      <div class="field">
        <label>✨ Aurisi Pro</label>
        <div id="proBox"></div>
        <div class="hint">Students use Aurisi free while the Aurisi team keeps it free. If the team switches Pro on, a Pro code is needed to use the app.</div>
      </div>'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: openSettings - render pro box too
F3 = 'function openSettings(){updateAcctUI();instRenderBox();'
R3 = 'function openSettings(){updateAcctUI();instRenderBox();proRenderBox();'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: version bump
F4 = 'var APP_VERSION="59.1"'
R4 = 'var APP_VERSION="60.0"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Student Pro patches, size: %d bytes" % len(h.encode("utf-8")))
