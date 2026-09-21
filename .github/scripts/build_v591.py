#!/usr/bin/env python3
# AURISI v59.1: Master Access Control (B2B licensing).
# The app owner (Aurisi team) is the only one who can mint institutes:
# institute creation now REQUIRES an activation code that only the Aurisi
# team sells (e.g. Rs 5k for 1 year). Server-side: create_institute RPC
# validates the activation code, generates the 6-char institute code, sets
# the subscription expiry, and burns the activation code. The Aurisi team
# also holds a kill switch (active flag) and expiry on every institute.
# Base: AURISI.html v59.0. Idempotent: no-op if already v59.1.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="59.1"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v59.1 - no-op")
    sys.exit(0)

assert 'APP_VERSION="59.0"' in h, "base must be v59.0"

# Patch 1: replace instCreate with activation-code flow (server RPC)
A = 'async function instCreate(){'
B = 'function instLeave(){'
iA = h.find(A)
iB = h.find(B)
assert iA != -1 and iB != -1 and iA < iB, "P1 anchors not found"
NEW = r'''async function instCreate(){
  var act=(prompt("Activation code (from the Aurisi team — you get it when you buy institute access):","")||"").trim();
  if(!act)return;
  var name=(prompt("Institute name (your students will see this):\nExample: Vaheka Tuition Classes","Vaheka Tuition Classes")||"").trim();
  if(!name)return;
  var cls=(prompt("Which classes do you teach?\nExample: 6-12, 6-8, 9-10, 11-12","6-12")||"").trim();
  if(!cls)return;
  var exams=(prompt("Any exams you prepare students for? (optional)\nExample: NEET, SSC — leave blank for school only","")||"").trim();
  var pin=(prompt("Set a 4-digit owner PIN (you will need it to add material):","")||"").trim();
  if(!/^[0-9]{4}$/.test(pin)){toast("Owner PIN must be exactly 4 digits");return}
  toast("Creating your institute…");
  var code="";
  try{
    var r=await fetch(SB_URL+"/rpc/create_institute",{method:"POST",headers:{apikey:SB_KEY,Authorization:"Bearer "+SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({p_act:act,p_name:name,p_cls:cls,p_exams:exams,p_pin:pin})});
    var res=await r.json();
    if(typeof res!=="string"||res.indexOf("ERR:")===0){toast(res||"Could not create — check your activation code");return}
    code=res;
  }catch(e){toast("Could not reach the server — check your internet");return}
  localStorage.setItem(STORAGE+"inst",JSON.stringify({code:code,name:name,cls:cls,exams:exams}));
  saveProfile("student","");
  toast("Created! Your institute code is "+code);
  instShowCode();
}
'''
h = h[:iA] + NEW + h[iB:]

# Patch 2: settings hint - activation code required
F2 = 'School or tuition owner? Create your institute, get a code and share it with your students — they will see only your classes and your material, synced from your cloud.'
R2 = 'Institutes need a paid activation code from the Aurisi team. Create your institute with it, then share your 6-character code with your students — they see only your classes and your material.'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: create button label clarity
F3 = '🏫 Create an institute (owner)'
R3 = '🏫 Create an institute (activation code)'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: version bump
F4 = 'var APP_VERSION="59.0"'
R4 = 'var APP_VERSION="59.1"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Master Access patches, size: %d bytes" % len(h.encode("utf-8")))
