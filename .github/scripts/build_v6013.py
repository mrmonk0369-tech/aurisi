#!/usr/bin/env python3
# AURISI v60.13: Chalkboard Video Lesson.
#  1) PEN-WRITING REVEAL: during playback each bullet is "written" onto the
#     smart board with a left-to-right chalk animation synced to narration.
#  2) SAVE VIDEO button: renders the whole lesson to a 1280x720 chalkboard
#     canvas with Gemini TTS narration, records via the browser's native
#     MediaRecorder (zero downloads, zero cost) and saves a .webm video file
#     students can keep or share on WhatsApp.
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.12. Idempotent: no-op if already v60.13.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.13"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.13 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.12"' in h, "base must be v60.12"

# P1: chalk-writing reveal (slides box, DOM playback)
F1 = Q('''          var items=[].slice.call(ul.children);
          items.forEach(function(it){it.style.transition="opacity .35s,transform .35s";it.style.opacity="1";it.style.transform="none"});
          revealB=function(n){items.forEach(function(it,i){it.style.opacity=i<=n?"1":"0.15";it.style.transform=(i===n)?"scale(1.04)":"none"})};''')
R1 = Q('''          var items=[].slice.call(ul.children);
          items.forEach(function(it){it.style.transition="opacity .35s,transform .35s";it.style.opacity="1";it.style.transform="none";it.style.clipPath="none"});
          revealB=function(n){items.forEach(function(it,i){
            if(i<n){it.style.opacity="1";it.style.transform="none";it.style.clipPath="none"}
            else if(i===n){
              it.style.opacity="1";it.style.transform="scale(1.03)";
              var len=(it.textContent||"").length||24;
              var dur=Math.max(1.1,Math.min(3.2,len*0.05));
              try{
                it.style.transition="none";it.style.clipPath="inset(0 100% 0 0)";
                var f1=it;
                requestAnimationFrame(function(){requestAnimationFrame(function(){
                  f1.style.transition="clip-path "+dur+"s steps(26,end)";
                  f1.style.clipPath="inset(0 0 0 0)";
                })});
              }catch(e2){it.style.clipPath="none"}
            }
            else{it.style.opacity="0.15";it.style.transform="none";it.style.clipPath="inset(0 100% 0 0)"}
          })};''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: Save Video button
F2 = Q('''        const nextB=document.createElement("button");nextB.className="btn small soft";nextB.textContent="~B~u23ED";
        bar.appendChild(prevB);bar.appendChild(playB);bar.appendChild(nextB);''')
R2 = Q('''        const nextB=document.createElement("button");nextB.className="btn small soft";nextB.textContent="~B~u23ED";
        const recB=document.createElement("button");recB.className="btn small soft";recB.textContent="~B~u23FA Video";recB.title="Save this lesson as a video file";
        bar.appendChild(prevB);bar.appendChild(playB);bar.appendChild(nextB);bar.appendChild(recB);''')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: recordLesson engine — inserted after playB.onclick
F3 = Q('''        playB.onclick=()=>{
          if(playing){stopSpeak();return}
          playing=true;playB.textContent="~B~u23F8 Stop";try{speechSynthesis.cancel()}catch(e){}
          speakSlide();
        };''')
R3 = Q('''        playB.onclick=()=>{
          if(playing){stopSpeak();return}
          playing=true;playB.textContent="~B~u23F8 Stop";try{speechSynthesis.cancel()}catch(e){}
          speakSlide();
        };
        async function recordLesson(){
          if(recB.disabled)return;
          if(!window.MediaRecorder){toast("Video save is not supported in this browser");return}
          var vkey=(localStorage.getItem(STORAGE+"geminiKey")||(cfgGet("ai_house_key")||"")).trim();
          if(!vkey){toast("Video voice needs an AI key — set one in Settings");return}
          recB.disabled=true;recB.textContent="~B~u23F3 Recording~B~u2026";
          toast("Recording video lesson~B~2026");
          var actx=null;
          try{
            var AC=window.AudioContext||window.webkitAudioContext;
            actx=new AC();
            var dest=actx.createMediaStreamDestination();
            var jobs=[];
            slides.forEach(function(s){
              var narr=s.n||((s.t+". ")+s.b.join(". "));
              var sents=narr.match(/[^.!?]+[.!?]+/g)||[narr];
              var nb=Math.max(1,s.b.length);
              var cs=[];
              for(var ci=0;ci<nb;ci++){
                var share=Math.ceil(sents.length/nb);
                var seg=sents.slice(ci*share,(ci+1)*share).join(" ");
                if(!seg)seg=s.b[ci]||s.t;
                if(ci===0&&!s.n)seg=s.t+". "+seg;
                cs.push(cleanForSpeech(plainMath(seg)));
              }
              jobs.push(cs);
            });
            var totalChunks=0;
            for(var tc=0;tc<jobs.length;tc++)totalChunks+=jobs[tc].length;
            var doneChunks=0;
            var bufs=[];
            for(var sj=0;sj<jobs.length;sj++){
              var row=[];
              for(var cj=0;cj<jobs[sj].length;cj++){
                var buf=null;
                try{
                  var r2=await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent",{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":vkey},body:JSON.stringify({contents:[{parts:[{text:String(jobs[sj][cj]).slice(0,1200)}]}],generationConfig:{responseModalities:["AUDIO"],speechConfig:{voiceConfig:{prebuiltVoiceConfig:{voiceName:getAiVoice()}}}}})});
                  if(r2.ok){var d2=await r2.json();
                    var part=d2&&d2.candidates&&d2.candidates[0]&&d2.candidates[0].content&&d2.candidates[0].content.parts&&d2.candidates[0].content.parts[0];
                    if(part&&part.inlineData&&part.inlineData.data){
                      var m2=/rate=(~B~d+)/.exec(part.inlineData.mimeType||"");
                      var url2=pcmToWavUrl(part.inlineData.data,m2&&m2[1]?parseInt(m2[1],10):24000);
                      var ab2=await (await fetch(url2)).arrayBuffer();
                      buf=await actx.decodeAudioData(ab2);
                    }
                  }
                }catch(e3){}
                row.push(buf);
                doneChunks++;
                try{uploadProg(Math.round(100*doneChunks/totalChunks),"~B~u{1F3AC} Preparing voice "+doneChunks+" / "+totalChunks)}catch(e3b){}
              }
              bufs.push(row);
            }
            try{uploadDone(true)}catch(e3c){}
            var cv=document.createElement("canvas");cv.width=1280;cv.height=720;
            var cx=cv.getContext("2d");
            var st2=cv.captureStream(30);
            try{dest.stream.getAudioTracks().forEach(function(tk){st2.addTrack(tk)})}catch(e4){}
            var mime="";
            try{mime=["video/webm;codecs=vp9,opus","video/webm;codecs=vp8,opus","video/webm"].filter(function(m3){return MediaRecorder.isTypeSupported(m3)})[0]||""}catch(e5){}
            var rec=new MediaRecorder(st2,mime?{mimeType:mime}:undefined);
            var parts2=[];
            rec.ondataavailable=function(ev2){if(ev2.data&&ev2.data.size)parts2.push(ev2.data)};
            var finished=false;
            rec.onstop=function(){
              try{
                var blob=new Blob(parts2,{type:"video/webm"});
                var url3=URL.createObjectURL(blob);
                var a=document.createElement("a");a.href=url3;a.download="Aurisi-Lesson.webm";
                document.body.appendChild(a);a.click();
                setTimeout(function(){try{URL.revokeObjectURL(url3);a.remove()}catch(e6){}},5000);
                toast("Video saved ~B~u2014 check your downloads ~B~u2705");
              }catch(e7){toast("Could not save the video")}
              recB.disabled=false;recB.textContent="~B~u23FA Video";
            };
            var segs=[],tt=0.8;
            for(var p2=0;p2<jobs.length;p2++){
              for(var q2=0;q2<jobs[p2].length;q2++){
                var dur=(bufs[p2][q2]&&bufs[p2][q2].duration)||3.2;
                segs.push({sl:p2,bl:q2,st:tt,du:dur,au:bufs[p2][q2]});
                tt+=dur+0.18;
              }
              tt+=0.45;
            }
            var total2=tt+0.8;
            rec.start(250);
            segs.forEach(function(sg){
              setTimeout(function(){
                try{
                  if(sg.au){
                    var src=actx.createBufferSource();src.buffer=sg.au;
                    src.connect(actx.destination);src.connect(dest);src.start();
                  }
                }catch(e8){}
              },sg.st*1000);
            });
            function wrapText(txt2,x,y2,maxW,lh,frac){
              var words=String(txt2).split(" ");var line="";var yy=y2;
              var full=words.join(" ");
              var budget=Math.max(0,Math.floor(full.length*(frac===undefined?1:frac)));
              var used=0;
              for(var wi=0;wi<words.length;wi++){
                var test=line?line+" "+words[wi]:words[wi];
                if(cx.measureText(test).width>maxW&&line){
                  var take=Math.max(0,budget-used);
                  if(take>=line.length){cx.fillText(line,x,yy);used+=line.length+1;}
                  else{cx.fillText(line.slice(0,take),x,yy);used+=take;return yy+lh;}
                  line=words[wi];yy+=lh;
                }else{line=test}
              }
              if(line){
                var take2=Math.max(0,budget-used);
                if(take2>=line.length){cx.fillText(line,x,yy);used+=line.length;}
                else{cx.fillText(line.slice(0,take2),x,yy);used+=take2;}
              }
              return yy+lh;
            }
            var t0=performance.now();
            function frame(){
              var el=(performance.now()-t0)/1000;
              if(el>=total2){
                if(!finished){finished=true;try{rec.stop()}catch(e9){}
                  setTimeout(function(){try{actx.close()}catch(e10){}},900);
                  return}
              }
              var cur=segs[segs.length-1];
              for(var z=0;z<segs.length;z++){if(el>=segs[z].st&&el<segs[z].st+segs[z].du){cur=segs[z];break}}
              var sl2=slides[cur.sl];
              cx.fillStyle="#1c222b";cx.fillRect(0,0,1280,720);
              cx.fillStyle="rgba(255,255,255,.05)";
              for(var gx=0;gx<1280;gx+=40)for(var gy=0;gy<720;gy+=40)cx.fillRect(gx,gy,2,2);
              cx.textAlign="left";
              cx.fillStyle="#f3d9b1";cx.font="700 40px system-ui,-apple-system,Segoe UI,sans-serif";
              var ty=wrapText((cur.sl+1)+". "+plainMath(sl2.t),90,120,1100,52,1);
              cx.font="500 30px system-ui,-apple-system,Segoe UI,sans-serif";
              var by=Math.min(ty+40,200);
              for(var bi=0;bi<sl2.b.length;bi++){
                var txt3=plainMath(sl2.b[bi]);
                var frac=bi<cur.bl?1:(bi===cur.bl?Math.min(1,Math.max(0,(el-cur.st)/cur.du)):0);
                cx.fillStyle=bi===cur.bl?"#ffffff":(bi<cur.bl?"#e8e3da":"rgba(255,255,255,.25)");
                by=wrapText("~B~u2022  "+txt3,110,by,1060,44,frac)+16;
              }
              cx.fillStyle="rgba(255,255,255,.55)";cx.font="600 22px system-ui,sans-serif";
              cx.fillText("Aurisi ~B~u2014 AI Teacher",90,672);
              cx.textAlign="right";
              cx.fillText("Slide "+(cur.sl+1)+" / "+slides.length,1190,672);
              cx.textAlign="left";
              cx.fillStyle="rgba(255,255,255,.15)";cx.fillRect(90,688,1100,6);
              cx.fillStyle="#7fbf7f";cx.fillRect(90,688,1100*Math.min(1,el/total2),6);
              requestAnimationFrame(frame);
            }
            requestAnimationFrame(frame);
          }catch(err){
            toast("Could not record video");
            recB.disabled=false;recB.textContent="~B~u23FA Video";
            try{if(actx)actx.close()}catch(e11){}
          }
        }
        recB.onclick=()=>{recordLesson()};''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

F4 = 'var APP_VERSION="60.12"'
R4 = 'var APP_VERSION="60.13"'
assert h.count(F4) == 1
h = h.replace(F4, R4)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Chalkboard Video, size: %d bytes" % len(h.encode("utf-8")))
