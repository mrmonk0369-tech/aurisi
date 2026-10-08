#!/usr/bin/env python3
# AURISI v60.64 : foreign-language CONTENT removed from Library/Collections
# Removes: language packs (Spanish/French/German/Korean/Japanese/Mandarin) from STUDY_PACKS,
#          language collections from CONT_CATS, and the "Learn a language" starter pill.
import sys, io, re

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1904318, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.63"' in h

LANGS = {"spanish", "french", "german", "korean", "japanese", "mandarin", "italian", "portuguese", "russian", "arabic"}

# ---------- 1. drop language packs from STUDY_PACKS ----------
decl = "var STUDY_PACKS=["
s = h.find(decl)
assert s > 0
i = s + len(decl); depth = 0; instr = False; esc = False; end = None
while i < len(h):
    c = h[i]
    if instr:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': instr = False
    else:
        if c == '"': instr = True
        elif c in "[{": depth += 1
        elif c in "]}":
            if depth == 0:
                end = i + 1; break
            depth -= 1
    i += 1
assert end and end > s
seg_start = s + len(decl)
seg = h[seg_start:end - 1]

# top-level entries inside the array
spans = []
j = 0; n = len(seg); depth = 0; start = None; instr = False; esc = False
while j < n:
    c = seg[j]
    if instr:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': instr = False
    else:
        if c == '"': instr = True
        elif c == "{":
            if depth == 0: start = j
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and start is not None:
                spans.append((start, j + 1)); start = None
    j += 1

total = len(spans)
drops = []
for (a, b) in spans:
    m = re.search(r'"cat"\s*:\s*"(\w+)"', seg[a:b])
    if m and m.group(1) in LANGS:
        drops.append((a, b, m.group(1), b - a))
assert len(drops) >= 8, "expected several language packs, got %d" % len(drops)
dropped_bytes = sum(d[3] for d in drops)

# delete from the end backwards, eating the following ", "
new_seg = seg
for (a, b, _c, _L) in sorted(drops, key=lambda x: -x[0]):
    e = b
    if new_seg[e:e + 2] == ", ": e += 2
    elif new_seg[e:e + 1] == ",": e += 1
    new_seg = new_seg[:a] + new_seg[e:]
h = h[:seg_start] + new_seg + h[end - 1:]
kept = total - len(drops)
print("STUDY_PACKS: %d -> %d entries (dropped %d language packs, %d bytes)" % (total, kept, len(drops), dropped_bytes))

# ---------- 2. language collections out of CONT_CATS ----------
before = h.count('id:"spanish"')
h2 = re.sub(r' \{id:"(?:spanish|french|german|korean|japanese|mandarin)",label:"[^"]*"\},\n', '', h)
assert h2 != h, "CONT_CATS language rows not found"
h = h2
assert 'id:"spanish"' not in h and 'id:"korean"' not in h and 'id:"japanese"' not in h
for keep in ['id:"english"', 'id:"sanskrit"', 'id:"hssc"', 'id:"class10"', 'id:"neet"']:
    assert keep in h, "lost collection: " + keep

# ---------- 3. "Learn a language" starter pill ----------
k = h.find('data-i18n="starterLanguage"')
assert k > 0
a = h.rfind('<button', 0, k)
b = h.find("</button>", k) + len("</button>")
assert 'Learn a language' in h[a:b]
h = h[:a] + h[b:]

# ---------- 3b. unused i18n keys for the removed pill ----------
h2 = re.sub(r'starterLanguage:"[^"]*",', '', h)
assert h2 != h, "starterLanguage i18n keys not found"
h = h2
assert 'starterLanguage' not in h

# ---------- 4. version ----------
h = h.replace('APP_VERSION="60.63"', 'APP_VERSION="60.64"')
h = h.replace('v60.63 \u2014 LANGUAGE HUB FULLY REMOVED + POLISH', 'v60.64 \u2014 LANGUAGE CONTENT REMOVED FROM LIBRARY')

out = h.encode("utf-8")
print("new size:", len(out))
for bad in ['"cat": "spanish"', '"cat": "french"', '"cat": "german"', '"cat": "korean"', '"cat": "japanese"', '"cat": "mandarin"', 'id:"spanish"', 'id:"korean"', 'Learn a language', 'Spanish \u2014 Starter Kit', 'Korean Hangul Master Table']:
    assert bad not in h, "still present: " + bad
for keep in ['APP_VERSION="60.64"', 'STUDY_PACKS', 'id:"english"', 'id:"hssc"', 'id:"neet"', 'uiLangSel']:
    assert keep in h, "missing: " + keep
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6064 OK -> %d bytes" % len(out))
