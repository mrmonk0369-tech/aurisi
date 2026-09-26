import sys,io,os
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1935927, 'base size mismatch: %d'%len(h.encode('utf-8'))
assert h.count('APP_VERSION="60.52"')==1
i=h.find('/* ===================== v60.52 LANGUAGE LAB')
assert i>0, 'old LL block not found'
j=h.find('function instCloseModals(){')
assert j>i, 'instCloseModals not found after block'
block=io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'p53_block.txt'),encoding='utf-8').read()
h=h[:i]+block+h[j:]
h=h.replace('APP_VERSION="60.52"','APP_VERSION="60.53"')
out=h.encode('utf-8')
assert len(out)==1945423, 'output size mismatch: %d'%len(out)
for m in ['llHub','llMigrate','openLangLab','llPronCheck','llSim','llPick','llDrop','Language Hub']:
    assert m in h, 'missing marker '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6053 OK ->',len(out),'bytes')
