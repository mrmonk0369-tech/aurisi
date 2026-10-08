#!/usr/bin/env python3
# AURISI v60.63 : Language Hub leftovers removed (Language Mode system) + polish
# NOTE: .lang-tile / .lang-grid / .lt-flag CSS is KEPT — the Collections UI reuses those classes.
import sys, io, re

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1914846, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.62"' in h

def cut(a, b, tag):
    global h
    c = h.count(a)
    assert c == 1, "%s: found %d" % (tag, c)
    h = h.replace(a, b)

# 1) whole v19.6 LANGUAGE MODES section -> keep a dormant LANG_ON declaration
s = h.find("/* ===================== v19.6 LANGUAGE MODES")
e = h.find("/* =====================", s + 40)
assert s > 0 and e > s and "LANG_MODES" in h[s:e] and "stopLangMode" in h[s:e]
h = h[:s] + 'var LANG_ON="";\n\n' + h[e:]

# 2) Language Mode chip markup
s = h.find('<div class="fy-chip" id="langChip"')
assert s > 0
e = h.find("</div>", s) + len("</div>")
assert "stopLangMode" in h[s:e]
h = h[:s] + h[e:]

# 3) renderLangChip() calls
h = h.replace("renderFeynmanChip();renderSanskritChip();renderLangChip();", "renderFeynmanChip();renderSanskritChip();")
h = h.replace("renderSanskritChip();renderLangChip();", "renderSanskritChip();")
h = h.replace("renderFeynmanChip();renderLangChip();", "renderFeynmanChip();")
h = h.replace("  renderLangChip();\n", "")
h = re.sub(r"renderLangChip\(\);", "", h)

# 4) word-bank side effects (WORD + BASE tokens)
cut('      if(LANG_ON&&langAddWord(LANG_ON,w,mn)){try{toast("\\u26A1 +1 word added to your "+(LANG_MODES[LANG_ON]?LANG_MODES[LANG_ON].name:"language")+" bank")}catch(e2){}}\n', "", "word token")
cut('      if(b&&LANG_ON){var _pb=langProf(LANG_ON);var _ch=_pb.base!==b;langSetBase(LANG_ON,b);if(_ch){try{toast("\\u26A1 Meanings will be shown in "+b)}catch(e3){}}}\n', "", "base token")

# 5) generate(): drop the LANG_ON rules branch
cut('+(LANG_ON?("\\n\\n"+langRules()):(SANS_ON?("\\n\\n"+SANSKRIT_RULES):(FEYNMAN_ON?("\\n\\n"+FEYNMAN_RULES):"")));',
    '+(SANS_ON?("\\n\\n"+SANSKRIT_RULES):(FEYNMAN_ON?("\\n\\n"+FEYNMAN_RULES):""));',
    "generate langRules")

# 6) clean LANG_ON assignments
h = h.replace('SANS_ON=false;LANG_ON="";', 'SANS_ON=false;')
h = h.replace('FEYNMAN_ON=false;LANG_ON="";', 'FEYNMAN_ON=false;')
h = h.replace('FEYNMAN_ON=false;SANS_ON=false;LANG_ON="";', 'FEYNMAN_ON=false;SANS_ON=false;')
h = h.replace('(LANG_MODES[m]?LANG_MODES[m].emoji:"\\u{1F4AC}")', '"\\u{1F4AC}"')
h = h.replace('LANG_ON=(LANG_MODES[md]&&md!=="feynman"&&md!=="sanskrit")?md:"";', 'LANG_ON="";')
h = h.replace('    if(LANG_ON)localStorage.setItem(STORAGE+"langmode",LANG_ON);else localStorage.removeItem(STORAGE+"langmode");\n', '')
h = h.replace('c.mode=FEYNMAN_ON?"feynman":(SANS_ON?"sanskrit":(LANG_ON||""));', 'c.mode=FEYNMAN_ON?"feynman":(SANS_ON?"sanskrit":"");')

# 6b) the "stop <language>" command that called the removed function
cut('  if(/^stop[! ]*(language|english|spanish|mandarin|chinese|german|korean|japanese|french)$/i.test(v)){el.value="";stopLangMode();return}\n', "", "stop-language command")

# 7) polish
POLISH = """
/* ===== v60.63 polish ===== */
.msg-row,.agent-card,.art-card{animation:aurIn .45s cubic-bezier(.22,.61,.36,1) both}
@keyframes aurIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""
h = h.replace('</style>', POLISH + '</style>', 1)

# 8) version
h = h.replace('APP_VERSION="60.62"', 'APP_VERSION="60.63"')
h = h.replace('v60.62 \u2014 LANGUAGE HUB REMOVED', 'v60.63 \u2014 LANGUAGE HUB FULLY REMOVED + POLISH')

out = h.encode("utf-8")
print("new size:", len(out))
for bad in ["LANG_MODES", "LANG_NATIVE", "startLangMode", "stopLangMode", "langRules", "langProf", "langAddWord", "langSetBase", "renderLangChip", "langChip", "IM_CITY", "Language Mode", "Language Hub"]:
    assert bad not in h, "still present: " + bad
for keep in ['APP_VERSION="60.63"', 'var LANG_ON=""', 'UI_LANGS', 'uiLangSel', 'speechLangFor', 'getUiLang', 'SANSKRIT_RULES', 'FEYNMAN_RULES', 'function instCloseModals(){', 'lang-tile', 'lang-grid']:
    assert keep in h, "missing: " + keep
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6063 OK -> %d bytes" % len(out))
