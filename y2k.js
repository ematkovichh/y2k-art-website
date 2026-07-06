const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];

/* intro / XP desktop */
const intro=$('#intro');
function enterArchive(){intro.classList.add('gone');document.body.style.overflow='';}
$('#enterBtn').addEventListener('click',enterArchive);
$('#bootBtn').addEventListener('click',enterArchive);
/* centered ENTER alert -> enter + go to first room (like the navbar) */
$('#alertEnter').addEventListener('click',()=>{enterArchive();setTimeout(()=>document.getElementById('crystal')?.scrollIntoView({behavior:'smooth'}),650);});
document.body.style.overflow='hidden';

/* navbar X = back to the landing / desktop */
$('.navx').addEventListener('click',()=>{intro.classList.remove('gone');document.body.style.overflow='hidden';window.scrollTo({top:0});});

/* close popups via X */
$$('.popup .winx').forEach(x=>x.addEventListener('click',e=>{e.stopPropagation();x.closest('.popup').style.display='none';}));
/* welcome window X = enter */
$('.welcome .winx').addEventListener('click',enterArchive);

/* double-click desktop to enter */
intro.addEventListener('dblclick',e=>{if(!e.target.closest('.win')&&!e.target.closest('.startmenu')&&!e.target.closest('.taskbar'))enterArchive();});

/* navigator is primary nav: from the landing, a tab enters the archive then scrolls */
function goHome(){intro.classList.remove('gone');document.body.style.overflow='hidden';window.scrollTo({top:0});}
$$('.nav-tabs a').forEach(a=>a.addEventListener('click',e=>{
  if(a.dataset.room==='top'){e.preventDefault();goHome();return;}        // HOME = back to desktop
  if(!intro.classList.contains('gone')){
    const id=a.getAttribute('href');enterArchive();
    if(id){e.preventDefault();setTimeout(()=>document.querySelector(id)?.scrollIntoView({behavior:'smooth'}),650);}
  }
}));

/* pixel companion follows the XP arrow with lag, + low-pixel spark trail
   (fine pointers only — touch devices synthesize mousemove but never see the trail) */
const FINE_POINTER=matchMedia('(pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion: reduce)').matches;
if(FINE_POINTER){
  const pix=$('#pixie');let cx=0,cy=0,tx=0,ty=0,lastSpark=0;
  const COLORS=['#ff5fa2','#7af9ff','#ffd9a0','#c9b6ff','#ffffff'];
  addEventListener('mousemove',e=>{
    tx=e.clientX;ty=e.clientY;
    if(performance.now()-lastSpark>45){
      lastSpark=performance.now();
      const s=document.createElement('div');s.className='spark';
      s.style.left=(tx+(Math.random()*16-8))+'px';s.style.top=(ty+(Math.random()*16-8))+'px';
      s.style.background=COLORS[Math.random()*COLORS.length|0];
      document.body.appendChild(s);setTimeout(()=>s.remove(),700);
    }
  });
  (function loop(){cx+=(tx-cx)*.16;cy+=(ty-cy)*.16;pix.style.left=(cx+16)+'px';pix.style.top=(cy+16)+'px';requestAnimationFrame(loop);})();
}

/* diamond dropdown */
const navDrop=$('#navDrop');
navDrop.querySelector('.drop-toggle').addEventListener('click',e=>{e.stopPropagation();navDrop.classList.toggle('open');});
document.addEventListener('click',e=>{if(!e.target.closest('#navDrop'))navDrop.classList.remove('open');});
$$('.dropdown a').forEach(a=>a.addEventListener('click',()=>navDrop.classList.remove('open')));

/* interactive spinning CD */
const cdDisc=$('#cdDisc'),cdBtn=$('#cdBtn');
function cdToggle(){const on=cdDisc.classList.toggle('playing');cdBtn.textContent=on?'⏸ pause memory':'▶ play memory';}
cdDisc.addEventListener('click',cdToggle);cdBtn.addEventListener('click',cdToggle);

/* liquified CRT notepad — readable pixel typewriter, click to pause/play + ripple */
const crtText=$('#crtText'),crtScreen=$('#crtScreen'),npWin=$('#npWin'),npPaused=$('#npPaused');
const LYRIC="I listen to a lotta True Crime\nI listen to it at night\nI like the girl talk vibes\nThey make me feel alright\nI like scary stories in the morning\nAnd I like 'em at night\nI like the girl talk vibes\nThey make me feel just fine\nI listen to a lotta true crime\n\nI like scary stories in the morning,\nand I like them at night\ntrue crime... true crime...";
let ci=0,crtTimer,crtPaused=false;
function crtType(){
  if(crtPaused) return;
  if(ci<=LYRIC.length){crtText.textContent=LYRIC.slice(0,ci);ci++;crtTimer=setTimeout(crtType, LYRIC[ci-1]==='\n'?240:46);}
  else{crtTimer=setTimeout(()=>{ci=0;crtType();},4200);}
}
crtType();
crtScreen.addEventListener('click',()=>{
  npWin.classList.remove('ripple');void npWin.offsetWidth;npWin.classList.add('ripple');
  crtPaused=!crtPaused;npPaused.classList.toggle('show',crtPaused);
  if(!crtPaused){clearTimeout(crtTimer);crtType();}
});

