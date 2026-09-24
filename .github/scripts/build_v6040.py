#!/usr/bin/env python3
# AURISI v60.40: VOCABULARY LIGHT
#  Owner request: "apne aap vocabulary lighter ho jaye - kisi ko English
#  words ka meaning baar baar puchhna na pade."
#  Two parts:
#  P1 PROMPT: AUTO-GLOSS - first time a genuinely difficult English word
#     appears, AI immediately adds its short meaning in the student's own
#     language in round brackets (max 3 per reply, no repeats, no asking).
#  P2 JS+CSS: TAP-TO-MEANING - tap any English word inside an AI message
#     -> small popup appears with the word; a silent one-line AI lookup
#     (separate API call, chat untouched) fills in the meaning; popup has
#     an in-session cache; closes on any tap/scroll.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.39 (1870070). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.40"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.40 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.39"' in h, "base must be v60.39"

# P1: prompt rule - auto-gloss hard words
F1 = 'let the picture do the talking. "+"You are Aurisi'
R1 = 'let the picture do the talking. VOCABULARY LIGHT: automatically lighten vocabulary - the first time a genuinely difficult English word appears in a reply, immediately follow it with its short, simple meaning in the student\'s own language in round brackets, like: photosynthesis (roshni se khana banane ki prakriya). Maximum 3 glosses per reply, never the same word twice in one conversation, never gloss easy everyday words, and never ask whether they want meanings - just quietly include them. "+"You are Aurisi'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2a: CSS - popup styles (insert after .msg-row base rule)
F2 = '.msg-row{display:flex;gap:12px;margin:22px 0;animation:fadeUp .25s ease}'
R2 = '.msg-row{display:flex;gap:12px;margin:22px 0;animation:fadeUp .25s ease}\n.wpop{position:fixed;z-index:9998;max-width:300px;background:var(--surface);color:var(--text);border:1px solid var(--line);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25);padding:10px 13px;font-size:13.5px;line-height:1.5;animation:fadeUp .18s ease}\n.wpop .wp-w{font-weight:800;font-size:14px;color:var(--accent);text-transform:lowercase}\n.wpop .wp-m{margin-top:3px}\n.wpop .wp-x{display:block;margin-top:6px;font-size:10.5px;opacity:.55}'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P2b: JS - tap-to-meaning (insert before updateTopTitle)
F3 = 'function updateTopTitle(){'
R3 = '''/* ===== TAP-TO-MEANING (vocabulary light) ===== */
var WPOP={el:null,cur:"",cache:{}};
function wpopKill(){if(WPOP.el){try{WPOP.el.remove()}catch(e){}}WPOP.el=null;WPOP.cur=""}
function wordFromPoint(x,y){
  var node=null,off=0;
  try{
    if(document.caretRangeFromPoint){var rr=document.caretRangeFromPoint(x,y);node=rr.startContainer;off=rr.startOffset}
    else if(document.caretPositionFromPoint){var pp=document.caretPositionFromPoint(x,y);node=pp.offsetNode;off=pp.offset}
  }catch(e){return null}
  if(!node||node.nodeType!==3)return null;
  var t=String(node.nodeValue||"");
  var a=off,b=off;
  var W=/[A-Za-z'-]/;
  while(a>0&&W.test(t[a-1]))a--;
  while(b<t.length&&W.test(t[b]))b++;
  if(b-a<3||b-a>28)return null;
  return t.slice(a,b);
}
async function wordMean(w){
  var k=w.toLowerCase();
  if(WPOP.cache[k]!==undefined)return WPOP.cache[k];
  var key="";
  try{key=(localStorage.getItem(STORAGE+"geminiKey")||(cfgGet("ai_house_key")||"")).trim()}catch(e){}
  if(!key)return null;
  var models=[localStorage.getItem(STORAGE+"workingModel")||"gemini-2.5-flash-lite","gemini-2.5-flash-lite","gemini-flash-latest"];
  var seen={};
  for(var i=0;i<models.length;i++){
    var mo=models[i];if(!mo||seen[mo])continue;seen[mo]=1;
    try{
      var r=await fetch("https://generativelanguage.googleapis.com/v1beta/models/"+mo+":generateContent",{
        method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":key},
        body:JSON.stringify({contents:[{role:"user",parts:[{text:'Give the meaning of the English word "'+w+'" for an Indian school or college student. Reply with ONE short line only: a simple, easy meaning in English, then the same meaning in Hindi (Hinglish is fine). No examples, no extra words.'}]}],generationConfig:{temperature:0.2,maxOutputTokens:120}})
      });
      var d=await r.json();
      var txt="";
      try{txt=((d.candidates||[])[0].content.parts||[]).map(function(p){return p.text||""}).join("").trim()}catch(e2){}
      if(txt){WPOP.cache[k]=txt;return txt}
    }catch(e){}
  }
  WPOP.cache[k]=null;return null;
}
function wpopShow(x,y,w){
  wpopKill();
  var el=document.createElement("div");el.className="wpop";
  var wd=document.createElement("div");wd.className="wp-w";wd.textContent=w;
  var mm=document.createElement("div");mm.className="wp-m";mm.textContent="\U0001F50E looking up\U00002026";
  var xx=document.createElement("span");xx.className="wp-x";xx.textContent="tap anywhere to close";
  el.appendChild(wd);el.appendChild(mm);el.appendChild(xx);
  document.body.appendChild(el);WPOP.el=el;WPOP.cur=w.toLowerCase();
  var vw=360,vh=640;
  try{vw=window.innerWidth||document.documentElement.clientWidth||360;vh=window.innerHeight||document.documentElement.clientHeight||640}catch(e){}
  try{el.style.left=Math.max(10,Math.min(x-20,vw-320))+"px"}catch(e){el.style.left="10px"}
  try{el.style.top=Math.max(10,Math.min(y+18,vh-150))+"px"}catch(e){el.style.top="40px"}
  wordMean(w).then(function(m){
    if(!WPOP.el||WPOP.cur!==w.toLowerCase())return;
    mm.textContent=m||"meaning not found - ask in chat";
  });
}
document.addEventListener("click",function(e){
  if(WPOP.el)wpopKill();
  var t=e.target;
  if(!t||!t.closest)return;
  if(!t.closest(".ai-md"))return;
  if(t.closest("button,a,img,svg,pre,code,.katex,.quiz-box,.opt-btn,.wpop,.ai-code-block"))return;
  var w=wordFromPoint(e.clientX,e.clientY);
  if(w&&/^[A-Za-z][A-Za-z'-]{2,27}$/.test(w))wpopShow(e.clientX,e.clientY,w);
});
document.addEventListener("scroll",wpopKill,true);
function updateTopTitle(){'''
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.39"'
R4 = 'var APP_VERSION="60.40"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied vocabulary light, size: %d bytes" % len(h.encode("utf-8")))
