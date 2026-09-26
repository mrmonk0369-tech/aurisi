import sys,io,os
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1945423, 'base size mismatch: %d'%len(h.encode('utf-8'))
assert h.count('APP_VERSION="60.53"')==1
bd=os.path.join(os.path.dirname(os.path.abspath(__file__)),'p53_block.txt')
s=io.open(bd,encoding='utf-8').read()
old1="  '1. Speak ONLY '+L.name+' in your lessons and examples. If the student writes in Hindi, give a SHORT Hindi explanation (1-2 lines), then immediately continue in '+L.name+'.\\n'+"
new1=("  '1. THE BILINGUAL LADDER (MOST IMPORTANT RULE \u2014 a confused student learns nothing):\\n'+\n"
"  (L.days&&d<=30?'   FOUNDATION phase = FULL BILINGUAL: every sentence you write in '+L.name+' MUST be immediately followed by its Hindi translation in brackets. Every new word: '+L.name+' word \u2014 Hindi meaning. For sentences the student must learn, give word-by-word breakdown. The student must NEVER wonder what something means.':'')+\n"
"  (L.days&&d>30&&d<=60?'   IMMERSION phase = '+L.name+' first, but give Hindi meaning for every NEW word and a 1-line Hindi summary after each paragraph.':'')+\n"
"  (L.days&&d>60?'   FLUENCY phase = pure '+L.name+'. Use Hindi ONLY to explain a mistake or if asked.':'')+\n"
"  (!L.days?'   FULL BILINGUAL: every sentence in '+L.name+' followed by Hindi translation in brackets; every new word with Hindi meaning.':'')+'\\n'+\n"
"  '2. If the student types ? or asks the meaning \u2014 STOP and re-explain your last message in Hindi, word by word, then continue.\\n'+")
assert old1 in s, 'rule1 anchor missing'
s=s.replace(old1,new1)
for a,b in [("'2. NO TIMEPASS","'3. NO TIMEPASS"),("'3. FRONT-LOAD","'4. FRONT-LOAD"),("'4. Correct EVERY","'5. Correct EVERY"),("'5. End every reply","'6. End every reply"),("'6. Use real places","'7. Use real places"),("'7. Keep lessons tight","'8. Keep lessons tight"),("'8. THE STUDENT IS ON A 90-DAY","'9. THE STUDENT IS ON A 90-DAY"),("'8. Teach as a full deep course","'9. Teach as a full deep course")]:
    assert a in s, 'anchor missing: '+a
    s=s.replace(a,b)
old_tip='<div class="ll-row ll-link" onclick="llMission(\\\'speak\\\')">\U0001F5E3\uFE0F Practice speaking now \u2014 AURISI is your conversation partner</div>'
assert old_tip in s, 'tip anchor missing'
s=s.replace(old_tip,old_tip+'<div class="ll-row">\U0001F4A1 Type <b>?</b> in chat anytime \u2014 AURISI will re-explain in Hindi, word by word. Early days = full bilingual support; it fades as you improve.</div>')
s=s.replace('v60.53 LANGUAGE HUB \u2014 4 PILLARS + PRONUNCIATION ENGINE','v60.54 LANGUAGE HUB \u2014 BILINGUAL LADDER EDITION')
i=h.find('/* ===================== v60.53 LANGUAGE HUB')
assert i>0, 'old block not found'
j=h.find('function instCloseModals(){')
assert j>i
h=h[:i]+s+h[j:]
h=h.replace('APP_VERSION="60.53"','APP_VERSION="60.54"')
out=h.encode('utf-8')
assert len(out)==1946390, 'output size mismatch: %d'%len(out)
for m in ['BILINGUAL LADDER','word by word','llHub','llPronCheck','openLangLab','APP_VERSION="60.54"']:
    assert m in h, 'missing marker '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6054 OK ->',len(out),'bytes')
