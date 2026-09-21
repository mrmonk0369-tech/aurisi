#!/usr/bin/env python3
# AURISI v58.0 "Fix & Flow" builder
# Base: AURISI.html v57.0 (APP_VERSION="57.0"). Idempotent: exits 0 untouched if already v58.
# NOTE: this file deliberately avoids double-backslash and backslash-quote literals;
# risky strings are derived from the base file at runtime (transport-proof).
import sys, io

BS = chr(92)
BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_v58.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.0"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58 - no-op")
    sys.exit(0)

assert 'APP_VERSION="57.0"' in h, "base must be v57.0"

# ---------- runtime-derived building blocks ----------
# exact quoting used by the existing paper-length chips (self-calibrating)
_ex = h.find("EXAM_SEL.len=" + BS)
EXAM_Q = h[_ex + 13:_ex + 15]
_li = h.find("EXAM_LENS.forEach(function(l)")
_le = h.find("});", _li)
lenloop = h[_li:_le + 3]
diffloop = (lenloop
    .replace("EXAM_LENS.forEach(function(l)", "EXAM_DIFFS.forEach(function(dd)")
    .replace("EXAM_SEL.len=", "EXAM_SEL.diff=")
    .replace("l.id", "dd.id")
    .replace("l.name", "dd.name"))
# exact quoting used by the New Lesson agent-card button
_nl_i = h.find("<b>New Lesson</b>")
_nl_k = h.rfind("<button", 0, _nl_i)
NL_FIND = h[_nl_k:_nl_i + 17]
_nl_s = h.find("switchView(", _nl_k)
NL_Q = h[_nl_s + 11:_nl_s + 13]

assert NL_Q == BS + chr(39), 'NL_Q sanity failed: ' + repr(NL_Q)
assert EXAM_Q == BS + chr(39), 'EXAM_Q sanity failed: ' + repr(EXAM_Q)

PATCHES = []

def P(name, find, repl, count=1):
    PATCHES.append((name, find, repl, count))

# 1. Version bump
P("version",
  'var APP_VERSION="57.0"',
  'var APP_VERSION="58.0"')

# 2. KaTeX delimiters: add display math
P("katex-delims",
  '{left:"' + BS + BS + '(",right:"' + BS + BS + ')",display:false},{left:"$",right:"$",display:false}],throwOnError:false});',
  '{left:"' + BS + BS + '(",right:"' + BS + BS + ')",display:false},{left:"$",right:"$",display:false},{left:"' + BS + BS + '[",right:"' + BS + BS + ']",display:true}],throwOnError:false});')

# 3. Flashcards: render math on every card face
P("cards-math",
  'cnt.textContent=(idx+1)+" of "+pairs.length;\n      }',
  'cnt.textContent=(idx+1)+" of "+pairs.length;\n        try{renderMathIn(qtext);renderMathIn(ans)}catch(e){}\n      }')

# 4. Strip HTML comments before markdown render (pack reader bug)
P("strip-comments",
  'function safeMarkdown(text){\n  let html=formatMarkdown(text||"");',
  'function safeMarkdown(text){\n  text=String(text||"").replace(/<!--[' + BS + 's' + BS + 'S]*?-->/g,"");\n  let html=formatMarkdown(text||"");')

# 5. FAB hide when modal open (CSS)
P("fab-css",
  'body.fab-on #fabDim{display:block}',
  'body.fab-on #fabDim{display:block}\nbody.modal-on #dsFab,body.modal-on #fabDim,body:has(.modal-back.open) #dsFab,body:has(.modal-back.open) #fabDim{display:none!important}')

# 6. openSettings adds body class
P("settings-open",
  'settingsTab("general");\n  $("modalBack").classList.add("open");\n}',
  'settingsTab("general");\n  $("modalBack").classList.add("open");try{document.body.classList.add("modal-on")}catch(e){}\n}')

# 7. closeModal removes body class
P("settings-close",
  'function closeModal(){$("modalBack").classList.remove("open")}',
  'function closeModal(){$("modalBack").classList.remove("open");try{document.body.classList.remove("modal-on")}catch(e){}}')

