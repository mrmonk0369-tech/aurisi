import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1955474, 'base size mismatch'
assert h.count('APP_VERSION="60.60"')==1
pairs=[
  (r'''  var isNew=!h.langs[code];
  if(isNew)h.langs[code]={start:Date.now(),done:{}};
  h.active=code;llSaveHub(h);
  closeLL();''',
   r'''  var isNew=!h.langs[code];
  var prev=h.active;
  if(isNew)h.langs[code]={start:Date.now(),done:{}};
  h.active=code;llSaveHub(h);
  closeLL();
  if(prev!==code){try{newChat()}catch(e){};toast('✨ Fresh chat for '+LL_LANGS[code].name+' — every language gets its own clean chat, no mixing')}'''),
  (r'''The end goal: this student can talk to anyone, in any country, on any stage — classroom to cinema.\n';''',
   r'''The end goal: this student can talk to anyone, in any country, on any stage — classroom to cinema.\n12. LANGUAGE SEPARATION (CRITICAL): teach ONLY in this language. If earlier messages in this conversation are in a DIFFERENT language or about another language\'s lessons, IGNORE them completely — never mix languages, never reference the other language\'s content, never translate into it. This chat belongs to ONE language only.\n';'''),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor P%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjYwIExBTkdVQUdFIEhVQiDigJQgV09STEQgRU5HTElTSCBFRElUSU9OAHY2MC42MSBMQU5HVUFHRSBIVUIg4oCUIExBTkdVQUdFLVNFUEFSQVRJT04gRklY').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.60"','APP_VERSION="60.61"')
out=h.encode('utf-8')
assert len(out)==1955980, 'output mismatch: %d'%len(out)
for m in ['LANGUAGE SEPARATION','Fresh chat','APP_VERSION="60.61"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6061 OK ->',len(out))
