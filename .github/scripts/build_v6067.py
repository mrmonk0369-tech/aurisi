#!/usr/bin/env python3
# AURISI v60.67 : ON-DEVICE AI via WebGPU (MLC WebLLM) — offline, no key, no cost
import sys, io

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1779806, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.66"' in h

# ---------- 1. Settings panel ----------
anchor = '      <div class="s-sec-h">How Aurisi talks to you</div>'
assert h.count(anchor) == 1
PANEL = '''      <div class="s-sec-h">On this device \\u2014 works offline</div>
      <p class="hint" style="margin:6px 0 10px">Run a small AI model right here on your phone using WebGPU. Aurisi then answers with no internet, no rate limits and nothing to pay. One download, then it is yours for good.</p>
      <div id="localStatus" class="hint"></div>
      <div id="localModels" style="display:flex;flex-wrap:wrap;gap:7px;margin-top:11px"></div>
      <div id="localBarWrap" style="display:none;margin-top:12px">
        <div style="height:6px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden"><i id="localBar" style="display:block;height:100%;width:0%;background:var(--accent);border-radius:99px;transition:width .2s"></i></div>
        <div class="hint" id="localLabel" style="margin-top:6px"></div>
      </div>
      <button class="btn" id="localBtn" style="margin-top:12px;width:100%">Download and turn on</button>
      <p class="hint" style="margin-top:8px">Needs WebGPU \\u2014 Chrome on Android or a computer, or Safari 18+. The model is a few hundred MB, downloaded once and kept on your device.</p>
''' + anchor
h = h.replace(anchor, PANEL)

# ---------- 2. engine ----------
ENGINE = r'''
/* ===== v60.67 ON-DEVICE AI (WebGPU + MLC WebLLM): offline, no key, no cost ===== */
var LOCAL={engine:null,model:"",ready:false,busy:false,pct:0,label:"",err:""};
var LOCAL_WANT=[["Qwen2.5-0.5B-Instruct-q4f16_1-MLC","Tiny","~0.4 GB - fastest, most phones"],
                ["Qwen2.5-1.5B-Instruct-q4f16_1-MLC","Balanced","~1 GB - better answers"],
                ["Llama-3.2-1B-Instruct-q4f16_1-MLC","Llama 1B","~0.9 GB - good general chat"],
                ["SmolLM2-1.7B-Instruct-q4f16_1-MLC","SmolLM 1.7B","~1 GB - strong small model"]];
var LOCAL_CDN=["https://cdn.jsdelivr.net/npm/@mlc-ai/web-llm/+esm",
               "https://unpkg.com/@mlc-ai/web-llm?module",
               "https://cdn.jsdelivr.net/npm/@mlc-ai/web-llm"];
function gpuOk(){return typeof navigator!=="undefined"&&!!navigator.gpu}
function localModel(){try{return localStorage.getItem(STORAGE+"deviceModel")||LOCAL_WANT[0][0]}catch(e){return LOCAL_WANT[0][0]}}
function localOn(){try{return localStorage.getItem(STORAGE+"localAI")==="1"}catch(e){return false}}
function localReady(){return LOCAL.ready&&localOn()}
async function loadLocalEngine(){
  if(LOCAL.ready||LOCAL.busy)return;
  LOCAL.err="";
  if(!gpuOk()){LOCAL.err="This browser does not support WebGPU, so the on-device coach cannot run here. Chrome on Android or a computer, or Safari 18+, does. Until then the free cloud coach works everywhere.";renderLocalAI();return}
  LOCAL.busy=true;LOCAL.pct=0;LOCAL.label="Starting...";renderLocalAI();
  var mod=null,lastErr=null;
  for(var i=0;i<LOCAL_CDN.length;i++){try{mod=await import(LOCAL_CDN[i]);break}catch(e){lastErr=e}}
  if(!mod){LOCAL.busy=false;LOCAL.err="Could not fetch the on-device engine (one-time download). Check your connection and try again.";renderLocalAI();return}
  try{
    var engine=await mod.CreateMLCEngine(localModel(),{initProgressCallback:function(r){
      LOCAL.pct=Math.round((r.progress||0)*100);LOCAL.label=String(r.text||"").slice(0,110);renderLocalAI();
    }});
    LOCAL.engine=engine;LOCAL.ready=true;LOCAL.busy=false;LOCAL.pct=100;LOCAL.label="Ready";
    try{localStorage.setItem(STORAGE+"localAI","1")}catch(e){}
    renderLocalAI();toast("On-device coach ready - it works offline now.");
  }catch(e){
    LOCAL.busy=false;LOCAL.err="The model did not load: "+String((e&&e.message)||e).slice(0,140);renderLocalAI();
  }
}
function turnOffLocal(){
  try{if(LOCAL.engine&&LOCAL.engine.unload)LOCAL.engine.unload()}catch(e){}
  LOCAL.engine=null;LOCAL.ready=false;LOCAL.pct=0;LOCAL.label="";
  try{localStorage.setItem(STORAGE+"localAI","0")}catch(e){}
  renderLocalAI();toast("On-device coach off - back to the free cloud coach.");
}
async function localChat(userText,system){
  if(!LOCAL.ready||!LOCAL.engine)return "";
  var msgs=[];if(system)msgs.push({role:"system",content:String(system).slice(0,6000)});
  try{
    var hist=(state.chatHistory||[]).slice(-6);
    for(var i=0;i<hist.length;i++){
      var m=hist[i];if(m.role!=="user"&&m.role!=="model")continue;
      var t=((m.parts||[]).map(function(p){return p.text||""}).join(" ")).trim();
      if(t)msgs.push({role:m.role==="model"?"assistant":"user",content:t.slice(0,1500)});
    }
  }catch(e){}
  msgs.push({role:"user",content:userText});
  var r=await LOCAL.engine.chat.completions.create({messages:msgs,temperature:0.7,max_tokens:320});
  var c=r&&r.choices&&r.choices[0]&&r.choices[0].message&&r.choices[0].message.content;
  return String(c||"").trim();
}
function renderLocalAI(){
  var st=$("localStatus");if(!st)return;
  var chipBox=$("localModels"),bar=$("localBar"),barW=$("localBarWrap"),lbl=$("localLabel"),btn=$("localBtn");
  if(LOCAL.ready){st.innerHTML="<b>On-device coach is on.</b> Aurisi answers on this device - no internet, no limits, no cost."}
  else if(LOCAL.busy){st.innerHTML="<b>Downloading the model...</b> Keep this page open. One-time download."}
  else if(LOCAL.err){st.innerHTML=escH(LOCAL.err)}
  else if(!gpuOk()){st.innerHTML="This browser does not support WebGPU. Chrome on Android or a computer, or Safari 18+, does. Until then the free cloud coach works everywhere."}
  else{st.innerHTML="Your browser supports WebGPU. Pick a size, download once, and Aurisi runs here for good."}
  if(chipBox){
    chipBox.innerHTML="";
    LOCAL_WANT.forEach(function(w){
      var b=document.createElement("button");
      b.className="btn"+(localModel()===w[0]?"":" ghost");
      b.style.cssText="font-size:12px;padding:8px 12px";
      b.textContent=w[1];
      b.onclick=function(){if(LOCAL.busy||LOCAL.ready)return;try{localStorage.setItem(STORAGE+"deviceModel",w[0])}catch(e){}renderLocalAI()};
      chipBox.appendChild(b);
    });
  }
  if(lbl){var w=LOCAL_WANT.filter(function(x){return x[0]===localModel()})[0];lbl.textContent=LOCAL.busy?LOCAL.label:(w?w[1]+" - "+w[2]:"")}
  if(barW)barW.style.display=LOCAL.busy?"block":"none";
  if(bar)bar.style.width=LOCAL.pct+"%";
  if(btn){btn.textContent=LOCAL.ready?"Turn it off":(LOCAL.busy?("Downloading - "+LOCAL.pct+"%"):"Download and turn on");btn.disabled=LOCAL.busy;
    btn.onclick=function(){if(LOCAL.ready)turnOffLocal();else loadLocalEngine()}}
}
'''
anchor2 = 'var AURISI_CAPS={webgpu:false,gpuAdapter:null,offline:false,sw:false,canvas2d:true};'
assert h.count(anchor2) == 1
h = h.replace(anchor2, ENGINE + anchor2)

