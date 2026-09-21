#!/usr/bin/env python3
# AURISI v60.2: Controlled reveal (business model hidden by default).
# Like big software companies, Aurisi now shows only what it wants to show.
# - Normal students see NO business section in Settings - just a tiny
#   discreet "For institutes & tuitions" chip that opens a minimal
#   code-entry modal (no model explanation, no pricing, no strategy).
# - The full "Business & Institute" section with the guide is visible ONLY
#   when the Aurisi team flips the server config biz_mode to 'visible',
#   or to users who already joined an institute.
# - The Pro field only shows when Pro is enabled or the user has Pro.
# Base: AURISI.html v60.1. Idempotent: no-op if already v60.2.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.2"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.2 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.1"' in h, "base must be v60.1"

# Patch 1: bizApplyMode + discreet modal JS, before profileCats
F1 = 'function profileCats(){'
R1 = r'''function openBizDiscreet(){
  var old=document.getElementById("bizModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="bizModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>🏫 Aurisi for Institutes</h2><div class="sub">Have a code from your teacher or the Aurisi team?</div>'+
  '<div class="feat-sec"><div style="margin-top:8px"><button class="lib-chip" onclick="instJoin()">🔑 Join my institute (I have a code)</button></div>'+
  '<div style="margin-top:8px"><button class="lib-chip" onclick="instCreate()">🔑 I have an activation code (owner)</button></div></div>';
  b.appendChild(m);document.body.appendChild(b);
}
function bizApplyMode(){
  var f=$("bizField");var d=$("bizDiscreet");var p=$("proField");
  var showFull=cfgGet("biz_mode")==="visible"||!!getInst();
  if(f)f.style.display=showFull?"":"none";
  if(d)d.style.display=showFull?"none":"";
  if(p)p.style.display=(isPro()||cfgGet("student_pro_enabled")==="true")?"":"none";
}
function profileCats(){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: restructure the Business field (ids + separate Pro field + discreet chip)
F2 = '''<div class="field">
        <label>💼 Business & Institute</label>
        <button class="lib-open" style="width:100%;margin-bottom:10px" onclick="openBizGuide()">📖 How Aurisi Business works</button>
        <div id="instBox"></div>
        <div id="proBox"></div>
        <div class="hint">One app, three plans: students learn free, institutes run on a paid license, and Pro unlocks the full app. Tap the guide for details.</div>
      </div>'''
R2 = '''<div class="field" id="bizField">
        <label>💼 Business & Institute</label>
        <button class="lib-open" style="width:100%;margin-bottom:10px" onclick="openBizGuide()">📖 How Aurisi Business works</button>
        <div id="instBox"></div>
        <div class="hint">One app, three plans: students learn free, institutes run on a paid license, and Pro unlocks the full app. Tap the guide for details.</div>
      </div>

      <div class="field" id="proField" style="display:none">
        <label>✨ Aurisi Pro</label>
        <div id="proBox"></div>
      </div>

      <div id="bizDiscreet" style="display:none;text-align:center;margin-top:4px"><button class="lib-chip" onclick="openBizDiscreet()">🏫 For institutes & tuitions</button></div>'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: openSettings - apply visibility rules
F3 = 'function openSettings(){updateAcctUI();instRenderBox();proRenderBox();'
R3 = 'function openSettings(){updateAcctUI();instRenderBox();proRenderBox();bizApplyMode();'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: version bump
F4 = 'var APP_VERSION="60.1"'
R4 = 'var APP_VERSION="60.2"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Controlled Reveal patches, size: %d bytes" % len(h.encode("utf-8")))
