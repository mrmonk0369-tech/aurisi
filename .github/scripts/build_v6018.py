#!/usr/bin/env python3
# AURISI v60.18: EDIT MESSAGES + INSTALL APP.
#  1) EDIT: every sent message gets a small pencil button (top-right of the
#     bubble). Tap it -> the message text returns to the input box, history
#     is trimmed back to that point, student fixes and resends.
#  2) INSTALL: a phone-download icon appears in the topbar whenever the
#     browser allows install (Android Chrome) or on iOS Safari (not yet
#     installed). Tapping it fires the native install prompt, or shows
#     exact manual steps (Safari: Share -> Add to Home Screen; Chrome: menu
#     -> Add to Home screen). PWA icons/manifest were verified correct.
# Transport: backslashes as ~B~ (unwrapped by Q); REAL newlines only.
# Base: AURISI.html v60.17 (1851934). Idempotent.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.18"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.18 - no-op"); sys.exit(0)
assert 'APP_VERSION="60.17"' in h, "base must be v60.17"

# P1: CSS for the edit button
F1 = ".msg-row.user .bubble{position:relative;background:var(--ai-user-bg);color:var(--ai-user-text);border:2px solid var(--text);border-radius:18px 18px 5px 18px;padding:11px 15px;white-space:pre-wrap;box-shadow:3px 3px 0 var(--line)}"
R1 = F1 + "\n.msg-edit{position:absolute;top:3px;right:4px;border:0;background:rgba(255,255,255,.28);color:inherit;font-size:11px;line-height:1;padding:4px 5px;border-radius:9px;cursor:pointer;opacity:.55}\n.msg-edit:active{opacity:1;transform:scale(.9)}"
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: edit button on user messages
F2 = Q('''    b.textContent=txt;
    if(img){const im=document.createElement("img");im.className="att";im.src="data:"+(img.inline_data.mime_type||"image/jpeg")+";base64,"+img.inline_data.data;b.appendChild(im)}
    row.appendChild(b);''')
R2 = Q('''    b.textContent=txt;
    if(txt){
      const eb=document.createElement("button");eb.className="msg-edit";eb.title="Edit message";eb.setAttribute("aria-label","Edit message");
      eb.textContent="~B~u270F~B~uFE0F";
      eb.onclick=function(){
        var idx=-1;
        for(var ei=0;ei<state.chatHistory.length;ei++){if(state.chatHistory[ei]===m){idx=ei;break}}
        if(idx>-1){state.chatHistory=state.chatHistory.slice(0,idx);persist();renderChat()}
        var p2=$("prompt");
        if(p2){try{switchView("chat")}catch(e9y){};p2.value=txt;autoGrow(p2);try{p2.focus()}catch(e9z){}}
      };
      b.appendChild(eb);
    }
    if(img){const im=document.createElement("img");im.className="att";im.src="data:"+(img.inline_data.mime_type||"image/jpeg")+";base64,"+img.inline_data.data;b.appendChild(im)}
    row.appendChild(b);''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: install button in topbar (after theme button)
F3 = Q('''      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.2 5.8L20 10l-5.8 2.2L12 18l-2.2-5.8L4 10l5.8-2.2L12 2z"/></svg>
    </button>''')
R3 = Q('''      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.2 5.8L20 10l-5.8 2.2L12 18l-2.2-5.8L4 10l5.8-2.2L12 2z"/></svg>
    </button>
    <button class="icon-btn" onclick="installApp()" id="installBtn" aria-label="Install app" title="Install app" style="display:none">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
    </button>''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: install logic after sw registration (first occurrence only)
F4 = Q('''if(typeof navigator!=="undefined"&&navigator.serviceWorker){window.addEventListener("load",function(){try{navigator.serviceWorker.register("sw.js").catch(function(e){})}catch(e){}})}''')
R4 = Q('''if(typeof navigator!=="undefined"&&navigator.serviceWorker){window.addEventListener("load",function(){try{navigator.serviceWorker.register("sw.js").catch(function(e){})}catch(e){}})}
var AURISI_INSTALL=null;
window.addEventListener("beforeinstallprompt",function(e){e.preventDefault();AURISI_INSTALL=e;try{$("installBtn").style.display=""}catch(x){}});
try{
  var _standalone=window.matchMedia&&window.matchMedia("(display-mode: standalone)").matches;
  var _ios=/iphone|ipad|ipod/i.test(navigator.userAgent||"");
  if(!_standalone&&_ios){try{$("installBtn").style.display=""}catch(x3){}}
}catch(x2){}
function installApp(){
  if(AURISI_INSTALL){AURISI_INSTALL.prompt();AURISI_INSTALL.userChoice.then(function(){AURISI_INSTALL=null});return}
  var isIOS=/iphone|ipad|ipod/i.test(navigator.userAgent||"");
  toast(isIOS?"Safari: Share (up arrow) - Add to Home Screen":"Chrome: (menu) - Add to Home screen / Install app");
}''')
assert h.count(F4) >= 1, "P4 anchor not found"
h = h.replace(F4, R4, 1)

F5 = 'var APP_VERSION="60.17"'
R5 = 'var APP_VERSION="60.18"'
assert h.count(F5) == 1
h = h.replace(F5, R5)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Edit + Install, size: %d bytes" % len(h.encode("utf-8")))
