#!/usr/bin/env python3
# AURISI v60.8: Upload Progress.
# A floating progress bar now shows "PDF kitna % hua" for every PDF path:
#  1) Chat / Video-Lesson attach (extractPdf): FileReader % + per-page %
#  2) Book library import (rdOnFile): per-page % up to 400 pages
#  3) Exam PDF uploads (examFiles): per-file + per-page %, file k/n
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.7. Idempotent: no-op if already v60.8.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.8"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.8 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.7"' in h, "base must be v60.7"

# P1: helper overlay + instrumented extractPdf
F1 = Q('''function extractPdf(file,ev){
  if(!window.pdfjsLib){toast("PDF engine still loading — try again in a second");ev.target.value="";return}
  try{pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"}catch(e){}
  const reader=new FileReader();
  reader.onload=async()=>{
    try{
      const pdf=await pdfjsLib.getDocument({data:reader.result}).promise;
      let text="";
      const MAXP=20;
      for(let i=1;i<=pdf.numPages&&i<=MAXP;i++){
        const page=await pdf.getPage(i);
        const tc=await page.getTextContent();
        text+=tc.items.map(t=>t.str).join(" ")+"~B~n";
      }
      if(!text.trim()){toast("No readable text found — is it a scanned PDF?");ev.target.value="";return}
      state.pdfText={name:file.name,text:text.slice(0,20000)};STUDIO_PDF_ID=null;if(document.getElementById("vstudioModalBack")){var _vn=document.getElementById("vsFileName");if(_vn)_vn.textContent=state.pdfText.name.slice(0,40)}else openStudio();
      showPdfChip();
      toast("PDF attached ("+Math.min(pdf.numPages,MAXP)+" pages read)");
    }catch(e){toast("Could not read this PDF")}
    ev.target.value="";
  };
  reader.readAsArrayBuffer(file);
}''')
R1 = Q('''function uploadProg(pct,label){
  var b=document.getElementById("upBar");
  if(!b){b=document.createElement("div");b.id="upBar";
    b.style.cssText="position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:99999;min-width:250px;max-width:86vw;background:#111827;color:#fff;border-radius:12px;padding:10px 14px;box-shadow:0 8px 24px rgba(0,0,0,.35);font-size:13px;font-family:inherit";
    b.innerHTML='<div style="display:flex;justify-content:space-between;gap:12px;margin-bottom:6px"><span id="upBarN" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></span><span id="upBarP" style="font-weight:700;flex-shrink:0"></span></div><div style="height:6px;border-radius:3px;background:rgba(255,255,255,.18);overflow:hidden"><div id="upBarF" style="height:100%;width:0%;border-radius:3px;background:linear-gradient(90deg,#22c55e,#a3e635);transition:width .25s"></div></div>';
    document.body.appendChild(b);}
  try{
    var n=document.getElementById("upBarN"),p=document.getElementById("upBarP"),fl=document.getElementById("upBarF");
    if(label&&n)n.textContent=label;
    var v=Math.max(1,Math.min(100,Math.round(pct)));
    if(p)p.textContent=v+"%";
    if(fl)fl.style.width=v+"%";
  }catch(e){}
}
function uploadDone(ok){
  var b=document.getElementById("upBar");if(!b)return;
  try{var p=document.getElementById("upBarP"),fl=document.getElementById("upBarF");
    if(ok&&fl){fl.style.width="100%";if(p)p.textContent="100%"}
  }catch(e){}
  setTimeout(function(){var x=document.getElementById("upBar");if(x&&x.parentNode)x.parentNode.removeChild(x)},700);
}
function extractPdf(file,ev){
  if(!window.pdfjsLib){toast("PDF engine still loading — try again in a second");ev.target.value="";return}
  try{pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"}catch(e){}
  uploadProg(2,"📄 "+file.name);
  const reader=new FileReader();
  try{reader.onprogress=function(e2){if(e2.lengthComputable&&e2.total)uploadProg(2+23*(e2.loaded/e2.total))}}catch(e3){}
  reader.onload=async()=>{
    try{
      uploadProg(28,"📄 "+file.name);
      const pdf=await pdfjsLib.getDocument({data:reader.result}).promise;
      let text="";
      const MAXP=20;
      const NP=Math.min(pdf.numPages,MAXP)||1;
      for(let i=1;i<=pdf.numPages&&i<=MAXP;i++){
        const page=await pdf.getPage(i);
        const tc=await page.getTextContent();
        text+=tc.items.map(t=>t.str).join(" ")+"~B~n";
        uploadProg(28+67*(i/NP),"📄 "+file.name+" — page "+i+" / "+NP);
      }
      if(!text.trim()){uploadDone(false);toast("No readable text found — is it a scanned PDF?");ev.target.value="";return}
      state.pdfText={name:file.name,text:text.slice(0,20000)};STUDIO_PDF_ID=null;if(document.getElementById("vstudioModalBack")){var _vn=document.getElementById("vsFileName");if(_vn)_vn.textContent=state.pdfText.name.slice(0,40)}else openStudio();
      showPdfChip();
      uploadDone(true);
      toast("PDF attached ("+Math.min(pdf.numPages,MAXP)+" pages read)");
    }catch(e){uploadDone(false);toast("Could not read this PDF")}
    ev.target.value="";
  };
  reader.readAsArrayBuffer(file);
}''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: book library import - per-page progress
F2 = Q('''  toast("⏳ Extracting your book...");
  f.arrayBuffer().then(function(buf){return pdfjsLib.getDocument({data:buf}).promise}).then(function(pdf){
    var n=Math.min(pdf.numPages,400),parts=[],done=0;
    function nextPage(i){pdf.getPage(i).then(function(pg){return pg.getTextContent()}).then(function(tc){
      var line="",lines=[];(tc.items||[]).forEach(function(it){line+=it.str;if(it.hasEOL){lines.push(line);line=""}});if(line)lines.push(line);
      parts.push(lines.join(" "));done++;
      if(done<n){setTimeout(function(){nextPage(done+1)},0)}else{
        rdAddBook(f.name.replace(/~B~.pdf$/i,""),parts.join("~B~n~B~n"))
      }}).catch(function(){done++;if(done<n)setTimeout(function(){nextPage(done+1)},0);else rdAddBook(f.name.replace(/~B~.pdf$/i,""),parts.join("~B~n~B~n"))});}
    nextPage(1);
  }).catch(function(){toast("Could not read this PDF — is it protected?")});''')
R2 = Q('''  uploadProg(4,"📄 "+f.name);
  f.arrayBuffer().then(function(buf){return pdfjsLib.getDocument({data:buf}).promise}).then(function(pdf){
    var n=Math.min(pdf.numPages,400),parts=[],done=0;
    uploadProg(10,"📄 "+f.name);
    function nextPage(i){pdf.getPage(i).then(function(pg){return pg.getTextContent()}).then(function(tc){
      var line="",lines=[];(tc.items||[]).forEach(function(it){line+=it.str;if(it.hasEOL){lines.push(line);line=""}});if(line)lines.push(line);
      parts.push(lines.join(" "));done++;uploadProg(10+88*(done/n),"📄 "+f.name+" — page "+done+" / "+n);
      if(done<n){setTimeout(function(){nextPage(done+1)},0)}else{
        uploadDone(true);rdAddBook(f.name.replace(/~B~.pdf$/i,""),parts.join("~B~n~B~n"))
      }}).catch(function(){done++;uploadProg(10+88*(done/n));if(done<n)setTimeout(function(){nextPage(done+1)},0);else{uploadDone(true);rdAddBook(f.name.replace(/~B~.pdf$/i,""),parts.join("~B~n~B~n"))}});}
    nextPage(1);
  }).catch(function(){uploadDone(false);toast("Could not read this PDF — is it protected?")});''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: exam PDF uploads - per-file + per-page progress
F3 = Q('''async function examFiles(inp){
  var files=[].slice.call(inp.files||[]);
  try{inp.value=""}catch(e){}
  if(!files.length)return;
  if(!window.pdfjsLib){toast("PDF engine still loading — try again in a second");return}
  try{pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"}catch(e){}
  for(const f of files){
    try{
      const buf=await f.arrayBuffer();
      const pdf=await pdfjsLib.getDocument({data:buf}).promise;
      let text="";const MAXP=20;
      for(let i=1;i<=pdf.numPages&&i<=MAXP;i++){const page=await pdf.getPage(i);const tc=await page.getTextContent();text+=tc.items.map(x=>x.str).join(" ")+"~B~n"}
      if(text.trim()){EXAM_FILES.push({name:f.name,text:text.slice(0,20000)});toast("📎 "+f.name+" added ("+Math.min(pdf.numPages,MAXP)+" pages)")}
      else toast(f.name+": no readable text — scanned PDF?")
    }catch(e){toast("Could not read "+f.name)}
  }
  renderExam();
}''')
R3 = Q('''async function examFiles(inp){
  var files=[].slice.call(inp.files||[]);
  try{inp.value=""}catch(e){}
  if(!files.length)return;
  if(!window.pdfjsLib){toast("PDF engine still loading — try again in a second");return}
  try{pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"}catch(e){}
  var fi=0;
  for(const f of files){
    var base=Math.round(100*(fi/files.length)),span=Math.round(100/files.length);
    try{
      uploadProg(base+Math.max(1,Math.round(span*0.1)),"📄 "+f.name+" ("+(fi+1)+"/"+files.length+")");
      const buf=await f.arrayBuffer();
      const pdf=await pdfjsLib.getDocument({data:buf}).promise;
      let text="";const MAXP=20;const NP2=Math.min(pdf.numPages,MAXP)||1;
      for(let i=1;i<=pdf.numPages&&i<=MAXP;i++){const page=await pdf.getPage(i);const tc=await page.getTextContent();text+=tc.items.map(x=>x.str).join(" ")+"~B~n";uploadProg(base+Math.round(span*(0.1+0.85*(i/NP2))),"📄 "+f.name+" ("+(fi+1)+"/"+files.length+")")}
      if(text.trim()){EXAM_FILES.push({name:f.name,text:text.slice(0,20000)});toast("📎 "+f.name+" added ("+Math.min(pdf.numPages,MAXP)+" pages)")}
      else toast(f.name+": no readable text — scanned PDF?")
    }catch(e){toast("Could not read "+f.name)}
    uploadProg(base+span,"📄 "+f.name);
    fi++;
  }
  uploadDone(true);
  renderExam();
}''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.7"'
R4 = 'var APP_VERSION="60.8"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Upload Progress, size: %d bytes" % len(h.encode("utf-8")))
