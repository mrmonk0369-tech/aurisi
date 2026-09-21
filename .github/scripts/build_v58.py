#!/usr/bin/env python3
# AURISI v58.0 "Fix & Flow" builder
# Base: AURISI.html v57.0 (APP_VERSION="57.0"). Idempotent: exits 0 untouched if already v58.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_v58.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.0"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58 - no-op")
    sys.exit(0)

assert 'APP_VERSION="57.0"' in h, "base must be v57.0"

PATCHES = []

def P(name, find, repl, count=1):
    PATCHES.append((name, find, repl, count))

# 1. Version bump
P("version",
  'var APP_VERSION="57.0"',
  'var APP_VERSION="58.0"')

# 2. KaTeX delimiters: add \\[ \\] display math
P("katex-delims",
  '{left:"\\\\(",right:"\\\\)",display:false},{left:"$",right:"$",display:false}],throwOnError:false});',
  '{left:"\\\\(",right:"\\\\)",display:false},{left:"$",right:"$",display:false},{left:"\\\\[",right:"\\\\]",display:true}],throwOnError:false});')

# 3. Flashcards: render math on every card face
P("cards-math",
  'cnt.textContent=(idx+1)+" of "+pairs.length;\n      }',
  'cnt.textContent=(idx+1)+" of "+pairs.length;\n        try{renderMathIn(qtext);renderMathIn(ans)}catch(e){}\n      }')

# 4. Strip HTML comments before markdown render (pack reader bug)
P("strip-comments",
  'function safeMarkdown(text){\n  let html=formatMarkdown(text||"");',
  'function safeMarkdown(text){\n  text=String(text||"").replace(/<!--[\\s\\S]*?-->/g,"");\n  let html=formatMarkdown(text||"");')

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
  '}catch(e){PUTER_BAD[model]=(PUTER_BAD[model]||0)+1;lastErr=(e&&e.message)||String(e);if(/balance|credit|quota|exceed|insufficient|payment/i.test(lastErr)){try{window.PUTER_OFF=true;toast("Puter free quota over — switching to the free backup engine. For best speed, add your free Groq key in Settings \\u2192 AI Keys.")}catch(_e){}}}')

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
  'var EXAM_SEL={type:"hssc",len:"half",diff:"balanced",pdfs:{},custom:""};\nvar EXAM_DIFFS=[{id:"balanced",name:"\\u2696\\ufe0f Balanced",p:[33,34,33],t:"A real-paper mix — a bit of everything"},{id:"easy",name:"\\U0001F331 Confidence build",p:[50,30,20],t:"Start easy, build momentum"},{id:"hard",name:"\\U0001F525 Topper mode",p:[20,35,45],t:"Hard-leaning — exam-level pressure"},{id:"prog",name:"\\U0001F4C8 Progressive",p:[15,40,45],t:"Gets harder as you go"}];\nfunction examDiffP(){return (EXAM_DIFFS.find(function(x){return x.id===EXAM_SEL.diff})||EXAM_DIFFS[0]).p}')

# 17. Exam Maker: difficulty card UI (after Paper length, before Generate)
P("exam-diff-ui",
  "  html+='</div></div>';\n  var n=L.pdfs.filter(function(p){return EXAM_SEL.pdfs[p.id]}).length+EXAM_FILES.length;",
  "  html+='</div></div>';\n  var _dd=EXAM_DIFFS.find(function(x){return x.id===EXAM_SEL.diff})||EXAM_DIFFS[0];\n  html+='<div class=\"ws-card\"><h3>4\\ufe0f\\u20e3 Difficulty mix</h3><div class=\"lib-chips\" style=\"margin-top:6px\">';\n  EXAM_DIFFS.forEach(function(dd){html+='<button class=\"lib-chip'+(EXAM_SEL.diff===dd.id?\" on\":\"\")+'\" onclick=\"EXAM_SEL.diff=\\''+dd.id+'\\';renderExam()\">'+dd.name+'</button>'});\n  html+='</div><small style=\"color:var(--muted);display:block;margin-top:8px\">'+_dd.t+' — roughly '+_dd.p[0]+'% easy · '+_dd.p[1]+'% medium · '+_dd.p[2]+'% hard, mixed through the paper.</small></div>';\n  var n=L.pdfs.filter(function(p){return EXAM_SEL.pdfs[p.id]}).length+EXAM_FILES.length;")

