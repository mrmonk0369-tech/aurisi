#!/usr/bin/env python3
# AURISI v60.17: REAL VOICE.
#  1) BOOK READER UPGRADE: the library reader now speaks with the natural
#     AI voice (Sarvam if key -> Gemini house-key voice -> best browser
#     voice). Students hear the same warm teacher voice as video lessons.
#  2) BEST-VOICE PICKER: every remaining browser-speech path (quiz viva,
#     quiz feedback, chat read-aloud, talk mode, slides fallback) now picks
#     the device's BEST voice (Google/Neural/Premium/Enhanced/Microsoft,
#     language-matched) instead of the first match - the robotic default is
#     gone. Free, offline-capable, no API needed.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.16 (1850504). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.17"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.17 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.16"' in h, "base must be v60.16"

# P1: bestVoice global
F1 = 'function msgRow(m,isLast){'
R1 = Q('''function bestVoice(lang){
  try{
    var vs=speechSynthesis.getVoices()||[];
    if(!vs.length)return null;
    var lp=String(lang||"en-IN").toLowerCase();
    var pref=lp.slice(0,2);
    var best=null,bs=-1;
    for(var i=0;i<vs.length;i++){
      var v=vs[i];var n=((v.name||"")+" "+(v.lang||"")).toLowerCase();var s=0;
      if((v.lang||"").toLowerCase().indexOf(lp)===0)s+=40;
      else if((v.lang||"").toLowerCase().indexOf(pref)===0)s+=18;
      if((v.name||"").indexOf("google")>-1)s+=25;
      if(n.indexOf("neural")>-1||n.indexOf("natural")>-1)s+=20;
      if(n.indexOf("premium")>-1||n.indexOf("enhanced")>-1)s+=14;
      if((v.name||"").indexOf("microsoft")>-1)s+=8;
      if(v.localService===false)s+=6;
      if(s>bs){bs=s;best=v}
    }
    return best;
  }catch(e){return null}
}
function msgRow(m,isLast){''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: rdSpeak - natural AI voice first, best browser voice fallback
F2 = Q('''  if(READER.speaking){try{speechSynthesis.cancel()}catch(e){}READER.speaking=false;rdSpeakUI(false);return}''')
R2 = Q('''  if(READER.speaking){try{stopAiAudio()}catch(e){}try{speechSynthesis.cancel()}catch(e){}READER.speaking=false;rdSpeakUI(false);return}''')
assert h.count(F2) == 1, "P2a anchor not found"
h = h.replace(F2, R2)

F3 = Q('''    var u=new SpeechSynthesisUtterance(pa.t);u.rate=.98;u.lang=document.documentElement.lang||"en-IN";
    u.onend=function(){if(!READER.speaking)return;READER.sel=idx;rdSavePos();idx++;setTimeout(speakNext,120)};
    u.onerror=function(){READER.speaking=false;rdSpeakUI(false)};
    try{speechSynthesis.speak(u)}catch(e){READER.speaking=false;rdSpeakUI(false)}
  }''')
R3 = Q('''    var advanced=function(){READER.sel=idx;rdSavePos();idx++;setTimeout(speakNext,140)};
    var browserPara=function(){
      var u=new SpeechSynthesisUtterance(pa.t);u.rate=.98;u.lang=document.documentElement.lang||"en-IN";
      var bvp=bestVoice(u.lang);if(bvp)u.voice=bvp;
      u.onend=function(){if(!READER.speaking)return;advanced()};
      u.onerror=function(){READER.speaking=false;rdSpeakUI(false)};
      try{speechSynthesis.speak(u)}catch(e){READER.speaking=false;rdSpeakUI(false)}
    };
    var afterAi=function(ok){if(!READER.speaking)return;if(ok)advanced();else browserPara()};
    var went=false;
    try{
      if(sarvamKeySet()){went=true;sarvamSpeak(pa.t,getSarvamVoice(),afterAi,true)}
      else{
        var vkey=(localStorage.getItem(STORAGE+"geminiKey")||(cfgGet("ai_house_key")||"")).trim();
        if(vkey){went=true;aiSpeak(pa.t,getAiVoice(),afterAi,true)}
      }
    }catch(e9r){}
    if(!went)browserPara();
  }''')
assert h.count(F3) == 1, "P2b anchor not found"
h = h.replace(F3, R3)

# P3: slides browserLine - best voice instead of rotating pool
F4 = Q('''            if(usePool.length>1&&usePool[i%usePool.length])u.voice=usePool[i%usePool.length];''')
R4 = Q('''            var bvl=bestVoice(u.lang);if(bvl)u.voice=bvl;''')
assert h.count(F4) == 1, "P3a anchor not found"
h = h.replace(F4, R4)

# P4: slides speakBrowser - best voice instead of pool[0]
F5 = Q('''              if(pool[0])u.voice=pool[0];''')
R5 = Q('''              var bvs=bestVoice(u.lang);if(bvs)u.voice=bvs;''')
assert h.count(F5) == 1, "P3b anchor not found"
h = h.replace(F5, R5)

# P5: quiz viva question voice
F6 = Q('''    u.lang=speechLangFor(getUiLang());u.rate=0.95;
    u.onend=()=>{setTimeout(()=>listenQuizAnswer(box,qData,opts,0),400)};''')
R6 = Q('''    u.lang=speechLangFor(getUiLang());u.rate=0.95;
    var bvq=bestVoice(u.lang);if(bvq)u.voice=bvq;
    u.onend=()=>{setTimeout(()=>listenQuizAnswer(box,qData,opts,0),400)};''')
assert h.count(F6) == 1, "P4a anchor not found"
h = h.replace(F6, R6)

# P6: quiz feedback voice
F7 = Q('''      u2.lang=speechLangFor(getUiLang());
      u2.onend=()=>{setTimeout(()=>{const nb=box.querySelector(".quiz-next");if(nb&&box.isConnected)nb.click()},900)};''')
R7 = Q('''      u2.lang=speechLangFor(getUiLang());
      var bv2q=bestVoice(u2.lang);if(bv2q)u2.voice=bv2q;
      u2.onend=()=>{setTimeout(()=>{const nb=box.querySelector(".quiz-next");if(nb&&box.isConnected)nb.click()},900)};''')
assert h.count(F7) == 1, "P4b anchor not found"
h = h.replace(F7, R7)

# P7: chat read-aloud / podcast fallback voice
F8 = Q('''      var u=new SpeechSynthesisUtterance(sents[k].t);
      u.lang=speechLangFor(getUiLang());u.rate=1;''')
R8 = Q('''      var u=new SpeechSynthesisUtterance(sents[k].t);
      u.lang=speechLangFor(getUiLang());u.rate=1;
      var bvc=bestVoice(u.lang);if(bvc)u.voice=bvc;''')
assert h.count(F8) == 1, "P5a anchor not found"
h = h.replace(F8, R8)

# P8: talk mode voice
F9 = Q('''    const vs=window.speechSynthesis.getVoices();
    const v=vs.find(x=>x.lang&&x.lang.indexOf((TALK_LANGS[talkLang]||"en").split("-")[0])===0);
    if(v)u.voice=v;''')
R9 = Q('''    const v=bestVoice(u.lang);
    if(v)u.voice=v;''')
assert h.count(F9) == 1, "P6 anchor not found"
h = h.replace(F9, R9)

F10 = 'var APP_VERSION="60.16"'
R10 = 'var APP_VERSION="60.17"'
assert h.count(F10) == 1
h = h.replace(F10, R10)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Real Voice, size: %d bytes" % len(h.encode("utf-8")))
