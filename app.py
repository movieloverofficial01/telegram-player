import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Single-file solution containing your exact UI & Telegram Streaming Logic
HTML_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#000000">
<title>Telegram Video Player</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&family=Orbitron:wght@700&display=swap">
<style>
:root{--blue:#2f6fd6;--b2:#4c8dff;--mute:#9aa0b4;--line:#1d2440}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{background:#000}
body{margin:0;color:#fff;font:500 16px Montserrat,system-ui,sans-serif;min-height:100vh;display:grid;place-items:center;padding:max(16px,env(safe-area-inset-top)) 16px 16px}
.wrap{width:min(100%,560px)}
.back{display:inline-block;color:var(--mute);text-decoration:none;font-size:14px;margin:0 6px 10px}
.card{background:#0e0e0e;border-radius:36px;padding:16px}
.shell{border:1.5px solid #262626;border-radius:28px;padding:14px;background:linear-gradient(180deg,#05060b,#000)}
.url-box{display:flex;gap:8px;margin-bottom:14px}
.url-box input{flex:1;background:#080a12;border:1.5px solid var(--line);border-radius:12px;padding:10px 14px;color:#fff;font:inherit;font-size:14px}
.url-box button{background:var(--blue);color:#fff;border:0;border-radius:12px;padding:10px 18px;font:inherit;font-weight:700;cursor:pointer}
.stage{position:relative;aspect-ratio:16/9;background:#000;border-radius:20px;overflow:hidden;border:1.5px solid #1a2550;box-shadow:0 0 38px #2c3a8c33;user-select:none;-webkit-user-select:none;touch-action:manipulation}
.stage.fs{width:100%;height:100%;aspect-ratio:auto;border:0;border-radius:0;box-shadow:none}
.stage.hide{cursor:none}
video{position:absolute;inset:0;width:100%;height:100%;background:#000;object-fit:contain}
video::cue{background:rgba(0,0,0,.65);color:#fff;font-size:1.05em}
.tap{position:absolute;inset:0;z-index:1}
.sk{position:absolute;top:50%;width:90px;height:90px;margin-top:-45px;border-radius:50%;background:#ffffff26;display:grid;place-items:center;font-weight:700;font-size:15px;opacity:0;pointer-events:none;z-index:2;transition:opacity .15s}
.sk.l{left:8%}.sk.r{right:8%}.sk.on{opacity:1}
.big{position:absolute;left:50%;top:50%;width:72px;height:72px;transform:translate(-50%,-50%);border-radius:50%;border:2px solid #666;background:#0008;display:grid;place-items:center;color:#fff;z-index:3;cursor:pointer;opacity:0;pointer-events:none;transition:opacity .2s}
.big svg{width:34px;height:34px;fill:currentColor;margin-left:4px}
.stage.paused.show .big{opacity:1;pointer-events:auto}
.spin{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px;border:4px solid #fff3;border-top-color:#fff;border-radius:50%;z-index:2;display:none;animation:rot .9s linear infinite}
.buffering .spin{display:block}
@keyframes rot{to{transform:rotate(360deg)}}
.bar{position:absolute;left:0;right:0;bottom:0;z-index:4;padding:30px 12px 8px;background:linear-gradient(transparent,#000d);opacity:0;pointer-events:none;transition:opacity .25s}
.stage.show .bar{opacity:1;pointer-events:auto}
.stage.fs .bar{padding:40px max(18px,env(safe-area-inset-right)) max(12px,env(safe-area-inset-bottom)) max(18px,env(safe-area-inset-left))}
.r1{display:flex;align-items:center;gap:10px}
.t{font-size:13px;font-variant-numeric:tabular-nums;color:#eee;min-width:42px}
.t:last-child{text-align:right}
.seek{flex:1;height:34px;display:flex;align-items:center;cursor:pointer;touch-action:none}
.trk{position:relative;width:100%;height:4px;border-radius:4px;background:#ffffff40}
.buf,.prg{position:absolute;left:0;top:0;bottom:0;border-radius:4px;width:0}
.buf{background:#ffffff60}.prg{background:var(--b2)}
.dot{position:absolute;top:50%;left:0;width:14px;height:14px;margin:-7px;border-radius:50%;background:#fff}
.r2{display:flex;align-items:center;gap:2px}
.sp{flex:1}
.ib{background:none;border:0;color:#fff;min-width:40px;height:40px;display:grid;place-items:center;cursor:pointer;border-radius:10px;font:700 13px Montserrat,sans-serif;padding:0 4px}
.ib svg{width:24px;height:24px;fill:currentColor}
.fitb{display:none}.fs .fitb{display:grid}
.menu{position:absolute;right:10px;bottom:90px;z-index:5;width:min(230px,calc(100% - 20px));max-height:calc(100% - 110px);overflow-y:auto;background:#0c0f1af2;border:1px solid var(--line);border-radius:16px;padding:6px;display:none}
.stage.fs .menu{right:max(18px,env(safe-area-inset-right));bottom:calc(env(safe-area-inset-bottom) + 84px)}
.menu.on{display:block}
.st{color:var(--mute);font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:8px 12px 4px}
.menu button{display:block;width:100%;text-align:left;background:none;border:0;color:#fff;font:inherit;font-size:14px;padding:9px 12px;border-radius:8px;cursor:pointer}
.menu button.sel{background:var(--blue)}
.load{position:absolute;inset:0;z-index:6;background:#000;display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center}
.loading .load{display:flex}
.load h2{margin:0;font:700 clamp(18px,5.4vw,28px) Orbitron,sans-serif}
.load p{margin:0;color:#c3c8dc;font-weight:400;font-size:clamp(14px,4vw,20px)}
.ind{width:min(70%,380px);height:4px;border-radius:4px;background:#161b2e;overflow:hidden;position:relative;margin-top:6px}
.ind i{position:absolute;top:0;bottom:0;width:40%;background:var(--b2);border-radius:4px;animation:ind 1.3s ease-in-out infinite}
@keyframes ind{0%{left:-40%}100%{left:100%}}
.toast{position:absolute;top:12px;left:50%;transform:translateX(-50%);z-index:7;background:#000b;padding:6px 14px;border-radius:999px;font-size:13px;opacity:0;pointer-events:none;transition:opacity .2s;white-space:nowrap}
.stage.fs .toast{top:max(12px,env(safe-area-inset-top))}
.toast.on{opacity:1}
.ctl{display:flex;flex-wrap:wrap;align-items:center;gap:10px 12px;margin-top:16px;color:var(--mute)}
.ctl svg{width:22px;height:22px;fill:currentColor}
.lbl{display:flex;align-items:center;gap:6px;font-size:14px;font-weight:400}
.grp{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.pill{font:inherit;font-size:14px;color:var(--mute);background:#080a12;border:1.5px solid var(--line);border-radius:999px;padding:6px 16px;cursor:pointer}
.pill.on{background:var(--blue);border-color:var(--blue);color:#fff;font-weight:700}
select{font:inherit;font-size:14px;color:#e8eaf5;background:#080a12;border:1.5px solid var(--line);border-radius:12px;padding:8px 30px 8px 12px;appearance:none;-webkit-appearance:none;cursor:pointer}
.err{color:#ff8a8a;font-size:14px;margin:12px 4px 0;display:none}
</style></head>
<body><div class="wrap">
<div class="card"><div class="shell">
 <div class="url-box">
  <input type="text" id="videoUrlInput" placeholder="Paste Telegram / Direct Video URL...">
  <button onclick="startPlay()">Play</button>
 </div>
 <div class="stage show" id="stage">
  <video id="v" playsinline preload="metadata"></video>
  <div class="tap" id="tap"></div>
  <div class="sk l" id="skl"></div><div class="sk r" id="skr"></div>
  <div class="spin"></div><div class="toast" id="toast"></div>
  <button class="big" id="big" aria-label="Play"><svg viewBox="0 0 24 24"><path d="M6 3.5v17l14-8.5z"/></svg></button>
  <div class="menu" id="menu"></div>
  <div class="load"><h2>Opening the stream</h2><p>Reaching Telegram</p><div class="ind"><i></i></div></div>
  <div class="bar" id="bar">
   <div class="r1"><span class="t" id="tc">0:00</span><div class="seek" id="seek"><div class="trk"><div class="buf" id="buf"></div><div class="prg" id="prog"></div><i class="dot" id="dot"></i></div></div><span class="t" id="td">0:00</span></div>
   <div class="r2">
    <button class="ib" id="pp" aria-label="Play/Pause"><svg viewBox="0 0 24 24" id="ppi"><path d="M7 4.5v15l12-7.5z"/></svg></button>
    <button class="ib" id="bk" aria-label="Back 10 seconds">-10</button>
    <button class="ib" id="fw" aria-label="Forward 10 seconds">+10</button>
    <button class="ib" id="mute" aria-label="Mute"><svg viewBox="0 0 24 24" id="mi"><path d="M3 9v6h4l5 4V5L7 9zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg></button>
    <span class="sp"></span>
    <button class="ib fitb" id="fit" aria-label="Fit or fill screen">Fill</button>
    <button class="ib" id="pip" aria-label="Picture in picture"><svg viewBox="0 0 24 24"><path d="M19 7h-8v6h8zm4-4H1v18h22zm-2 16.01H3V4.98h18z"/></svg></button>
    <button class="ib" id="gear" aria-label="Settings"><svg viewBox="0 0 24 24"><path d="M19.4 13a7.5 7.5 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3h-4l-.4 2.9a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.5 7.5 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1a7.4 7.4 0 0 0 1.7 1L11 21h4l.4-2.9a7.4 7.4 0 0 0 1.7-1l2.5 1 2-3.5zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z"/></svg></button>
    <button class="ib" id="fs" aria-label="Fullscreen"><svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7zM5 10h2V7h3V5H5zm12 7h-3v2h5v-5h-2zM14 5v2h3v3h2V5z"/></svg></button>
   </div>
  </div>
 </div>
 <div class="ctl">
  <span class="lbl">Quality:</span>
  <span class="grp" id="qs"><button class="pill on">Auto</button></span>
  <span class="grp"><span class="lbl">Audio:</span><select id="aud"><option>Default</option></select></span>
  <span class="grp"><span class="lbl">Subtitles:</span><select id="sub"><option value="-1">Off</option></select></span>
 </div>
 <p class="err" id="err"><span id="em"></span></p>
</div></div></div>
<script>
const $=id=>document.getElementById(id),v=$('v'),stage=$('stage'),menu=$('menu');
const fmt=s=>{if(!isFinite(s)||s<0)s=0;s=Math.floor(s);const h=s/3600|0,m=(s%3600)/60|0,r=s%60;return(h?h+':'+String(m).padStart(2,'0'):m)+':'+String(r).padStart(2,'0')};
let hideT,tapT,lastTap=0,lastSide=0,chain=0,acc=0,accDir=0,accT,dragging=false,dragF=0;

function setLoad(on){stage.classList.toggle('loading',on)}
function err(m){$('err').style.display=m?'block':'none';$('em').textContent=m||''}

function startPlay(){
 const url=$('videoUrlInput').value.trim();
 if(!url){alert('Please enter a valid URL');return}
 err('');setLoad(true);
 v.src='/proxy?url='+encodeURIComponent(url);
 v.load();
 v.play().catch(()=>{});
}

function show(){stage.classList.add('show');stage.classList.remove('hide');clearTimeout(hideT);
 if(!v.paused&&!menu.classList.contains('on')&&!dragging)hideT=setTimeout(hide,3000)}
function hide(){if(v.paused||menu.classList.contains('on')||dragging)return;stage.classList.remove('show');stage.classList.add('hide')}
$('bar').addEventListener('pointerdown',show);stage.addEventListener('mousemove',show);

v.addEventListener('loadedmetadata',()=>{if(v.duration)$('td').textContent=fmt(v.duration);setLoad(false)});
v.addEventListener('waiting',()=>stage.classList.add('buffering'));
['playing','canplay','seeked'].forEach(e=>v.addEventListener(e,()=>{stage.classList.remove('buffering');setLoad(false)}));
v.addEventListener('error',()=>{setLoad(false);stage.classList.remove('buffering');err('Stream failed to load.')});

const icoPlay='<path d="M7 4.5v15l12-7.5z"/>',icoPause='<path d="M6 4h4v16H6zm8 0h4v16h-4z"/>';
function sync(){stage.classList.toggle('paused',v.paused);$('ppi').innerHTML=v.paused?icoPlay:icoPause;show()}
['play','pause','ended'].forEach(e=>v.addEventListener(e,sync));
const toggle=()=>v.paused?v.play().catch(()=>{}):v.pause();
$('big').onclick=$('pp').onclick=toggle;

function paint(f){$('prog').style.width=f*100+'%';$('dot').style.left=f*100+'%';$('tc').textContent=fmt(f*(v.duration||0))}
v.addEventListener('timeupdate',()=>{if(!dragging&&v.duration)paint(v.currentTime/v.duration)});
const frac=e=>{const r=$('seek').getBoundingClientRect();return Math.min(Math.max((e.clientX-r.left)/r.width,0),1)};
$('seek').addEventListener('pointerdown',e=>{if(!v.duration)return;dragging=true;dragF=frac(e);paint(dragF);show()});
$('seek').addEventListener('pointermove',e=>{if(dragging){dragF=frac(e);paint(dragF)}});
$('seek').addEventListener('pointerup',()=>{if(!dragging)return;dragging=false;v.currentTime=dragF*v.duration;show()});

function seekBy(d){v.currentTime=Math.min(Math.max(v.currentTime+d*10,0),v.duration||1e9);show()}
$('bk').onclick=()=>seekBy(-1);$('fw').onclick=()=>seekBy(1);

$('tap').addEventListener('click',e=>{
 const r=stage.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,side=x<.35?-1:x>.65?1:0,now=Date.now();
 if(now-lastTap<300&&side===lastSide){clearTimeout(tapT);lastTap=0;if(side)seekBy(side);else toggle();return}
 lastTap=now;lastSide=side;clearTimeout(tapT);
 tapT=setTimeout(()=>{if(stage.classList.contains('show')&&!v.paused)hide();else show()},300)});

const isFs=()=>!!(document.fullscreenElement||document.webkitFullscreenElement);
$('fs').onclick=()=>{if(isFs())document.exitFullscreen();else stage.requestFullscreen()};
document.addEventListener('fullscreenchange',()=>stage.classList.toggle('fs',isFs()));
</script></body></html>"""

@app.route('/')
def index():
    return HTML_PAGE

@app.route('/proxy')
def proxy():
    video_url = request.args.get('url')
    if not video_url:
        return "No URL provided", 400

    try:
        req = requests.get(video_url, stream=True)
        return Response(
            req.iter_content(chunk_size=1024),
            status=req.status_code,
            headers=dict(req.headers)
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