# ---------- 3. route replies to the device when it is on ----------
old = '''    if(key.trim()){
      full=await callGeminiStream(key,histForApi,cb,myAbort.signal,_sys)||"";'''
assert h.count(old) == 1
new = '''    if(localReady()){
      try{full=await localChat(_lu,_sys)||""}catch(eL){full=""}
      if(full)typer.push(full);
    }else if(key.trim()){
      full=await callGeminiStream(key,histForApi,cb,myAbort.signal,_sys)||"";'''
h = h.replace(old, new)

# ---------- 4. paint the panel when Settings opens ----------
old2 = 'function openSettings(){updateAcctUI();instRenderBox();proRenderBox();bizApplyMode();'
assert h.count(old2) == 1
h = h.replace(old2, old2 + '\n  try{if(typeof renderLocalAI==="function")setTimeout(renderLocalAI,0)}catch(e){}')

# ---------- 5. version ----------
h = h.replace('APP_VERSION="60.66"', 'APP_VERSION="60.67"')
h = h.replace('v60.66 \u2014 REAL WebGPU GRAPH ENGINE (GPU-rendered plots + Canvas2D fallback)',
              'v60.67 \u2014 ON-DEVICE AI (WebGPU model: offline, no key, no cost)')

out = h.encode("utf-8")
print("new size:", len(out))
for keep in ['APP_VERSION="60.67"', 'localStatus', 'LOCAL_WANT', 'CreateMLCEngine', 'localChat', 'renderLocalAI',
             'if(localReady()){', 'function drawGraph57(cv,expr,xmin,xmax){']:
    assert keep in h, "missing: " + keep
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6067 OK -> %d bytes" % len(out))
