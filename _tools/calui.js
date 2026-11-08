
// '✓ 나옴' 줄을 누르면 실적 결과의 그 회사 노트로 이동(사용자 2026-10-30)
var FD=null;function feed(cb){if(FD)return cb(FD);fetch('d/earn_feed.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){FD=d.items||[];cb(FD)}).catch(function(){})}
function mmLinkDone(box){feed(function(it){var v=((document.querySelector('a[href*="p-earn.html"]')||{}).getAttribute||function(){return ''}).call(document.querySelector('a[href*="p-earn.html"]'),'href')||'';var q=(v.match(/\?v=\d+/)||[''])[0];
 box.querySelectorAll('.cn-as li.past').forEach(function(li){if(li.dataset.go)return;var n=(li.querySelector('b')||{}).textContent||'';n=n.trim();if(!n)return;
  var f=it.find(function(x){return x.name===n})||it.find(function(x){return x.name.indexOf(n)>=0||n.indexOf(x.name)>=0});if(!f)return;
  li.dataset.go=1;li.classList.add('go');var i=li.querySelector('i');if(i)i.textContent='✓ 결과 ›';li.setAttribute('role','link');li.tabIndex=0;
  li.addEventListener('click',function(){location.href='p-earn.html'+q+'#'+f.id})})})}
// 실적 일정 맨 위 요약(이번 주·오늘·아시아 추적)을 칸·줄 맞춘 모양으로(사용자 2026-10-29)
(function(){function fx(){var n=document.getElementById('next');if(!n)return;var t=n.textContent;if(n.dataset.sig===t)return;var d=[].slice.call(n.children);if(d.length<2)return;
 function part(i){var x=d[i];if(!x)return null;var b=x.querySelector('b');return {k:b?b.textContent.trim():'',v:x.textContent.replace(b?b.textContent:'','').trim()}}
 var w=part(0),td=part(1),as=part(2);var wN=(w&&w.v.match(/(\d+)곳/)||[])[1],tN=(td&&td.v.match(/(\d+)곳/)||[])[1];
 var slots=td?(td.v.match(/(장후|아시아|장전)\s*([\d:]+~?)/g)||[]):[];
 var items=as?as.v.split(/\s*·\s*/).map(function(s){var m=s.match(/^(\d+\/\d+)\s+([\d:]+)\s+(.+)$/);return m?{d:m[1],t:m[2],n:m[3]}:null}).filter(Boolean):[];
 var now=new Date(),y=now.getFullYear();
 if(!tN&&td&&/발표 없음/.test(td.v))tN='0'; // 오늘 발표 없으면 '—' 대신 0곳 + 다음 발표(사용자 2026-11-09 점검)
 var nx0=(tN==='0'&&items[0])?'<em style="display:block;font:600 12px/1.35 sans-serif;color:#8a6a2a;margin-top:3px;font-style:normal">다음 '+items[0].d+' '+items[0].n+'</em>':'';
 var h='<div class="cn-top"><div class="cn-tile"><small>이번 주</small><b>'+(wN||'—')+'<i>곳</i></b></div><div class="cn-tile"><small>오늘</small><b>'+(tN||'—')+'<i>곳</i></b>'+nx0+'</div></div>';
 if(slots.length)h+='<div class="cn-sl"><small>오늘 발표 시각</small><div>'+slots.map(function(s){var m=s.match(/(장후|아시아|장전)\s*([\d:]+)/);return '<span class="'+(m[1]==='장전'?'pre':'')+'"><em>'+m[1]+'</em>'+m[2]+'</span>'}).join('')+'</div></div>';
 if(items.length)h+='<div class="cn-as"><small>아시아 실시간 추적</small><ul>'+items.map(function(it){var p=it.d.split('/'),hm=it.t.split(':');var dt=new Date(y,+p[0]-1,+p[1],+hm[0],+hm[1]);var past=dt<now;return '<li class="'+(past?'past':'')+'"><span class="d">'+it.d+'</span><span class="t">'+it.t+'</span><b>'+it.n+'</b><i>'+(past?'✓ 나옴':'예정')+'</i></li>'}).join('')+'</ul></div>';
 var box=n.querySelector('.cn');if(!box){box=document.createElement('div');box.className='cn';n.appendChild(box)}box.innerHTML=h;mmLinkDone(box);n.classList.add('cn-on');n.dataset.sig=n.textContent.replace(box.textContent,'')===t?t:t}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,400)})();
try{new MutationObserver(function(){try{var n=document.getElementById('next');if(n&&!n.querySelector('.cn'))fx()}catch(e){}}).observe(document.body,{childList:true,subtree:true})}catch(e){}})();

