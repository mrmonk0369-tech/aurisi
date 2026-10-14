#!/usr/bin/env python3
# AURISI v60.66 : REAL WebGPU graph engine (GPU render + Canvas2D fallback)
import sys, io

src = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
dst = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"
h = io.open(src, encoding="utf-8").read()
assert len(h.encode("utf-8")) == 1776360, "base size mismatch: %d" % len(h.encode("utf-8"))
assert 'APP_VERSION="60.65"' in h

GPU = r'''
/* ===== v60.66 WebGPU ENGINE: graphs render on the GPU (2048 samples, instant) ===== */
var AURISI_GPU={ready:false,device:null,pipeline:null,format:null,note:""};
(function(){
  function boot(){
    try{
      if(!(typeof navigator!=="undefined"&&navigator.gpu&&navigator.gpu.requestAdapter))return;
      navigator.gpu.requestAdapter().then(function(ad){return ad?ad.requestDevice():null}).then(function(dev){
        if(!dev)return;
        AURISI_GPU.device=dev;AURISI_GPU.ready=true;
        AURISI_GPU.format=(navigator.gpu.getPreferredCanvasFormat?navigator.gpu.getPreferredCanvasFormat():"bgra8unorm");
        try{console.log("[AURISI] WebGPU active",AURISI_GPU.format)}catch(e){}
      }).catch(function(){});
    }catch(e){}
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot);else boot();
})();
var AURISI_GPU_WGSL="struct VOut{@builtin(position) pos:vec4f};"+
"@vertex fn vs(@location(0) p:vec2f)->VOut{var o:VOut;o.pos=vec4f(p,0.0,1.0);return o;}"+
"@fragment fn fs()->@location(0) vec4f{return vec4f(0.96,0.62,0.18,1.0);}";
function aurisiGpuPlot(cv,expr,xmin,xmax){
  try{
    var G=AURISI_GPU;if(!G.ready||!G.device||!cv)return false;
    var f=null;try{f=graphFn57(expr)}catch(e){f=null}
    if(!f)return false;
    var x1=(typeof xmin==="number"&&!isNaN(xmin))?xmin:-6.28,x2=(typeof xmax==="number"&&!isNaN(xmax))?xmax:6.28;
    if(x2<=x1){var t=x2;x2=x1;x1=t}
    var N=2048,ys=[];
    for(var i=0;i<=N;i++){var x=x1+(x2-x1)*i/N;var y;try{y=f(x)}catch(e){y=NaN}ys.push(y)}
    var fin=ys.filter(function(y){return isFinite(y)});if(!fin.length)return false;
    var y1=Math.min.apply(null,fin),y2=Math.max.apply(null,fin);
    if(y2-y1<1e-9){y1-=1;y2+=1}
    var pad=(y2-y1)*0.08;y1-=pad;y2+=pad;
    var pts=[];
    for(var i2=0;i2<N;i2++){
      var a=ys[i2],b=ys[i2+1];if(!isFinite(a)||!isFinite(b))continue;
      var xa=x1+(x2-x1)*i2/N,xb=x1+(x2-x1)*(i2+1)/N;
      pts.push(((xa-x1)/(x2-x1))*2-1,1-((a-y1)/(y2-y1))*2);
      pts.push(((xb-x1)/(x2-x1))*2-1,1-((b-y1)/(y2-y1))*2);
    }
    if(pts.length<4)return false;
    if(!cv.__wg){cv.__wg=cv.getContext("webgpu")}
    var ctx=cv.__wg;if(!ctx)return false;
    ctx.configure({device:G.device,format:G.format,alphaMode:"premultiplied"});
    if(!G.pipeline){
      var mod=G.device.createShaderModule({code:AURISI_GPU_WGSL});
      G.pipeline=G.device.createRenderPipeline({layout:"auto",
        vertex:{module:mod,entryPoint:"vs",buffers:[{arrayStride:8,attributes:[{shaderLocation:0,offset:0,format:"float32x2"}]}]},
        fragment:{module:mod,entryPoint:"fs",targets:[{format:G.format}]},
        primitive:{topology:"line-list"}});
    }
    var buf=G.device.createBuffer({size:pts.length*4,usage:GPUBufferUsage.VERTEX|GPUBufferUsage.COPY_DST});
    G.device.queue.writeBuffer(buf,0,new Float32Array(pts));
    var enc=G.device.createCommandEncoder();
    var pass=enc.beginRenderPass({colorAttachments:[{view:ctx.getCurrentTexture().createView(),
      clearValue:{r:0.04,g:0.05,b:0.07,a:1},loadOp:"clear",storeOp:"store"}]});
    pass.setPipeline(G.pipeline);pass.setVertexBuffer(0,buf);pass.draw(pts.length/2);pass.end();
    G.device.queue.submit([enc.finish()]);
    return true;
  }catch(e){return false}
}
function aurisiGpuInfo(){return {webgpu:AURISI_GPU.ready,device:!!AURISI_GPU.device,format:AURISI_GPU.format}}
'''

anchor = 'var AURISI_CAPS={webgpu:false,gpuAdapter:null,offline:false,sw:false,canvas2d:true};'
assert h.count(anchor) == 1
h = h.replace(anchor, GPU + anchor)

# hook the graph renderer: GPU first, Canvas2D fallback
old = 'function drawGraph57(cv,expr,xmin,xmax){'
assert h.count(old) == 1
h = h.replace(old, old + '\n  try{if(window.AURISI_GPU&&AURISI_GPU.ready&&aurisiGpuPlot(cv,expr,xmin,xmax))return}catch(eGpu){}', 1)

h = h.replace('APP_VERSION="60.65"', 'APP_VERSION="60.66"')
h = h.replace('v60.65 \u2014 ADVANCED VISUAL TUTOR (any field, step-by-step diagrams, WebGPU-ready)',
              'v60.66 \u2014 REAL WebGPU GRAPH ENGINE (GPU-rendered plots + Canvas2D fallback)')

out = h.encode("utf-8")
print("new size:", len(out))
for keep in ['APP_VERSION="60.66"', 'AURISI_GPU', 'aurisiGpuPlot', 'AURISI_GPU_WGSL', 'aurisiGpuInfo',
             'function drawGraph57(cv,expr,xmin,xmax){', 'createRenderPipeline', 'line-list']:
    assert keep in h, "missing: " + keep
io.open(dst, "w", encoding="utf-8").write(h)
print("build_v6066 OK -> %d bytes" % len(out))
