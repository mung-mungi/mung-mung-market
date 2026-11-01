// 버전업 표시 + 바뀐 점 설명서(사용자 2026-11-02) — 자료 d/changelog.json
// 메인: 머리 아래 'v판 · 새로 바뀐 것 n ›' 알약(안 본 판이면 빨간 점) / 바뀐 페이지: 3일 동안 'NEW · 바뀐 점 ›' 알약
// 누르면 아래에서 설명서가 올라옴(새로/순서/고침 · 무엇이 · 왜 · 그 자리로 가기)
(function(){
var C=null,FILE=(location.pathname.split('/').pop()||'index.html'),MAIN=FILE==='index.html';
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function md(d){var a=String(d).split('-');return (+a[1])+'.'+(+a[2])}
function days(d){var a=String(d).split('-');var t=new Date(+a[0],+a[1]-1,+a[2]);return (Date.now()-t.getTime())/864e5}
function ver(){var v=document.getElementById('mm-ver');var t=v&&v.textContent.trim();return /^v/.test(t||'')?t:(C.releases[0].ver?'v'+C.releases[0].ver:'판 '+md(C.releases[0].date))}
function mine(r){return r.items.filter(function(i){return i.page===FILE||i.page==='all'})}
function go(h){var a=h.split('#'),f=a[0]||FILE,id=a[1];if(f!==FILE&&!(f==='index.html'&&MAIN)){location.href=h;return}close();if(id)jump(id)}
function jump(id){var k=0;(function t(){var e=document.querySelector('[data-mmband="'+id+'"]')||document.getElementById(id);if(e&&e.offsetParent!==null){var y=e.getBoundingClientRect().top+scrollY-10;scrollTo({top:y,behavior:'smooth'});e.classList.add('mm-cl-flash');setTimeout(function(){e.classList.remove('mm-cl-flash')},1800);return}if(++k<30)setTimeout(t,300)})()}
var dim=null;
function close(){if(dim){dim.remove();dim=null;document.documentElement.classList.remove('mm-cl-lock')}}
function item(i){var w=el('div','it');var hd=el('div','hd');hd.appendChild(el('span','tg tg-'+({'새로':'new','순서':'ord','고침':'fix'}[i.tag]||'ord'),i.tag));hd.appendChild(el('span','nm',i.name));w.appendChild(hd);
 var p=el('p');p.appendChild(el('b','','무엇이 '));p.appendChild(document.createTextNode(i.what));w.appendChild(p);
 if(i.why){w.appendChild(el('p','why','왜 — '+i.why))}
 if(i.go){var g=el('a','go',(i.label||'그 자리로')+' →');g.href=i.go;g.onclick=function(e){e.preventDefault();go(i.go)};w.appendChild(g)}return w}
function open(only){close();var R=C.releases,r=R[0];dim=el('div','mm-cl-dim');var sh=el('div','mm-cl-sheet');sh.setAttribute('role','dialog');sh.appendChild(el('div','grab'));
 sh.appendChild(el('div','k','📘 바뀐 점 설명서 · '+ver()+' · '+md(r.date)));sh.appendChild(el('h3','',r.title));
 var its=only?mine(r):r.items;sh.appendChild(el('p','sub',(only?'이 페이지에서 바뀐 것 ':'바뀐 것 ')+its.length+'가지 · 누르면 그 자리로 갑니다'));
 its.forEach(function(i){sh.appendChild(item(i))});
 if(only&&its.length<r.items.length){var a=el('a','all','이번 판 전체 '+r.items.length+'가지 보기 ›');a.href='#';a.onclick=function(e){e.preventDefault();open(false)};sh.appendChild(a)}
 if(R.length>1){var d=el('details','old');d.appendChild(el('summary','','지난 판 보기 ('+R.slice(1,4).map(function(x){return md(x.date)}).join(' · ')+')'));R.slice(1,6).forEach(function(x){d.appendChild(el('div','oh',md(x.date)+' — '+x.title));x.items.forEach(function(i){d.appendChild(item(i))})});sh.appendChild(d)}
 var b=el('button','ok','확인했습니다');b.onclick=close;sh.appendChild(b);
 dim.appendChild(sh);dim.onclick=function(e){if(e.target===dim)close()};document.body.appendChild(dim);document.documentElement.classList.add('mm-cl-lock');
 ls('mm_cl_seen',r.id);ls('mm_cl_pg_'+FILE,r.id);var dot=document.querySelector('.mm-cl-pill i');if(dot)dot.remove();var np=document.querySelector('.mm-cl-new');if(np)np.classList.add('seen')}
function mainPill(){var h=document.querySelector('header.bn'),mv=document.getElementById('mm-ver');if(!h||!mv)return false;if(document.querySelector('.mm-cl-pill'))return true;var r=C.releases[0];
 var p=el('button','mm-cl-pill');if(ls('mm_cl_seen')!==r.id&&!r.minor)p.appendChild(el('i'));p.appendChild(document.createTextNode(ver()+' · 새로 바뀐 것 '+r.items.length+' ›'));p.onclick=function(){open(false)};
 var w=el('div','mm-cl-row');w.appendChild(p);h.after(w);return true}
function pagePill(){var ex=document.querySelector('.mm-cl-new'),hb=document.querySelector('.mm-st-hero .tp b');if(ex){if(ex.offsetParent!==null&&(!hb||ex.previousElementSibling===hb))return true;ex.remove()}var r=C.releases.filter(function(x){return days(x.date)<=3})[0];if(!r)return true;
 if(!r.items.some(function(i){return i.page===FILE}))return true; // 'all' 항목만 있는 페이지엔 알약을 달지 않음
 var hp=document.querySelector('.mm-st-hero .tp b');if(hp){var q=el('button','mm-cl-new'+(ls('mm_cl_pg_'+FILE)===r.id?' seen':''),'NEW · 바뀐 점 ›');q.onclick=function(e){e.preventDefault();e.stopPropagation();open(true)};hp.after(q);return q.offsetParent!==null}
 var t=document.getElementById('take')||document.querySelector('.pg-take'),c=t&&(t.querySelector('b.mm-chipx')||t.querySelector('.mm-stale'));
 var anchor=c||(t&&t.querySelector('h1,h2'))||document.querySelector('.mm-st-hero h2,.mm-st-hero h1,main h1,h1');if(!anchor)return false;
 var p=el('button','mm-cl-new'+(ls('mm_cl_pg_'+FILE)===r.id?' seen':''),'NEW · 바뀐 점 ›');p.onclick=function(e){e.preventDefault();e.stopPropagation();open(true)};
 var s=c&&c.nextElementSibling&&c.nextElementSibling.classList.contains('mm-stale')?c.nextElementSibling:c;if(s)s.after(p);else anchor.after(p);return p.offsetParent!==null}
function run(){var k=0;(function t(){var ok;try{ok=MAIN?mainPill():pagePill()}catch(e){ok=false}if((!ok||!MAIN)&&++k<25)setTimeout(t,ok?800:400)})();
 if(location.hash.length>1&&!MAIN){var id=location.hash.slice(1);setTimeout(function(){jump(id)},1200)}}
fetch('d/changelog.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j||!j.releases||!j.releases.length)return;C=j;
 document.readyState==='loading'?document.addEventListener('DOMContentLoaded',run):run()}).catch(function(){});
})();
