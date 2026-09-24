#!/usr/bin/env python3
# AURISI v60.41: LANGUAGE HUB PRO
#  Owner request: inside the Language Hub, every language gets its own
#  experience - regular vocab + lots of learning aids, with meanings shown
#  in whatever language the student wants (English-to-English, French
#  words with Hindi meanings, anything).
#  Changes:
#  P1 JS: per-language profile store (localStorage langJ): {base, words[],
#     streak, lastDay} + langProfs/langProf/langSaveP/langSetBase/langAddWord.
#  P2 JS: langRules() upgrade - MEANING LANGUAGE rule ([[BASE|lang]] token
#     to save choice), DAILY DOSE rule (5 words/session as [[WORD|word|
#     pron|meaning|example]] tokens), REVIEW FIRST rule (3 [[Q]] on saved
#     words), profile injection into the system prompt.
#  P3 JS: msgRow parse of [[WORD|...]] (renders a word card + saves to the
#     bank, dedupe, streak, toast) and [[BASE|...]] (saves meaning language).
#  P4 JS: startLangMode welcome shows word bank + streak + meaning-language
#     setup question.
#  P5 JS: Language Hub tiles show saved word counts.
#  P6 CSS: .word-card styles.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.40 (1874490). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.41"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.41 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.40"' in h, "base must be v60.40"

# P1: profile store + langRules head (inject profile read into langRules)
F1 = 'function langRules(){\n  var L=LANG_MODES[LANG_ON];if(!L)return "";\n  return "===== '
R1 = (
    'function langProfs(){try{return JSON.parse(localStorage.getItem(STORAGE+"langJ")||"{}")}catch(e){return {}}}\n'
    'function langProf(k){var p=langProfs();if(!p[k])p[k]={base:"",words:[],streak:0,lastDay:""};return p[k]}\n'
    'function langSaveP(p){try{localStorage.setItem(STORAGE+"langJ",JSON.stringify(p))}catch(e){}}\n'
    'function langSetBase(k,b){var p=langProfs();if(!p[k])p[k]={base:"",words:[],streak:0,lastDay:""};p[k].base=b;langSaveP(p)}\n'
    'function langAddWord(k,w,m){\n'
    '  var p=langProfs();if(!p[k])p[k]={base:"",words:[],streak:0,lastDay:""};\n'
    '  w=String(w||"").trim();if(!w)return false;\n'
    '  for(var i=0;i<p[k].words.length;i++){if(String(p[k].words[i][0]).toLowerCase()===w.toLowerCase()){langSaveP(p);return false}}\n'
    '  p[k].words.push([w,String(m||"").trim()]);\n'
    '  var today=new Date().toDateString();\n'
    '  if(p[k].lastDay!==today){var y=new Date(Date.now()-86400000).toDateString();p[k].streak=(p[k].lastDay===y)?(p[k].streak+1):1;p[k].lastDay=today}\n'
    '  langSaveP(p);return true;\n'
    '}\n'
    'function langRules(){\n'
    '  var L=LANG_MODES[LANG_ON];if(!L)return "";\n'
    '  var p=langProf(LANG_ON),prof="";\n'
    "  if(p.words.length){var rec=[];for(var i=p.words.length-1;i>=Math.max(0,p.words.length-12);i--)rec.push(String(p.words[i][0]));prof=\"LANGUAGE PROFILE: this student's saved word bank for \"+L.name+\" has \"+p.words.length+\" words (recent: \"+rec.join(\", \")+\")\"+(p.streak?(\" and a \"+p.streak+\"-day streak\"):\"\")+\". \"}\n"
    '  return "===== '
)
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: langRules rules (6)-(9) -> new (6) MEANING LANGUAGE, (7) DAILY DOSE,
#     (8) REVIEW FIRST, (9)-(12) shifted old rules
F2 = (
    "  \"(6) Explain in the learner's language (how they write to you), but all teaching content stays in the target language. \"+\n"
    '  "(7) Weave in ONE cultural note occasionally (customs, etiquette, famous phrases) — max once every few turns. "+\n'
    '  "(8) End each section with a 1-line recap + one practice sentence to translate. "+\n'
    '  "(9) If asked how to exit: tap the ~B~u2715 on the language badge at the top. "+\n'
    '  "Keep every other Aurisi rule (identity, safety).";'
)
R2 = (
    "  \"(6) MEANING LANGUAGE: every new word and phrase gets its meaning in the student's chosen meaning language\"+(p.base?(\" — they chose: \"+p.base+\". Remember it for the whole conversation\"):\" — ask once which language they want meanings in (their own language, simple English, or any other language; if they pick the target language itself, give simple target-language definitions, like English-to-English), then output the token [[BASE|their choice]] alone on its own line so it is saved\")+\". "+\n"
    '  "(7) DAILY DOSE: in every session teach 5 new useful everyday words for their level, each as ONE token on its own line: [[WORD|the word|simple pronunciation|meaning in their meaning language|one short example sentence in the target language]] with no | character inside any part — these tokens build their saved word bank automatically. "+\n'
    '  "(8) REVIEW FIRST: if the LANGUAGE PROFILE shows saved words, begin the session with 3 quick [[Q]] recall questions on their old words before teaching the Daily Dose. "+prof+\n'
    "  \"(9) Explain in the learner's language (how they write to you), but all teaching content stays in the target language. \"+\n"
    '  "(10) Weave in ONE cultural note occasionally (customs, etiquette, famous phrases) — max once every few turns. "+\n'
    '  "(11) End each section with a 1-line recap + one practice sentence to translate. "+\n'
    '  "(12) If asked how to exit: tap the ~B~u2715 on the language badge at the top. "+\n'
    '  "Keep every other Aurisi rule (identity, safety).";'
)
assert h.count(Q(F2)) == 1, "P2 anchor not found"
h = h.replace(Q(F2), Q(R2))

