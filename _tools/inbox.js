// 멍터 알림함(사용자 2026-11-06): 휴대폰 알림이 쌓여도 여기서 몰아 보기 — 메인 맨 위 '🔔 알림함 ›' + 놓친 알림 한 줄 정리 + 누르면 그 내용 자리로
(function(){try{
var LS='mm_ib_seen',seen=0;try{seen=+localStorage.getItem(LS)||0}catch(e){}
var D=null,btn=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function ts(s){return Date.parse(s)||0}
function hm(s){var d=new Date(ts(s));return ('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2)}
var WD='일월화수목금토';
function day(s){var d=new Date(ts(s)),t=new Date(),y=new Date(Date.now()-864e5);var k=d.toDateString();return (k===t.toDateString()?'오늘 · ':k===y.toDateString()?'어제 · ':'')+(d.getMonth()+1)+'.'+d.getDate()+' ('+WD[d.getDay()]+')'}
function ago(s){var m=Math.round((Date.now()-ts(s))/6e4);return m<60?m+'분 전':m<1440?Math.round(m/60)+'시간 전':Math.round(m/1440)+'일 전'}
function unread(){return D?D.items.filter(function(x){return ts(x.at)>seen}):[]}
function paint(){if(!btn||!D)return;var u=unread(),f=D.items[0];
 btn.querySelector('.t').innerHTML='';var b=el('b',null,'알림함');btn.querySelector('.t').appendChild(b);
 btn.querySelector('.t').appendChild(document.createTextNode(f?(u.length?'놓친 알림 '+u.length+'건 · ':'최근 · ')+f.title:'아직 알림이 없습니다'));
 var n=btn.querySelector('.n');n.textContent=u.length;n.hidden=!u.length}
// 놓친 알림 한 줄 정리: 종류별 개수 + 가장 앞에 둘 소식(속보 > 지표 > 실적 > 전달, 같은 종류면 최신)
function summary(u,all){var box=el('div','mm-ib-sum');
 if(!u.length){box.innerHTML='<b>새로 놓친 알림은 없습니다.</b> 최근 알림은 아래에 시간순으로 있습니다.';return box}
 var c={};u.forEach(function(x){c[x.kind]=(c[x.kind]||0)+1});
 var order=['속보','지표','실적','전달'],parts=order.filter(function(k){return c[k]}).map(function(k){return k+' '+c[k]});
 var top=null;order.some(function(k){return u.some(function(x){if(x.kind===k){top=x;return true}})});
 var first=u[u.length-1];
 box.innerHTML='<b>마지막으로 보신 뒤 놓친 알림 '+u.length+'건</b> ('+parts.join(' · ')+')<br>';
 box.appendChild(document.createTextNode('가장 먼저 볼 것: '+(top?'['+top.kind+'] '+top.title:'')+(u.length>1?' — '+ago(first.at)+'부터 쌓였습니다.':'')));
 var ks=[];u.filter(function(x){return x.kind==='실적'}).forEach(function(x){x.title.replace(/^실적 \d+곳 · /,'').replace(/ 외 \d+곳$/,'').split(' · ').forEach(function(n){n=n.split(/\s*〔/)[0].trim();if(n&&ks.indexOf(n)<0)ks.push(n)})});
 if(ks.length>1){box.appendChild(el('br'));box.appendChild(document.createTextNode('실적: '+ks.slice(0,6).join(' · ')+(ks.length>6?' 외 '+(ks.length-6)+'곳':'')))}
 return box}
function open(){if(!D)return;var u=unread(),sc=el('div','mm-ib-scrim'),sh=el('div','mm-ib-sheet');sh.setAttribute('role','dialog');
 var top=el('div','mm-ib-top');top.appendChild(el('h3',null,'🔔 알림함'));var x=el('button','x','×');x.type='button';x.setAttribute('aria-label','닫기');top.appendChild(x);sh.appendChild(top);
 var body=el('div','mm-ib-body');body.appendChild(summary(u,D.items));
 if(!D.items.length)body.appendChild(el('div','mm-ib-empty','아직 받은 알림이 없습니다.'));
 var last='';D.items.forEach(function(it){var dd=day(it.at);if(dd!==last){body.appendChild(el('div','mm-ib-day',dd));last=dd}
  var a=el('a','mm-ib-row'+(ts(it.at)>seen?' new':''));a.href=it.url||'index.html';
  var h=el('div','mm-ib-h');h.appendChild(el('span','mm-ib-k k-'+it.kind,it.kind));h.appendChild(el('span',null,hm(it.at)));if(ts(it.at)>seen)h.appendChild(el('span','dot','새 알림'));a.appendChild(h);
  a.appendChild(el('div','mm-ib-t',it.title));if(it.body)a.appendChild(el('div','mm-ib-b',it.body));body.appendChild(a)});
 sh.appendChild(body);document.body.appendChild(sc);document.body.appendChild(sh);
 function close(){sc.remove();sh.remove()}x.onclick=close;sc.onclick=close;
 seen=D.items.length?ts(D.items[0].at):Date.now();try{localStorage.setItem(LS,seen)}catch(e){}paint()}
function mount(){if(btn)return;var hd=document.querySelector('header.bn');if(!hd||!hd.parentNode)return;
 btn=el('button','mm-ib-btn');btn.type='button';btn.innerHTML='<span class="ic">🔔</span><span class="t"><b>알림함</b>불러오는 중</span><span class="n" hidden></span><span class="go">열기 ›</span>';
 btn.onclick=open;var w=el('div','mm-ib-wrap');w.appendChild(btn);hd.parentNode.insertBefore(w,hd.nextSibling);paint()}
function load(){fetch('d/inbox.json?t='+Math.floor(Date.now()/6e4),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j.items){D=j;paint()}}).catch(function(){})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){mount();load()});else{mount();load()}
setInterval(load,5*6e4);document.addEventListener('visibilitychange',function(){if(!document.hidden)load()});
}catch(e){}})();