// 지난달 실적 보기(사용자 2026-11-02) — '이번 주 / 10월' 전환, 자료 d/cal_arc.json(실적 결과 카드에서 자동으로 쌓임)
(function(){var DAY='일월화수목금토',A=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function dt(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2])}
function md(x){return (x.getMonth()+1)+'/'+x.getDate()}
function earnHref(){var a=document.querySelector('a[href*="p-earn.html"]'),m=a&&(a.getAttribute('href')||'').match(/\?v=\d+/);return 'p-earn.html'+(m?m[0]:'')}
function rowHtml(x,h){return '<a class="mmc-row" href="'+h+'#'+esc(x.id)+'"><span class="mmc-n">'+esc(x.n)+(x.s?'<em>'+esc(x.s)+'</em>':'')+'<span class="mmc-x">'+esc(x.x)+'</span></span><span class="mmc-v'+(x.v==='호재'?' g':'')+'">'+esc(x.v||'결과')+'</span><span class="mmc-c">›</span></a>'}
function draw(ym){var box=document.getElementById('mmc-arc'),its=A.filter(function(x){return x.d.slice(0,7)===ym}),h=earnHref(),wk={};
 its.forEach(function(x){var d=dt(x.d),m=new Date(d);m.setDate(d.getDate()-((d.getDay()+6)%7));var k=m.getFullYear()+'-'+('0'+(m.getMonth()+1)).slice(-2)+'-'+('0'+m.getDate()).slice(-2);(wk[k]=wk[k]||[]).push(x)});
 var ks=Object.keys(wk).sort().reverse(),good=its.filter(function(x){return x.v==='호재'}).length,big=its.slice().sort(function(a,b){return a.r-b.r}).slice(0,3).map(function(x){return x.n}).join('·');
 var out='<div class="mmc-sum"><b>'+(+ym.slice(5))+'월 발표 '+its.length+'곳</b> · AI 관점 호재 '+good+'곳<br>'+esc(big)+' 등 · 누르면 실적 결과로 이동합니다</div>';
 ks.forEach(function(k,i){var m=dt(k),e=new Date(m);e.setDate(m.getDate()+6);var ds={};wk[k].forEach(function(x){(ds[x.d]=ds[x.d]||[]).push(x)});
  out+='<section class="mmc-wk"><button class="mmc-wh" aria-expanded="'+(i===0)+'">'+md(m)+' ~ '+md(e)+' <small>'+wk[k].length+'곳</small><em>'+(i===0?'접기 ▴':'펼치기 ▾')+'</em></button><div class="mmc-b"'+(i===0?'':' hidden')+'>'+Object.keys(ds).sort().reverse().map(function(d){var t=dt(d);return '<div class="mmc-day">'+md(t)+' '+DAY[t.getDay()]+'<i>'+ds[d].length+'곳</i></div>'+ds[d].map(function(x){return rowHtml(x,h)}).join('')}).join('')+'</div></section>'});
 box.innerHTML=out;
 box.querySelectorAll('.mmc-wh').forEach(function(b){b.addEventListener('click',function(){var w=b.nextElementSibling,o=w.hidden;w.hidden=!o;b.setAttribute('aria-expanded',o);b.querySelector('em').textContent=o?'접기 ▴':'펼치기 ▾'})})}
function pick(v){var on=v!=='now';document.body.classList.toggle('mmc-on',on);document.querySelectorAll('#mmc-tabs button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.m===v)});if(on)draw(v);try{history.replaceState(null,'',on?'#'+v:location.pathname+location.search)}catch(e){}}
function start(){var n=document.getElementById('next');if(!n||document.getElementById('mmc-tabs'))return;
 fetch('d/cal_arc.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){A=d.items||[];if(!A.length||document.getElementById('mmc-tabs'))return;
  var ms={};A.forEach(function(x){ms[x.d.slice(0,7)]=1});var ks=Object.keys(ms).sort().reverse();
  var t=document.createElement('div');t.id='mmc-tabs';t.setAttribute('role','tablist');t.innerHTML='<button role="tab" data-m="now">이번 주</button>'+ks.map(function(k){return '<button role="tab" data-m="'+k+'">'+(+k.slice(5))+'월</button>'}).join('');
  n.parentNode.insertBefore(t,n);var b=document.createElement('div');b.id='mmc-arc';n.parentNode.appendChild(b);
  t.addEventListener('click',function(e){var x=e.target.closest('button');if(x)pick(x.dataset.m)});
  var h=location.hash.slice(1);pick(ms[h]?h:'now')}).catch(function(){})}
var c=0;(function go(){start();if(++c<8&&!document.getElementById('mmc-tabs'))setTimeout(go,400)})()})();
