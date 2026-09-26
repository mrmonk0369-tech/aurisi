import io, os

D = os.path.dirname(os.path.abspath(__file__))

def rf(p):
    return io.open(os.path.join(D, p), encoding='utf-8').read()

# ---- patch pairs: (old file, new file) ----
pairs = [('p51_1o.txt', 'p51_1n.txt'), ('p51_2o.txt', 'p51_2n.txt'), ('p51_3o.txt', 'p51_3n.txt')]

import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'AURISI.html'
dst = sys.argv[2] if len(sys.argv) > 2 else 'AURISI_new.html'
h = io.open(src, encoding='utf-8').read()

for i, (o, n) in enumerate(pairs, 1):
    old = rf(o)
    new = rf(n)
    cnt = h.count(old)
    assert cnt == 1, 'patch %d anchor count=%d (expected 1)' % (i, cnt)
    h = h.replace(old, new)
    print('patch %d applied (%d -> %d bytes)' % (i, len(old.encode()), len(new.encode())))

io.open(dst, 'w', encoding='utf-8', newline='').write(h)
print('built', dst, len(h.encode()), 'bytes')
