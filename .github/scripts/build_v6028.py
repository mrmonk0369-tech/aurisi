#!/usr/bin/env python3
# AURISI v60.28: VOICE + VIDEO LESSON DIAGRAMS.
#  1) SARVAM VOICES UPGRADED to Bulbul v3's production-best speakers
#     (docs: Tier-1 mani/priya/ishita/varun, plus ratan/roopa/shubh/
#     ashutosh/suhani/ritu/aditya/neha) with quality labels; podcast
#     pairing map updated; settings default fixed (was v2-only "anushka").
#  2) SVG DIAGRAMS IN VIDEO LESSONS: a slide may carry a 4th :: segment
#     with a raw <svg> diagram (sanitized via sanSvg). The Smart Board
#     shows it under the title, and the recorded video (recordLesson)
#     draws the diagram onto the canvas instead of bullets while the
#     voice reads title + narration. Prompt teaches the format.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.27 (1858397). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.28"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.28 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.27"' in h, "base must be v60.27"

# P1: Sarvam voice list -> Bulbul v3 production-best speakers
F1 = 'const SARVAM_VOICE_OPTIONS=[["shubh","Shubh \u00b7 Male"],["aditya","Aditya \u00b7 Male"],["rahul","Rahul \u00b7 Male"],["ritu","Ritu \u00b7 Female"],["priya","Priya \u00b7 Female"],["neha","Neha \u00b7 Female"],["pooja","Pooja \u00b7 Female"],["shruti","Shruti \u00b7 Female"]];'
R1 = 'const SARVAM_VOICE_OPTIONS=[["mani","Mani \u00b7 Male \u2605 best"],["priya","Priya \u00b7 Female \u2605 best"],["ishita","Ishita \u00b7 Female \u2605 best"],["varun","Varun \u00b7 Male \u2605 best"],["ratan","Ratan \u00b7 Male \u00b7 English"],["roopa","Roopa \u00b7 Female"],["shubh","Shubh \u00b7 Male \u00b7 Hindi"],["ashutosh","Ashutosh \u00b7 Male"],["suhani","Suhani \u00b7 Female"],["ritu","Ritu \u00b7 Female"],["aditya","Aditya \u00b7 Male"],["neha","Neha \u00b7 Female"]];'
assert h.count(F1) == 1, "P1a anchor not found"
h = h.replace(F1, R1)
F1c = 'const SARVAM_PAIR={shubh:"priya",aditya:"ritu",rahul:"neha",ritu:"aditya",priya:"shubh",neha:"rahul",pooja:"aditya",shruti:"shubh"};'
R1c = 'const SARVAM_PAIR={mani:"priya",priya:"varun",ishita:"ratan",varun:"ishita",ratan:"ishita",roopa:"shubh",shubh:"roopa",ashutosh:"suhani",suhani:"ashutosh",ritu:"ratan",aditya:"neha",neha:"aditya"};'
assert h.count(F1c) == 1, "P1c anchor not found"
h = h.replace(F1c, R1c)

# P1b: settings save default was v2-only voice
F1b = '$("sarvamVoiceSel").value||"anushka"'
R1b = '$("sarvamVoiceSel").value||"shubh"'
assert h.count(F1b) == 1, "P1b anchor not found"
h = h.replace(F1b, R1b)

