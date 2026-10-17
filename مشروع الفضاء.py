import http.server, socketserver, webbrowser, urllib.parse, os

PORT = 8000
LOGO_PATH = "logo.png"
HAS_LOGO = os.path.exists(LOGO_PATH)

HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>رحلة الفضاء والجاذبية</title>
<style>
:root{--text:#eaf2ff;--muted:rgba(234,242,255,.75);--a:#7c4dff;--b:#00e5ff}
*{box-sizing:border-box}
body{margin:0;font-family:"Tajawal","Cairo","Segoe UI",Tahoma,sans-serif;color:var(--text);background:#000;min-height:100vh;overflow:hidden}
#cv{position:fixed;inset:0;z-index:1}
#svgo{position:fixed;inset:0;z-index:150;pointer-events:none;width:100vw;height:100vh}
.laser{stroke:#00e5ff;stroke-width:2;stroke-dasharray:6,6;animation:dm 1.5s linear infinite;filter:drop-shadow(0 0 6px #00e5ff)}
@keyframes dm{from{stroke-dashoffset:24}to{stroke-dashoffset:0}}
header{position:fixed;top:12px;right:12px;left:12px;z-index:10;display:flex;align-items:center;gap:12px;padding:10px 16px;background:rgba(10,15,30,.75);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,.12);border-radius:16px;pointer-events:none}
header h1{margin:0;font-size:18px;background:linear-gradient(45deg,#00d2ff,#3a7bd5);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
header p{margin:2px 0 0;font-size:12px;color:var(--muted)}
.logo{height:40px;border-radius:8px}

/* شاشة الصاروخ */
#launch{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at 50% 100%,#1a1050 0,#070a1c 55%,#02030a 100%);transition:opacity .8s,visibility .8s;overflow:hidden}
#launch.hidden{opacity:0;visibility:hidden;pointer-events:none}
.tw{position:absolute;inset:0;background-image:radial-gradient(2px 2px at 20% 30%,#fff,transparent),radial-gradient(1.5px 1.5px at 70% 20%,#fff,transparent),radial-gradient(2px 2px at 85% 60%,#cde,transparent),radial-gradient(1.5px 1.5px at 10% 80%,#fff,transparent),radial-gradient(1.5px 1.5px at 45% 70%,#fff,transparent),radial-gradient(2px 2px at 60% 90%,#cde,transparent);animation:tw 3s ease-in-out infinite alternate}
@keyframes tw{from{opacity:.4}to{opacity:1}}
.word{position:absolute;top:7%;text-align:center;font-weight:900;font-size:clamp(26px,6vw,44px);background:linear-gradient(90deg,#00e5ff,#c4b5fd,#ff7aa2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.word small{display:block;font-size:.4em;font-weight:500;-webkit-text-fill-color:var(--muted);margin-top:6px}
#rocket{position:relative;width:min(300px,78vw);aspect-ratio:240/470;margin-top:8vh;animation:hover 3s ease-in-out infinite;transition:transform 1.8s cubic-bezier(.5,0,.9,.4)}
@keyframes hover{0%,100%{translate:0 0}50%{translate:0 -10px}}
#rocket.go{transform:translateY(-150vh);animation:shake .08s linear infinite}
@keyframes shake{0%{translate:-2px 0}50%{translate:2px 0}100%{translate:-2px 0}}
#rocket svg{width:100%;height:100%;overflow:visible}
.flame{transform-origin:120px 392px;animation:fl .15s ease-in-out infinite alternate}
#rocket.go .flame{transform:scaleY(2.2);animation:none}
@keyframes fl{from{transform:scaleY(.85) scaleX(.95)}to{transform:scaleY(1.2) scaleX(1.05)}}
.form{position:absolute;left:19%;right:19%;top:41%;display:flex;flex-direction:column;gap:8px;padding:12px;border-radius:14px;background:linear-gradient(180deg,#0f1f55,#070d2c);border:2px solid #4b5fa8;box-shadow:inset 0 0 14px #000,0 0 18px rgba(0,229,255,.25)}
.form h2{margin:0;font-size:14px;text-align:center;color:#fff}
.form input{width:100%;padding:9px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(0,0,10,.5);color:#fff;text-align:center;font:inherit;font-size:14px;outline:none}
.form input:focus{border-color:#00e5ff;box-shadow:0 0 12px rgba(0,229,255,.5)}
.go-btn{border:0;cursor:pointer;padding:10px;border-radius:10px;font:inherit;font-weight:800;font-size:15px;color:#fff;background:linear-gradient(135deg,#ff9a3c,#ff2e63);box-shadow:0 6px 16px rgba(255,46,99,.5);transition:.15s}
.go-btn:hover{transform:translateY(-2px);filter:brightness(1.1)}

/* شاشة الآيات */
#verses{position:fixed;inset:0;z-index:120;display:flex;align-items:center;justify-content:center;background:rgba(2,4,14,.9);backdrop-filter:blur(8px);opacity:0;visibility:hidden;transition:opacity 1s}
#verses.show{opacity:1;visibility:visible}
.vbox{width:min(700px,94vw);text-align:center;padding:30px 22px}
.hello{color:#00e5ff;font-size:16px;margin-bottom:18px}
.verse{font-family:"Amiri","Scheherazade New","Traditional Arabic",serif;font-size:clamp(28px,6.5vw,46px);line-height:2.1;color:#fff;min-height:7.5em;display:flex;align-items:center;justify-content:center;transition:opacity .8s;text-shadow:0 0 18px rgba(124,77,255,.8)}
.src{color:#c4b5fd;font-size:15px;margin:8px 0 18px}
.dots{display:flex;gap:8px;justify-content:center;margin-bottom:20px}
.dots i{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.25);transition:.3s}
.dots i.on{background:#00e5ff;box-shadow:0 0 8px #00e5ff;width:22px;border-radius:6px}
.enter{max-width:300px;width:100%}

/* بطاقات */
.planet-label{position:absolute;z-index:20;color:#fff;background:rgba(10,15,30,.85);padding:5px 10px;border-radius:8px;border:1px solid rgba(0,229,255,.3);font-size:.75rem;pointer-events:none;text-align:center;opacity:0;transition:opacity .5s;white-space:nowrap;top:0;left:0}
.planet-label.visible{opacity:1}.planet-label strong{color:#00e5ff;display:block}
.sunv{position:absolute;z-index:20;top:0;left:0;width:340px;text-align:center;pointer-events:none;opacity:0;transition:opacity .5s;font-family:"Amiri","Scheherazade New","Traditional Arabic",serif;font-size:28px;line-height:1.8;color:#ffd978;text-shadow:0 0 16px rgba(255,170,0,.95)}
.sunv.visible{opacity:1}
.sunv small{display:block;color:#fff;font-size:15px;opacity:.85;font-family:"Tajawal","Segoe UI",sans-serif}
.mo{position:fixed;inset:0;background:rgba(0,0,0,.75);backdrop-filter:blur(8px);z-index:200;display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:.3s}
.mo.active{opacity:1;visibility:visible}
.mc{background:linear-gradient(135deg,rgba(15,31,61,.96),rgba(8,17,35,.96));border:1px solid rgba(0,229,255,.4);box-shadow:0 0 40px rgba(0,229,255,.25);border-radius:20px;padding:24px;width:min(500px,92vw);max-height:85vh;overflow:auto;text-align:right}
.mc.sunmode{border-color:rgba(255,170,0,.6);box-shadow:0 0 45px rgba(255,150,0,.35)}
.mc.sunmode h3{color:#ffc247}
.mc h3{margin:0 0 10px;color:#00e5ff;font-size:1.4rem}
.wh{background:rgba(0,229,255,.1);border:1px dashed rgba(0,229,255,.4);padding:10px;border-radius:10px;text-align:center;font-weight:bold;margin:10px 0}
.wh span{color:#00e5ff}
.is{margin-top:10px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);padding:10px 12px;border-radius:12px}
.is h4{margin:0 0 4px;color:#a78bfa;font-size:.95rem}.is p{margin:0;color:var(--muted);line-height:1.7;font-size:13.5px}
.is ul{margin:0;padding:0 18px 0 0;color:var(--muted);line-height:1.8;font-size:13.5px}
.cl{margin-top:16px;width:100%;border:0;color:#fff;padding:10px;border-radius:10px;cursor:pointer;font:inherit;font-weight:bold;background:linear-gradient(135deg,var(--b),var(--a))}
.hud{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);z-index:50;background:rgba(10,15,30,.85);backdrop-filter:blur(10px);padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.12);display:flex;gap:10px;align-items:center;opacity:0;visibility:hidden;transition:.4s;font-size:13px;white-space:nowrap}
.hud.visible{opacity:1;visibility:visible}
.hb{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;padding:6px 12px;border-radius:999px;cursor:pointer;font:inherit;font-size:12px}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head><body>
<div id="cv"></div>
<svg id="svgo"><line id="laser" class="laser" style="display:none"/></svg>

<header><img class="logo" src="/logo.png" onerror="this.style.display='none'"/>
<div><h1>لوحة الكواكب التفاعلية</h1><p id="sub">انقر على أي كوكب لتعرف وزنك عليه</p></div></header>

<!-- الصاروخ -->
<div id="launch">
  <div class="tw"></div>
  <div class="word">وزنك في الفضاء<small>أدخل بياناتك داخل الصاروخ وانطلق</small></div>
  <div id="rocket">
    <svg viewBox="0 0 240 470">
      <defs>
        <linearGradient id="red" x1="0" x2="1"><stop offset="0" stop-color="#9b1030"/><stop offset=".45" stop-color="#ff5c7c"/><stop offset="1" stop-color="#a3122f"/></linearGradient>
        <linearGradient id="met" x1="0" x2="1"><stop offset="0" stop-color="#8d96a8"/><stop offset=".4" stop-color="#f4f7fc"/><stop offset="1" stop-color="#7c8598"/></linearGradient>
        <radialGradient id="fl" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#ffd54a"/><stop offset=".7" stop-color="#ff6b1a"/><stop offset="1" stop-color="#ff2e00" stop-opacity="0"/></radialGradient>
        <linearGradient id="gold" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#fff3b0"/><stop offset=".45" stop-color="#ffc400"/><stop offset="1" stop-color="#b8860b"/></linearGradient>
      </defs>
      <g class="flame"><path d="M95 392 Q120 520 145 392 Z" fill="url(#fl)"/><path d="M108 392 Q120 470 132 392 Z" fill="#fff" opacity=".85"/></g>
      <path d="M62 300 Q20 340 18 410 L62 370 Z" fill="url(#red)"/>
      <path d="M178 300 Q220 340 222 410 L178 370 Z" fill="url(#red)"/>
      <path d="M96 372 L84 398 Q120 410 156 398 L144 372 Z" fill="#3b4254"/>
      <path d="M60 372 L60 120 Q60 70 120 6 Q180 70 180 120 L180 372 Q120 384 60 372Z" fill="url(#met)"/>
      <path d="M60 120 Q60 70 120 6 Q180 70 180 120 Z" fill="url(#red)"/>
      <path d="M78 112 Q86 62 118 24" stroke="#fff" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>
      <rect x="60" y="118" width="120" height="8" fill="#2a2f3e"/>
      <rect x="60" y="344" width="120" height="26" fill="#c4163b"/>
      <text x="120" y="364" font-size="22" font-weight="900" fill="url(#gold)" stroke="#7a5200" stroke-width=".6" text-anchor="middle" letter-spacing="3" font-family="Segoe UI,Arial,sans-serif">Tu</text>
      <circle cx="120" cy="152" r="26" fill="#3b4254"/><circle cx="120" cy="152" r="20" fill="#0a2a6b"/>
      <circle cx="120" cy="152" r="20" fill="#27c4ff" opacity=".35"/><text x="120" y="160" font-size="22" text-anchor="middle">🧑‍🚀</text>
      <path d="M108 140 Q114 132 124 134" stroke="#fff" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>
    </svg>
    <div class="form">
      <h2>جاهز للإقلاع؟ 🚀</h2>
      <input id="nameIn" placeholder="اسمك" autocomplete="off"/>
      <input id="wIn" type="number" placeholder="وزنك (كجم)" min="1" step="0.1"/>
      <button class="go-btn" onclick="launch()">إقلاع 🚀</button>
    </div>
  </div>
</div>

<!-- الآيات -->
<div id="verses"><div class="vbox">
  <div class="hello" id="hello"></div>
  <div class="verse" id="vt"></div>
  <div class="src" id="vs"></div>
  <div class="dots" id="dots"></div>
  <button class="go-btn enter" onclick="enterSpace()">ادخل المجرة 🌌</button>
</div></div>

<div id="labels"></div>
<div class="sunv" id="sunv">﴿ وَجَعَلْنَا سِرَاجًا وَهَّاجًا ﴾<small>سورة النبأ – 13 &nbsp;•&nbsp; انقر على الشمس ☀️</small></div>
<div class="planet-label" id="bhl">الثقب الأسود<strong>وزنك: ∞</strong></div>

<div class="mo" id="pm"><div class="mc" id="pcard">
  <h3 id="pt"></h3><div class="wh">وزنك عليه: <span id="pw"></span> كجم</div>
  <div class="is"><h4>📐 الحسبة</h4><p id="pmath"></p></div>
  <div class="is"><h4 id="ph4">✨ حقيقة علمية</h4><p id="pinfo"></p></div>
  <div class="is" id="pbenBox" style="display:none"><h4>🌱 فوائد الشمس</h4><ul id="pben"></ul></div>
  <button class="cl" onclick="closeP()">إغلاق 🌠</button></div></div>

<div class="hud" id="hud"><span id="hw"></span>
  <button class="hb" onclick="resetJ()">🔄 تغيير الوزن</button></div>

<script>
const VERSES=[
["وَهُوَ الَّذِي خَلَقَ اللَّيْلَ وَالنَّهَارَ وَالشَّمْسَ وَالْقَمَرَ ۖ كُلٌّ فِي فَلَكٍ يَسْبَحُونَ","سورة الأنبياء – 33"],
["وَالسَّمَاءَ بَنَيْنَاهَا بِأَيْدٍ وَإِنَّا لَمُوسِعُونَ","سورة الذاريات – 47"],
["لَا الشَّمْسُ يَنبَغِي لَهَا أَن تُدْرِكَ الْقَمَرَ وَلَا اللَّيْلُ سَابِقُ النَّهَارِ ۚ وَكُلٌّ فِي فَلَكٍ يَسْبَحُونَ","سورة يس – 40"],
["وَلَقَدْ زَيَّنَّا السَّمَاءَ الدُّنْيَا بِمَصَابِيحَ","سورة الملك – 5"],
["إِنَّ فِي خَلْقِ السَّمَاوَاتِ وَالْأَرْضِ وَاخْتِلَافِ اللَّيْلِ وَالنَّهَارِ لَآيَاتٍ لِّأُولِي الْأَلْبَابِ","سورة آل عمران – 190"]
];
const PD=[
["عطارد","Mercury",0xaaaaaa,.6,11,.015,.38,"أصغر الكواكب وأقربها للشمس، وفرق الحرارة بين ليله ونهاره هائل."],
["الزهرة","Venus",0xe3bb76,.9,17,.012,.91,"أشد الكواكب حرارة بسبب غلافه الكثيف من ثاني أكسيد الكربون."],
["الأرض","Earth",0x2266ff,1,23,.009,1,"كوكبنا، الوحيد المعروف بوجود الحياة والماء السائل."],
["المريخ","Mars",0xff4422,.7,29,.007,.38,"الكوكب الأحمر، وفيه أعلى بركان في المجموعة الشمسية: أوليمبوس مونس."],
["المشتري","Jupiter",0xd4a373,2.1,38,.004,2.53,"أكبر الكواكب، وكتلته أكبر من باقي الكواكب مجتمعة."],
["زحل","Saturn",0xf4e285,1.7,47,.003,1.07,"سيد الحلقات الجليدية، وكثافته أقل من الماء."],
["أورانوس","Uranus",0x72efdd,1.2,55,.002,.89,"عملاق جليدي يدور على جانبه."],
["نبتون","Neptune",0x4ea8de,1.2,63,.0015,1.14,"الأبعد والأكثر عاصفة، رياحه تتجاوز 2000 كم/ساعة."]
];
const SUN_G=27.9;
const SUN_BEN=[
"الضوء والدفء: بدونها تتجمد الأرض ويعمّ الظلام.",
"البناء الضوئي: تستخدمه النباتات لصنع غذائها وإنتاج الأكسجين الذي نتنفسه.",
"فيتامين D: يصنعه جلدك بتعرضه لأشعتها باعتدال، وهو مهم لقوة العظام.",
"دورة الماء: حرارتها تبخّر البحار فتتكوّن السحب والأمطار.",
"الطاقة الشمسية: تُحوَّل إلى كهرباء نظيفة عبر الألواح الشمسية.",
"الفصول والرياح والمناخ: كلها تتحرك بفعل طاقتها.",
"تنظيم الساعة الحيوية: ضوء النهار يضبط نومنا ومزاجنا."
];
let scene,camera,renderer,stars,sun,bh,bhCore,bhArc,bhDisk,planets=[],ray=new THREE.Raycaster(),mouse=new THREE.Vector2(),active=null,base=70,started=false,uname="",vi=0,vtimer;
const $=id=>document.getElementById(id);

function init(){
 scene=new THREE.Scene();
 camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,1000);camera.position.set(0,42,68);camera.lookAt(0,0,0);
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(devicePixelRatio);
 $('cv').appendChild(renderer.domElement);
 scene.add(new THREE.AmbientLight(0x444444));scene.add(new THREE.PointLight(0xffffff,2.2,400));
 const g=new THREE.BufferGeometry(),p=new Float32Array(12000);for(let i=0;i<p.length;i++)p[i]=(Math.random()-.5)*600;
 g.setAttribute('position',new THREE.BufferAttribute(p,3));
 stars=new THREE.Points(g,new THREE.PointsMaterial({color:0xffffff,size:.9,transparent:true,opacity:.8}));scene.add(stars);
 sun=new THREE.Mesh(new THREE.SphereGeometry(4.5,32,32),new THREE.MeshBasicMaterial({color:0xffaa00}));scene.add(sun);

 // الثقب الأسود
 bh=new THREE.Group();bh.position.set(-26,10,-38);
 bhCore=new THREE.Mesh(new THREE.SphereGeometry(2.2,32,32),new THREE.MeshBasicMaterial({color:0x000000}));
 const glow=new THREE.Mesh(new THREE.SphereGeometry(2.6,32,32),new THREE.MeshBasicMaterial({color:0x7c4dff,transparent:true,opacity:.35,side:THREE.BackSide}));
 bhDisk=new THREE.Mesh(new THREE.RingGeometry(3,7,64),new THREE.MeshBasicMaterial({color:0xff8a1f,side:THREE.DoubleSide,transparent:true,opacity:.45}));
 bhArc=new THREE.Mesh(new THREE.RingGeometry(3.2,6.5,64,1,0,Math.PI*1.2),new THREE.MeshBasicMaterial({color:0xfff1b0,side:THREE.DoubleSide,transparent:true,opacity:.85}));
 bhDisk.rotation.x=bhArc.rotation.x=Math.PI/2.4;
 bh.add(glow,bhCore,bhDisk,bhArc);scene.add(bh);

 PD.forEach(d=>{
  const o=new THREE.Mesh(new THREE.RingGeometry(d[4]-.05,d[4]+.05,128),new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide,transparent:true,opacity:.12}));
  o.rotation.x=Math.PI/2;scene.add(o);
  const m=new THREE.Mesh(new THREE.SphereGeometry(d[3],32,32),new THREE.MeshStandardMaterial({color:d[2],roughness:.7}));scene.add(m);
  const l=document.createElement('div');l.className='planet-label';$('labels').appendChild(l);
  planets.push({mesh:m,name:d[0],r:d[4],s:d[5],g:d[6],info:d[7],a:Math.random()*6.28,label:l});
 });
 addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
 addEventListener('click',onClick);
 animate();
}
function place(el,pos,tx,ty){
 const v=pos.clone().project(camera);
 el.style.transform=`translate(${(v.x*.5+.5)*innerWidth}px,${(v.y*-.5+.5)*innerHeight}px) translate(${tx},${ty})`;
}
function animate(){
 requestAnimationFrame(animate);
 stars.rotation.y+=.00015;sun.rotation.y+=.002;
 bhArc.rotation.z+=.03;bhDisk.rotation.z-=.01;
 planets.forEach(p=>{
  p.a+=p.s;p.mesh.position.set(Math.cos(p.a)*p.r,0,Math.sin(p.a)*p.r);p.mesh.rotation.y+=.01;
  if(started)place(p.label,p.mesh.position,'-50%','-140%');
 });
 if(started){
  place($('sunv'),new THREE.Vector3(0,6,0),'-50%','-100%');
  place($('bhl'),new THREE.Vector3(bh.position.x,bh.position.y+7,bh.position.z),'-50%','-100%');
 }
 laser();renderer.render(scene,camera);
}
function laser(){
 const L=$('laser');
 if(!$('pm').classList.contains('active')||!active){L.style.display='none';return}
 const v=active.mesh.position.clone().project(camera),b=$('pcard').getBoundingClientRect();
 L.setAttribute('x1',(v.x*.5+.5)*innerWidth);L.setAttribute('y1',(v.y*-.5+.5)*innerHeight);
 L.setAttribute('x2',b.left+b.width/2);L.setAttribute('y2',b.top+b.height/2);L.style.display='block';
}
function onClick(e){
 if(!started)return;
 mouse.set(e.clientX/innerWidth*2-1,-(e.clientY/innerHeight)*2+1);ray.setFromCamera(mouse,camera);
 const h=ray.intersectObjects([...planets.map(p=>p.mesh),bhCore,bhDisk,sun]);
 if(!h.length)return;
 const o=h[0].object;
 if(o===sun)return showSun();
 if(o===bhCore||o===bhDisk)return showBH();
 const p=planets.find(x=>x.mesh===o);if(p)showP(p);
}
function resetCard(){
 $('pcard').classList.remove('sunmode');$('pbenBox').style.display='none';$('ph4').innerText="✨ حقيقة علمية";
}
function showP(p){
 resetCard();
 active=p;$('pt').innerText=p.name;$('pw').innerText=(base*p.g).toFixed(1);
 $('pmath').innerText=`الوزن على ${p.name} = وزنك على الأرض (${base}) × معامل الجاذبية (${p.g}).`;
 $('pinfo').innerText=p.info;$('pm').classList.add('active');
}
function showSun(){
 resetCard();
 active={mesh:sun};$('pcard').classList.add('sunmode');
 $('pt').innerText="الشمس ☀️";$('pw').innerText=(base*SUN_G).toFixed(0);
 $('pmath').innerText=`جاذبية سطح الشمس ≈ ${SUN_G} ضعف جاذبية الأرض، فالوزن = ${base} × ${SUN_G}. (حسبة نظرية فقط، فلا يمكن الوقوف عليها لأنها كرة غازية شديدة الحرارة).`;
 $('ph4').innerText="🌡️ درجة الحرارة";
 $('pinfo').innerText="سطحها حوالي 5,500°C، ولبّها حوالي 15 مليون°C حيث تحدث الاندماجات النووية التي تنتج الطاقة. والمفاجئ أن هالتها الخارجية (الإكليل) أسخن من سطحها وتتجاوز المليون°C. وهي نجم متوسط الحجم، وتتسع لأكثر من مليون كرة أرضية.";
 $('pben').innerHTML=SUN_BEN.map(t=>`<li>${t}</li>`).join('');
 $('pbenBox').style.display='block';
 $('pm').classList.add('active');
}
function showBH(){
 resetCard();
 active={mesh:bh};$('pt').innerText="الثقب الأسود ⚫";$('pw').innerText="∞";
 $('pmath').innerText="جاذبيته قوية لدرجة أن حتى الضوء لا يستطيع الهروب منه، فلا يوجد وزن يمكن قياسه، والحسبة تؤول إلى اللانهاية.";
 $('pinfo').innerText="ينشأ الثقب الأسود غالباً من انهيار نجم ضخم، وحدّه الذي لا عودة بعده يسمى أفق الحدث. والحلقة المتوهجة حوله غاز يسخن بشدة وهو يدور قبل أن يسقط فيه.";
 $('pm').classList.add('active');
}
function closeP(){active=null;$('pm').classList.remove('active')}

function launch(){
 const w=parseFloat($('wIn').value);
 if(!w||w<=0){alert("الرجاء إدخال وزن صحيح على الأرض!");return}
 base=w;uname=$('nameIn').value.trim()||"أيها المستكشف";
 $('rocket').classList.add('go');
 setTimeout(()=>{$('launch').classList.add('hidden');showVerses()},1500);
}
function showVerses(){
 $('hello').innerText=`مرحباً بك يا ${uname} ✨ تأمّل قبل أن تبدأ رحلتك`;
 $('dots').innerHTML=VERSES.map(()=>'<i></i>').join('');
 vi=0;$('verses').classList.add('show');setV();
 vtimer=setInterval(()=>{vi=(vi+1)%VERSES.length;setV()},5500);
}
function setV(){
 const t=$('vt');t.style.opacity=0;
 setTimeout(()=>{t.innerText="﴿ "+VERSES[vi][0]+" ﴾";$('vs').innerText=VERSES[vi][1];t.style.opacity=1;
  [...$('dots').children].forEach((d,i)=>d.classList.toggle('on',i===vi))},400);
}
function enterSpace(){
 clearInterval(vtimer);$('verses').classList.remove('show');started=true;
 $('sub').innerText=`أهلاً ${uname} 🌟 | وزنك: ${base} كجم | انقر على أي كوكب أو على الشمس`;
 $('hw').innerText=`وزنك على الأرض: ${base} كجم`;$('hud').classList.add('visible');
 $('sunv').classList.add('visible');$('bhl').classList.add('visible');
 planets.forEach(p=>{p.label.innerHTML=`${p.name}<strong>${(base*p.g).toFixed(1)} كجم</strong>`;p.label.classList.add('visible')});
}
function resetJ(){
 started=false;closeP();$('hud').classList.remove('visible');
 $('sunv').classList.remove('visible');$('bhl').classList.remove('visible');
 planets.forEach(p=>p.label.classList.remove('visible'));
 const r=$('rocket');r.classList.remove('go');r.style.transition='none';r.style.transform='';
 setTimeout(()=>r.style.transition='',50);$('launch').classList.remove('hidden');
}
onload=init;
</script></body></html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def send_bytes(self, status, ctype, data):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html", ""):
            return self.send_bytes(200, "text/html; charset=utf-8", HTML.encode("utf-8"))
        if path == "/logo.png" and HAS_LOGO:
            with open(LOGO_PATH, "rb") as f:
                return self.send_bytes(200, "image/png", f.read())
        self.send_bytes(404, "text/plain; charset=utf-8", b"404")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/"
        print("تم التشغيل على:", url)
        try: webbrowser.open(url)
        except: pass
        httpd.serve_forever()
