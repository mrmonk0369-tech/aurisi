#!/usr/bin/env python3
# AURISI v58.4: Video Studio - dedicated PDF-to-Video screen.
# - New self-service screen: Home > "PDF to Video" -> upload PDF or paste
#   notes/questions -> narrated video lesson. No chat navigation needed.
# - PDF Studio actions now include Video lesson (was missing).
# - extractPdf: if the Video Studio modal is open, update it instead of
#   opening the PDF Studio panel; toast text made context-neutral.
# Base: AURISI.html v58.3. Idempotent: no-op if already v58.4.
import sys, io

BS = chr(92)

def Q(s):
    return s.replace('~B~', BS)

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="58.4"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v58.4 - no-op")
    sys.exit(0)

assert 'APP_VERSION="58.3"' in h, "base must be v58.3"

# Patch 1: extractPdf - when Video Studio modal is open, refresh it instead of
# opening the PDF Studio panel.
F1 = 'state.pdfText={name:file.name,text:text.slice(0,20000)};STUDIO_PDF_ID=null;openStudio();'
R1 = ('state.pdfText={name:file.name,text:text.slice(0,20000)};STUDIO_PDF_ID=null;'
      'if(document.getElementById("vstudioModalBack")){var _vn=document.getElementById("vsFileName");'
      'if(_vn)_vn.textContent=state.pdfText.name.slice(0,40)}else openStudio();')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# Patch 2: context-neutral toast
F2 = 'pages read) \u2014 tap Make notes")'
R2 = 'pages read)")'
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# Patch 3: PDF Studio actions - add Video lesson
F3 = '["\U0001F3A7 Podcast",()=>{switchView("chat");makePodcast()}],'
R3 = '["\U0001F3A7 Podcast",()=>{switchView("chat");makePodcast()}],["🎬 Video lesson",()=>{switchView("chat");makeVideoLesson()}],'
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# Patch 4: Home agent card - PDF to Video (self-service)
F4 = '<small>Start a fresh chat on any subject or topic</small></span></button>\';'
R4 = ('<small>Start a fresh chat on any subject or topic</small></span></button>\';\n'
      '  html+=\'<button class="agent-card" onclick="openVideoStudio()"><span class="agent-ico">🎬</span>'
      '<span><b>PDF to Video</b><small>Upload any PDF or notes \u2014 learn it as a video lesson</small></span></button>\';')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# Patch 5: Video Studio functions before renderStudio
F5 = 'function renderStudio(){'
HUB = Q(r'''function openVideoStudio(){
  var old=document.getElementById("vstudioModalBack");if(old)old.remove();
  var b=document.createElement("div");b.className="modal-back open";b.id="vstudioModalBack";
  b.onclick=function(e){if(e.target===b)b.remove()};
  var m=document.createElement("div");m.className="modal feat-modal";
  m.innerHTML='<h2>🎬 Video Studio</h2><div class="sub">Turn any material into a narrated video lesson ~B~u2014 no chat needed.</div>'
  +'<div class="feat-sec"><b>1 ~B~u00b7 UPLOAD PDF</b><div class="feat-row"><span id="vsFileName">'+escH(state.pdfText?state.pdfText.name.slice(0,40):"No file chosen")+'</span><small>Text PDFs up to 20 pages</small></div>'
  +'<button class="btn" style="width:100%;margin-top:8px" onclick="document.getElementById(~B~'vsFile~B~').click()">📄 Choose PDF</button>'
  +'<input type="file" id="vsFile" accept="application/pdf" style="display:none" onchange="vsFileChosen(this)"></div>'
  +'<div class="feat-sec" style="margin-top:10px"><b>2 ~B~u00b7 OR PASTE NOTES / QUESTIONS</b>'
  +'<textarea id="vsNotes" placeholder="Paste notes, questions or any study material here~B~u2026" style="width:100%;min-height:90px;margin-top:8px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--text);font-size:14px;resize:vertical;font-family:inherit"></textarea></div>'
  +'<button class="btn" style="width:100%;margin-top:10px" onclick="vsCreate()">🎬 Create video lesson</button>'
  +'<button class="btn" style="width:100%;margin-top:6px" onclick="vsClose()">Close</button>';
  b.appendChild(m);document.body.appendChild(b);
}
function vsClose(){var x=document.getElementById("vstudioModalBack");if(x)x.remove()}
function vsFileChosen(inp){if(inp.files&&inp.files[0])extractPdf(inp.files[0],inp);inp.value=""}
function vsCreate(){
  var t="";try{t=(document.getElementById("vsNotes")||{}).value||""}catch(e){}
  if(t.trim()){state.pdfText={name:"My notes",text:t.slice(0,20000)};STUDIO_PDF_ID=null;showPdfChip()}
  if(!state.pdfText){toast("Choose a PDF or paste notes first");return}
  vsClose();switchView("chat");makeVideoLesson();
}
''')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, HUB + F5)

# Patch 6: version bump
F6 = 'var APP_VERSION="58.3"'
R6 = 'var APP_VERSION="58.4"'
assert h.count(F6) == 1
h = h.replace(F6, R6)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied video studio patches, size: %d bytes" % len(h.encode("utf-8")))
