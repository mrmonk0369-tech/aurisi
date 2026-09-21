#!/usr/bin/env python3
# AURISI v60.14: REAL TEACHER MODE.
#  1) VOICE = BOARD: the teacher voice now reads the title and every bullet
#     EXACTLY as written on the smart board - jo likhta hai wahi bolta hai.
#  2) CHALK TRACKS VOICE: the pen-writing reveal follows the actual audio
#     position (AI_AUDIO.currentTime/duration) - writing finishes exactly
#     when the spoken sentence finishes.
#  3) COMPLETE CHAPTER: prompts now allow 25-40 slides for a whole-chapter
#     request => a real 10-30 minute class. Narration optional to save tokens.
#  4) NO UGLY INSTRUCTION BUBBLE: the Video Lesson auto-prompt is sent hidden.
#  5) TOKEN LEAK FIX: broken "]]|[[SLIDES|" fragments merge back into one lesson
#     instead of dumping raw text.
# Transport: backslashes as ~B~ (unwrapped by Q). Base: v60.13 (1199837).
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.14"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.14 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.13"' in h, "base must be v60.13"

# P1: writeTrack + stopSpeak cancel (slides box closure)
F1 = Q('''        let si=0,playing=false;
        const stopSpeak=()=>{playing=false;playB.textContent="~B~u25B6 Play lecture";try{speechSynthesis.cancel()}catch(e){};try{stopAiAudio()}catch(e){}};''')
