#!/usr/bin/env python3
# AURISI v60.6: Video Lesson polish.
# 1) Truncated/unmatched [[SLIDES|...]] tokens now still parse into the
#    smart-board card instead of dumping raw code into the chat.
# 2) Smart-board slide text renders math: KaTeX when available, plain
#    readable notation otherwise ($ stripped, \frac -> (a)/(b), greek
#    letters, sqrt -> v, exponents kept readable).
# 3) Narration spoken aloud uses the same readable math (no "backslash
#    frac" in the voice).
# Base: AURISI.html v60.5. Idempotent: no-op if already v60.6.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.6"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.6 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.5"' in h, "base must be v60.5"

# P1: plainMath helper before msgRow
F1 = "function msgRow(m,isLast){"
R1 = '''function plainMath(s){
  s=String(s||"").replace(/\\$\\$?/g,"");
  var gm={alpha:"\u03b1",beta:"\u03b2",gamma:"\u03b3",delta:"\u03b4",Delta:"\u0394",epsilon:"\u03b5",theta:"\u03b8",lambda:"\u03bb",mu:"\u03bc",pi:"\u03c0",rho:"\u03c1",sigma:"\u03c3",tau:"\u03c4",phi:"\u03c6",Phi:"\u03a6",omega:"\u03c9",Omega:"\u03a9",infty:"\u221e",times:"\u00d7",cdot:"\u00b7",approx:"\u2248",neq:"\u2260",leq:"\u2264",geq:"\u2265",to:"\u2192",sum:"\u03a3",int:"\u222b",pm:"\u00b1",ldots:"\u2026"};
  s=s.replace(/\\\\([A-Za-z]+)/g,function(m,k){return gm[k]!==undefined?gm[k]:m});
  s=s.replace(/\\\\frac\\s*\\{([^{}]*)\\}\\s*\\{([^{}]*)\\}/g,"($1)/($2)");
  s=s.replace(/\\\\sqrt\\s*\\{([^{}]*)\\}/g,"\u221a($1)");
  s=s.replace(/\\^\\{([^{}]+)\\}/g,"^($1)");
  s=s.replace(/_\\{([^{}]+)\\}/g,"_($1)");
  s=s.replace(/\\\\left|\\\\right|\\\\,|\\\\;|\\\\!/g,"");
  return s;
}
function msgRow(m,isLast){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: smart-board show() renders math (KaTeX or plain fallback)
F2 = '''st.textContent=(si+1)+". "+s.t;
          ul.innerHTML=s.b.map(b=>"<div><span>\u2022</span><span>"+escH(b)+"</span></div>").join("");'''
R2 = '''st.textContent=(si+1)+". "+(window.renderMathInElement?s.t:plainMath(s.t));
          if(window.renderMathInElement){ul.innerHTML=s.b.map(b=>"<div><span>\u2022</span><span>"+escH(b)+"</span></div>").join("");try{renderMathIn(ul)}catch(e){}}
          else{ul.innerHTML=s.b.map(b=>"<div><span>\u2022</span><span>"+escH(plainMath(b))+"</span></div>").join("");}'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: narration spoken as readable math
F3 = 'const txt=s.n||((s.t+". ")+s.b.join(". "));'
R3 = 'const txt=plainMath(s.n||((s.t+". ")+s.b.join(". ")));'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: truncated/unmatched [[SLIDES token still parses
F4 = 'if(slTok){txt=txt.replace(slTok[0],"").trim();slData=slTok[1].split("|").map(s=>s.trim()).filter(Boolean)}'
R4 = '''if(slTok){txt=txt.replace(slTok[0],"").trim();slData=slTok[1].split("|").map(s=>s.trim()).filter(Boolean)}
    if(!slTok){const slAny=txt.match(/\\[\\[\\s*SLIDES\\s*\\|/i);if(slAny){var _rest=txt.slice(slAny.index+slAny[0].length).replace(/\\]\\]\\s*$/,"");slData=_rest.split("|").map(s=>s.trim()).filter(Boolean);txt=txt.slice(0,slAny.index).trim()}}'''
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.5"'
R5 = 'var APP_VERSION="60.6"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Video Lesson polish, size: %d bytes" % len(h.encode("utf-8")))
