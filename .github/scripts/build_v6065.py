#!/usr/bin/env python3
# AURISI v60.65 : ADVANCED VISUAL TUTOR
#  - teaches ANY field/level (school -> MIT/engineering/medicine/law), step-by-step
#  - MANDATORY diagrams/graphs/charts (labelled angles, forces, circuits) for STEM
#  - WebGPU + offline capability detection (honest, with automatic fallback)
import sys, io

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1774257, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.64"' in h

# ---------- 1. advanced teaching rules, inserted before the DOODLE rule ----------
anchor = '"DOODLE: whenever a picture would teach better than words'
assert h.count(anchor) == 1
NEW_RULES = (
 '"LEVEL & FIELD: teach ANY subject at ANY level \\u2014 school, board, competitive, university/MIT-level '
 'engineering, medicine, law, finance, coding, design. Read the learner\\u2019s level from their words and the '
 'app profile, then teach at THAT level: never water it down unless asked, and never jump above their level '
 'without saying so. "+\n  '
 '"STEP-BY-STEP ALWAYS: number every step, one idea per step, never skip algebra or a reasoning jump. For any '
 'problem show GIVEN \\u2192 FIND \\u2192 FORMULA \\u2192 SUBSTITUTION (line by line) \\u2192 ANSWER with units \\u2192 one-line CHECK. '
 'Add one fully worked example when the idea is new. "+\n  '
 '"VISUALS ARE MANDATORY FOR STEM: for any physics, maths, engineering, chemistry or biology idea that has '
 'shape, force, angle, circuit, ray, vector or graph, you MUST include a [[DOODLE|short title|<svg>...]] figure '
 'with every angle, force, label and value written ON the figure, plus a [[GRAPH|expr|minX|maxX]] whenever a '
 'function or relation is involved, and a [[CHART|bar|title|labels|values]] for any data. Place the figure at the '
 'exact step where it is needed. Engineering: free-body diagrams, circuits, tolerances, stress-strain, CAD-style '
 'views. Maths: triangles with marked angles, unit circle, labelled axes. "+\n  '
)
h = h.replace(anchor, NEW_RULES + anchor)

# ---------- 2. capability detection (WebGPU + offline + service worker) ----------
anchor2 = 'if(typeof navigator!=="undefined"&&navigator.serviceWorker){window.addEventListener("load",function(){try{navigator.serviceWorker.register("sw.js").catch(function(e){})}catch(e){}})}'
assert h.count(anchor2) == 1
CAPS = anchor2 + '''
/* ===== v60.65 capabilities: WebGPU + offline (honest detect, automatic fallback) ===== */
var AURISI_CAPS={webgpu:false,gpuAdapter:null,offline:false,sw:false,canvas2d:true};
try{AURISI_CAPS.offline=(typeof navigator!=="undefined"&&("onLine" in navigator))?!navigator.onLine:false}catch(e){}
try{AURISI_CAPS.sw=!!(typeof navigator!=="undefined"&&navigator.serviceWorker)}catch(e){}
try{
  if(typeof navigator!=="undefined"&&navigator.gpu&&navigator.gpu.requestAdapter){
    navigator.gpu.requestAdapter().then(function(ad){ if(ad){AURISI_CAPS.webgpu=true;AURISI_CAPS.gpuAdapter=ad;} }).catch(function(){});
  }
}catch(e){}
window.addEventListener("online",function(){AURISI_CAPS.offline=false});
window.addEventListener("offline",function(){AURISI_CAPS.offline=true});
function aurisiCaps(){return AURISI_CAPS}
'''
h = h.replace(anchor2, CAPS)

# ---------- 3. version ----------
h = h.replace('APP_VERSION="60.64"', 'APP_VERSION="60.65"')
h = h.replace('v60.64 \u2014 LANGUAGE CONTENT REMOVED FROM LIBRARY', 'v60.65 \u2014 ADVANCED VISUAL TUTOR (any field, step-by-step diagrams, WebGPU-ready)')

out = h.encode("utf-8")
print("new size:", len(out))
for keep in ['APP_VERSION="60.65"', 'LEVEL & FIELD', 'STEP-BY-STEP ALWAYS', 'VISUALS ARE MANDATORY FOR STEM',
             'AURISI_CAPS', 'requestAdapter', 'DOODLE: whenever a picture', 'GRAPH|expr|minX|maxX', 'CHART|bar|title']:
    assert keep in h, "missing: " + keep
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6065 OK -> %d bytes" % len(out))