# P3: [[WORD]] + [[BASE]] parse in msgRow (after svData block)
F3 = "      svData.forEach(function(d){txt=txt.replace(d[3],'<div data-svslot=\"'+d[2]+'\"></div>')});\n    }\n    let chData=null;"
R3 = (
    "      svData.forEach(function(d){txt=txt.replace(d[3],'<div data-svslot=\"'+d[2]+'\"></div>')});\n"
    "    }\n"
    "    const wRe=/~B~[~B~[~B~s*WORD~B~s*~B~|([^|~B~]]+)~B~|([^|~B~]]*)~B~|([^|~B~]]+)~B~|([^|~B~]]+)~B~]~B~]/gi;\n"
    "    txt=txt.replace(wRe,function(_aw,w,pr,mn,ex){\n"
    "      if(LANG_ON&&langAddWord(LANG_ON,w,mn)){try{toast(\"~B~u26A1 +1 word added to your \"+(LANG_MODES[LANG_ON]?LANG_MODES[LANG_ON].name:\"language\")+\" bank\")}catch(e2){}}\n"
    "      return '<div class=\"word-card\"><b class=\"wc-word\">'+escH(w)+'</b>'+(pr?'<span class=\"wc-pron\">'+escH(pr)+'</span>':'')+'<span class=\"wc-mean\">'+escH(mn)+'</span>'+(ex?'<span class=\"wc-ex\">'+escH(ex)+'</span>':'')+'</div>';\n"
    "    });\n"
    "    txt=txt.replace(/~B~[~B~[~B~s*BASE~B~s*~B~|([^|~B~]]+)~B~]~B~]/gi,function(_ab,b){\n"
    "      b=String(b||\"\").trim();\n"
    "      if(b&&LANG_ON){var _pb=langProf(LANG_ON);var _ch=_pb.base!==b;langSetBase(LANG_ON,b);if(_ch){try{toast(\"~B~u26A1 Meanings will be shown in \"+b)}catch(e3){}}}\n"
    "      return \"\";\n"
    "    });\n"
    "    let chData=null;"
)
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, Q(R3))

# P4: startLangMode welcome - show profile + meaning-language question
F4 = 'state.chatHistory.push({role:"model",parts:[{text:L.emoji+" **"+L.name+" Mode ON!**~B~n~B~nFrom now on, I am your dedicated "+L.name+" teacher ~B~u2014 reading, writing, speaking and real understanding, step by step.~B~n~B~n**First, tell me your level:**~B~n**1~B~uFE0F Complete beginner** ~B~u2014 start from the basics~B~n**2~B~uFE0F Some knowledge** ~B~u2014 build sentences & conversation~B~n**3~B~uFE0F Advanced** ~B~u2014 fluency, nuance & culture~B~n~B~nOr just tell me what you want to learn first! ~B~u{1F3AF}"}]});'
R4 = (
    'var _pf=langProf(k),_ps="";\n'
    '  if(_pf.words.length)_ps="**Your word bank:** "+_pf.words.length+" "+L.name+" words"+(_pf.streak?("~B~u00B7 ~B~u{1F525} "+_pf.streak+"-day streak"):"")+"~B~n";\n'
    '  if(_pf.base)_ps+="**Meanings in:** "+_pf.base+"~B~n";\n'
    '  state.chatHistory.push({role:"model",parts:[{text:L.emoji+" **"+L.name+" Mode ON!**~B~n~B~nI am your dedicated "+L.name+" teacher ~B~u2014 reading, writing, speaking and real understanding, step by step.~B~n"+_ps+"~B~n**Quick setup ~B~u2014 tell me:**~B~n**1~B~uFE0F Your level** ~B~u2014 beginner / some knowledge / advanced~B~n**2~B~uFE0F Meaning language** ~B~u2014 which language should word meanings be in? (your own language, simple English, or any language you like)~B~n~B~nOr just tell me what you want to learn first! ~B~u{1F3AF}"}]});'
)
assert h.count(Q(F4)) == 1, "P4 anchor not found"
h = h.replace(Q(F4), Q(R4))

# P5: hub tiles show word-bank counts
F5 = "<small>'+(LANG_NATIVE[k]||L.name)+'</small></button>';"
R5 = "<small>'+(LANG_NATIVE[k]||L.name)+(langProf(k).words.length?(' ~B~u00B7 '+langProf(k).words.length+' words'):'')+'</small></button>';"
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, Q(R5))

# P6: word-card CSS
F6 = '.wpop .wp-x{display:block;margin-top:6px;font-size:10.5px;opacity:.55}'
R6 = (
    '.wpop .wp-x{display:block;margin-top:6px;font-size:10.5px;opacity:.55}\n'
    '.word-card{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:14px;padding:12px 15px;margin:10px 0;background:var(--surface2)}\n'
    '.word-card .wc-word{display:block;font-size:17px;font-weight:800;color:var(--accent)}\n'
    '.word-card .wc-pron{display:block;font-size:12.5px;color:var(--muted);margin-top:2px}\n'
    '.word-card .wc-mean{display:block;font-size:14px;margin-top:5px}\n'
    '.word-card .wc-ex{display:block;font-size:13px;color:var(--muted);margin-top:5px;font-style:italic}'
)
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.40"'
R7 = 'var APP_VERSION="60.41"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied language hub pro, size: %d bytes" % len(h.encode("utf-8")))