# P2: slide parser - optional 4th :: segment = diagram svg
F2 = 'return{t:(pp[0]||"").trim(),b:(pp[1]||"").split(";").map(x=>x.trim()).filter(Boolean),n:(pp[2]||"").trim()}}).filter(s=>s.t);'
R2 = 'return{t:(pp[0]||"").trim(),b:(pp[1]||"").split(";").map(x=>x.trim()).filter(Boolean),n:(pp[2]||"").trim(),g:(typeof sanSvg==="function")?(sanSvg(pp[3]||"")||null):null}}).filter(s=>s.t);'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: diagram container in slide view
F3 = 'view.appendChild(eyebrow);view.appendChild(st);view.appendChild(ul);'
R3 = 'const dg=document.createElement("div");dg.className="slide-diagram";dg.style.display="none";view.appendChild(eyebrow);view.appendChild(st);view.appendChild(dg);view.appendChild(ul);'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: show() renders the diagram (sanitized) or hides it
F4 = 'st.textContent=(si+1)+". "+(window.renderMathInElement?s.t:plainMath(s.t));'
R4 = F4 + '\n          if(s.g){dg.style.display="block";dg.innerHTML=s.g}else{dg.style.display="none"}'
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: diagram CSS
F5 = '.splash-foot{font-size:10.5px}'
R5 = F5 + "\n" + Q('.slide-diagram{max-width:100%;margin:6px auto 2px;text-align:center}\n.slide-diagram svg{max-width:100%;height:auto;max-height:34vh}')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: video voice reads title + narration for diagram slides
F6 = 's.b.forEach(function(bb){cs.push(cleanForSpeech(plainMath(bb)))});\n              jobs.push(cs);'
R6 = 's.b.forEach(function(bb){cs.push(cleanForSpeech(plainMath(bb)))});\n              if(s.g&&s.n)cs.push(cleanForSpeech(plainMath(s.n)).slice(0,600));\n              jobs.push(cs);'
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

# P7: preload diagram images before recording
F7 = 'try{uploadDone(true)}catch(e3c){}\n            var cv=document.createElement("canvas");'
R7 = Q('try{uploadDone(true)}catch(e3c){}\n            var svgs=[];\n            for(var si2=0;si2<slides.length;si2++){\n              var imA=null;\n              if(slides[si2].g){\n                imA=await new Promise(function(res2){var ii=new Image();ii.onload=function(){res2(ii)};ii.onerror=function(){res2(null)};ii.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(slides[si2].g.replace(/<svg/i,\'<svg width="480" height="320"\'))});\n              }\n              svgs.push(imA);\n            }\n            var cv=document.createElement("canvas");')
assert h.count(F7) == 1, "P7 anchor not found"
h = h.replace(F7, R7)

# P8: frame() draws the diagram instead of bullets for diagram slides
F8 = 'var by=Math.min(ty+40,200);\n              for(var bi=0;bi<sl2.b.length;bi++){'
R8 = Q('var by=Math.min(ty+40,200);\n              if(sl2.g&&svgs[cur.sl]){\n                var im3=svgs[cur.sl];\n                var zoneY=Math.min(by+16,170),zoneH=660-zoneY;\n                var sc2=Math.min(1040/im3.width,zoneH/im3.height,1.5);\n                var iw3=im3.width*sc2,ih3=im3.height*sc2;\n                cx.drawImage(im3,(1280-iw3)/2,zoneY+(zoneH-ih3)/2,iw3,ih3);\n              }else for(var bi=0;bi<sl2.b.length;bi++){')
assert h.count(F8) == 1, "P8 anchor not found"
h = h.replace(F8, R8)

# P9: prompt teaches diagram slides
F9 = ':: separates title/bullets/narration, ; between bullets, never | inside content. "'
R9 = ':: separates title/bullets/narration, ; between bullets, never | inside content. A slide may end with a 4th :: segment holding a raw <svg>...</svg> diagram (same drawing rules as the DIAGRAMS token, viewBox 0 0 480 320, never any | character; use max 1-2 diagram slides per lesson and only for visual topics); for a diagram slide its narration must describe the diagram aloud. "'
assert h.count(F9) == 1, "P9 anchor not found"
h = h.replace(F9, R9)

F10 = 'var APP_VERSION="60.27"'
R10 = 'var APP_VERSION="60.28"'
assert h.count(F10) == 1
h = h.replace(F10, R10)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Voice+Video Diagrams, size: %d bytes" % len(h.encode("utf-8")))
