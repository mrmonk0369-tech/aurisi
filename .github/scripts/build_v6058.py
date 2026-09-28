import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1950287, 'base size mismatch'
assert h.count('APP_VERSION="60.57"')==1
pairs=[
  ('''function llVital(){''',
   '''function llHow(){
  var s=llHub();if(!s||!s.active)return;var L=llLang();
  var old=document.getElementById('llHowBack');if(old)old.remove();
  var b=document.createElement('div');b.className='modal-back open';b.id='llHowBack';
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement('div');m.className='modal feat-modal';
  m.innerHTML='<h2>🔤 How to Pronounce — '+L.flag+' '+L.name+'</h2><div class="sub">Type ANY word or sentence. I will show you exactly how to say it — like: I’m (eye, m).</div>'+
  '<div class="feat-sec"><div style="display:flex;gap:8px"><input id="llHowIn" placeholder="Type a word or sentence…" style="flex:1;padding:11px 14px;border-radius:10px;border:1px solid #232b3d;background:#141926;color:#e8ecf4;font-size:14px;outline:none">'+
  '<button class="btn" onclick="llHowGo()">🔊 Say it</button></div></div>'+
  '<div class="ll-row">💡 Example: type “I’m” → you get: (eye, m) · type “comfortable” → (KUM-fur-tuh-bul)</div>';
  b.appendChild(m);document.body.appendChild(b);
  var inp=document.getElementById('llHowIn');if(inp&&inp.focus)try{inp.focus()}catch(e){}
}
function llHowGo(){
  var el=document.getElementById('llHowIn');var w=el?String(el.value||'').trim().slice(0,200):'';
  if(!w){toast('Type a word first');return}
  var s=llHub();if(!s||!s.active)return;var L=llLang();
  var b=document.getElementById('llHowBack');if(b)b.remove();
  try{speakText(w)}catch(e){}
  quick('HOW TO PRONOUNCE in '+L.name+' — say it out loud for me too. The word/sentence: "'+w+'". Teach me EXACTLY how to say it: (1) SOUND-WORDS in brackets, made of simple small words/sounds I already know — exactly like: I’m (eye, m) · comfortable (KUM-fur-tuh-bul) · world (wur-ld) · schedule (SKED-jool). Do this for EVERY word I typed. (2) SYLLABLES: split each word, stressed part in CAPS. (3) SLOW-MO: small repeatable chunks. (4) SILENT LETTERS in it, if any. (5) Mouth tip for the hardest sound. (6) Two more words that follow the same pattern. Never Hindi.');
  setTimeout(llMark,1500);
}
function llVital(){'''),
  ('''html+='<div class="ll-row ll-link" onclick="llMaster()">''',
   '''html+='<div class="ll-row ll-link" onclick="llHow()">🔤 How to pronounce — type any word, get (eye, m) style sound-words</div>';
    html+='<div class="ll-row ll-link" onclick="llMaster()">'''),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor R%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjU3IExBTkdVQUdFIEhVQiDigJQgQ09NUExFVEUgTUFTVEVSWSBFRElUSU9OAHY2MC41OCBMQU5HVUFHRSBIVUIg4oCUIEhPVy1UTy1QUk9OT1VOQ0UgRURJVElPTg==').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.57"','APP_VERSION="60.58"')
out=h.encode('utf-8')
assert len(out)==1952493, 'output mismatch: %d'%len(out)
for m in ['llHow','llHowGo','HOW TO PRONOUNCE','llHowIn','APP_VERSION="60.58"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6058 OK ->',len(out))
