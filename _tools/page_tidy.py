# 페이지별 '보기 편하게' 정리(사용자 2026-10-29 지시 — 스크롤 압박 줄이기). site_live.py가 부르고 동기화 때마다 다시 넣음.
# 화면 코드(원본)는 건드리지 않고, 사이트 판에만 덧입히는 CSS + 작은 스크립트.
import os, re

COMMON_JS = r"""
window.mmFold=function(card,keep,label,open){ // card 안에서 keep(남길 것) 말고 나머지를 접기
  if(!card||card.dataset.fold)return; card.dataset.fold=1;
  var kids=[].slice.call(card.children).filter(function(k){return !k.matches(keep)});
  if(!kids.length)return; var d=document.createElement('details'); d.className='mm-fold'; if(open)d.open=true;
  var s=document.createElement('summary'); s.innerHTML='<span>'+label+'</span>'; d.appendChild(s);
  kids[0].before(d); kids.forEach(function(k){d.appendChild(k)});
};
"""

PAGES = {
 'p-lights.html': {
  'css': """
/* 영역별 경고등: 2열 카드, 항목은 이름 한 줄 + 지금·기준 작게 */
#areas{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}
#areas .area{padding:10px 11px!important;margin:0!important;border-radius:12px!important;min-width:0}
#areas .area .hd{display:flex;flex-direction:column;gap:1px;margin-bottom:6px}
#areas .area .hd b{font-size:15px}#areas .area .hd .cnt{font-size:12.5px}
#areas .area ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:5px}
#areas .area li{font-size:12.5px;line-height:1.35;padding-left:12px;position:relative}
#areas .area li::before{content:"○";position:absolute;left:0;top:0;font-size:10px;color:var(--color-fg-muted,#8a877f)}
#areas .area li.on::before{content:"●";color:#c4453a}
#areas .area li b{display:block;font-weight:700;font-size:12.5px}
#areas .area li small{display:block;color:var(--color-fg-muted,#6b675f);font-size:11.5px}
#areas .area a{font-size:12px;margin-top:6px;display:inline-block}
/* 표는 글자 조금 작게, 칸 여백 줄임 */
#score td,#score th,#chg td,#chg th,#amp td,#amp th{padding:7px 4px!important;font-size:13px!important}
#score td small,#score td em{font-size:11px!important}
/* 긴 설명: 3줄만 보이고 누르면 펼침 */
#hist-one{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden;cursor:pointer}
#hist-one.open{-webkit-line-clamp:unset;display:block}
.lw-one{font-size:14.5px!important;line-height:1.6!important}
""",
  'js': r"""
function tidy(){
  document.querySelectorAll('#areas .area li').forEach(function(li){
    if(li.dataset.t)return; var t=li.textContent; var m=t.split(' — '); if(m.length<2)return; li.dataset.t=1;
    var on=/켜짐|●/.test(t)||li.className.indexOf('on')>=0;
    li.innerHTML='<b></b><small></small>'; li.firstChild.textContent=m[0]; li.lastChild.textContent=m.slice(1).join(' — ').replace(/^지금\s*/,'지금 ');
  });
  var ho=document.getElementById('hist-one'); if(ho&&!ho.dataset.c){ho.dataset.c=1;ho.title='눌러서 펼치기';ho.addEventListener('click',function(){ho.classList.toggle('open')})}
  mmFold(document.getElementById('score-card'),'h2,.k,.tbl,#score','표 읽는 법');
  mmFold(document.getElementById('chg-card'),'h2,.k,.lw-one,#chg-one','바뀐 날 표 보기');
  mmFold(document.getElementById('amp-card'),'h2,.k,.lw-one,#amp-one','조합별 표 보기');
  mmFold(document.getElementById('th-card'),'h2,.k','기준표 펼치기 (불마다 왜 이 기준인지)');
}
""",
 },
 'p-targets.html': {
  'css': """
/* 분야 버튼 줄: 한 줄로 옆으로 밀기 */
.pt-chips{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;scrollbar-width:none;gap:6px!important;padding-bottom:4px!important;-webkit-overflow-scrolling:touch}
.pt-chips::-webkit-scrollbar{display:none}.pt-chips>*{flex:none!important}
/* 설명 글: 2줄만, 누르면 펼침 */
#dash-root p.sub{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden;cursor:pointer}
#dash-root p.sub.open{display:block}
/* 최근 변경 코멘트: 3줄만, 카드를 누르면 펼침 */
#recent-list li .cm{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden}
#recent-list li.open .cm{display:block}
/* 요약 칸 4개 한 줄 */
.pt-tiles{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:6px!important}
.pt-tile{padding:8px 7px!important;min-height:0!important}
.pt-tile>*:first-child{font-size:11px!important;line-height:1.3!important}
.pt-tile .v,.pt-tile b{font-size:21px!important}
.pt-tile>*:last-child{font-size:10.5px!important}
/* 종목별 보기: 요약 칸 3열, 기관 범례는 접기, 출처 접기 */
#tk-sec .pt-tiles{grid-template-columns:repeat(3,minmax(0,1fr))!important}
#srcs a{display:block;font-size:11.5px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
""",
  'js': r"""
function tidy(){
  document.querySelectorAll('#dash-root p.sub').forEach(function(p){ if(p.dataset.c)return; p.dataset.c=1; p.title='눌러서 펼치기'; p.addEventListener('click',function(){p.classList.toggle('open')}); });
  document.querySelectorAll('#recent-list li').forEach(function(li){ if(li.dataset.c)return; li.dataset.c=1; li.addEventListener('click',function(e){ if(e.target.closest('a,button'))return; li.classList.toggle('open'); }); });
  var wrap=function(el,label){ if(!el||el.closest('details.mm-fold'))return; var d=document.createElement('details'); d.className='mm-fold'; d.innerHTML='<summary><span>'+label+'</span></summary>'; el.before(d); d.appendChild(el); };
  wrap(document.querySelector('#month-card ul.mkey'),'막대·선 읽는 법');
  wrap(document.getElementById('legend'),'기관별 선 고르기 · 가장 긍정·비관 기관');
  wrap(document.getElementById('srcs'),'출처 보기');
  var mk=document.querySelector('#vsprice ul.mkey'); if(mk&&!mk.closest('details')){ var d=document.createElement('details'); d.className='mm-fold'; d.innerHTML='<summary><span>막대·점 읽는 법</span></summary>'; mk.before(d); d.appendChild(mk); }
}
""",
 },
 'p-trend.html': {
  'css': """
/* 토스식 기본 화면: 큰 가격, 기간 등락 한 줄, 깔끔한 차트, 기간 알약 한 줄. '자세한 차트'를 켜면 추세선·매물대 차트 */
#main .hd .pr{font:800 32px/1.15 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif!important;letter-spacing:-.02em;border:0!important}
#main .hd .kind{font-size:12px!important}
.mmt-chg{margin:2px 0 6px;font-size:15px;color:#6b675f}.mmt-chg b{font-weight:700}
.mmt-tip{min-height:18px;font-size:12.5px;font-weight:700;color:#141210;text-align:center}
.mmt-empty{margin:40px 0;text-align:center;color:#8a877f;font-size:14px}
.mmt-per{display:flex;gap:4px;margin:8px 0 4px;padding:3px;border-radius:12px;background:#f3f1ec}
.mmt-per button{flex:1;font:inherit;font-size:14.5px;font-weight:700;padding:7px 0;border:0;border-radius:9px;background:transparent;color:#8a877f}
.mmt-per button[aria-pressed=true]{background:#fff;color:#141210;box-shadow:0 1px 0 rgba(0,0,0,.06),0 2px 6px rgba(0,0,0,.08)}
.mmt-top{display:flex;align-items:center;gap:5px;margin:2px 0 4px;min-height:32px}.mmt-top .mmt-chg{font-size:14px!important;letter-spacing:-.01em}.mmt-top .mmt-chg{flex:1;min-width:0;margin:0!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mmt-tg{flex:none;display:inline-flex;align-items:center;gap:5px;height:30px;padding:0 10px;border-radius:999px;border:1px solid #e3dfd6;background:#fff;font:inherit;font-size:13px;font-weight:700;color:#6b675f;cursor:pointer;box-shadow:0 1px 0 rgba(0,0,0,.05),0 2px 5px rgba(0,0,0,.05)}
.mmt-tg[aria-pressed=true],.mmt-tg.on{background:#141210;color:#fff;border-color:#141210}
.mmt-det input{position:absolute;opacity:0;width:1px;height:1px}
.mmt-ttl{display:none}
#main .mmt-box svg,#main .ch svg{touch-action:none!important;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
html.mm-land,html.mm-land body{overflow:hidden!important;height:100%;overscroll-behavior:none}html.mm-land #main .mmt{touch-action:none;overscroll-behavior:contain}html.mm-land #main .mmt svg{touch-action:none!important}
html.mm-land #main .mmt{position:fixed;inset:0;z-index:9999;background:#fff;display:flex!important;flex-direction:column;padding:8px max(14px,env(safe-area-inset-right)) 6px max(14px,env(safe-area-inset-left))}
html.mm-land .mmt-ttl{display:block;font-size:15px;font-weight:800;color:#141210;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html.mm-land #main .mmt .mmt-box,html.mm-land #main .mmt .mmt-chg,html.mm-land #main .mmt .mmt-per{display:flex!important}
html.mm-land #main .mmt .mmt-chg{display:block!important}
html.mm-land .mmt-box{flex:1;min-height:0;flex-direction:column}
html.mm-land .mmt-det{display:none}html.mm-land .mmt-trd{display:inline-flex!important}
html.mm-land .mmt-per{margin:4px 0 0}html.mm-land .mmt-per button{padding:5px 0}html.mm-land .mmt-top{min-height:28px}
#main.mmt-detail .mmt-trd{display:none}

#main.mmt-on:not(.mmt-detail) .rg,#main.mmt-on:not(.mmt-detail) .ch,#main.mmt-on:not(.mmt-detail) .mm-lv,#main.mmt-on:not(.mmt-detail) details.mm-fold,#main.mmt-on:not(.mmt-detail) p.nt{display:none!important}
#main.mmt-detail .mmt-box,#main.mmt-detail .mmt-chg,#main.mmt-detail .mmt-per{display:none!important}#main.mmt-detail .mmt-top{justify-content:flex-end}
#main .rg{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:6px!important;scrollbar-width:none}#main .rg::-webkit-scrollbar{display:none}#main .rg>*{flex:none!important}
/* 토스식 1일 차트 */
#main.mm-1d-on .mm-lv{display:none!important}
#main .hd .pr{cursor:pointer;border-bottom:1px dashed rgba(0,0,0,.18)}
.mm1d-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;margin:6px 0 2px;font-size:13px;color:#6b675f}.mm1d-h b{font-size:17px}.mm1d-h .tip{flex-basis:100%;min-height:1.2em;font-weight:700;color:#141210}
/* 추세선·채널선 가늘고 옅게, 추세 가이드 글씨 작게 */
#main details.mm-fold p.gl,#main details.mm-fold p.nt{font-size:13px!important;line-height:1.6!important}
#main details.mm-fold p.gl small{font-size:12px!important}
/* 기간별 등락 6칸은 빼고 그만큼 차트를 크게(사용자 2026-10-29) */
#main .rt{display:none!important}
/* 차트 위 핵심 4칸(저항·지지·단기 채널·장기 추세) */
.mm-lv{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;margin:6px 0 2px}
.mm-lv>div{border-radius:9px;padding:5px 6px;text-align:center;background:#f6f3ec;border:1px solid rgba(0,0,0,.05);min-width:0}
.mm-lv small{display:block;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#8a877f;font-weight:700;letter-spacing:.02em}
.mm-lv b{display:block;font-size:13px;letter-spacing:-.02em;font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mm-lv em{display:none}
.mm-lv .up{background:#fdf0ee}.mm-lv .up b{color:#b23a2e}.mm-lv .dn{background:#edf7ef}.mm-lv .dn b{color:#1f7a3f}
/* 추세 가이드·선 설명은 접기 */
#main details.mm-fold p.gl{margin-top:4px}
/* 분야 버튼 한 줄 */
#cats{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;scrollbar-width:none;gap:6px!important;padding-bottom:4px}
#cats::-webkit-scrollbar{display:none}#cats>*{flex:none!important}
/* 종목 목록: 한 줄 카드(이름 · 티커 · 1일 · 고점 대비) */
#list .grp h3{font-size:14px!important;margin:12px 0 4px!important}#list .grp h3 span{font-size:11.5px!important}
#list .rows{display:flex;flex-direction:column;gap:5px}
#list .row{display:flex!important;align-items:center!important;gap:8px!important;padding:9px 12px!important;min-height:0!important;border-radius:12px!important;background:var(--color-panel,#fff)!important;border:1px solid rgba(0,0,0,.06)!important;box-shadow:0 2px 0 rgba(30,22,8,.06)!important;text-align:left}
#list .row b{order:1;flex:0 1 auto;min-width:0;font-size:15px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#list .row small{order:2;flex:none;font-size:11.5px!important;color:#8a877f;margin:0!important}
#list .row .d1{order:3;margin-left:auto;flex:none;font-weight:700;font-size:14px!important}
#list .row .dd{order:4;flex:none;font-size:12px!important;color:#8a877f;min-width:4.6em;text-align:right}
#list .row[aria-current=true]{background:#f4ecdb!important;border-color:rgba(162,106,12,.35)!important}
""",
  'js': r"""
window.__mm1d=window.__mm1d||false; window.__mmIntra=window.__mmIntra||null; window.__mmIntraAt=window.__mmIntraAt||0;
function mmIntra(cb){ if(window.__mmIntra&&Date.now()-window.__mmIntraAt<60000){cb(window.__mmIntra);return}
  fetch('live/intraday.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(d){if(d){window.__mmIntra=d;window.__mmIntraAt=Date.now()}cb(d)}).catch(function(){cb(null)}); }
function mmTk(){ var t=document.querySelector('#main .hd .tk'), k=t?t.textContent.trim():''; try{ var m=DATA.P.filter(function(r){return r.ticker.replace('^','')===k})[0]; if(m) return m.ticker; }catch(e){} return k; }
function mmKst(sec){ var d=new Date(sec*1000+9*3600000); var p=function(n){return (n<10?'0':'')+n}; return p(d.getUTCHours())+':'+p(d.getUTCMinutes()); }
function mmDraw1d(){
  var main=document.getElementById('main'), ch=main&&main.querySelector('.ch'); if(!ch)return;
  mmIntra(function(D){
    var tk=mmTk(), x=D&&D.d&&(D.d[tk]||D.d[tk.replace('.', '-')]);
    if(!window.__mm1d)return;
    ch.dataset.d1=tk; ch.innerHTML='';
    if(!x||!x.p||x.p.length<2){ ch.innerHTML='<p style="margin:30px 0;text-align:center;color:#8a877f;font-size:14px">오늘 흐름 자료가 아직 없습니다(장 시작 후 5분마다 채워짐)</p>'; return; }
    var W=Math.max(260,ch.clientWidth||330), H=Math.round(Math.min(420,Math.max(280,W*0.86))), m={l:6,r:56,t:30,b:24};
    var s0=x.s, rs=x.reg&&x.reg[0]||s0, re=x.reg&&x.reg[1]||(s0+57600);
    var X0=Math.min(s0, rs-330*60), X1=re+240*60;
    var pts=x.p.map(function(a){return [s0+a[0]*60,a[1]]}); var pc=x.pc||pts[0][1];
    var vs=pts.map(function(a){return a[1]}).concat([pc]); var lo=Math.min.apply(0,vs), hi=Math.max.apply(0,vs), pad=(hi-lo)*0.12||hi*0.01; lo-=pad; hi+=pad;
    var sx=function(t){return m.l+(t-X0)/(X1-X0)*(W-m.l-m.r)}, sy=function(v){return m.t+(hi-v)/(hi-lo)*(H-m.t-m.b)};
    var last=pts[pts.length-1], up=last[1]>=pc, col=up?'#1f7a3f':'#c4453a', chg=(last[1]/pc-1)*100;
    var dec=(x.cur==='KRW'||x.cur==='JPY')?0:2, f=function(v){return v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec})};
    var path=pts.map(function(a,i){return (i?'L':'M')+sx(a[0]).toFixed(1)+','+sy(a[1]).toFixed(1)}).join('');
    var area=path+'L'+sx(last[0]).toFixed(1)+','+(H-m.b)+'L'+sx(pts[0][0]).toFixed(1)+','+(H-m.b)+'Z';
    var gid='g'+Math.random().toString(36).slice(2,7);
    var svg='<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;height:auto;display:block;touch-action:pan-y" class="mm1d">'
     +'<defs><linearGradient id="'+gid+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+col+'" stop-opacity=".22"/><stop offset="1" stop-color="'+col+'" stop-opacity="0"/></linearGradient></defs>'
     +'<rect x="'+sx(X0)+'" y="'+m.t+'" width="'+(sx(rs)-sx(X0))+'" height="'+(H-m.t-m.b)+'" fill="#000" opacity=".035"/>'
     +'<rect x="'+sx(re)+'" y="'+m.t+'" width="'+(sx(X1)-sx(re))+'" height="'+(H-m.t-m.b)+'" fill="#000" opacity=".035"/>'
     +'<text x="'+(sx(X0)+4)+'" y="'+(m.t+12)+'" font-size="10.5" fill="#9a978f">프리마켓</text><text x="'+(sx(re)+4)+'" y="'+(m.t+12)+'" font-size="10.5" fill="#9a978f">애프터</text>'
     +'<line x1="'+m.l+'" x2="'+(W-m.r)+'" y1="'+sy(pc)+'" y2="'+sy(pc)+'" stroke="#8a877f" stroke-dasharray="3 4" stroke-width="1"/>'
     +'<text x="'+(W-m.r+4)+'" y="'+(sy(pc)+4)+'" font-size="10.5" fill="#8a877f">전일 '+f(pc)+'</text>'
     +'<path d="'+area+'" fill="url(#'+gid+')"/><path d="'+path+'" fill="none" stroke="'+col+'" stroke-width="2" stroke-linejoin="round"/>'
     +'<circle cx="'+sx(last[0])+'" cy="'+sy(last[1])+'" r="4" fill="'+col+'" stroke="#fff" stroke-width="1.5"/>'
     +'<rect x="'+(W-m.r+2)+'" y="'+(sy(last[1])-11)+'" width="'+(m.r-4)+'" height="22" rx="5" fill="'+col+'"/><text x="'+(W-m.r/2)+'" y="'+(sy(last[1])+4.5)+'" font-size="11.5" font-weight="700" fill="#fff" text-anchor="middle">'+f(last[1])+'</text>'
     +'<text x="'+sx(rs)+'" y="'+(H-6)+'" font-size="10.5" fill="#8a877f" text-anchor="middle">'+mmKst(rs)+' 개장</text><text x="'+sx(re)+'" y="'+(H-6)+'" font-size="10.5" fill="#8a877f" text-anchor="middle">'+mmKst(re)+' 마감</text>'
     +'<line class="cx" x1="0" x2="0" y1="'+m.t+'" y2="'+(H-m.b)+'" stroke="#141210" stroke-width="1" opacity="0"/><circle class="cd" r="4" fill="#141210" opacity="0"/>'
     +'</svg>';
    var head='<div class="mm1d-h"><b style="color:'+col+'">오늘 '+(chg>=0?'+':'−')+Math.abs(chg).toFixed(2)+'%</b> <span>전일 종가 대비 · '+mmKst(last[0])+' 기준(한국시간)</span><span class="tip"></span></div>';
    ch.innerHTML=head+svg;
    var el=ch.querySelector('svg'), tip=ch.querySelector('.tip');
    function mv(e){ var r=el.getBoundingClientRect(), px=(e.clientX-r.left)/r.width*W, t=X0+(px-m.l)/(W-m.l-m.r)*(X1-X0), b=pts[0];
      pts.forEach(function(a){ if(Math.abs(a[0]-t)<Math.abs(b[0]-t))b=a; });
      el.querySelector('.cx').setAttribute('x1',sx(b[0]));el.querySelector('.cx').setAttribute('x2',sx(b[0]));el.querySelector('.cx').setAttribute('opacity','.35');
      var cd=el.querySelector('.cd');cd.setAttribute('cx',sx(b[0]));cd.setAttribute('cy',sy(b[1]));cd.setAttribute('opacity','1');
      tip.textContent=mmKst(b[0])+' · '+f(b[1])+' ('+((b[1]/pc-1)*100>=0?'+':'−')+Math.abs((b[1]/pc-1)*100).toFixed(2)+'%)'; }
    el.addEventListener('pointermove',mv); el.addEventListener('pointerdown',mv);
    el.addEventListener('pointerleave',function(){ el.querySelector('.cx').setAttribute('opacity','0'); el.querySelector('.cd').setAttribute('opacity','0'); tip.textContent=''; });
  });
}
function mmSet1d(on){ window.__mm1d=on; var main=document.getElementById('main'); if(!main)return;
  main.classList.toggle('mm-1d-on',on);
  main.querySelectorAll('.rg .pb-chip').forEach(function(b){ if(b.dataset.d1btn) b.setAttribute('aria-pressed',String(on)); else if(on && /개월/.test(b.textContent)) b.setAttribute('aria-pressed','false'); });
  if(on) mmDraw1d(); }
function mm1dTidy(){
  var main=document.getElementById('main'); if(!main)return; var rg=main.querySelector('.rg'), pr=main.querySelector('.hd .pr');
  if(rg&&!rg.querySelector('[data-d1btn]')){
    var b=document.createElement('button'); b.type='button'; b.className='pb-chip'; b.dataset.d1btn=1; b.textContent='1일'; b.setAttribute('aria-pressed',String(window.__mm1d));
    b.addEventListener('click',function(e){ e.stopPropagation(); mmSet1d(true); }); rg.insertBefore(b, rg.firstChild);
    rg.querySelectorAll('.pb-chip').forEach(function(x){ if(!x.dataset.d1btn && /개월/.test(x.textContent)) x.addEventListener('click',function(){ window.__mm1d=false; },true); });
  }
  if(pr&&!pr.dataset.d1){ pr.dataset.d1=1; pr.style.cursor='pointer'; pr.title='눌러서 오늘 흐름 보기'; pr.addEventListener('click',function(){ mmSet1d(!window.__mm1d); }); }
  var ch=main.querySelector('.ch');
  if(window.__mm1d){ main.classList.add('mm-1d-on'); if(ch&&ch.dataset.d1!==mmTk()) mmSet1d(true); }
  else main.classList.remove('mm-1d-on');
}

/* 토스식 종목 차트(사용자 2026-10-29): 큰 가격 · 기간 등락 한 줄 · 깔끔한 선 차트(최고·최저) · 아래 기간 알약 한 줄 · '자세한 차트'로 추세선·매물대 */
window.__mmT = window.__mmT || { per: '3m', det: false };
var MMT_PER = [['1d','1일','오늘'],['1w','1주','지난주보다'],['1m','1달','지난달보다'],['3m','3달','3달 전보다'],['1y','1년','1년 전보다'],['5y','5년','5년 전보다']];
function mmtRow(){ var tk=mmTk(); try{ return DATA.P.filter(function(r){return r.ticker===tk})[0]; }catch(e){ return null; } }
function mmtDaily(tk){ try{ return (DATA.H[tk]||[]).filter(function(a){return !a[2]}).map(function(a){return [Date.parse(a[0]+'T21:00:00Z')/1000,a[1]]}); }catch(e){ return []; } }
function mmtFmt(v,cur){ if(cur==='%') return v.toFixed(3).replace(/0$/,'')+'%'; var d=(cur==='KRW'||cur==='JPY')?0:2; return (cur==='USD'?'$':'')+v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d})+(cur==='KRW'?'원':cur&&cur!=='USD'?' '+cur:''); }
function mmtTick(v,cur,st){ var d=st<0.01?3:st<0.1?2:st<1?1:0; if(cur==='%') return v.toFixed(Math.max(d,1))+'%'; if(v>=100000) return (v/10000).toLocaleString('en-US',{maximumFractionDigits:1})+'만'; return v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d}); }
function mmtKst(sec,withDate){ var d=new Date(sec*1000+9*3600000), p=function(n){return (n<10?'0':'')+n}; return withDate?(d.getUTCFullYear()%100)+'.'+(d.getUTCMonth()+1)+'.'+d.getUTCDate():p(d.getUTCHours())+':'+p(d.getUTCMinutes()); }
function mmtChart(box, pts, base, cur, intra){
  var LAND=document.documentElement.classList.contains('mm-land'), W=Math.max(260,box.clientWidth||330), H=LAND?Math.max(150,(box.clientHeight||innerHeight-120)-22):Math.round(Math.min(380,Math.max(260,W*0.78))), m={l:4,r:44,t:34,b:30};
  var t0=pts[0][0], t1=pts[pts.length-1][0]; if(intra){ t0=Math.min(t0,intra.x0); t1=Math.max(t1,intra.x1); }
  var vs=pts.map(function(a){return a[1]}); if(base!=null) vs.push(base);
  var lo=Math.min.apply(0,vs), hi=Math.max.apply(0,vs), pad=(hi-lo)*0.08||hi*0.01; lo-=pad; hi+=pad;
  var sx=function(t){return m.l+(t-t0)/((t1-t0)||1)*(W-m.l-m.r)}, sy=function(v){return m.t+(hi-v)/(hi-lo)*(H-m.t-m.b)};
  var last=pts[pts.length-1], up=base==null||last[1]>=base, col=up?'#e0423a':'#3a6fe0';
  var path=pts.map(function(a,i){return (i?'L':'M')+sx(a[0]).toFixed(1)+','+sy(a[1]).toFixed(1)}).join('');
  var iMax=0,iMin=0; pts.forEach(function(a,i){ if(a[1]>pts[iMax][1])iMax=i; if(a[1]<pts[iMin][1])iMin=i; });
  var lab=function(i,top){ var a=pts[i], x=sx(a[0]), y=sy(a[1]), anc=x<W*0.2?'start':x>W*0.8?'end':'middle';
    return '<circle cx="'+x+'" cy="'+y+'" r="3" fill="'+col+'" opacity=".55"/><text x="'+x+'" y="'+(top?y-9:y+17)+'" font-size="11.5" fill="'+col+'" text-anchor="'+anc+'">'+(top?'최고 ':'최저 ')+mmtFmt(a[1],cur)+'</text>'; };
  var s='<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;height:'+(LAND?H+'px':'auto')+';display:block;touch-action:none">';
  if(intra){ s+='<rect x="'+sx(intra.rs)+'" y="'+m.t+'" width="'+(sx(intra.re)-sx(intra.rs))+'" height="'+(H-m.t-m.b)+'" fill="#000" opacity=".025"/>'
     +'<text x="'+sx(intra.rs)+'" y="'+(H-8)+'" font-size="10.5" fill="#9a978f" text-anchor="middle">'+mmtKst(intra.rs)+' 개장</text><text x="'+sx(intra.re)+'" y="'+(H-8)+'" font-size="10.5" fill="#9a978f" text-anchor="middle">'+mmtKst(intra.re)+' 마감</text>'; }
  // 눈금(사용자 2026-10-29): 오른쪽 가격 3~4개, 아래 날짜 3~4개 — 옅게
  (function(){ var span=hi-lo, raw=span/4, p=Math.pow(10,Math.floor(Math.log10(raw))), st=[1,2,2.5,5,10].map(function(k){return k*p}).filter(function(k){return k>=raw})[0]||raw;
    for(var v=Math.ceil(lo/st)*st; v<=hi; v+=st){ var y=sy(v); if(y<m.t+6||y>H-m.b-4) continue;
      s+='<line x1="'+m.l+'" x2="'+(W-m.r+4)+'" y1="'+y+'" y2="'+y+'" stroke="#ece9e2" stroke-width="1"/><text x="'+(W-2)+'" y="'+(y+4)+'" font-size="10.5" fill="#a29f97" text-anchor="end">'+mmtTick(v,cur,st)+'</text>'; }
    if(!intra){ var sp=(t1-t0)/86400; for(var k=0;k<4;k++){ var t=t0+(t1-t0)*(k+0.5)/4, d=new Date(t*1000+9*3600000), lb=sp<=100?(d.getUTCMonth()+1)+'/'+d.getUTCDate():sp<=400?(d.getUTCFullYear()%100)+'.'+(d.getUTCMonth()+1):(d.getUTCFullYear())+'';
      s+='<text x="'+sx(t)+'" y="'+(H-8)+'" font-size="10.5" fill="#a29f97" text-anchor="middle">'+lb+'</text>'; } }
    else { [intra.rs+(intra.re-intra.rs)/3, intra.rs+(intra.re-intra.rs)*2/3].forEach(function(t){ s+='<text x="'+sx(t)+'" y="'+(H-8)+'" font-size="10.5" fill="#c2bfb8" text-anchor="middle">'+mmtKst(t)+'</text>'; }); }
    if(window.__mmT&&window.__mmT.tr&&!intra&&pts.length>5){ // 간단 추세선: 보이는 기간 종가의 직선 추세(최소제곱)
      var n=pts.length, mx=0, my=0; pts.forEach(function(a){mx+=a[0];my+=a[1]}); mx/=n; my/=n; var sxy=0,sxx=0; pts.forEach(function(a){sxy+=(a[0]-mx)*(a[1]-my); sxx+=(a[0]-mx)*(a[0]-mx)});
      var b1=sxx?sxy/sxx:0, f=function(t){return my+b1*(t-mx)}, ya=f(pts[0][0]), yb=f(pts[n-1][0]), ch=(yb/ya-1)*100;
      s+='<line x1="'+sx(pts[0][0])+'" x2="'+sx(pts[n-1][0])+'" y1="'+sy(ya)+'" y2="'+sy(yb)+'" stroke="#6b675f" stroke-width="1.3" stroke-dasharray="5 4" opacity=".55"/>'
       +'<text x="'+(m.l+2)+'" y="'+(m.t-20)+'" font-size="11" font-weight="700" fill="#6b675f">추세 '+(b1>=0?'↗ ':'↘ ')+(cur==='%'?((yb-ya>=0?'+':'−')+Math.round(Math.abs(yb-ya)*100)+'bp'):((ch>=0?'+':'−')+Math.abs(ch).toFixed(1)+'%'))+'</text>'; }
  })();
  if(base!=null) s+='<line x1="'+m.l+'" x2="'+(W-m.r)+'" y1="'+sy(base)+'" y2="'+sy(base)+'" stroke="#c9c6bf" stroke-dasharray="2 4" stroke-width="1"/>';
  s+='<path d="'+path+'" fill="none" stroke="'+col+'" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'+lab(iMax,true)+lab(iMin,false)
   +'<circle cx="'+sx(last[0])+'" cy="'+sy(last[1])+'" r="4.5" fill="'+col+'" stroke="#fff" stroke-width="2"/>'
   +'<line class="cx" x1="0" x2="0" y1="'+m.t+'" y2="'+(H-m.b)+'" stroke="#141210" stroke-width="1" opacity="0"/><circle class="cd" r="4.5" fill="#141210" opacity="0"/></svg>';
  box.innerHTML='<div class="mmt-tip"></div>'+s;
  var el=box.querySelector('svg'), tip=box.querySelector('.mmt-tip');
  function mv(e){ var r=el.getBoundingClientRect(), t=t0+((e.clientX-r.left)/r.width*W-m.l)/(W-m.l-m.r)*(t1-t0), b=pts[0];
    pts.forEach(function(a){ if(Math.abs(a[0]-t)<Math.abs(b[0]-t))b=a; });
    var cx=el.querySelector('.cx'), cd=el.querySelector('.cd'); cx.setAttribute('x1',sx(b[0]));cx.setAttribute('x2',sx(b[0]));cx.setAttribute('opacity','.3'); cd.setAttribute('cx',sx(b[0]));cd.setAttribute('cy',sy(b[1]));cd.setAttribute('opacity','1');
    tip.textContent=(intra?mmtKst(b[0]):mmtKst(b[0],true))+'  '+mmtFmt(b[1],cur)+(base?'  ('+((b[1]/base-1)*100>=0?'+':'−')+Math.abs((b[1]/base-1)*100).toFixed(2)+'%)':''); }
  el.addEventListener('pointermove',mv); el.addEventListener('pointerdown',mv);
  el.addEventListener('pointerleave',function(){ el.querySelector('.cx').setAttribute('opacity','0'); el.querySelector('.cd').setAttribute('opacity','0'); tip.textContent=''; });
  return {up:up, last:last};
}
var __mmL=null, __mmLq=null;
function mmLong(cb){ if(__mmL) return cb(__mmL); if(__mmLq){ __mmLq.push(cb); return; } __mmLq=[cb];
  var v=''; try{ v=(window.__SYNC__||'')+String(Math.floor(Date.now()/3600000)); }catch(e){}
  fetch('live/long.json?v='+v).then(function(x){return x.ok?x.json():null}).catch(function(){return null}).then(function(d){ __mmL=d||{d:{}}; var q=__mmLq; __mmLq=null; q.forEach(function(f){ try{f(__mmL)}catch(e){} }); }); }
function mmtDraw(){
  var main=document.getElementById('main'); if(!main)return; var T=window.__mmT, r=mmtRow(); if(!r)return;
  var wrap=main.querySelector('.mmt'); if(!wrap){ wrap=document.createElement('div'); wrap.className='mmt'; wrap.innerHTML='<div class="mmt-ttl"></div><div class="mmt-top"><p class="mmt-chg"></p><button type="button" class="mmt-tg mmt-trd">추세</button><label class="mmt-det mmt-tg"><input type="checkbox">자세히</label></div><div class="mmt-box"></div><div class="mmt-per"></div>';
    var hd=main.querySelector('.hd'); hd.after(wrap);
    var pr=wrap.querySelector('.mmt-per'); MMT_PER.forEach(function(p){ var b=document.createElement('button'); b.type='button'; b.textContent=p[1]; b.dataset.p=p[0]; b.addEventListener('click',function(){ T.per=p[0]; mmtDraw(); }); pr.appendChild(b); });
    wrap.querySelector('.mmt-trd').addEventListener('click',function(){ T.tr=!T.tr; mmtDraw(); });
    var cb=wrap.querySelector('input'); cb.addEventListener('change',function(){ T.det=cb.checked; wrap.querySelector('.mmt-det').classList.toggle('on',T.det); main.classList.toggle('mmt-detail',T.det); setTimeout(function(){ window.__mmForce=1; window.dispatchEvent(new Event('resize')); },30); }); }
  wrap.querySelector('.mmt-trd').setAttribute('aria-pressed',String(!!T.tr)); wrap.querySelector('.mmt-det').classList.toggle('on',!!T.det);
  wrap.querySelector('input').checked=T.det; main.classList.toggle('mmt-detail',T.det); main.classList.add('mmt-on');
  wrap.dataset.tk=r.ticker;
  var ttl=wrap.querySelector('.mmt-ttl'); if(ttl){ ttl.textContent=r.name+'  '+mmtFmt(Number(r.price),r.currency); }
  wrap.querySelectorAll('.mmt-per button').forEach(function(b){ b.setAttribute('aria-pressed',String(b.dataset.p===T.per)); });
  var box=wrap.querySelector('.mmt-box'), chg=wrap.querySelector('.mmt-chg'), cur=r.currency, now=Number(r.price);
  var pe=main.querySelector('.hd .pr'); var lv=pe&&pe.textContent.match(/[\d,]+\.?\d*/); if(pe&&pe.classList.contains('mm-fh')&&lv) now=Number(lv[0].replace(/,/g,''));
  function setChg(base,label){ if(base==null){chg.textContent='';return} var dv=now-base, dp=dv/base*100, c=dv>=0?'#e0423a':'#3a6fe0'; chg.innerHTML='<span></span> <b style="color:'+c+'"></b>'; chg.firstChild.textContent=label; chg.lastChild.textContent=(cur==='%')?((dv>=0?'+':'−')+Math.round(Math.abs(dv)*100)+'bp'):((dv>=0?'+':'−')+mmtFmt(Math.abs(dv),cur)+' ('+Math.abs(dp).toFixed(1)+'%)'); }
  if(T.per==='1d'){
    mmIntra(function(D){ var x=D&&D.d&&D.d[r.ticker]; if(!x||!x.p||x.p.length<2){ box.innerHTML='<p class="mmt-empty">오늘 흐름 자료가 아직 없습니다 · 장 시작 후 5분마다 채워집니다</p>'; setChg(r.prev_close,'어제보다'); return; }
      var pts=x.p.map(function(a){return [x.s+a[0]*60,a[1]]}); if(Math.abs(pts[pts.length-1][1]-now)>1e-9 && pe&&pe.classList.contains('mm-fh')) pts.push([Date.now()/1000,now]);
      var rs=x.reg&&x.reg[0]||x.s, re=x.reg&&x.reg[1]||x.s+57600; mmtChart(box,pts,x.pc,cur,{rs:rs,re:re,x0:rs-330*60,x1:re+240*60}); setChg(x.pc,'어제보다'); });
    return; }
  if(T.per==='5y'){ // 5년: 하루 한 번 받는 주간 종가(live/long.json) + 최근 일별
    mmLong(function(Lg){ if(T.per!=='5y'||mmTk()!==r.ticker)return; var wk=(Lg&&Lg.d&&Lg.d[r.ticker])||[], dly=mmtDaily(r.ticker), t0=dly.length?dly[0][0]:Infinity;
      var pts=wk.map(function(a){return [Date.parse(a[0]+'T21:00:00Z')/1000,a[1]]}).filter(function(a){return a[0]<t0}).concat(dly); pts.push([Date.now()/1000,now]);
      if(pts.length<3){ box.innerHTML='<p class="mmt-empty">5년 자료를 불러오는 중입니다 · 잠시 뒤 다시 열어 주세요</p>'; chg.textContent=''; return; }
      mmtChart(box,pts,pts[0][1],cur,null); setChg(pts[0][1],(pts[0][0]<Date.now()/1000-4.5*365*86400)?'5년 전보다':'자료 시작보다'); });
    return; }
  var all=mmtDaily(r.ticker); var tNow=Date.now()/1000; all.push([tNow,now]);
  var days={'1w':7,'1m':31,'3m':92,'1y':366}[T.per]; var from=tNow-days*86400; var pts=all.filter(function(a){return a[0]>=from});
  if(pts.length<2) pts=all.slice(-2);
  var prev=all.filter(function(a){return a[0]<from}); var base=prev.length?prev[prev.length-1][1]:pts[0][1];
  mmtChart(box,pts,base,cur,null); setChg(base,MMT_PER.filter(function(p){return p[0]===T.per})[0][2]);
}

function mmtStyleDetail(){ // 자세한 차트: 추세선은 가늘고 옅게, 주가 선은 맨 위에 흰 테두리로 또렷하게
  var svg=document.querySelector('#main .ch svg'); if(!svg||svg.dataset.st)return; svg.dataset.st=1;
  var A=function(e,n){return e.getAttribute(n)||''};
  svg.querySelectorAll('line').forEach(function(l){ var st=A(l,'stroke'), d=A(l,'stroke-dasharray');
    if(st==='var(--color-fg)'&&(d==='6 0'||A(l,'stroke-width')==='1.8')){ l.setAttribute('stroke-width','1'); l.setAttribute('opacity','.3'); }
    else if(st==='var(--color-fg)'){ l.setAttribute('opacity','.18'); }
    else if(st==='var(--color-bad)'||st==='var(--color-ok)'){ l.setAttribute('stroke-width','1.1'); l.setAttribute('opacity', d?'.3':'.5'); } });
  svg.querySelectorAll('rect').forEach(function(r){ if(A(r,'opacity')==='0.08') r.setAttribute('opacity','.05'); });
  svg.querySelectorAll('text').forEach(function(t){ if(/^고점/.test(t.textContent)) t.setAttribute('opacity','.75'); });
  // 내 관점 1차 관문선: 선은 가늘고 옅게, 차트 안 글자는 빼고 오른쪽 눈금 꼬리표로(사용자 2026-10-29)
  svg.querySelectorAll('line').forEach(function(l){ if(A(l,'stroke')==='var(--color-warn)'){ l.setAttribute('stroke-width','1.3'); l.setAttribute('opacity', A(l,'stroke-dasharray')?'.45':'.65'); } });
  svg.querySelectorAll('circle').forEach(function(c){ if(A(c,'stroke')==='var(--color-warn)'){ c.setAttribute('r','2.6'); c.setAttribute('stroke-width','1.2'); c.setAttribute('opacity','.7'); } });
  svg.querySelectorAll('text').forEach(function(t){ var m=t.textContent.match(/1차 관문\s*([\d,.]+)/); if(m){ svg.dataset.gate=m[1]; svg.dataset.gateOk=/돌파|✓/.test(t.textContent)?'1':''; t.remove(); } else if(t.textContent.trim()==='★'&&A(t,'fill')==='var(--color-warn)'){ t.remove(); } });
  var pr=[].slice.call(svg.querySelectorAll('path')).filter(function(p){return A(p,'stroke')==='var(--line)'&&A(p,'fill')==='none'})[0];
  if(pr){ var g=pr.parentNode, halo=pr.cloneNode(); halo.setAttribute('stroke','#fff'); halo.setAttribute('stroke-width','5.5'); halo.setAttribute('opacity','.9');
    pr.setAttribute('stroke-width','2.4'); g.appendChild(halo); g.appendChild(pr);
    [].slice.call(g.querySelectorAll('circle')).filter(function(c){return A(c,'fill')==='var(--line)'}).forEach(function(c){ g.appendChild(c); }); }
}

function mmtAxisTags(){ // 자세한 차트: 지지·저항 수치를 주가 선이 없는 빈 자리에 쓰고, 오른쪽 눈금까지 점선으로 이음(사용자 2026-10-29)
  var svg=document.querySelector('#main .ch svg'); if(!svg||svg.dataset.tg)return; var gl=document.querySelector('#main p.gl'); if(!gl)return;
  var t=gl.textContent.replace(/\s+/g,' '), R=t.match(/위 저항 후보\s*([\d,.]+)~([\d,.]+)/), S=t.match(/아래 지지 후보\s*([\d,.]+)~([\d,.]+)/); if(!R&&!S)return;
  var num=function(x){return +String(x).replace(/,/g,'')}, A=function(e,n){return e.getAttribute(n)||''};
  var W=svg.viewBox.baseVal.width, ticks=[].slice.call(svg.querySelectorAll('text')).filter(function(e){return +e.getAttribute('x')>W-70&&/^[\d,.]+$/.test(e.textContent.trim())});
  var pr=[].slice.call(svg.querySelectorAll('path')).filter(function(p){return A(p,'stroke')==='var(--line)'&&A(p,'fill')==='none'&&A(p,'stroke-width')!=='5.5'})[0];
  if(ticks.length<2||!pr)return; svg.dataset.tg=1;
  var a=ticks.map(function(e){return [num(e.textContent),+e.getAttribute('y')-4]}).sort(function(x,y){return x[0]-y[0]}), Y=function(v){return a[0][1]+(v-a[0][0])/(a[a.length-1][0]-a[0][0])*(a[a.length-1][1]-a[0][1])};
  var L=pr.getTotalLength(), pts=[]; for(var i=0;i<=160;i++){ var p=pr.getPointAtLength(L*i/160); pts.push([p.x,p.y]); }
  var x0=Math.min.apply(null,pts.map(function(p){return p[0]})), x1=+ticks[0].getAttribute('x')-6;
  var boxes=[].slice.call(svg.querySelectorAll('text')).filter(function(e){return ticks.indexOf(e)<0&&e.textContent.trim()}).map(function(e){ try{var b=e.getBBox();return [b.x-3,b.y-2,b.x+b.width+3,b.y+b.height+2]}catch(x){return null} }).filter(Boolean);
  var ns='http://www.w3.org/2000/svg', h=15;
  function put(lo,hi,txt,col,bg){ var ym=(Y(hi)+Y(lo))/2, w=txt.length*7+10, best=null;
    // 선 높이(ym) 그대로가 비어 있으면 거기에, 주가가 그 높이를 계속 오가면 점선 바로 위·아래로 살짝 띄워 주가 선과 안 겹치는 자리에
    for(var dy=-26;dy<=26;dy+=2){ var yc=ym+dy; if(yc-h/2<a[a.length-1][1]-6||yc+h/2>a[0][1]+6)continue;
      for(var x=x0+2;x<=x1-w-14;x+=3){
        if(boxes.some(function(b){return x<b[2]&&x+w>b[0]&&yc-h/2<b[3]&&yc+h/2>b[1]}))continue;
        var cl=99; pts.forEach(function(p){ if(p[0]>=x-6&&p[0]<=x+w+6) cl=Math.min(cl,Math.abs(p[1]-yc)-h/2); });
        if(cl<3)continue;
        var sc=Math.min(cl,10)*2-Math.abs(dy)*0.6+x*0.01; if(!best||sc>best.sc) best={x:x,y:yc,sc:sc}; } }
    if(!best) best={x:x1-w-14,y:ym};
    var g=document.createElementNS(ns,'g'); g.setAttribute('class','mm-tag');
    var near=Math.abs(best.y-ym)<4, lx=near?best.x+w+2:best.x+w/2;
    var ln=document.createElementNS(ns,'line'); ln.setAttribute('x1',lx); ln.setAttribute('x2',x1); ln.setAttribute('y1',ym); ln.setAttribute('y2',ym); ln.setAttribute('stroke',col); ln.setAttribute('stroke-width','1'); ln.setAttribute('stroke-dasharray','3 3'); ln.setAttribute('opacity','.55'); g.appendChild(ln);
    if(!near){ var st=document.createElementNS(ns,'line'); st.setAttribute('x1',lx); st.setAttribute('x2',lx); st.setAttribute('y1',ym); st.setAttribute('y2',best.y+(best.y<ym?h/2:-h/2)); st.setAttribute('stroke',col); st.setAttribute('stroke-width','1'); st.setAttribute('opacity','.45'); g.appendChild(st); }
    var r=document.createElementNS(ns,'rect'); r.setAttribute('x',best.x); r.setAttribute('y',best.y-h/2); r.setAttribute('width',w); r.setAttribute('height',h); r.setAttribute('rx',7.5); r.setAttribute('fill',bg); r.setAttribute('stroke',col); r.setAttribute('stroke-opacity','.25'); r.setAttribute('stroke-width','.8'); g.appendChild(r);
    var tx=document.createElementNS(ns,'text'); tx.setAttribute('x',best.x+w/2); tx.setAttribute('y',best.y+3.5); tx.setAttribute('text-anchor','middle'); tx.setAttribute('font-size','10'); tx.setAttribute('font-weight','700'); tx.setAttribute('fill',col); tx.textContent=txt; g.appendChild(tx);
    boxes.push([best.x-4,best.y-h/2-2,best.x+w+4,best.y+h/2+2]);
    pr.parentNode.insertBefore(g, pr.previousSibling&&A(pr.previousSibling,'stroke-width')==='5.5'?pr.previousSibling:pr); }
  if(R) put(num(R[1]),num(R[2]),'저항 '+R[1],'#b23a2e','#fff5f4');
  if(S) put(num(S[1]),num(S[2]),'지지 '+S[1],'#1f7a3f','#f2faf4');
}
// 휴대폰을 가로로 돌리면 차트만 전체 화면(사용자 2026-10-29)
function mmLand(){ var on=false; try{ on=matchMedia('(orientation: landscape)').matches&&innerHeight<560&&!!document.querySelector('#main .mmt'); }catch(e){}
  var h=document.documentElement; if(h.classList.contains('mm-land')===on) return; h.classList.toggle('mm-land',on); setTimeout(function(){ try{mmtDraw()}catch(e){} },60); }
addEventListener('resize',function(){ clearTimeout(window.__mmLt); window.__mmLt=setTimeout(mmLand,120); }); addEventListener('orientationchange',function(){ setTimeout(mmLand,250); });
// 차트 위에서는 손가락·마우스 휠이 페이지를 움직이지 않게(사용자 2026-10-29) — 차트 훑기만
(function(){ function inChart(e){ var t=e.target; return t&&t.closest&&t.closest('#main .mmt-box svg, #main .ch svg'); }
  document.addEventListener('touchmove',function(e){ if(inChart(e)) e.preventDefault(); },{passive:false,capture:true});
  document.addEventListener('wheel',function(e){ if(inChart(e)) e.preventDefault(); },{passive:false,capture:true}); })();
function mmtTidy(){ var main=document.getElementById('main'); if(!main||!main.querySelector('.hd'))return; var w=main.querySelector('.mmt'); if(!w||w.dataset.tk!==mmTk()) mmtDraw(); }

function tidy(){
  var main=document.getElementById('main'); if(!main)return; try{mmtTidy()}catch(e){console.log(e)} try{mmtStyleDetail()}catch(e){} try{mmtAxisTags()}catch(e){console.log(e)}
  // 차트 안에서 선과 겹치던 글자 빼기(장기 추세·단기 상단·하단) — 같은 내용은 위 4칸에
  main.querySelectorAll('.ch svg text').forEach(function(t){ if(/^(장기 추세|단기 상단|단기 하단)/.test(t.textContent))t.remove(); });
  var gl=main.querySelector('p.gl'), ch=main.querySelector('.ch');
  if(gl&&ch&&!main.querySelector('.mm-lv')){
    var t=gl.textContent.replace(/\s+/g,' ');
    var R=t.match(/위 저항 후보\s*([\d,.~]+)\s*·\s*지금보다\s*([\d.~]+%)/), S=t.match(/아래 지지 후보\s*([\d,.~]+)\s*·\s*지금보다\s*([\d.~]+%)/);
    var C=t.match(/(단기 [^(]*채널)[^·]*·\s*상단\s*([\d,.]+)[^·]*·\s*하단\s*([\d,.]+)/), L=t.match(/장기 추세선보다\s*([−+\-]?[\d.]+%)/);
    var box=document.createElement('div'); box.className='mm-lv';
    function cell(cls,k,v,e){ if(!v)return; var d=document.createElement('div'); if(cls)d.className=cls; d.innerHTML='<small></small><b></b><em></em>'; d.children[0].textContent=k; d.children[1].textContent=v; d.children[2].textContent=e||''; box.appendChild(d); }
    if(R)cell('up','▲ 저항',R[1],'');
    if(S)cell('dn','▼ 지지',S[1],'');
    if(C)cell('',C[1].replace(/ 채널/,''),C[2]+'/'+C[3],'');
    if(L)cell('','장기 추세',L[1],'');
    if(box.children.length)ch.after(box);
  }
  if(gl&&!gl.closest('details')){ var nt=main.querySelector('p.nt'); var d=document.createElement('details'); d.className='mm-fold'; d.innerHTML='<summary><span>추세 가이드 자세히 · 선 읽는 법</span></summary>'; gl.before(d); d.appendChild(gl); if(nt)d.appendChild(nt); }
}
""",
 },
}