# 8. Carousel: neighbours stay readable
P("carousel-op",
  'op=Math.max(0,1.02-.46*ad);',
  'op=Math.max(.25,1.04-.4*ad);')

# 9. School Mode: teacher-paced by default (no auto-advance)
P("school-pace",
  'BOARD.lesson=lesson;BOARD.i=0;BOARD.auto=true;BOARD.voice=true;',
  'BOARD.lesson=lesson;BOARD.i=0;BOARD.auto=false;BOARD.voice=true;')

# 10. Native language for students (auto mode)
P("native-lang",
  'langLine="Default to clean, simple language matching how the user writes to you; if the user writes in a specific language, reply in that same language.";',
  'langLine="Default to clean, simple language matching how the user writes to you; if the user writes in a specific language, reply in that same language. If the learner writes Hinglish (Hindi in English letters) or any Indian language, reply in that language in its native script (e.g. Devanagari for Hindi) while keeping technical terms, formulas and exam keywords in English so the learner stays exam-ready. The app UI stays in English, but the learner is always free to study in their own language.";')

# 11. Score predictor: no instruction echo (no-history branch)
P("predict-1",
  'quick("Predict my exam score and my biggest risk areas. (Note: I have no quiz history yet — ask me to take a quiz first, then tell me honestly.)");',
  'quick("Predict my exam score and my biggest risk areas. (Note: I have no quiz history yet — ask me to take a quiz first, then tell me honestly.) Output ONLY the student-facing prediction — never echo these instructions or add notes about how to answer.");')

# 12. Score predictor: no instruction echo (with-data branch)
P("predict-2",
  'quick("Predict my exam score honestly from my real data.',
  'quick("Output ONLY the student-facing prediction — never echo these instructions or add notes about how to answer. Predict my exam score honestly from my real data.')

# 13. Puter low balance: disable for session + friendly toast (non-stream)
P("puter-lowbal",
  '}catch(e){PUTER_BAD[model]=(PUTER_BAD[model]||0)+1;lastErr=(e&&e.message)||String(e)}',
  '}catch(e){PUTER_BAD[model]=(PUTER_BAD[model]||0)+1;lastErr=(e&&e.message)||String(e);if(/balance|credit|quota|exceed|insufficient|payment/i.test(lastErr)){try{window.PUTER_OFF=true;toast("Puter free quota over — switching to the free backup engine. For best speed, add your free Groq key in Settings → AI Keys.")}catch(_e){}}}')

# 14. Puter low balance (stream path)
P("puter-lowbal-stream",
  '}catch(err){\n      if(err&&err.name==="AbortError")throw err;\n      lastErr=err.message||String(err);\n    }',
  '}catch(err){\n      if(err&&err.name==="AbortError")throw err;\n      lastErr=err.message||String(err);\n      if(/balance|credit|quota|exceed|insufficient|payment/i.test(lastErr)){try{window.PUTER_OFF=true;toast("Puter free quota over — switching to the free backup engine.")}catch(_e){}}\n    }')

# 15. puterReady honours session off flag
P("puter-ready",
  'function puterReady(){return typeof puter!=="undefined"&&puter.ai&&typeof puter.ai.chat==="function"}',
  'function puterReady(){return !window.PUTER_OFF&&typeof puter!=="undefined"&&puter.ai&&typeof puter.ai.chat==="function"}')

# 16. Exam Maker: difficulty mix data
P("exam-diffs",
  'var EXAM_SEL={type:"hssc",len:"half",pdfs:{},custom:""};',
  'var EXAM_SEL={type:"hssc",len:"half",diff:"balanced",pdfs:{},custom:""};\nvar EXAM_DIFFS=[{id:"balanced",name:"⚖️ Balanced",p:[33,34,33],t:"A real-paper mix — a bit of everything"},{id:"easy",name:"🌱 Confidence build",p:[50,30,20],t:"Start easy, build momentum"},{id:"hard",name:"🔥 Topper mode",p:[20,35,45],t:"Hard-leaning — exam-level pressure"},{id:"prog",name:"📈 Progressive",p:[15,40,45],t:"Gets harder as you go"}];\nfunction examDiffP(){return (EXAM_DIFFS.find(function(x){return x.id===EXAM_SEL.diff})||EXAM_DIFFS[0]).p}')

