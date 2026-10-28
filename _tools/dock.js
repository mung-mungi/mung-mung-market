// 아래 메뉴: 자주 쓰는 칸 + ☰ 전체 메뉴판(사용자 2026-10-29) — 링크는 기존 페이지 줄(nav.ib)에서 읽음
(function(){var IC={'p-lights':'🚦','p-brief':'📰','p-prices':'📈','p-trend':'🧭','p-earn':'📑','p-cal':'🗓️','p-econ':'📊','p-bond':'🏦','p-opt':'🌡️','p-targets':'🎯','p-short':'🐻','p-fx':'💱','p-capex':'🏗️','p-policy':'🌐','p-tech':'🎤','p-supply':'🚢','p-neo':'☁️','p-qtr':'📉','p-insider':'🕵️'};
function key(a){var m=(a.getAttribute('href')||'').match(/(p-[a-z]+)\.html/);return m?m[1]:''}
function build(){var n=document.querySelector('nav.ib');if(!n||document.querySelector('.mmd'))return;var home=n.querySelector('a.home');var cur=n.querySelector('[aria-current=page]');var ck=cur?key(cur):'';
 var groups=[],g=null;[].forEach.call(n.children,function(c){if(c.classList.contains('tg')){g={t:c.textContent.trim(),l:[]};groups.push(g);return}if(c.tagName==='A'&&!c.classList.contains('home')&&g)g.l.push(c)});
 var by={};[].forEach.call(n.querySelectorAll('a'),function(a){by[key(a)]=a});
 function lab(a){return (a.textContent||'').trim().replace('데일리 ','')}
 var d=document.createElement('nav');d.className='mmd';
 var row=(home?'<a href="'+home.getAttribute('href')+'"><i>🏠</i><span>홈</span></a>':'')+groups.map(function(g,gi){return (gi?'<b class="sep"></b>':'')+g.l.map(function(a){var k=key(a);return '<a href="'+a.getAttribute('href')+'"'+(k===ck?' class="on"':'')+'><i>'+(IC[k]||'•')+'</i><span>'+lab(a)+'</span></a>'}).join('')}).join('');
 d.innerHTML='<button type="button" class="grab" aria-label="전체 메뉴"><em></em></button><div class="row">'+row+'</div>';
 var sh=document.createElement('div');sh.className='mmd-sheet';sh.hidden=true;
 sh.innerHTML='<div class="mmd-dim"></div><div class="mmd-pan"><div class="mmd-grab"></div>'+groups.map(function(g){return '<p class="mmd-g">'+g.t+'</p><div class="mmd-grid">'+g.l.map(function(a){var k=key(a);return '<a href="'+a.getAttribute('href')+'"'+(k===ck?' class="on"':'')+'><i>'+(IC[k]||'•')+'</i><span>'+lab(a)+'</span></a>'}).join('')+'</div>'}).join('')+'</div>';
 document.body.appendChild(d);document.body.appendChild(sh);document.body.classList.add('mmd-on');
 function open(o){sh.hidden=!o;document.documentElement.style.overflow=o?'hidden':''}
 d.querySelector('.grab').onclick=function(){open(sh.hidden)};
 var rw=d.querySelector('.row');var c0=rw.querySelector('.on');if(c0)rw.scrollLeft=c0.offsetLeft-rw.clientWidth/2+c0.offsetWidth/2;
 var sx=0,sy=0,s0=0,md=null;d.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;s0=rw.scrollLeft;md=null},{passive:true});
 d.addEventListener('touchmove',function(e){var t=e.touches[0],dx=t.clientX-sx,dy=t.clientY-sy;if(md===null&&(Math.abs(dx)>6||Math.abs(dy)>6))md=Math.abs(dx)>Math.abs(dy)?'x':'y';if(md==='x'){rw.scrollLeft=s0-dx}e.preventDefault()},{passive:false});
 d.addEventListener('touchend',function(e){var dy=e.changedTouches[0].clientY-sy;if(md==='y'&&dy<-25)open(true);if(md==='x'){rw.querySelectorAll('a').forEach(function(a){a.__nc=Date.now()})}md=null},{passive:true});
 rw.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&a.__nc&&Date.now()-a.__nc<350){e.preventDefault()}},true);sh.querySelector('.mmd-dim').onclick=function(){open(false)};
 var y0=null;var pan=sh.querySelector('.mmd-pan');pan.addEventListener('touchstart',function(e){y0=e.touches[0].clientY},{passive:true});pan.addEventListener('touchend',function(e){if(y0!=null&&e.changedTouches[0].clientY-y0>60&&pan.scrollTop<=0)open(false);y0=null},{passive:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',build);else build();setTimeout(build,800)})();
