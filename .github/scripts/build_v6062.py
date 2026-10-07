#!/usr/bin/env python3
# AURISI v60.62 : Language Hub COMPLETELY REMOVED
# Removes: LL_* 90-day hub block, llSys hook, Language Hub workspace card,
#          Language Hub modal (langLab/langBack), openLangLab/closeLangLab,
#          and the Language Hub entry in the features list.
import sys, io

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()

assert len(h.encode("utf-8")) == 1955980, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.61"' in h

# ---- 1. the whole LL_* Language Hub block ----
i = h.find("var LL_LANGS")
j = h.find("function instCloseModals(){")
assert i > 0 and j > i, "LL block bounds not found"
ll_block = h[i:j]
assert "llMountCard" in ll_block and "llSys" in ll_block, "LL block content unexpected"
h = h[:i] + h[j:]

# ---- 2. llSys hook in generate() ----
a = "  var _sys=SYS_PROMPT();try{_sys+=llSys()}catch(e){}"
assert h.count(a) == 1, "llSys hook not found"
h = h.replace(a, "  var _sys=SYS_PROMPT();")

# ---- 3. Language Hub workspace card in the Studio ----
a = "html+='<div class=\"ws-h\">\U0001F30D Language Hub</div>"
s = h.find(a)
assert s > 0, "ws Language Hub card not found"
e = h.find("</button></div>';", s)
assert e > s, "ws card end not found"
h = h[:s] + h[e + len("</button></div>';"):]

# ---- 4. Language Hub modal (langBack + langLab) ----
a = '<div class="modal-back" id="langBack" onclick="closeLangLab()"></div>'
s = h.find(a)
assert s > 0, "langLab modal not found"
e = h.find('<div class="modal-back" id="contBack"', s)
assert e > s, "langLab modal end not found"
assert 'id="langLab"' in h[s:e] and "Language Hub" in h[s:e]
h = h[:s] + h[e:]

# ---- 5. openLangLab + closeLangLab functions ----
s = h.find("function openLangLab(){")
assert s > 0, "openLangLab not found"
e = h.find("function startLangMode(", s)
assert e > s, "closeLangLab end not found"
seg = h[s:e]
assert "closeLangLab" in seg and "langLabGrid" in seg
h = h[:s] + h[e:]

# ---- 6. Language Hub entry in the features list ----
a = '["\U0001F30D Language Hub","Spanish, French, Japanese + more, level-tracked"],'
assert h.count(a) == 1, "feature-list entry not found"
h = h.replace(a, "")

# ---- 6b. leftover Language Hub references ----
a = '  if(getInst())secs[0][1]=secs[0][1].filter(function(f){return f[0].indexOf("Language Hub")<0});\n'
assert h.count(a) == 1, "features filter line not found"
h = h.replace(a, "")
a = '  if(ins)hs=hs.concat(["Language Hub"]);\n'
assert h.count(a) == 1, "home-cards Language Hub line not found"
h = h.replace(a, "")

# ---- 7. version bump ----
h = h.replace('APP_VERSION="60.61"', 'APP_VERSION="60.62"')
h = h.replace('v60.61 LANGUAGE HUB \u2014 LANGUAGE-SEPARATION FIX', 'v60.62 \u2014 LANGUAGE HUB REMOVED')

out = h.encode("utf-8")
assert len(out) == 1914846, "output size mismatch: %d" % len(out)
for bad in ["LL_LANGS", "llSys", "llMountCard", "openLangLab", "closeLangLab", 'id="langLab"', "Language Hub", "llPick", "llWorld"]:
    assert bad not in h, "still present: " + bad
assert 'APP_VERSION="60.62"' in h
assert "function instCloseModals(){" in h and "startLangMode" in h and "LANG_MODES" in h
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6062 OK -> %d bytes" % len(out))