# 17. Exam Maker: difficulty card UI (uses the runtime-derived diffloop)
P17_FIND = "  html+='</div></div>';\n  var n=L.pdfs.filter(function(p){return EXAM_SEL.pdfs[p.id]}).length+EXAM_FILES.length;"
P17_REPL = ("  html+='</div></div>';\n  var _dd=EXAM_DIFFS.find(function(x){return x.id===EXAM_SEL.diff})||EXAM_DIFFS[0];\n"
  + '  html+=\'<div class="ws-card"><h3>4️⃣ Difficulty mix</h3><div class="lib-chips" style="margin-top:6px">\';\n'
  + "  " + diffloop + "\n"
  + '  html+=\'</div><small style="color:var(--muted);display:block;margin-top:8px">\'+_dd.t+\' — roughly \'+_dd.p[0]+\'% easy · \'+_dd.p[1]+\'% medium · \'+_dd.p[2]+\'% hard, mixed through the paper.</small></div>\';\n'
  + "  var n=L.pdfs.filter(function(p){return EXAM_SEL.pdfs[p.id]}).length+EXAM_FILES.length;")
P("exam-diff-ui", P17_FIND, P17_REPL)

# 18. startExam prompt: inject difficulty mix
P("exam-diff-prompt",
  '+". Rules: every question must come from the attached material only.',
  '+". Difficulty mix: roughly "+examDiffP()[0]+"% easy, "+examDiffP()[1]+"% medium and "+examDiffP()[2]+"% hard questions, mixed through the paper — do not group them in blocks. Rules: every question must come from the attached material only.')

# 19. Language Lab -> Language Hub (4 user-visible strings)
P("hub-1",
  '<b>Language Lab</b><small>One lab, every language — pick yours</small>',
  '<b>Language Hub</b><small>One hub, every language — pick yours</small>')
P("hub-2",
  'ws-h">🌍 Language Lab</div>',
  'ws-h">🌍 Language Hub</div>')
P("hub-3",
  '">One lab. Every language.</b>',
  '">One hub. Every language.</b>')
P("hub-4",
  'Open the Language Lab</button>',
  'Open the Language Hub</button>')

# 20. New Lesson gets its own room (find/repl derived at runtime)
P("newlesson-room",
  NL_FIND,
  NL_FIND.replace(');newChat()', ');roomStart(' + NL_Q + '✨' + NL_Q + ',' + NL_Q + 'New Lesson' + NL_Q + ')'))

# 21. Features overview: welcome link
P("feat-welcome",
  "<h2 data-i18n=\"welcomeTitle\">Hi, I'm Aurisi</h2>",
  "<h2 data-i18n=\"welcomeTitle\">Hi, I'm Aurisi</h2>\n        <button class=\"feat-tour\" onclick=\"showFeatures()\">✨ What's inside AURISI?</button>")

# 22. Features overview: drawer button
P("feat-drawer",
  '<button class="drawer-list-btn" onclick="closeDrawer();openTestCenter()"><span class="dl-ico">📝</span><span>Mock Test Center</span></button>',
  '<button class="drawer-list-btn" onclick="closeDrawer();openTestCenter()"><span class="dl-ico">📝</span><span>Mock Test Center</span></button>\n  <button class="drawer-list-btn" onclick="closeDrawer();showFeatures()"><span class="dl-ico">✨</span><span>What' + "'" + 's inside AURISI</span></button>')

