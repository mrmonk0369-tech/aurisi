import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1952493, 'base size mismatch'
assert h.count('APP_VERSION="60.58"')==1
pairs=[
  (r'''CURRENT STEP: '+llStep()+'. Build today\'s lesson around this step topic.\n';''',
   r'''CURRENT STEP: '+llStep()+'. Build today\'s lesson around this step topic.\n10. QUIZ AFTER EVERY LESSON (MANDATORY): when the lesson content is done, give a 5-question quiz on what you just taught. One question at a time, use EXACTLY this token format: [[QUIZ|question|option A|option B|option C|option D|correct letter|one-line explanation|2-4 word topic]] — exactly 4 options, correct letter is A, B, C or D, keep fields short, never use the | character inside a field. After the quiz, report my score and my weak growth areas.\n';'''),
  (r'''lesson — CURRENT STEP: '+llStep()+'. ';''',
   r'''lesson — CURRENT STEP: '+llStep()+'. End with the 5-question lesson quiz. ';'''),
  (r'''complete and unforgettable.');''',
   r'''complete and unforgettable. End with a 5-question quiz on this foundation, one question at a time, format: [[QUIZ|question|option A|option B|option C|option D|correct letter|one-line explanation|topic]].');'''),
  (r'''function llVital(){''',
   r'''function llQuiz(){
  var s=llHub();if(!s||!s.active)return;var L=llLang();
  closeLL();
  quick('QUIZ TIME — '+L.name+'. Give me a 10-question interactive quiz covering everything I have learned so far (my current step is: '+llStep()+'), mixing older steps in too. One question at a time, use EXACTLY this format: [[QUIZ|question|option A|option B|option C|option D|correct letter|one-line explanation|2-4 word topic]] — exactly 4 options, correct letter A, B, C or D, short fields, never use | inside a field. After the last question, report my score and my weak growth areas.');
  setTimeout(llMark,1500);
}
function llVital(){'''),
  (r'''html+='<div class="ll-row ll-link" onclick="llHow()">''',
   r'''html+='<div class="ll-row ll-link" onclick="llQuiz()">📝 Quiz me — 10-question test on my progress + growth areas</div>';
    html+='<div class="ll-row ll-link" onclick="llHow()">'''),
  (r'''+LL_STEPS[phK][Math.min(si+2,29)]+'</div>';''',
   r'''+LL_STEPS[phK][Math.min(si+2,29)]+'</div>';
    html+='<div class="ll-road">✅ After every lesson: a 5-question quiz with score & growth areas</div>';'''),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor P%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjU4IExBTkdVQUdFIEhVQiDigJQgSE9XLVRPLVBST05PVU5DRSBFRElUSU9OAHY2MC41OSBMQU5HVUFHRSBIVUIg4oCUIFFVSVotQUZURVItTEVTU09OIEVESVRJT04=').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.58"','APP_VERSION="60.59"')
out=h.encode('utf-8')
assert len(out)==1954016, 'output mismatch: %d'%len(out)
for m in ['llQuiz','QUIZ AFTER EVERY LESSON','Quiz me','APP_VERSION="60.59"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6059 OK ->',len(out))
