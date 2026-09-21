#!/usr/bin/env python3
# AURISI v60.1: Business Guide section.
# All business-model features (Institute Mode + Aurisi Pro) now live in ONE
# dedicated Settings section "Business & Institute" with a clear
# plain-language guide modal that explains the whole model: students free,
# institutes on paid activation codes, Pro when the team enables it.
# Base: AURISI.html v60.0. Idempotent: no-op if already v60.1.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.1"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.1 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.0"' in h, "base must be v60.0"

# Patch 1: Business guide modal function, before profileCats
F1 = 'function profileCats(){'
R1 = r'''function openBizGuide(){
  var old=document.getElementById("bizModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="bizModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>💼 Aurisi for Business</h2><div class="sub">One app, three ways to use it — pick yours</div>'+
  '<div class="feat-sec"><b>🎓 STUDENTS — FREE</b><small>Any student can use Aurisi free: AI teacher, exams, library, everything. No code needed, no payment.</small></div>'+
  '<div class="feat-sec"><b>🏫 INSTITUTES & TUITIONS — PAID LICENSE</b><small>Own a tuition, school or coaching? Buy an activation code from the Aurisi team (monthly or yearly plan). Then:<br>1. Tap "Create an institute" and enter your activation code<br>2. You get a 6-character code — share it with your students<br>3. Their app becomes YOURS: your name, your classes, your material<br>4. Plan expired? Renew with a new activation code</small><div style="margin-top:10px"><button class="lib-chip" onclick="instJoin()">🔑 Join my institute (I have a code)</button> <button class="lib-chip" onclick="instCreate()">🏫 Create an institute (activation code)</button></div></div>'+
  '<div class="feat-sec"><b>✨ AURISI PRO — STUDENT PLAN</b><small>Students use Aurisi free while the Aurisi team keeps it free. If the team switches Pro on, a Pro code is needed to use the app. Your status right now: <b>'+(isPro()?'Pro active':'Free')+'</b></small></div>'+
  '<div class="feat-sec"><b>❓ WANT ACCESS?</b><small>To buy an activation code or a Pro code, contact the Aurisi team.</small></div>';
  b.appendChild(m);document.body.appendChild(b);
}
function profileCats(){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: merge Institute Mode + Pro fields into one Business & Institute section
F2 = '''<div class="field">
        <label>🏢 Institute Mode</label>
        <div id="instBox"></div>
        <div class="hint">Institutes need a paid activation code from the Aurisi team. Create your institute with it, then share your 6-character code with your students — they see only your classes and your material.</div>
      </div>

      <div class="field">
        <label>✨ Aurisi Pro</label>
        <div id="proBox"></div>
        <div class="hint">Students use Aurisi free while the Aurisi team keeps it free. If the team switches Pro on, a Pro code is needed to use the app.</div>
      </div>'''
R2 = '''<div class="field">
        <label>💼 Business & Institute</label>
        <button class="lib-open" style="width:100%;margin-bottom:10px" onclick="openBizGuide()">📖 How Aurisi Business works</button>
        <div id="instBox"></div>
        <div id="proBox"></div>
        <div class="hint">One app, three plans: students learn free, institutes run on a paid license, and Pro unlocks the full app. Tap the guide for details.</div>
      </div>'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: version bump
F3 = 'var APP_VERSION="60.0"'
R3 = 'var APP_VERSION="60.1"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Business Guide patches, size: %d bytes" % len(h.encode("utf-8")))
