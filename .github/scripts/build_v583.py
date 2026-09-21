#!/usr/bin/env python3
# AURISI v58.3: Spaced Repetition hub. Transport-proof build (no literal backslashes).
# Fix: "Spaced Review not open" - old code refused to open with <2 due cards and
# showed a dead toast when the deck was empty. Now 1 due card opens the review,
# and nothing due / empty deck opens the Spaced Repetition hub modal.
# Base: AURISI.html v58.2. Idempotent: no-op if already v58.3.
import sys, io

BS = chr(92)

def Q(s):
    return s.replace('~B~', BS)

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.3"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.3 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.2"' in h, "base must be v58.2"

# Patch 1: srsStudyDue opens hub instead of dead toast; 1 card is enough
F1 = Q('if(pairs.length<2){toast("No cards due right now ~B~u2014 come back later ~B~u{1F9E0}");return}')
R1 = 'if(pairs.length<1){openSrsHub();return}'
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: insert hub functions before srsRec
F2 = 'function srsRec(front,r,back){'
HUB = Q(r'''function openSrsHub(){
  var old=document.getElementById("srsModalBack");if(old)old.remove();
  var d={};try{d=JSON.parse(localStorage.getItem(STORAGE+"cardsrs")||"{}")}catch(e){}
  var now=Date.now(),due=0,tot=0,next=0,up=[];
  for(var k in d){var c=d[k];if(!c||!c.f)continue;tot++;if(c.due&&c.due<=now)due++;else if(c.due&&c.due>now){up.push(c);if(!next||c.due<next)next=c.due}}
  up.sort(function(a,b){return a.due-b.due});
  var when=function(ts){var dd=Math.ceil((ts-now)/86400000);return dd<=0?"due now":(dd===1?"tomorrow":"in "+dd+" days")};
  var b=document.createElement("div");b.className="modal-back open";b.id="srsModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  var html='<h2>🧠 Spaced Repetition</h2><div class="sub">Your long-term memory deck ~B~u2014 SM-2 schedule, saved on this device.</div>';
  html+='<div class="feat-sec"><b>DECK</b><div class="feat-row"><span>'+due+'</span><small>cards due right now</small></div><div class="feat-row"><span>'+tot+'</span><small>total cards scheduled</small></div>'+(next?'<div class="feat-row"><span>'+when(next)+'</span><small>next scheduled review</small></div>':'')+'</div>';
  if(due>0)html+='<button class="btn" style="width:100%;margin-top:6px" onclick="srsModalClose();srsStudyDue()">Review '+due+' due card'+(due>1?'s':'')+' 🚀</button>';
  else html+='<button class="btn" style="width:100%;margin-top:6px" onclick="srsModalClose();srsMakeTopic()">Add flashcards ~B~u2795</button>';
  if(up.length){html+='<div class="feat-sec" style="margin-top:10px"><b>COMING UP</b>';up.slice(0,4).forEach(function(c){html+='<div class="feat-row"><span>'+escH(String(c.f).slice(0,38))+'</span><small>'+when(c.due)+'</small></div>'});html+='</div>'}
  html+='<div class="feat-sec" style="margin-top:10px"><b>ADD CARDS</b><div style="display:flex;gap:8px;margin-top:8px"><input id="srsTopicInput" placeholder="Topic ~B~u2014 e.g. Indian Polity" style="flex:1;min-width:0;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--text);font-size:14px"><button class="btn" style="margin:0" onclick="srsMakeTopic()">Go</button></div></div>';
  html+='<div class="feat-sec" style="margin-top:10px"><b>HOW IT WORKS</b><div class="feat-row"><span>Rate any flashcard</span><small>Hard comes back tomorrow ~B~u00b7 Good in a few days ~B~u00b7 Easy much later</small></div><div class="feat-row"><span>Build the deck</span><small>Make flashcards on any topic, then rate them</small></div></div>';
  m.innerHTML=html+'<button class="btn" style="width:100%;margin-top:6px" onclick="srsModalClose()">Close</button>';
  b.appendChild(m);document.body.appendChild(b);
}
function srsModalClose(){var x=document.getElementById("srsModalBack");if(x)x.remove()}
function srsMakeTopic(){
  var t="";try{t=(document.getElementById("srsTopicInput")||{}).value||""}catch(e){}
  var x=document.getElementById("srsModalBack");if(x)x.remove();
  switchView("chat");
  quick("Make 8 exam-focused flashcards on "+(t?t:"the most important topics from my recent study history")+". Output ONLY the token [[CARDS|front 1|back 1|front 2|back 2|front 3|back 3|...]] ~B~u2014 short punchy fronts, answer-only backs. I will rate each card Hard/Good/Easy so it enters my spaced-review schedule.");
}
''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, HUB + F2)

# Patch 3: version bump
F3 = 'var APP_VERSION="58.2"'
R3 = 'var APP_VERSION="58.3"'
assert h.count(F3) == 1
h = h.replace(F3, R3)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied srs hub patches, size: %d bytes" % len(h.encode("utf-8")))
