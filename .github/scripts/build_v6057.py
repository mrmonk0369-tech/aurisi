import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1950110, 'base size mismatch'
assert h.count('APP_VERSION="60.56"')==1
pairs=[
  ('Adjectives & their opposites','Verb forms: V1 V2 V3 of key verbs'),
  ('Work & study words','Word forms: noun verb adjective adverb'),
  ('Humour: jokes & wordplay','Global English: accents, slang, any country'),
  (base64.b64decode('' +
    'KDMpIFRFTlNFUzogQUxMIGVzc2VudGlhbCB0ZW5zZXMg4oCUIG5hbWUsIHdoZW4gdG8gdXNlLCBo' +
    'b3cgdG8gZm9ybSwgb25lIG1pbmkgZXhhbXBsZSBlYWNoOyAoNCkgVE9QIDUwIFBIUkFTRVM6').decode('utf-8'),
   base64.b64decode('' +
    'KDMpIFRFTlNFUzogQUxMIGVzc2VudGlhbCB0ZW5zZXMg4oCUIG5hbWUsIHdoZW4gdG8gdXNlLCBo' +
    'b3cgdG8gZm9ybSwgb25lIG1pbmkgZXhhbXBsZSBlYWNoOyAoM2IpIFZFUkIgRk9STVM6IDFzdCwg' +
    'Mm5kLCAzcmQgZm9ybSAoVjEgVjIgVjMpIG9mIHRoZSA2MCBtb3N0IGltcG9ydGFudCB2ZXJicywg' +
    'cGx1cyB3b3JkIGZvcm1zIChzYW1lIHdvcmQgYXMgbm91bi92ZXJiL2FkamVjdGl2ZS9hZHZlcmIp' +
    'OyAoNCkgVE9QIDUwIFBIUkFTRVM6').decode('utf-8')),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor R%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjU2IExBTkdVQUdFIEhVQiDigJQgVE9QLVRJRVIgU1RFUC1CWS1TVEVQIEVESVRJT04AdjYwLjU3IExBTkdVQUdFIEhVQiDigJQgQ09NUExFVEUgTUFTVEVSWSBFRElUSU9O').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.56"','APP_VERSION="60.57"')
out=h.encode('utf-8')
assert len(out)==1950287, 'output mismatch'
for m in ['V1 V2 V3','Word forms','Global English','ONE-SHOT MASTER FOUNDATION','llMaster','APP_VERSION="60.57"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6057 OK ->',len(out))