CSS_COMMON = """
details.mm-fold{margin-top:8px;border-top:1px dashed rgba(0,0,0,.12)}
details.mm-fold>summary{list-style:none;cursor:pointer;padding:9px 2px 2px;font:700 14px/1.4 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;color:#9a6200}
details.mm-fold>summary::-webkit-details-marker{display:none}
details.mm-fold>summary::after{content:" ▾"}details.mm-fold[open]>summary::after{content:" ▴"}
details.mm-fold[open]>summary{margin-bottom:8px}
"""


def run(root):
    done = []
    p = os.path.join(root, 'p-trend.html')
    if os.path.exists(p):  # 종목 차트: 휴대폰에서 차트를 크게(사용자 2026-10-29)
        s = open(p, encoding='utf-8').read(); o = s
        s = s.replace('Math.round(Math.min(300, Math.max(200, W * 0.42)))', 'Math.round(Math.min(440, Math.max(300, W * 0.95)))')
        # 금리(%) 표시: 소수 둘째 자리, 'USD' 대신 '%'(사용자 2026-10-29 채권·유가 층위)
        s = s.replace("const fmtShort = (x, cur) => { if (x == null) return ''; const d = cur === 'USD'", "const fmtShort = (x, cur) => { if (x == null) return ''; const d = cur === '%' ? 2 : cur === 'USD'")
        s = s.replace("+ ' ' + r.currency", "+ (r.currency === '%' ? '%' : ' ' + r.currency)")
        s = s.replace("const rank = (c) => (/지수|ETF/.test(c) ? 0 :", "const rank = (c) => (/지수|ETF/.test(c) ? 0 : /금리|유가/.test(c) ? 0.5 :")  # 채권·유가 층위는 지수 바로 뒤
        s = s.replace("Math.pow(10, Math.max(0, Math.floor(Math.log10(Math.abs(v))) - 3))", "Math.pow(10, Math.max((typeof r !== 'undefined' && r && r.currency === '%') ? -3 : 0, Math.floor(Math.log10(Math.abs(v))) - 3))")  # 금리는 소수까지
        # 휴대폰 스크롤 때 주소창이 숨었다 나오며 생기는 '높이만 바뀐' resize로 차트 전체를 다시 그려 깜빡이던 것 막기(사용자 2026-10-29)
        s = s.replace("let rt0 = null; addEventListener('resize', () => { clearTimeout(rt0); rt0 = setTimeout(draw, 150); });", "let rt0 = null, rw0 = innerWidth; addEventListener('resize', () => { if (innerWidth === rw0 && !window.__mmForce) return; rw0 = innerWidth; window.__mmForce = 0; clearTimeout(rt0); rt0 = setTimeout(draw, 150); });")
        s = re.sub(r'const MYLINES = \{.*?\};\n', 'const MYLINES = {};\n', s, count=1)  # 내 관점 관문선은 사이트에서 생략(사용자 2026-10-29)
        if s != o: open(p, 'w', encoding='utf-8').write(s); done.append('trend-height')
    for f, cfg in PAGES.items():
        p = os.path.join(root, f)
        if not os.path.exists(p): continue
        s = o = open(p, encoding='utf-8').read()
        s = re.sub(r'<style data-ptidy>[\s\S]*?</style><script data-ptidy>[\s\S]*?</script>', '', s)
        js = COMMON_JS + cfg['js'] + "\n(function(){var q=0;function go(){try{tidy()}catch(e){}}go();document.addEventListener('DOMContentLoaded',go);window.addEventListener('load',go);try{new MutationObserver(function(){if(q)return;q=1;setTimeout(function(){q=0;go()},150)}).observe(document.documentElement,{subtree:true,childList:true})}catch(e){}})();"
        add = '<style data-ptidy>' + CSS_COMMON + cfg['css'] + '</style><script data-ptidy>' + js + '</script>'
        s = s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add
        if s != o: open(p, 'w', encoding='utf-8').write(s); done.append(f)
    return done
