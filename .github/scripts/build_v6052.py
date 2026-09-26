import sys,io,os
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1916935, 'base size mismatch: %d'%len(h.encode('utf-8'))
assert h.count('APP_VERSION="60.51"')==1
assert h.count('var _sys=SYS_PROMPT();')==1
assert h.count('function instCloseModals(){')==1
block=io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'p52_block.txt'),encoding='utf-8').read()
h=h.replace('APP_VERSION="60.51"','APP_VERSION="60.52"')
h=h.replace('var _sys=SYS_PROMPT();','var _sys=SYS_PROMPT();try{_sys+=llSys()}catch(e){}')
h=h.replace('function instCloseModals(){',block+'\nfunction instCloseModals(){')
out=h.encode('utf-8')
assert len(out)==1935927, 'output size mismatch: %d'%len(out)
for m in ['llSys','openLangLab','llMission','llKit','llVital','Language Lab']:
    assert m in h, 'missing marker '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6052 OK ->',len(out),'bytes')
