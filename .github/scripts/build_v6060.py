import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1954016, 'base size mismatch'
assert h.count('APP_VERSION="60.59"')==1
pairs=[
  (r'''After the quiz, report my score and my weak growth areas.\n';''',
   r'''After the quiz, report my score and my weak growth areas.\n11. WORLD ENGLISH GOAL (for English courses): teach ONE English that works EVERYWHERE — a clear, neutral, globally understood accent (the accent of movies, news and business). Regularly show how the same sentence sounds in American, British, Australian and Indian English so the student understands EVERYONE, anywhere. Include real performance skills: movie dialogue delivery (acting), song lyric pronunciation (singing), public speaking and interviews. The end goal: this student can talk to anyone, in any country, on any stage — classroom to cinema.\n';'''),
  (r'''function llVital(){''',
   r'''function llWorld(){
  var s=llHub();if(!s||!s.active)return;var L=llLang();
  closeLL();
  quick('WORLD ENGLISH MODE — '+L.name+'. Train me for the world stage. Start with ONE arena now, then cover them all: (1) NEUTRAL GLOBAL ACCENT — crystal-clear pronunciation everyone on Earth understands; (2) UNDERSTAND EVERYONE — the same sentence spoken in American, British, Australian and Indian accents, with the differences explained; (3) ACTING — give me famous-movie-style dialogues to perform, then correct my delivery line by line; (4) SINGING — song lyric pronunciation, rhythm and flow; (5) PUBLIC SPEAKING & INTERVIEWS — stage, camera, presentations. Make me PRACTISE out loud, not just read. End with a 5-question quiz.');
  setTimeout(llMark,1500);
}
function llVital(){'''),
  (r'''html+='<div class="ll-row ll-link" onclick="llQuiz()">''',
   r'''html+='<div class="ll-row ll-link" onclick="llWorld()">🌍 World English — one English for every country, stage & screen</div>';
    html+='<div class="ll-row ll-link" onclick="llQuiz()">'''),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor P%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjU5IExBTkdVQUdFIEhVQiDigJQgUVVJWi1BRlRFUi1MRVNTT04gRURJVElPTgB2NjAuNjAgTEFOR1VBR0UgSFVCIOKAlCBXT1JMRCBFTkdMSVNIIEVESVRJT04=').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.59"','APP_VERSION="60.60"')
out=h.encode('utf-8')
assert len(out)==1955474, 'output mismatch: %d'%len(out)
for m in ['llWorld','WORLD ENGLISH GOAL','World English','APP_VERSION="60.60"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6060 OK ->',len(out))
