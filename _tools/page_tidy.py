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
/* 토스식 1일 차트 */
#main.mm-1d-on .mm-lv{display:none!important}
#main .hd .pr{cursor:pointer;border-bottom:1px dashed rgba(0,0,0,.18)}
.mm1d-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;margin:6px 0 2px;font-size:13px;color:#6b675f}.mm1d-h b{font-size:17px}.mm1d-h .tip{flex-basis:100%;min-height:1.2em;font-weight:700;color:#141210}
/* 추세선·채널선 가늘고 옅게, 추세 가이드 글씨 작게 */
#main .ch svg line,#main .ch svg path[stroke-dasharray]{stroke-width:1.1!important}
#main details.mm-fold p.gl,#main details.mm-fold p.nt{font-size:13px!important;line-height:1.6!important}
#main details.mm-fold p.gl small{font-size:12px!important}
/* 기간별 등락 6칸은 빼고 그만큼 차트를 크게(사용자 2026-10-29) */
#main .rt{display:none!important}
/* 차트 위 핵심 4칸(저항·지지·단기 채널·장기 추세) */
.mm-lv{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;margin:8px 0 2px}
.mm-lv>div{border-radius:11px;padding:7px 9px;background:#f6f3ec;border:1px solid rgba(0,0,0,.05);min-width:0}
.mm-lv small{display:block;font-size:11px;color:#8a877f;font-weight:700;letter-spacing:.02em}
.mm-lv b{display:block;font-size:15.5px;font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mm-lv em{font-style:normal;font-size:11.5px;color:#6b675f;font-weight:600}
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
function mmTk(){ var t=document.querySelector('#main .hd .tk'); return t?t.textContent.trim():''; }
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

function tidy(){
  var main=document.getElementById('main'); if(!main)return; try{mm1dTidy()}catch(e){}
  // 차트 안에서 선과 겹치던 글자 빼기(장기 추세·단기 상단·하단) — 같은 내용은 위 4칸에
  main.querySelectorAll('.ch svg text').forEach(function(t){ if(/^(장기 추세|단기 상단|단기 하단)/.test(t.textContent))t.remove(); });
  var gl=main.querySelector('p.gl'), ch=main.querySelector('.ch');
  if(gl&&ch&&!main.querySelector('.mm-lv')){
    var t=gl.textContent.replace(/\s+/g,' ');
    var R=t.match(/위 저항 후보\s*([\d,.~]+)\s*·\s*지금보다\s*([\d.~]+%)/), S=t.match(/아래 지지 후보\s*([\d,.~]+)\s*·\s*지금보다\s*([\d.~]+%)/);
    var C=t.match(/(단기 [^(]*채널)[^·]*·\s*상단\s*([\d,.]+)[^·]*·\s*하단\s*([\d,.]+)/), L=t.match(/장기 추세선보다\s*([−+\-]?[\d.]+%)/);
    var box=document.createElement('div'); box.className='mm-lv';
    function cell(cls,k,v,e){ if(!v)return; var d=document.createElement('div'); if(cls)d.className=cls; d.innerHTML='<small></small><b></b><em></em>'; d.children[0].textContent=k; d.children[1].textContent=v; d.children[2].textContent=e||''; box.appendChild(d); }
    if(R)cell('up','▲ 위 저항',R[1],'지금보다 +'+R[2]);
    if(S)cell('dn','▼ 아래 지지',S[1],'지금보다 −'+S[2]);
    if(C)cell('',C[1],C[2]+' / '+C[3],'상단 / 하단');
    if(L)cell('','장기 추세 대비',L[1],'12개월 추세선');
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
