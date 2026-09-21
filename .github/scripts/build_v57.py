#!/usr/bin/env python3
# AURISI v57.0 builder: applies v57 Power Features patch to a v56.0 AURISI.html
import io,re,sys,os
src=sys.argv[1] if len(sys.argv)>1 else "AURISI.html"
D=os.path.dirname(os.path.abspath(__file__))
h=io.open(src,encoding='utf-8').read()
assert 'APP_VERSION="56.0"' in h and 'v57 POWER' not in h, "expected clean v56.0 input"
css=io.open(os.path.join(D,'v57_css.txt'),encoding='utf-8').read()
j=h.find('</style>')
h=h[:j]+css+h[j:]
anchor='if(pdTok){txt=txt.replace(pdTok[0],"").trim();pData=pdTok[1].split("|").map(s=>s.trim()).filter(Boolean)}'
assert h.count(anchor)==1
h=h.replace(anchor,anchor+'\n'+io.open(os.path.join(D,'v57_parse.txt'),encoding='utf-8').read(),1)
ranchor='      pbox.appendChild(btn);\n      md.appendChild(pbox);\n    }\n    const acts='
assert h.count(ranchor)==1
h=h.replace(ranchor,io.open(os.path.join(D,'v57_render.txt'),encoding='utf-8').read(),1)
i=h.find('function srsRec')
j=h.find('}catch(e){}}',i)
assert i>0 and j>i
h=h[:i]+io.open(os.path.join(D,'v57_srs.txt'),encoding='utf-8').read()+h[j+len('}catch(e){}}'):]
canchor='srsRec(pairs[idx][0],rk);'
assert h.count(canchor)==1
h=h.replace(canchor,'srsRec(pairs[idx][0],rk,pairs[idx][1]);',1)
tanchor='<button class="btn small" data-i18n="testPaperBtn" onclick="makeTestPaper()">📋 Test paper</button>'
assert h.count(tanchor)==1
h=h.replace(tanchor,tanchor+'\n      <button class="btn small" onclick="makeMindMap()">🗺️ Mind map</button>\n      <button class="btn small" onclick="makeVideoLesson()">🎬 Video lesson</button>',1)
key='testWeak()"><span class="agent-ico">📕'
i=h.find(key);assert i>0
i0=h.rfind("html+='",0,i);j=h.find("';",i);assert i0>0 and j>i
extra="html+='<button class=\"agent-card\" onclick=\"srsStudyDue()\"><span class=\"agent-ico\">🧠</span><span><b>Spaced Review</b><small>Due flashcards \\u2014 they come back right before you forget</small></span></button>';"
h=h[:j+2]+extra+h[j+2:]
sanchor='Use 3D sparingly. "+'
assert h.count(sanchor)==1
h=h.replace(sanchor,sanchor+'\n'+io.open(os.path.join(D,'v57_docs.txt'),encoding='utf-8').read(),1)
m2=re.search(r'<script>(.*?)</script>\s*</body>',h,re.S)
assert m2
h=h[:m2.end(1)]+'\n'+io.open(os.path.join(D,'v57_gjs.txt'),encoding='utf-8').read()+'\n'+h[m2.end(1):]
assert h.count('APP_VERSION="56.0"')==1
h=h.replace('APP_VERSION="56.0"','APP_VERSION="57.0"')
io.open(src,'w',encoding='utf-8').write(h)
print('built v57.0, size:',len(h.encode('utf-8')))
