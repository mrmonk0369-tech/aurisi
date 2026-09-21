#!/usr/bin/env python3
# AURISI v60.6: Video Lesson polish.
# 1) Truncated/unmatched [[SLIDES|...]] tokens now still parse into the
#    smart-board card instead of dumping raw code into the chat.
# 2) Smart-board slide text renders math: KaTeX when available, plain
#    readable notation otherwise ($ stripped, frac -> (a)/(b), greek
#    letters, sqrt symbol, readable exponents).
# 3) Narration spoken aloud uses the same readable math.
# Transport note: every backslash is written as ~B~ and unwrapped by Q(),
# so this file contains no literal backslash characters at all.
# Base: AURISI.html v60.5. Idempotent: no-op if already v60.6.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

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
R1 = Q(
'function plainMath(s){\n'
'  s=String(s||"").replace(/~B~$~B~$?/g,"");\n'
'  var gm={alpha:"α",beta:"β",gamma:"γ",delta:"δ",Delta:"Δ",epsilon:"ε",theta:"θ",lambda:"λ",mu:"μ",pi:"π",rho:"ρ",sigma:"σ",tau:"τ",phi:"φ",Phi:"Φ",omega:"ω",Omega:"Ω",infty:"∞",times:"×",cdot:"·",approx:"≈",neq:"≠",leq:"≤",geq:"≥",to:"→",sum:"Σ",int:"∫",pm:"±",ldots:"…"};\n'
'  s=s.replace(/~B~~B~([A-Za-z]+)/g,function(m,k){return gm[k]!==undefined?gm[k]:m});\n'
'  s=s.replace(/~B~~B~frac~B~s*~B~{([^{}]*)}~B~s*~B~{([^{}]*)}/g,"($1)/($2)");\n'
'  s=s.replace(/~B~~B~sqrt~B~s*~B~{([^{}]*)}/g,"√($1)");\n'
'  s=s.replace(/~B~^{([^{}]+)}/g,"^($1)");\n'
'  s=s.replace(/_{([^{}]+)}/g,"_($1)");\n'
'  s=s.replace(/~B~~B~left|~B~~B~right|~B~~B~,|~B~~B~;|~B~~B~!/g,"");\n'
'  return s;\n'
'}\n'
'function msgRow(m,isLast){')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: smart-board show() renders math (KaTeX or plain fallback)
F2 = Q(
'st.textContent=(si+1)+". "+s.t;\n'
'          ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(b)+"</span></div>").join("");')
R2 = Q(
'st.textContent=(si+1)+". "+(window.renderMathInElement?s.t:plainMath(s.t));\n'
'          if(window.renderMathInElement){ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(b)+"</span></div>").join("");try{renderMathIn(ul)}catch(e){}}\n'
'          else{ul.innerHTML=s.b.map(b=>"<div><span>~B~u2022</span><span>"+escH(plainMath(b))+"</span></div>").join("");}')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: narration spoken as readable math
F3 = 'const txt=s.n||((s.t+". ")+s.b.join(". "));'
R3 = 'const txt=plainMath(s.n||((s.t+". ")+s.b.join(". ")));'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: truncated/unmatched [[SLIDES token still parses
F4 = 'if(slTok){txt=txt.replace(slTok[0],"").trim();slData=slTok[1].split("|").map(s=>s.trim()).filter(Boolean)}'
R4 = Q(
'if(slTok){txt=txt.replace(slTok[0],"").trim();slData=slTok[1].split("|").map(s=>s.trim()).filter(Boolean)}\n'
'    if(!slTok){const slAny=txt.match(/~B~[~B~[~B~s*SLIDES~B~s*~B~|/i);if(slAny){var _rest=txt.slice(slAny.index+slAny[0].length).replace(/~B~]~B~]~B~s*$/,"");slData=_rest.split("|").map(s=>s.trim()).filter(Boolean);txt=txt.slice(0,slAny.index).trim()}}')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

F5 = 'var APP_VERSION="60.5"'
R5 = 'var APP_VERSION="60.6"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Video Lesson polish, size: %d bytes" % len(h.encode("utf-8")))
