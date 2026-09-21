#!/usr/bin/env python3
# AURISI v60.7: Real Video Lesson.
# 1) Slides now teach: prompts demand 8-14 slides, 3-5 COMPLETE teaching
#    sentences per slide (facts, formulas, examples - never short labels)
#    and 3-6 sentences of narration that explains like a real teacher.
# 2) Video feel: during playback each bullet is revealed and highlighted
#    in sync with its narration chunk (bullet-by-bullet karaoke reveal).
# 3) Robotic browser voice REMOVED from video lessons. Voice is API-only:
#    Sarvam Bulbul if a Sarvam key is set, else Gemini TTS which now also
#    works with the owner's House AI key. If no key at all, the lesson
#    still plays silently with timed slide progression.
# Transport note: backslashes are written as ~B~ and unwrapped by Q();
# newlines inside anchors are REAL newlines in triple-quoted strings.
# Base: AURISI.html v60.6. Idempotent: no-op if already v60.7.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.7"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.7 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.6"' in h, "base must be v60.6"

# P1: SYS prompt - richer slides
F1 = Q(']] ~B~u2014 6-12 slides, 2-4 bullets each, narration 2-3 spoken sentences, :: separates title/bullets/narration, ; between bullets, never | inside content.')
R1 = Q(']] ~B~u2014 8-14 slides, 3-5 bullets each where every bullet is a COMPLETE TEACHING SENTENCE with real content (facts, formulas, examples, dates - never short labels), narration 3-6 spoken sentences that explain like a real teacher, :: separates title/bullets/narration, ; between bullets, never | inside content.')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: PDF prompt - richer slides
F2 = Q('~B~u2014 6-12 slides, 2-4 bullets per slide, narration is 2-3 spoken sentences per slide, :: separates title/bullets/narration, ; separates bullets, never the | character inside content:')
R2 = Q('~B~u2014 8-14 slides, 3-5 bullets per slide where every bullet is a COMPLETE TEACHING SENTENCE with real content from the PDF, narration is 3-6 spoken sentences per slide explaining like a real teacher, :: separates title/bullets/narration, ; separates bullets, never the | character inside content:')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: aiSpeak also works with the house key
F3 = Q('''async function aiSpeak(text,voice,onend,quiet){
  text=cleanForSpeech(text);
  var key=(localStorage.getItem(STORAGE+"geminiKey")||"").trim();''')
R3 = Q('''async function aiSpeak(text,voice,onend,quiet){
  text=cleanForSpeech(text);
  var key=(localStorage.getItem(STORAGE+"geminiKey")||(cfgGet("ai_house_key")||"")).trim();''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: show() with bullet-reveal support
F4 = Q('''const show=()=>{
          si=Math.max(0,Math.min(slides.length-1,si));
          const s=slides[si];
          st.textContent=(si+1)+". "+(window.renderMathInElement?s.t:plainMath(s.t));
          if(window.renderMathInElement){ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(b)+"</span></div>").join("");try{renderMathIn(ul)}catch(e){}}
          else{ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(plainMath(b))+"</span></div>").join("");}
          dots.querySelectorAll(".slide-dot").forEach((d,i)=>d.classList.toggle("on",i===si));
        };''')
R4 = Q('''let revealB=null;
        const show=()=>{
          si=Math.max(0,Math.min(slides.length-1,si));
          const s=slides[si];
          st.textContent=(si+1)+". "+(window.renderMathInElement?s.t:plainMath(s.t));
          if(window.renderMathInElement){ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(b)+"</span></div>").join("");try{renderMathIn(ul)}catch(e){}}
          else{ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(plainMath(b))+"</span></div>").join("");}
          var items=[].slice.call(ul.children);
          items.forEach(function(it){it.style.transition="opacity .35s,transform .35s";it.style.opacity="1";it.style.transform="none"});
          revealB=function(n){items.forEach(function(it,i){it.style.opacity=i<=n?"1":"0.15";it.style.transform=(i===n)?"scale(1.04)":"none"})};
          dots.querySelectorAll(".slide-dot").forEach((d,i)=>d.classList.toggle("on",i===si));
        };''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: speakSlide - chunked narration, bullet reveal, API-only voice
F5 = Q('''const speakSlide=()=>{
          if(!playing)return;
          if(si>=slides.length){stopSpeak();toast("Lecture finished ~B~u2705");return}
          show();
          const s=slides[si];
          const txt=plainMath(s.n||((s.t+". ")+s.b.join(". ")));
          const goNext=()=>{if(!playing)return;si++;setTimeout(speakSlide,420)};
          if(sarvamKeySet()){sarvamSpeak(txt,getSarvamVoice(),function(ok){if(ok)goNext();else speakBrowser(txt,goNext)},true)}
          else if(aiVoicesOn()){aiSpeak(txt,getAiVoice(),function(ok){if(ok)goNext();else speakBrowser(txt,goNext)},true)}
          else speakBrowser(txt,goNext);
        };''')
R5 = Q('''const speakSlide=()=>{
          if(!playing)return;
          if(si>=slides.length){stopSpeak();toast("Lecture finished ~B~u2705");return}
          show();
          const s=slides[si];
          var narr=s.n||((s.t+". ")+s.b.join(". ")));
          var sents=narr.match(/[^.!?]+[.!?]+/g)||[narr];
          var nb=Math.max(1,s.b.length);
          var chunks=[];
          for(var ci=0;ci<nb;ci++){
            var share=Math.ceil(sents.length/nb);
            var seg=sents.slice(ci*share,(ci+1)*share).join(" ");
            if(!seg)seg=s.b[ci]||s.t;
            if(ci===0&&!s.n)seg=s.t+". "+seg;
            chunks.push(seg);
          }
          const goNext=()=>{if(!playing)return;si++;setTimeout(speakSlide,420)};
          const timed=(txt,after)=>{var ms=Math.max(1800,Math.min(9000,String(txt).split(/~B~s+/).length*420));setTimeout(after,ms)};
          const speakChunk=(idx)=>{
            if(!playing)return;
            if(idx>=chunks.length){goNext();return}
            if(revealB)revealB(idx);
            const c=plainMath(chunks[idx]);
            const next=()=>speakChunk(idx+1);
            if(sarvamKeySet()){sarvamSpeak(c,getSarvamVoice(),function(ok){if(ok)next();else timed(c,next)},true)}
            else{aiSpeak(c,getAiVoice(),function(ok){if(ok)next();else timed(c,next)},true)}
          };
          speakChunk(0);
        };''')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: play button always allowed (silent timed playback if no voice)
F6 = Q('''if(playing){stopSpeak();return}
          if(!window.speechSynthesis&&!aiVoicesOn())return;
          playing=true;''')
R6 = Q('''if(playing){stopSpeak();return}
          playing=true;''')
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.6"'
R7 = 'var APP_VERSION="60.7"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Real Video Lesson, size: %d bytes" % len(h.encode("utf-8")))