R1 = Q('''        let si=0,playing=false;
        var WSTOP=null;
        function writeTrack(it){
          if(WSTOP){WSTOP();WSTOP=null}
          it.style.transition="none";it.style.clipPath="inset(0 100% 0 0)";
          var alive=true;WSTOP=function(){alive=false};
          var start=performance.now();
          var est=Math.max(1.6,Math.min(5,((it.textContent||"").length||24)*0.055));
          function tick(){
            if(!alive)return;
            var p=0,act=false;
            try{
              if(AI_AUDIO&&!AI_AUDIO.paused&&AI_AUDIO.currentTime>0&&isFinite(AI_AUDIO.duration)&&AI_AUDIO.duration>0.5){
                p=Math.min(1,AI_AUDIO.currentTime/AI_AUDIO.duration);act=true;
              }
            }catch(e){}
            var waited=(performance.now()-start)/1000;
            if(!act){if(waited>3.5)p=Math.min(1,(waited-3.5)/est);else p=0}
            if(p>=1){it.style.clipPath="none";WSTOP=null;return}
            it.style.clipPath="inset(0 "+(Math.round(100*(1-p)))+"% 0 0)";
            requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        }
        const stopSpeak=()=>{playing=false;playB.textContent="~B~u25B6 Play lecture";if(WSTOP){WSTOP();WSTOP=null}try{speechSynthesis.cancel()}catch(e){};try{stopAiAudio()}catch(e){}};''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: revealB uses writeTrack (real chalk following the voice)
F2 = Q('''          revealB=function(n){items.forEach(function(it,i){
            if(i<n){it.style.opacity="1";it.style.transform="none";it.style.clipPath="none"}
            else if(i===n){
              it.style.opacity="1";it.style.transform="scale(1.03)";
              var len=(it.textContent||"").length||24;
              var dur=Math.max(1.1,Math.min(3.2,len*0.05));
              try{
                it.style.transition="none";it.style.clipPath="inset(0 100% 0 0)";
                var f1=it;
                requestAnimationFrame(function(){requestAnimationFrame(function(){
                  f1.style.transition="clip-path "+dur+"s steps(26,end)";
                  f1.style.clipPath="inset(0 0 0 0)";
                })});
              }catch(e2){it.style.clipPath="none"}
            }
            else{it.style.opacity="0.15";it.style.transform="none";it.style.clipPath="inset(0 100% 0 0)"}
          })};''')
R2 = Q('''          revealB=function(n){items.forEach(function(it,i){
            if(i<n){it.style.opacity="1";it.style.transform="none";it.style.clipPath="none"}
            else if(i===n){
              it.style.opacity="1";it.style.transform="scale(1.03)";
              writeTrack(it);
            }
            else{it.style.opacity="0.15";it.style.transform="none";it.style.clipPath="inset(0 100% 0 0)"}
          })};''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: speakSlide - voice reads exactly the board (title + bullets)
F3 = Q('''          const s=slides[si];
          var narr=s.n||((s.t+". ")+s.b.join(". "));
          var sents=narr.match(/[^.!?]+[.!?]+/g)||[narr];
          var nb=Math.max(1,s.b.length);
          var chunks=[];
          for(var ci=0;ci<nb;ci++){
            var share=Math.ceil(sents.length/nb);
            var seg=sents.slice(ci*share,(ci+1)*share).join(" ");
            if(!seg)seg=s.b[ci]||s.t;
            if(ci===0&&!s.n)seg=s.t+". "+seg;
            chunks.push(seg);
          }''')
R3 = Q('''          const s=slides[si];
          var chunks=[s.t].concat(s.b);''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: speakChunk reveals bullet when its voice starts (idx 0 = title)
F4 = Q('''            if(idx>=chunks.length){goNext();return}
            if(revealB)revealB(idx);''')
R4 = Q('''            if(idx>=chunks.length){goNext();return}
            if(idx>0&&revealB)revealB(idx-1);''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: recordLesson chunks = title + bullets (video file matches board too)
F5 = Q('''            var jobs=[];
            slides.forEach(function(s){
              var narr=s.n||((s.t+". ")+s.b.join(". "));
              var sents=narr.match(/[^.!?]+[.!?]+/g)||[narr];
              var nb=Math.max(1,s.b.length);
              var cs=[];
              for(var ci=0;ci<nb;ci++){
                var share=Math.ceil(sents.length/nb);
                var seg=sents.slice(ci*share,(ci+1)*share).join(" ");
                if(!seg)seg=s.b[ci]||s.t;
                if(ci===0&&!s.n)seg=s.t+". "+seg;
                cs.push(cleanForSpeech(plainMath(seg)));
              }
              jobs.push(cs);
            });''')
R5 = Q('''            var jobs=[];
            slides.forEach(function(s){
              var cs=[cleanForSpeech(plainMath(s.t))];
              s.b.forEach(function(bb){cs.push(cleanForSpeech(plainMath(bb)))});
              jobs.push(cs);
            });''')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: SYS_PROMPT - complete chapter + voice reads the board
F6 = Q('''8-14 slides, 3-5 bullets each where every bullet is a COMPLETE TEACHING SENTENCE with real content (facts, formulas, examples, dates - never short labels), narration 3-6 spoken sentences that explain like a real teacher, :: separates title/bullets/narration, ; between bullets, never | inside content.''')
R6 = Q('''8-16 slides for one topic, 25-40 slides when the student asks to complete a whole chapter, full book or paper end-to-end (a real 10-30 minute class), 3-5 bullets each where every bullet is a COMPLETE TEACHING SENTENCE with real content (facts, formulas, examples, dates - never short labels) - the teacher voice reads the slide title and every bullet aloud EXACTLY as written, so bullets must flow as spoken teaching; narration is optional and may be omitted, :: separates title/bullets/narration, ; between bullets, never | inside content.''')
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

# P7: makeVideoLesson - hidden send, whole chapter, no narration bloat
F7 = Q('''function makeVideoLesson(){
  if(!state.pdfText){toast("Attach a PDF first");return}
  roomStart("~B~u{1F3AC}","Video Lesson");
  quick("Turn the attached PDF into a narrated video lesson on the smart board. Output ONLY one token: [[SLIDES|Slide title::bullet 1;bullet 2;bullet 3::narration sentences|Next slide title::bullets::narration|...]] ~B~u2014 8-14 slides, 3-5 bullets per slide where every bullet is a COMPLETE TEACHING SENTENCE with real content from the PDF, narration is 3-6 spoken sentences per slide explaining like a real teacher, :: separates title/bullets/narration, ; separates bullets, never the | character inside content:");
}''')
R7 = Q('''var HIDE_SEND=false;
function makeVideoLesson(){
  if(!state.pdfText){toast("Attach a PDF first");return}
  roomStart("~B~u{1F3AC}","Video Lesson");
  toast("~B~u{1F3AC} Making your video lesson~B~u2026");
  HIDE_SEND=true;
  try{quick("Turn the attached PDF into a complete video lesson on the smart board. Output ONLY one token: [[SLIDES|Slide title::bullet 1;bullet 2;bullet 3::narration|Next slide title::bullets::narration|...]] ~B~u2014 cover the WHOLE chapter: 15-35 slides, 3-5 bullets per slide where every bullet is a COMPLETE TEACHING SENTENCE with real content from the PDF; the teacher voice reads the title and every bullet aloud EXACTLY as written; narration optional, omit it to save space, :: separates title/bullets/narration, ; separates bullets, never the | character inside content:")}finally{HIDE_SEND=false}
}''')
assert h.count(F7) == 1, "P7 anchor not found"
h = h.replace(F7, R7)

# P8: send() marks hidden prompts
F8 = 'state.chatHistory.push({role:"user",parts});'
R8 = 'state.chatHistory.push({role:"user",parts,hid:HIDE_SEND===true});HIDE_SEND=false;'
assert h.count(F8) == 1, "P8 anchor not found"
h = h.replace(F8, R8)

# P9: renderChat skips hidden entries
F9 = 'state.chatHistory.forEach((m,i)=>{log.appendChild(msgRow(m,i===state.chatHistory.length-1))});'
R9 = 'state.chatHistory.forEach((m,i)=>{if(m.hid)return;log.appendChild(msgRow(m,i===state.chatHistory.length-1))});'
assert h.count(F9) == 1, "P9 anchor not found"
h = h.replace(F9, R9)

# P10: parser - merge broken "]]|[[SLIDES|" fragments into one lesson
F10 = Q('''    let slData=null;
    const slTok=txt.match(/~B~[~B~[~B~s*SLIDES~B~s*~B~|([~B~s~B~S]+?)~B~]~B~]/i);''')
R10 = Q('''    txt=txt.replace(/~B~]{2,}~B~s*~B~|?~B~s*~B~[~B~[~B~s*SLIDES~B~s*~B~|/gi,"|").replace(/~B~]{2,}~B~s*~B~|~B~s*~B~[~B~[/g,"|");
    let slData=null;
    const slTok=txt.match(/~B~[~B~[~B~s*SLIDES~B~s*~B~|([~B~s~B~S]+?)~B~]~B~]/i);''')
assert h.count(F10) == 1, "P10 anchor not found"
h = h.replace(F10, R10)

F11 = 'var APP_VERSION="60.13"'
R11 = 'var APP_VERSION="60.14"'
assert h.count(F11) == 1
h = h.replace(F11, R11)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Real Teacher, size: %d bytes" % len(h.encode("utf-8")))