# 23. showFeatures() JS (insert before dailyBrief) — no backslashes at all
feat_js = '''function featModalClose(){var e=document.getElementById("featModalBack");if(e)e.remove()}
function showFeatures(){
  var old=document.getElementById("featModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="featModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  var secs=[["📖 LEARN",[["✨ New Lesson","Any subject, taught like a great teacher"],["🏫 School Mode","Smart-board class for any class & board"],["🌍 Language Hub","Spanish, French, Japanese + more, level-tracked"],["📚 World Library","Verified reference books built in"],["✏️ Doodle Board","Draw it — learn from your own doodle"]]],["🧪 PRACTICE",[["🧪 Exam Maker","Build a real exam from your own PDFs"],["📝 Mock Test Center","Full-screen timed tests, works offline"],["🩹 Mistake Drill","Re-tests only what you got wrong"],["🧠 Spaced Review","Cards that come back before you forget"],["📅 Daily Brief","Current affairs + a recall card"],["🔮 Score Predictor","Honest score forecast from your data"]]],["🛠️ TOOLS",[["🎧 Podcast","Any material as a 2-voice audio lesson"],["🗺️ Mind Map","Tap-to-fold topic tree"],["🎬 Video Lesson","Slides with narration"],["📈 Math Graphs","Plot any formula"],["🎯 Test Paper","Branded 50-mark papers"],["🎙️ Speaking Practice","Live talk, corrected as you go"],["⏱️ Focus Timer","Pomodoro with streaks"],["🗄️ My Locker","Your PDFs, notes & cloud backup"]]]];
  var html='<h2>✨ Everything inside AURISI</h2><div class="sub">One teacher, every tool — tap any feature from Home.</div>';
  secs.forEach(function(s){html+='<div class="feat-sec"><b>'+s[0]+'</b>';s[1].forEach(function(f){html+='<div class="feat-row"><span>'+f[0]+'</span><small>'+f[1]+'</small></div>'});html+='</div>'});
  m.innerHTML=html+'<button class="btn" style="width:100%;margin-top:6px" onclick="featModalClose()">Let us go 🚀</button>';
  b.appendChild(m);document.body.appendChild(b);
}
'''
P("feat-js",
  'function dailyBrief(){',
  feat_js + 'function dailyBrief(){')

# 24. Feature modal CSS
P("feat-css",
  'body.fab-on #fabDim{display:block}',
  '.feat-tour{margin:2px auto 0;display:block;background:var(--surface2);border:1px solid var(--line);color:var(--text);border-radius:99px;padding:6px 16px;font-size:11.5px;font-weight:700;cursor:pointer;font-family:inherit}\n.feat-modal{max-width:430px}\n.feat-sec{margin-top:12px}\n.feat-sec b{font-size:11px;letter-spacing:1px;color:var(--muted)}\n.feat-row{display:flex;align-items:baseline;gap:8px;padding:5px 0;border-bottom:1px dashed var(--line)}\n.feat-row span{font-size:13px;font-weight:700;white-space:nowrap}\n.feat-row small{font-size:11px;color:var(--muted)}\nbody.fab-on #fabDim{display:block}')

# 25. KaTeX load fallback + global re-render (insert before init call)
kat_js = '''/* ===== v58 KATEX RESILIENCE ===== */
(function(){
  function katAll(){try{document.querySelectorAll(".ai-md,.quiz-box,.quiz-result,.cards-box").forEach(function(el){renderMathIn(el)})}catch(e){}}
  var n=0;
  function chk(){
    if(window.renderMathInElement){if(window.__katReady)return;window.__katReady=1;katAll();return}
    if(++n>10)return;
    setTimeout(chk,1500);
  }
  chk();
  window.addEventListener("load",function(){
    setTimeout(function(){
      if(!window.renderMathInElement){
        var s1=document.createElement("script");s1.src="https://unpkg.com/katex@0.16.8/dist/katex.min.js";
        var s2=document.createElement("script");s2.src="https://unpkg.com/katex@0.16.8/dist/contrib/auto-render.min.js";
        s2.onload=function(){window.__katReady=0;chk()};
        document.head.appendChild(s1);
        setTimeout(function(){document.head.appendChild(s2)},500);
      }
    },800);
  });
})();
'''
P("katex-fallback",
  'initSnapCarousel();updateTopTitle();applyAccentBoot();',
  kat_js + 'initSnapCarousel();updateTopTitle();applyAccentBoot();')

applied = 0
for (name, find, repl, count) in PATCHES:
    c = h.count(find)
    assert c == count, "PATCH %s: found %d occurrences (expected %d) of %r" % (name, c, count, find[:80])
    h = h.replace(find, repl)
    applied += 1

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied %d patches, size: %d bytes" % (applied, len(h.encode("utf-8"))))
