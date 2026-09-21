#!/usr/bin/env python3
# AURISI v58.6: Profile-based content serving.
# A tuition teacher for classes 6-8 now sees ONLY class 6-8 level content
# in the Library (Content Studio collections) - NEET/JEE/UPSC/SSC packs
# are hidden - and anything they add themselves is always visible.
# Same for every profile: junior -> school basics, institute -> its exams,
# student -> everything (default).
# Base: AURISI.html v58.5. Idempotent: no-op if already v58.6.
import sys, io

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.6"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.6 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.5"' in h, "base must be v58.5"

# Patch 1: profileCats() - allowed content collections per profile
F1 = 'function applyProfileHome(el){'
R1 = '''function profileCats(){
  var p=getProfile();if(!p)return null;
  if(p.role==="teacher"){
    if(p.detail==="Classes 6-8")return ["class7","class8","english","sanskrit","other"];
    if(p.detail==="Classes 9-10")return ["class9","class10","english","sanskrit","other"];
    if(p.detail==="Classes 11-12")return ["class11","class12","neet","jee","english","other"];
    return ["class7","class8","class9","class10","class11","class12","neet","jee","english","sanskrit","other"];
  }
  if(p.role==="junior")return ["class7","class8","english","sanskrit","other"];
  if(p.role==="institute"){
    if(p.detail==="SSC & Govt exams")return ["ssc","hssc","dsssb","english","other"];
    if(p.detail==="NEET")return ["neet","class11","class12","other"];
    if(p.detail=="JEE")return ["jee","class11","class12","other"];
    if(p.detail=="Board exams")return ["class9","class10","class11","class12","english","other"];
    return null;
  }
  return null;
}
function applyProfileHome(el){'''
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: Library collections - filter tiles by profile (own content always stays)
F2 = 'CONT_CATS.forEach(function(c){\n    var n=contCount(c.id);'
R2 = '''CONT_CATS.forEach(function(c){
    if(profileCats()){
      var _own=false;try{_own=getContLib().some(function(x){return x.cat===c.id&&(!x.key||String(x.key).indexOf("pack_")!==0)})}catch(e){}
      if(profileCats().indexOf(c.id)<0&&!_own)return;
    }
    var n=contCount(c.id);'''
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: teacher AI line - recommend only their class-level packs
F3 = 'skip competitive-exam current affairs. "'
R3 = 'skip competitive-exam current affairs; in the Library recommend only their class-level collections. "'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: version bump
F4 = 'var APP_VERSION="58.5"'
R4 = 'var APP_VERSION="58.6"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied content-profile patches, size: %d bytes" % len(h.encode("utf-8")))