/* shrine widgets close on X (cute, restores on next visit) */
$$('.widget .win-bar .x').forEach(x=>x.addEventListener('click',()=>{const w=x.closest('.widget');w.style.transition='.3s';w.style.transform='scale(.7)';w.style.opacity='0';setTimeout(()=>{w.style.display='none';},300);}));

/* interactive guestbook.exe + loading screens */
(function(){
  const form=$('#gbForm'),list=$('#gbList'),loader=$('#gbLoader'),bar=loader.querySelector('.gb-bar'),lmsg=$('#gbLoadMsg');
  const MAX_ENTRIES=40;
  let entries=null;
  try{entries=JSON.parse(localStorage.getItem('gb_entries')||'null')}catch(e){}
  if(!Array.isArray(entries)||!entries.length)entries=[{n:'yokiie',m:'first ♡ luv this lil corner of the web'},{n:'crystalfairy99',m:'the crystal room made me cry (good way)'}];
  entries=entries.slice(-MAX_ENTRIES);
  const render=()=>{list.replaceChildren(...entries.map(e=>{
    const d=document.createElement('div');d.className='gb-entry';
    const b=document.createElement('b');b.textContent=`✦ ${e.n}`;
    const p=document.createElement('p');p.textContent=e.m;
    d.append(b,p);return d;
  }));list.scrollTop=list.scrollHeight;};
  render();
  function run(msg,done){loader.classList.add('show');bar.classList.remove('go');void bar.offsetWidth;bar.classList.add('go');lmsg.textContent=msg;
    setTimeout(()=>{lmsg.textContent=done;setTimeout(()=>loader.classList.remove('show'),750);},1250);}
  form.addEventListener('submit',e=>{e.preventDefault();const n=$('#gbName').value.trim(),m=$('#gbMsg').value.trim();if(!n||!m)return;
    entries.push({n,m});entries=entries.slice(-MAX_ENTRIES);
    try{localStorage.setItem('gb_entries',JSON.stringify(entries))}catch(_){}render();form.reset();run('saving…','✓ saved ♡');});
  new IntersectionObserver((es,o)=>es.forEach(x=>{if(x.isIntersecting){run('loading…','✓ loaded');o.disconnect();}}),{threshold:.35}).observe($('#gbApp'));
})();

/* scroll reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.12,rootMargin:'0px 0px -8% 0px'});
$$('.rv').forEach(el=>io.observe(el));

/* progress rail + active room (element refs cached, work batched into rAF) */
const rooms=$$('section[data-room]'),rail=$('#rail'),navTabs=$$('.nav-tabs a');
let railTick=false;
addEventListener('scroll',()=>{
  if(railTick)return;railTick=true;
  requestAnimationFrame(()=>{railTick=false;
    const h=document.documentElement;
    rail.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';
    let cur=null;rooms.forEach(r=>{if(r.getBoundingClientRect().top<innerHeight*.5)cur=r.dataset.room;});
    navTabs.forEach(a=>a.classList.toggle('on',a.dataset.room===cur));
  });
},{passive:true});

/* holographic tilt (hover-driven, so fine pointers only) */
if(FINE_POINTER)$$('.tilt').forEach(el=>{
  el.addEventListener('mousemove',e=>{const r=el.getBoundingClientRect();const px=(e.clientX-r.left)/r.width-.5;const py=(e.clientY-r.top)/r.height-.5;
    el.style.transform=`perspective(900px) rotateY(${px*9}deg) rotateX(${-py*9}deg) scale(1.02)`;});
  el.addEventListener('mouseleave',()=>el.style.transform='');
});

/* keyboard access for the clickable window chrome (spans/divs styled as XP controls) */
[['.popup .winx','close window'],['.welcome .winx','enter the archive'],['.navx','back to desktop'],
 ['.widget .win-bar .x','close widget'],['#crtScreen','pause or resume the notepad typewriter'],['#cdDisc','spin the CD']]
.forEach(([sel,label])=>$$(sel).forEach(el=>{
  el.setAttribute('role','button');el.setAttribute('tabindex','0');el.setAttribute('aria-label',label);
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click();}});
}));