# 18. startExam prompt: inject difficulty mix
P("exam-diff-prompt",
  '+". Rules: every question must come from the attached material only.',
  '+". Difficulty mix: roughly "+examDiffP()[0]+"% easy, "+examDiffP()[1]+"% medium and "+examDiffP()[2]+"% hard questions, mixed through the paper — do not group them in blocks. Rules: every question must come from the attached material only.')

# 19. Language Lab -> Language Hub (4 user-visible strings)
P("hub-1",
  '<b>Language Lab</b><small>One lab, every language — pick yours</small>',
  '<b>Language Hub</b><small>One hub, every language — pick yours</small>')
P("hub-2",
  'ws-h">\\U0001F30D Language Lab</div>',
  'ws-h">\\U0001F30D Language Hub</div>')
P("hub-3",
  '">One lab. Every language.</b>',
  '">One hub. Every language.</b>')
P("hub-4",
  'Open the Language Lab</button>',
  'Open the Language Hub</button>')

# 20. New Lesson gets its own room
P("newlesson-room",
  '\'<button class="agent-card" onclick="switchView(\\'chat\\');newChat()"><span class="agent-ico">\\u2728</span><span><b>New Lesson</b>',
  '\'<button class="agent-card" onclick="switchView(\\'chat\\');newChat();roomStart(\\'\\u2728\\',\\'New Lesson\\')"><span class="agent-ico">\\u2728</span><span><b>New Lesson</b>')

# 21. Features overview: welcome link
P("feat-welcome",
  '<h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>',
  '<h2 data-i18n="welcomeTitle">Hi, I\'m Aurisi</h2>\n        <button class="feat-tour" onclick="showFeatures()">\\u2728 What\'s inside AURISI?</button>')

# 22. Features overview: drawer button
P("feat-drawer",
  '<button class="drawer-list-btn" onclick="closeDrawer();openTestCenter()"><span class="dl-ico">\\U0001F4DD</span><span>Mock Test Center</span></button>',
  '<button class="drawer-list-btn" onclick="closeDrawer();openTestCenter()"><span class="dl-ico">\\U0001F4DD</span><span>Mock Test Center</span></button>\n  <button class="drawer-list-btn" onclick="closeDrawer();showFeatures()"><span class="dl-ico">\\u2728</span><span>What\'s inside AURISI</span></button>')

# 23. showFeatures() JS (insert before dailyBrief)
feat_js = '''function showFeatures(){
  var old=$("featModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="featModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  var secs=[["\\U0001F4D6 LEARN",[["\\u2728 New Lesson","Any subject, taught like a great teacher"],["\\U0001F3EB School Mode","Smart-board class for any class & board"],["\\U0001F30D Language Hub","Spanish, French, Japanese + more, level-tracked"],["\\U0001F4DA World Library","Verified reference books built in"],["\\u270F\\uFE0F Doodle Board","Draw it — learn from your own doodle"]]],["\\U0001F9EA PRACTICE",[["\\U0001F9EA Exam Maker","Build a real exam from your own PDFs"],["\\U0001F4DD Mock Test Center","Full-screen timed tests, works offline"],["\\U0001FA79 Mistake Drill","Re-tests only what you got wrong"],["\\U0001F9E0 Spaced Review","Cards that come back before you forget"],["\\U0001F4C5 Daily Brief","Current affairs + a recall card"],["\\U0001F52E Score Predictor","Honest score forecast from your data"]]],["\\U0001F6E0\\uFE0F TOOLS",[["\\U0001F3A7 Podcast","Any material as a 2-voice audio lesson"],["\\U0001F5FA\\uFE0F Mind Map","Tap-to-fold topic tree"],["\\U0001F3AC Video Lesson","Slides with narration"],["\\U0001F4C8 Math Graphs","Plot any formula"],["\\U0001F3AF Test Paper","Branded 50-mark papers"],["\\U0001F399\\uFE0F Speaking Practice","Live talk, corrected as you go"],["\\u23F1\\uFE0F Focus Timer","Pomodoro with streaks"],["\\U0001F5C4\\uFE0F My Locker","Your PDFs, notes & cloud backup"]]]];
  var html='<h2>\\u2728 Everything inside AURISI</h2><div class="sub">One teacher, every tool — tap any feature from Home.</div>';
  secs.forEach(function(s){html+='<div class="feat-sec"><b>'+s[0]+'</b>';s[1].forEach(function(f){html+='<div class="feat-row"><span>'+f[0]+'</span><small>'+f[1]+'</small></div>'});html+='</div>'});
  m.innerHTML=html+'<button class="btn" style="width:100%;margin-top:6px" onclick="this.closest(\\'.modal-back\\').remove()">Let\\'s go \\U0001F680</button>';
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
