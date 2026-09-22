#!/usr/bin/env python3
# AURISI v60.15: VISUAL LEARNING - AI-drawn SVG diagrams for ANY subject.
#  New token: [[SVG|short title|<svg ...>...</svg>]]
#   - The AI draws labeled educational diagrams (geometry, anatomy, circuits,
#     process flows, maps, timelines, forces) inline in any chat answer.
#   - Regex-sanitized (no script/foreignObject/image/use/href/on*=),
#     size-capped at 16000 chars, viewBox enforced, width/height stripped
#     so it renders responsive inside the chat card.
#   - Rendered in a bordered card with a caption, like IMAGE/DOODLE cards.
#  SYS_PROMPT now tells the model WHEN to draw (any visual concept) and HOW.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.14 (1200224). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.15"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.15 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.14"' in h, "base must be v60.14"

# P1: sanitizer (global, before msgRow)
F1 = 'function msgRow(m,isLast){'
R1 = Q('''function sanSvg(code){
  code=String(code||"").trim().slice(0,16000);
  if(!/^<svg[~B~s>]/i.test(code)||!/<~B~/svg~B~s*>$/i.test(code))return "";
  if(/<script|<foreignObject|<iframe|<image|<use[~B~s>]/i.test(code))return "";
  if(/javascript:/i.test(code))return "";
  if(/~B~son[a-z]+~B~s*=/i.test(code))return "";
  if(/~B~shref|xlink:href/i.test(code))return "";
  return code;
}
function msgRow(m,isLast){''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: parser (before chData parse)
F2 = '    let chData=null;'
R2 = Q('''    let svData=null;
    const svRe=/~B~[~B~[~B~s*SVG~B~s*~B~|([^|~B~]]+)~B~|([~B~s~B~S]+?)~B~]~B~]/gi;
    const svAll=[];let svm;
    while((svm=svRe.exec(txt)))svAll.push([svm[1].trim(),svm[2].trim(),svm[0]]);
    if(svAll.length){
      svData=svAll.map(function(d){
        return [d[0],d[1],"svl"+(msgRow._sv=(msgRow._sv||0)+1),d[2]];
      });
      svData.forEach(function(d){txt=txt.replace(d[3],'<div data-svslot="'+d[2]+'"></div>')});
    }
    let chData=null;''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: renderer (before chart render block)
F3 = 'if(chData){'
R3 = Q('''if(svData){
      svData.forEach(function(sv2){
        const vbox=document.createElement("div");vbox.className="svg-card";
        const vwrap=document.createElement("div");vwrap.className="svg-wrap";
        var code=sanSvg(sv2[1]);
        if(code){
          vwrap.innerHTML=code;
          try{
            var svEl=vwrap.querySelector("svg");
            if(svEl){
              if(!svEl.getAttribute("viewBox"))svEl.setAttribute("viewBox","0 0 480 320");
              svEl.removeAttribute("width");svEl.removeAttribute("height");
            }
          }catch(e0a){}
        }
        else vwrap.innerHTML='<div style="padding:14px;font-size:12.5px;color:var(--muted)">Diagram unavailable</div>';
        const vcap=document.createElement("div");vcap.className="svg-cap";vcap.textContent="~B~u{1F4D0} "+sv2[0];
        vbox.appendChild(vwrap);vbox.appendChild(vcap);
        var svlot=null;
        try{var ssel=md.querySelectorAll("[data-svslot]");for(var si2=0;si2<ssel.length;si2++){if(ssel[si2].getAttribute("data-svslot")===sv2[2]){svlot=ssel[si2];break}}}catch(e9b){}
        if(svlot)svlot.appendChild(vbox);else md.appendChild(vbox);
      });
    }
if(chData){''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: CSS
F4 = '.img-card{border:1px solid var(--line);border-radius:16px;margin:14px 0;max-width:480px;overflow:hidden;background:var(--surface)}'
R4 = Q('''.img-card{border:1px solid var(--line);border-radius:16px;margin:14px 0;max-width:480px;overflow:hidden;background:var(--surface)}
.svg-card{border:1px solid var(--line);border-radius:16px;margin:14px 0;max-width:480px;overflow:hidden;background:var(--surface)}
.svg-wrap{padding:12px}
.svg-wrap svg{width:100%;height:auto;display:block}
.svg-cap{padding:8px 14px 10px;font-size:12px;color:var(--muted);border-top:1px solid var(--line)}''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: SYS_PROMPT - teach the model to draw
F5 = Q('''never | inside content. "+
  "MOLECULES 3D: when the learner asks to SEE a molecule''')
R5 = Q('''never | inside content. "+
  "DIAGRAMS: whenever a concept is better understood visually (geometry shapes, labeled anatomy, circuits, process flows, timelines, maps, forces, machinery, set theory), output a token [[SVG|short title|<svg viewBox=~B~"0 0 480 320~B~" xmlns=~B~"http://www.w3.org/2000/svg~B~">...</svg>]] containing a clean labeled educational diagram: simple shapes, strokes, arrows and <text> labels for every part, 2-3 colors max, readable at 480x320, no scripts, no external images, never the | character in the title - then explain the diagram in the same answer. "+
  "MOLECULES 3D: when the learner asks to SEE a molecule''')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

F6 = 'var APP_VERSION="60.14"'
R6 = 'var APP_VERSION="60.15"'
assert h.count(F6) == 1
h = h.replace(F6, R6)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Visual Learning, size: %d bytes" % len(h.encode("utf-8")))
