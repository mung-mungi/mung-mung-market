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
.mm-sum{margin:10px 0 2px;padding:10px 12px;border-radius:12px;background:#faf8f3;border:1px solid #eee9de}
.mm-sum .ttl{display:block;font-size:14.5px;font-weight:800;color:#141210;margin-bottom:6px}
.mm-sum p{margin:0 0 5px;font-size:13.5px;line-height:1.5;color:#3a372f}.mm-sum p em{display:block;font-style:normal;font-weight:800;font-size:12.5px;color:#9a6200}
.mm-sum p.lg{margin:8px 0 0;font-size:11.5px;color:#8a877f}.mm-sum p.lg i{display:inline-block;width:12px;height:3px;border-radius:2px;margin:0 2px 2px;vertical-align:middle}

#main details.mm-fold{display:none!important}
#main .mmt-stage,#main .ch{margin-left:-12px!important;margin-right:-10px!important}
#main .mmt-per{margin-left:-4px;margin-right:-4px}
.mm-dtip{min-height:18px;height:18px;line-height:18px;margin:0;font-size:12.5px;color:#8a877f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.mm-dtip b{color:#141210;font-weight:800}.mm-dtip em{font-style:normal;font-weight:700}
#main.mmt-on:not(.mmt-detail) .mm-dtip{display:none}
.mmt-stage,#main .ch{position:relative}
.mmt-tools{position:absolute;top:0;right:0;z-index:3;display:flex;gap:5px}
.mmt-tools .mmt-tg{height:28px;padding:0 9px;font-size:12.5px;background:rgba(255,255,255,.92)}
.mmt-tools .mmt-fs{padding:0 7px}.mmt-tools .mmt-tg.on{background:#141210!important;color:#fff!important;border-color:#141210!important}.mmt-tools .mmt-drw.on{background:#9a6200!important;border-color:#9a6200!important}.mmt-box.drawing svg{cursor:crosshair}
#main.mmt-detail .mmt-drw,#main.mmt-detail .mmt-clr{display:none!important}
.mmt-pen{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:2px 0 6px;padding:6px;border-radius:12px;background:#faf6ee;border:1px solid #efe5d0}
.mmt-pen button{font:inherit;font-size:12px;font-weight:700;height:27px;padding:0 7px;border-radius:999px;border:1px solid #e3dfd6;background:#fff;color:#6b675f}
.mmt-pen button.on{background:#141210;color:#fff;border-color:#141210}
.mmt-pen i{flex:none;width:1px;height:18px;background:#e3dfd6;margin:0 2px}
.mmt-pen .pc{width:19px;height:19px;padding:0;border-radius:50%;background:var(--c)!important;border:2px solid #fff;box-shadow:0 0 0 1px #d8d3c8}
.mmt-pen .pc.on{box-shadow:0 0 0 2px var(--c)}
.mmt-pen .mmt-clr{margin-left:auto}
.mmt-pen .mmt-hint{flex:1 0 100%;margin:0;font-size:11.5px;color:#9a6200;font-weight:600}
#main.mmt-detail .mmt-pen{display:none!important}html.mm-full .mmt-pen,html.mm-land .mmt-pen{display:none!important}.mmt-x{display:none!important}
#main.mmt-detail .ch{padding-top:0;margin-top:-10px!important;margin-bottom:-10px!important}#main.mmt-detail .ch>.mmt-tools{top:0}#main .zhint{display:none!important}
/* 촘촘하게 */
#main.mmt-on{padding:10px 10px 8px!important;margin-top:6px!important;row-gap:4px!important;gap:4px!important}
#main.mmt-on .mm-rec{margin:0 0 2px!important}#main.mmt-on > .mm-shbar{margin-top:0!important}
/* 차트 페이지 아래 설명문·안내는 화면에서 빼고 '종목 바꾸기' 창 맨 아래로 */
body .wrap > p.foot,body .wrap > p.mm-foot{display:none!important}.mm-shbody .mm-foot2{margin:14px 4px 6px;font-size:11.5px;line-height:1.55;color:#9a978f}
#main.mmt-on .mm-rec{margin:0 0 6px}
#main.mmt-on .hd{margin:0!important;padding:0!important;row-gap:0!important}
#main.mmt-on .mmt{margin:0!important}#main.mmt-on .mmt-top{margin:2px 0 0!important;min-height:28px}
#main.mmt-on .mmt-per{margin:4px -4px 0!important}
html.mm-hx-off .wrap{padding-top:4px!important}
body .wrap{padding-top:0!important}#main.mmt-on{margin-top:0!important}
body{margin:0!important;padding:6px 8px 80px!important}html.mm-hx-off body .wrap{row-gap:0!important;gap:0!important}html.mm-hx-off body header.mm-hero.mm-hx{margin:0!important}
/* 배너 접힌 뒤엔 페이지가 위아래로 안 움직이게(차트만 고정) */
html.mm-hx-off.mm-lock,html.mm-hx-off.mm-lock body{overflow:hidden!important;overscroll-behavior:none}
.mm-rec{display:flex;gap:6px;align-items:center;overflow-x:auto;scrollbar-width:none;margin:-2px 0 10px;padding:2px 0}.mm-rec::-webkit-scrollbar{display:none}
.mm-rec .lb{flex:none;font-size:11.5px;font-weight:700;color:#9a978f;margin-right:2px}
.mm-rec button{flex:none;font:inherit;font-size:13px;font-weight:700;height:28px;padding:0 11px;border-radius:999px;border:1px solid #e3dfd6;background:#fff;color:#4a463f;box-shadow:0 1px 0 rgba(0,0,0,.05),0 2px 5px rgba(0,0,0,.05)}
.mm-rec button.on{background:#141210;color:#fff;border-color:#141210}
#main .mm-shbar{display:flex;width:calc(100% + 8px);margin:4px -4px 0;justify-content:center;align-items:center;gap:6px;height:40px;padding:3px;border-radius:12px;border:0;background:#f3f1ec;color:#141210;font:inherit;font-size:14.5px;font-weight:700;box-shadow:none}#main .mm-shbar small{font-size:11.5px;font-weight:600;color:#8a877f}#main .mmt-per{margin-bottom:0!important}
.mm-shbar small{font-size:11px;font-weight:600;color:#a39f96}
#mm-snd{display:none!important}
html.mm-land .mm-shbar,html.mm-full .mm-shbar{display:none}
.mm-sheet{position:fixed;inset:0;z-index:9990;pointer-events:none}
.mm-shbg{position:absolute;inset:0;background:rgba(20,18,16,.35);opacity:0;transition:opacity .25s}
.mm-shbox{position:absolute;left:0;right:0;bottom:0;height:82vh;background:#f7f5f0;border-radius:18px 18px 0 0;transform:translateY(102%);transition:transform .3s cubic-bezier(.2,.8,.2,1);display:flex;flex-direction:column;box-shadow:0 -8px 30px rgba(0,0,0,.18)}
html.mm-shon .mm-sheet{pointer-events:auto}html.mm-shon .mm-shbg{opacity:1}html.mm-shon .mm-shbox{transform:none}html.mm-shon,html.mm-shon body{overflow:hidden}
.mm-shhd{position:relative;display:flex;align-items:center;justify-content:center;height:46px;flex:none}.mm-shhd i{position:absolute;top:7px;left:50%;width:40px;height:4px;margin-left:-20px;border-radius:2px;background:#d8d3c8}.mm-shhd b{font-size:15px}
.mm-shx{position:absolute;right:12px;top:8px;width:32px;height:32px;border-radius:50%;border:1px solid #e3dfd6;background:#fff;font-size:14px}
.mm-shbody{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:0 12px max(16px,env(safe-area-inset-bottom))}
.mm-shbody section.side{margin:0!important;box-shadow:none!important}
.mm-shbody #list{max-height:none!important;overflow:visible!important}.mm-shbody .mm-lhint{display:none}
#list{max-height:560px;overflow-y:auto;overscroll-behavior:contain;padding:2px 4px 8px;margin:0 -4px;border-radius:12px;-webkit-overflow-scrolling:touch}
#list .grp+.grp{margin-top:4px!important}#list .grp h3{position:sticky;top:0;z-index:2;background:#fff;margin:0!important;padding:10px 4px 6px!important;font-size:14.5px!important}
#list .grp h3 span{font-size:11.5px!important}
#list button.row[data-mm]{display:grid!important;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr) auto 12px;align-items:center;gap:8px;padding:10px 10px 10px 14px!important;min-height:0!important;margin:0 0 7px!important;border:1px solid #ecdcb8!important;border-radius:14px!important;background:#fff!important;box-shadow:0 2px 0 rgba(30,22,8,.06),0 4px 10px rgba(30,22,8,.05)!important;text-align:left}
#list button.row[data-mm][aria-current=true]{background:#fbf3e2!important;border-color:#d9b46a!important}
#list .grp{margin:0!important;padding:0!important}#list .grp .rows{margin:0!important;gap:0!important}
#list .row .l{min-width:0;display:flex;flex-direction:column;gap:2px}#list .row .l b{order:1;font-size:15.5px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}#list .row .l i{order:2;font-style:normal;font-size:11.5px;color:#8a877f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#list .row .m{min-width:0;display:flex;flex-direction:column;align-items:stretch;gap:3px}#list .row .m em{font-style:normal;font-weight:800;font-size:15px;text-align:right}
#list .row .bar{position:relative;height:5px;border-radius:3px;background:linear-gradient(90deg,#b4c6ec,#e8e4dc,#efb3ae)}#list .row .bar s{position:absolute;top:-3px;width:3px;height:11px;margin-left:-1.5px;border-radius:2px;background:#141210;text-decoration:none}
#list .row .rg{display:flex;justify-content:space-between;font-size:10.5px;color:#9a978f}#list .row .rg u{text-decoration:none}
#list .row .r{display:flex;flex-direction:column;align-items:flex-end;gap:2px;min-width:52px}#list .row .r strong{font-size:16px;font-weight:800}#list .row .r small{font-size:11px;color:#8a877f;white-space:nowrap}
#list .row .r strong.up{color:#e0423a!important}#list .row .r strong.dn,#list .row .r strong.down{color:#3a6fe0!important}
#list .row .go{color:#9a6200;font-size:20px;font-weight:700;line-height:1}
.mm-lhint{margin:4px 2px 0;font-size:12px;color:#9a6200;text-align:center}
/* 종목 차트에선 멍뭉이 배너·오늘 한눈에 카드 숨기고 차트가 바로 보이게(사용자 2026-10-29) — 기준 시각은 차트 카드 위에 작게 */
html body .mm-take,html body .hx-card{display:none!important}
/* 멍뭉이 배너: 처음 5초 보이고 접힘, 20초 동안 아무것도 안 하면 다시 펼쳐짐(사용자 2026-10-29) */
html body header.mm-hero.mm-hx{overflow:hidden;max-height:240px;transition:max-height .45s ease,opacity .35s ease,margin .45s ease,padding .45s ease}
html.mm-hx-off body header.mm-hero.mm-hx{max-height:0!important;min-height:0!important;height:0!important;opacity:0;margin-top:0!important;margin-bottom:0!important;padding-top:0!important;padding-bottom:0!important;border-width:0!important}
.mm-asof2{margin:2px 4px 8px;font-size:12px;color:#8a877f;text-align:right}
#main .rg .zm{display:none!important}
#main .rg{background:#f3f1ec;padding:3px!important;border-radius:12px;gap:4px!important;overflow:hidden!important}
#main .rg .pb-chip{flex:1 1 0!important;min-width:0;border:0!important;background:transparent!important;box-shadow:none!important;color:#8a877f!important;font-size:14px!important;font-weight:700!important;padding:7px 0!important;border-radius:9px!important;justify-content:center;text-align:center}
#main .rg .pb-chip[aria-pressed=true]{background:#fff!important;color:#141210!important;box-shadow:0 1px 0 rgba(0,0,0,.06),0 2px 6px rgba(0,0,0,.08)!important}
#main .rg .gd{display:none!important}
.mmt-per button{font-size:13.5px!important;padding:7px 0!important;letter-spacing:-.02em}
html.mm-full,html.mm-full body{overflow:hidden!important;height:100%;overscroll-behavior:none}
html.mm-full #main .mmt{position:fixed;inset:0;z-index:9999;background:#fff;display:flex!important;flex-direction:column;padding:10px max(14px,env(safe-area-inset-right)) max(8px,env(safe-area-inset-bottom)) max(14px,env(safe-area-inset-left))}
html.mm-full .mmt-ttl{display:block;font-size:16px;font-weight:800;color:#141210}
html.mm-full .mmt-stage{flex:1;min-height:0;display:flex;flex-direction:column}html.mm-full .mmt-box{flex:1;min-height:0}
html.mm-full .mmt-tools{position:static!important;justify-content:flex-end;margin:4px 0 2px}html.mm-full .mmt-stage{position:relative}html.mm-full #main .mmt{padding-top:max(18px,calc(env(safe-area-inset-top) + 10px))!important}html.mm-full .mmt-find.on{top:118px!important}
html.mm-full .mmt-tools .mmt-det,html.mm-full .mmt-tools .mmt-fs{display:none!important}html.mm-full .mmt-x{display:inline-flex!important;font-size:15px}
html.mm-land .mmt-tools .mmt-fs{display:none!important}
.mmt-ext{display:none!important;text-decoration:none;align-items:center}html.mm-land .mmt.kakao .mmt-ext,html.mm-full .mmt.kakao .mmt-ext{display:inline-flex!important;background:#fee500!important;border-color:#e6cf00!important;color:#191600!important}
html.mm-land #main .mmt,html.mm-full #main .mmt{box-sizing:border-box}
.mmt-q{display:none!important}html.mm-land .mmt-q,html.mm-full .mmt-q{display:inline-flex!important;padding:0 8px!important}
.mmt-find{display:none}html.mm-land .mmt-find.on,html.mm-full .mmt-find.on{display:block;position:absolute;z-index:6;top:44px;right:max(12px,env(safe-area-inset-right));width:min(420px,70vw);padding:8px;border-radius:14px;background:#fff;border:1px solid #e3dfd6;box-shadow:0 8px 28px rgba(0,0,0,.16)}
.mmt-find input{width:100%;box-sizing:border-box;height:36px;border-radius:10px;border:1px solid #e3dfd6;padding:0 12px;font:inherit;font-size:16px;background:#faf8f3}
.mmt-res{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px;max-height:42vh;overflow:auto}
.mmt-res button{font:inherit;font-size:13px;height:30px;padding:0 10px;border-radius:999px;border:1px solid #e3dfd6;background:#fff;color:#141210;white-space:nowrap}.mmt-res button small{color:#9a6200;font-weight:700}
html.mm-land .mmt-stage{position:static!important}html.mm-land .mmt-tools{position:absolute!important;top:8px!important;right:max(12px,env(safe-area-inset-right))!important}html.mm-land .mmt-ttl{padding-right:330px}
.mmt-ttl{display:none}
#main .mmt-box svg,#main .ch svg{touch-action:none!important;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
html.mm-land,html.mm-land body{overflow:hidden!important;height:100%;overscroll-behavior:none}html.mm-land #main .mmt{touch-action:none;overscroll-behavior:contain}html.mm-land #main .mmt svg{touch-action:none!important}
html.mm-land #main .mmt{position:fixed;inset:0;z-index:9999;background:#fff;display:flex!important;flex-direction:column;padding:8px max(14px,env(safe-area-inset-right)) 6px max(14px,env(safe-area-inset-left))}
html.mm-land .mmt-ttl{display:block;font-size:15px;font-weight:800;color:#141210;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html.mm-land #main .mmt .mmt-box,html.mm-land #main .mmt .mmt-chg,html.mm-land #main .mmt .mmt-per{display:flex!important}
html.mm-land #main .mmt .mmt-chg{display:block!important}
html.mm-land .mmt-stage{flex:1;min-height:0;display:flex;flex-direction:column}html.mm-land .mmt-box{flex:1;min-height:0;flex-direction:column}
html.mm-land .mmt-det{display:none!important}html.mm-land .mmt-trd{display:inline-flex!important}
html.mm-land .mmt-per{margin:4px 0 0}html.mm-land .mmt-per button{padding:5px 0}html.mm-land .mmt-top{min-height:28px}
#main.mmt-detail .mmt-trd{display:none}

#main.mmt-on:not(.mmt-detail) .rg,#main.mmt-on:not(.mmt-detail) .ch,#main.mmt-on:not(.mmt-detail) .mm-lv,#main.mmt-on:not(.mmt-detail) details.mm-fold,#main.mmt-on:not(.mmt-detail) p.nt{display:none!important}
#main.mmt-on .ch,#main.mmt-on .rt,#main.mmt-on .mm-dtip,#main.mmt-on .mm-lv:not(.mm2),#main.mmt-on .mm-sum:not(.mm2),#main.mmt-on details.mm-fold{display:none!important}#main.mmt-detail .mmt-zn{display:none}
.mmt-chg b.sc{color:#141210;font-weight:800;font-size:13.5px}#main.mmt-on .rg{display:none!important}#main.mmt-detail .mmt-trd{display:none}
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
  'sync': True,
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
    el.addEventListener('pointerleave',function(){ el.querySelector('.cx').setAttribute('opacity','0'); el.querySelector('.cd').setAttribute('opacity','0'); });
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
var MMT_PER = [['1d','1일','오늘'],['1w','1주','지난주보다'],['1m','1달','지난달보다'],['3m','3달','3달 전보다'],['1y','1년','1년 전보다'],['5y','5년','5년 전보다'],['10y','10년','10년 전보다']];
function mmtRow(){ var tk=mmTk(); try{ return DATA.P.filter(function(r){return r.ticker===tk})[0]; }catch(e){ return null; } }
function mmtDaily(tk){ try{ return (DATA.H[tk]||[]).filter(function(a){return !a[2]}).map(function(a){return [Date.parse(a[0]+'T21:00:00Z')/1000,a[1]]}); }catch(e){ return []; } }
function mmtFmt(v,cur){ if(cur==='%') return v.toFixed(3).replace(/0$/,'')+'%'; var d=(cur==='KRW'||cur==='JPY')?0:2; return (cur==='USD'?'$':'')+v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d})+(cur==='KRW'?'원':cur&&cur!=='USD'?' '+cur:''); }
function mmtTick(v,cur,st){ if(Math.abs(v)<st*1e-6) v=0; var d=st<0.01?3:st<0.1?2:st<1?1:0; if(cur==='%') return v.toFixed(Math.max(d,1))+'%'; if(v>=100000) return (v/10000).toLocaleString('en-US',{maximumFractionDigits:1})+'만'; return v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d}); }
function mmtKst(sec,withDate){ var d=new Date(sec*1000+9*3600000), p=function(n){return (n<10?'0':'')+n}; return withDate?(d.getUTCFullYear()%100)+'.'+(d.getUTCMonth()+1)+'.'+d.getUTCDate():p(d.getUTCHours())+':'+p(d.getUTCMinutes()); }
function mmRG(pts){ var RG=null; if(pts.length>8){ var N=pts.length, iX=0, iN=0; pts.forEach(function(p,k){ if(p[1]>pts[iX][1])iX=k; if(p[1]<pts[iN][1])iN=k; });
    var minLeg=Math.max(5,Math.round(N*0.15)), cand=[[iX,-1],[iN,1]].filter(function(c){return N-1-c[0]>=minLeg}).sort(function(a,b){return b[0]-a[0]});
    if(cand.length){ var a0=cand[0][0], dir=cand[0][1], A=pts[a0], best=null;
      var gap=Math.max(3,Math.round((N-1-a0)*0.25)); // 꼭짓점 바로 옆 날(거의 같은 높이)에 걸려 선이 평평해지던 것 방지
      for(var k=a0+gap;k<Math.max(a0+gap+1,N-2);k++){ var sl=(pts[k][1]-A[1])/(pts[k][0]-A[0]); /* 마지막 이틀은 빼야 지금 가격이 선을 넘었는지 볼 수 있음 */ if(best===null||(dir<0?sl>best:sl<best)) best=sl; } if(best===null) best=0; // 하락: 모든 점 아래로 두는 가장 완만한 선 / 상승: 모든 점 위로 두는 가장 완만한 선
      var main_=function(t){return A[1]+best*(t-A[0])}, off=0; for(var k=a0;k<N;k++){ var d=pts[k][1]-main_(pts[k][0]); if(dir<0? d<off : d>off) off=d; }
      var par=function(t){return main_(t)+off};
      RG={dir:dir, ta:A[0], tb:pts[N-1][0], up:dir<0?main_:par, dn:dir<0?par:main_, anchor:A}; } } return RG; }
// 이전 추세들(사용자 2026-10-29): 지금 추세 시작점 전의 큰 오르내림(꼭짓점→꼭짓점)마다 채널 하나씩, 최대 3개
function mmLegs(pts, before){ var P=pts.filter(function(p){return p[0]<=before}); if(P.length<12) return [];
  var chg=P.slice(1).map(function(p,i){return Math.abs(p[1]/P[i][1]-1)}).sort(function(a,b){return a-b}), med=chg[Math.floor(chg.length/2)]||0.02; var piv=null; [Math.min(0.25,Math.max(0.08,med*6))].forEach(function(th){ var pv=[0], dir=0, ex=0, hi=0, lo=0;
    for(var i=1;i<P.length;i++){ var v=P[i][1];
      if(dir===0){ if(v>P[hi][1])hi=i; if(v<P[lo][1])lo=i; if(v<P[hi][1]*(1-th)){ pv=[hi]; ex=i; dir=-1; } else if(v>P[lo][1]*(1+th)){ pv=[lo]; ex=i; dir=1; } continue; }
      if(dir>0){ if(v>P[ex][1]) ex=i; else if(v<P[ex][1]*(1-th)){ pv.push(ex); ex=i; dir=-1; } }
      else { if(v<P[ex][1]) ex=i; else if(v>P[ex][1]*(1+th)){ pv.push(ex); ex=i; dir=1; } } }
    pv.push(P.length-1); piv=pv; });
  var legs=[]; for(var k=0;k<piv.length-1;k++){ var a=piv[k], b=piv[k+1]; if(b-a<8) continue; var seg=P.slice(a,b+1), dir=seg[seg.length-1][1]>=seg[0][1]?1:-1, A=seg[0], best=null;
    for(var j=Math.max(2,Math.round(seg.length*0.25));j<seg.length;j++){ var sl=(seg[j][1]-A[1])/(seg[j][0]-A[0]); if(best===null||(dir<0?sl>best:sl<best)) best=sl; }
    var mf=function(A,best){return function(t){return A[1]+best*(t-A[0])}}(A,best), off=0; seg.forEach(function(p){ var d=p[1]-mf(p[0]); if(dir<0?d<off:d>off) off=d; });
    legs.push({dir:dir, ta:A[0], tb:seg[seg.length-1][0], up:dir<0?mf:function(m,o){return function(t){return m(t)+o}}(mf,off), dn:dir<0?function(m,o){return function(t){return m(t)+o}}(mf,off):mf}); }
  return legs.slice(-3); }
function mmtChart(box, pts, base, cur, intra, opt){ opt=opt||{}; var OV=opt.ov||{}, CD=opt.cdl||null;
  var LAND=document.documentElement.classList.contains('mm-land')||document.documentElement.classList.contains('mm-full'), W=Math.max(260,box.clientWidth||330), H=LAND?Math.max(150,(box.clientHeight||innerHeight-120)-22):(window.__mmFitH||Math.round(Math.min(430,Math.max(280,W*0.86)))), m={l:4,r:38,t:50,b:30};
  var t0=pts[0][0], t1=pts[pts.length-1][0]; if(intra){ t0=Math.min(t0,intra.x0); t1=Math.max(t1,intra.x1); }
  if(!LAND) window.__mmH=H; // 자세한 차트도 같은 높이로
  var RNG=opt.rng||CD; var vs=RNG?[].concat.apply([],RNG.map(function(c){return [c[2],c[3]]})):pts.map(function(a){return a[1]}); if(base!=null) vs.push(base);
  // 추세(사용자 2026-10-29): 기간 안 가장 최근의 큰 꼭짓점(최고점·최저점)부터 지금까지의 흐름만 — 하락이면 고점들을 잇는 선 + 같은 기울기 아래 선, 상승이면 저점들을 잇는 선 + 위 선
  var RG=((OV.tr||(window.__mmT&&window.__mmT.tr))&&!opt.noTr)?mmRG(pts):null;
  var lo=Math.min.apply(0,vs), hi=Math.max.apply(0,vs), pad=(hi-lo)*0.08||hi*0.01; lo-=pad; hi+=pad;
  var sx=function(t){return m.l+(t-t0)/((t1-t0)||1)*(W-m.l-m.r)}, sy=function(v){return m.t+(hi-v)/(hi-lo)*(H-m.t-m.b)};
  var last=pts[pts.length-1], up=base==null||last[1]>=base, col=up?'#e0423a':'#3a6fe0';
  var path=pts.map(function(a,i){return (i?'L':'M')+sx(a[0]).toFixed(1)+','+sy(a[1]).toFixed(1)}).join('');
  var iMax=0,iMin=0; pts.forEach(function(a,i){ if(a[1]>pts[iMax][1])iMax=i; if(a[1]<pts[iMin][1])iMin=i; });
  var lab=function(i,top){ var a=pts[i], x=sx(a[0]), y=sy(a[1]), anc=x<W*0.2?'start':x>W*0.8?'end':'middle';
    var lc=(base!=null)?(a[1]>=base?'#e0423a':'#3a6fe0'):col;
    return '<circle cx="'+x+'" cy="'+y+'" r="3" fill="'+lc+'" opacity=".55"/><text x="'+x+'" y="'+(top?y-9:y+17)+'" font-size="11.5" fill="'+lc+'" text-anchor="'+anc+'">'+(top?'최고 ':'최저 ')+mmtFmt(a[1],cur)+'</text>'; };
  var s='<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;height:'+(LAND?H+'px':'auto')+';display:block;touch-action:none">';
  if(intra){ s+='<rect x="'+sx(intra.rs)+'" y="'+m.t+'" width="'+(sx(intra.re)-sx(intra.rs))+'" height="'+(H-m.t-m.b)+'" fill="#000" opacity=".025"/>'
     +'<text x="'+sx(intra.rs)+'" y="'+(H-8)+'" font-size="10.5" fill="#9a978f" text-anchor="middle">'+mmtKst(intra.rs)+' 개장</text><text x="'+sx(intra.re)+'" y="'+(H-8)+'" font-size="10.5" fill="#9a978f" text-anchor="middle">'+mmtKst(intra.re)+' 마감</text>'; }
  // 눈금(사용자 2026-10-29): 오른쪽 가격 3~4개, 아래 날짜 3~4개 — 옅게
  (function(){ var span=hi-lo, raw=span/7, p=Math.pow(10,Math.floor(Math.log10(raw))), st=[1,2,2.5,5,10].map(function(k){return k*p}).filter(function(k){return k>=raw*0.75})[0]||raw;
    var CY=RG?[sy(RG.up(RG.tb)),sy(RG.dn(RG.tb))].map(function(y){return (y<m.t||y>H-m.b)?-99:y}):[];
    for(var v=Math.ceil(lo/st)*st; v<=hi; v+=st){ var y=sy(v); if(y<m.t+6||y>H-m.b-4) continue; if(CY.some(function(c){return Math.abs(c-y)<13})||(base!=null&&Math.abs(sy(base)-y)<12)){ s+='<line x1="'+m.l+'" x2="'+(W-m.r+4)+'" y1="'+y+'" y2="'+y+'" stroke="#ece9e2" stroke-width="1"/>'; continue; }
      s+='<line x1="'+m.l+'" x2="'+(W-m.r+4)+'" y1="'+y+'" y2="'+y+'" stroke="#ece9e2" stroke-width="1"/><text x="'+(W-2)+'" y="'+(y+4)+'" font-size="10.5" fill="#a29f97" text-anchor="end">'+mmtTick(v,cur,st)+'</text>'; }
    if(!intra){ var sp=(t1-t0)/86400; for(var k=0;k<4;k++){ var t=t0+(t1-t0)*(k+0.5)/4, d=new Date(t*1000+9*3600000), lb=sp<=100?(d.getUTCMonth()+1)+'/'+d.getUTCDate():sp<=400?(d.getUTCFullYear()%100)+'.'+(d.getUTCMonth()+1):(d.getUTCFullYear())+'';
      s+='<text x="'+sx(t)+'" y="'+(H-8)+'" font-size="10.5" fill="#a29f97" text-anchor="middle">'+lb+'</text>'; } }

    s+='<clipPath id="mmclip2"><rect x="'+m.l+'" y="'+m.t+'" width="'+(W-m.l-m.r)+'" height="'+(H-m.t-m.b)+'"/></clipPath>';
    if(OV.zn&&opt.zones){ var Z=opt.zones; s+='<g clip-path="url(#mmclip2)">';
      [[Z.up2,'#c4453a',.06,0],[Z.dn2,'#2f8a4c',.06,0],[Z.up,'#c4453a',.13,1],[Z.dn,'#2f8a4c',.13,1]].forEach(function(z){ var c=z[0]; if(!c)return; var ya=sy(c.b), yb=sy(c.a); if(yb<m.t||ya>H-m.b) return;
        s+='<rect x="'+m.l+'" width="'+(W-m.l-m.r)+'" y="'+ya+'" height="'+Math.max(3,yb-ya)+'" fill="'+z[1]+'" opacity="'+z[2]+'"/>';
        if(z[3]) s+='<text x="'+(m.l+4)+'" y="'+(c===Z.up?ya-3:yb+11)+'" font-size="10" font-weight="700" fill="'+z[1]+'" opacity=".9" paint-order="stroke" stroke="#fff" stroke-width="3">'+(c===Z.up?'저항 ':'지지 ')+mmtTick(c.a,cur,(hi-lo)/40)+'~'+mmtTick(c.b,cur,(hi-lo)/40)+'</text>'; });
      s+='</g>'; }
    if(OV.lt&&opt.lt){ var tA=Math.max(t0,Date.now()/1000-366*86400), ya_=opt.lt(tA), yb_=opt.lt(t1); s+='<g clip-path="url(#mmclip2)"><line x1="'+sx(tA)+'" x2="'+sx(t1)+'" y1="'+sy(ya_)+'" y2="'+sy(yb_)+'" stroke="#8a877f" stroke-width="1.2" stroke-dasharray="7 4" opacity=".55"/></g>'; }
    if(RG){ var LG=mmLegs(pts, RG.ta); if(LG.length){ s+='<g clip-path="url(#mmclip2)">'; LG.slice(-2).forEach(function(L,ix){ var xa=sx(L.ta), xb=sx(L.tb), F=L.dir>0?L.dn:L.up, c=L.dir>0?'#2f8a4c':'#c4453a';
        s+='<line x1="'+xa+'" x2="'+xb+'" y1="'+sy(F(L.ta))+'" y2="'+sy(F(L.tb))+'" stroke="'+c+'" stroke-width="1.3" opacity=".5"/>'; }); s+='</g>'; } }
    var RGr=null; if(RG&&(t1-t0)>120*86400){ var p3=pts.filter(function(p){return p[0]>=t1-92*86400}); RGr=mmRG(p3); if(RGr&&Math.abs(RGr.ta-RG.ta)<5*86400) RGr=null; }
    if(RGr){ var xa=sx(RGr.ta), xb=sx(RGr.tb), Ua=RGr.up(RGr.ta), Ub=RGr.up(RGr.tb), Da=RGr.dn(RGr.ta), Db=RGr.dn(RGr.tb);
      s+='<g clip-path="url(#mmclip2)">'
       +(RGr.dir<0?'<line x1="'+xa+'" x2="'+xb+'" y1="'+sy(Ua)+'" y2="'+sy(Ub)+'" stroke="#c4453a" stroke-width="1.6" opacity=".8"/>':'<line x1="'+xa+'" x2="'+xb+'" y1="'+sy(Da)+'" y2="'+sy(Db)+'" stroke="#2f8a4c" stroke-width="1.6" opacity=".8"/>')+'</g>'; }
    if(RG){ // 추세(사용자 2026-10-29 '이해가 쉽게'): 주 추세선 하나(하락=고점 잇는 빨강, 상승=저점 잇는 초록)를 진하게 + 오른쪽 점선 연장, 반대쪽 평행선은 옅은 점선만
      var xa=sx(RG.ta), xb=sx(RG.tb), dn=RG.dir<0, F=dn?RG.up:RG.dn, G=dn?RG.dn:RG.up, c=dn?'#c4453a':'#2f8a4c', c2=dn?'#2f8a4c':'#c4453a';
      var tE=RG.tb+(RG.tb-RG.ta)*0.15, xE=sx(tE), Fb=F(RG.tb), Gb=G(RG.tb), above=dn?(last[1]>Fb):(last[1]<Fb);
      s+='<clipPath id="mmclip"><rect x="'+m.l+'" y="'+m.t+'" width="'+(W-m.l-m.r)+'" height="'+(H-m.t-m.b)+'"/></clipPath><g clip-path="url(#mmclip)">'
       +'<line x1="'+xa+'" x2="'+xb+'" y1="'+sy(G(RG.ta))+'" y2="'+sy(Gb)+'" stroke="'+c2+'" stroke-width="1" stroke-dasharray="3 4" opacity=".45"/>'
       +'<line x1="'+xa+'" x2="'+xb+'" y1="'+sy(F(RG.ta))+'" y2="'+sy(Fb)+'" stroke="'+c+'" stroke-width="2" opacity=".9"/>'
       +'<line x1="'+xb+'" x2="'+xE+'" y1="'+sy(Fb)+'" y2="'+sy(F(tE))+'" stroke="'+c+'" stroke-width="1.6" stroke-dasharray="4 3" opacity=".75"/>'
       +'<circle cx="'+xa+'" cy="'+sy(RG.anchor[1])+'" r="3.5" fill="#fff" stroke="'+c+'" stroke-width="1.6"/></g>'
       +(CY[0]<0?'':'<text x="'+(W-2)+'" y="'+((dn?CY[0]:CY[1])+4)+'" font-size="10.5" font-weight="800" fill="'+c+'" text-anchor="end">'+mmtTick(Fb,cur,(hi-lo)/40)+'</text>')
       +'<text x="'+(m.l+2)+'" y="'+(m.t-9)+'" font-size="11" font-weight="700" fill="'+c+'">'+(dn?'하락 추세선 ↘':'상승 추세선 ↗')+' <tspan font-weight="500" fill="#6b675f">'+mmtKst(RG.ta,true).replace(/^\d+\./,'').replace('.','/')+' '+(dn?'고점들을 이은 선':'저점들을 이은 선')+' · '+(dn?(above?'지금 선 위 → 탈출 시도':'선 넘으면 탈출'):(above?'지금 선 아래 → 이탈':'선 깨지면 이탈'))+'</tspan></text>'; }
  })();
  // 기준선(1일은 어제 종가, 그 밖은 기간 시작가): 또렷하게 + 값 표시. 선은 위는 빨강·아래는 파랑(양전·음전, 사용자 2026-10-29)
  var yB=base!=null?sy(base):null; if(yB!=null&&yB>m.t-2&&yB<H-m.b+2) s+='<line x1="'+m.l+'" x2="'+(W-m.r+2)+'" y1="'+yB+'" y2="'+yB+'" stroke="#9a978f" stroke-dasharray="4 3" stroke-width="1" opacity=".8"/><text x="'+(W-2)+'" y="'+(yB+4)+'" font-size="10" font-weight="700" fill="#6b675f" text-anchor="end">'+(intra?'전일 ':'시작 ')+mmtTick(base,cur,(hi-lo)/40)+'</text>';
  if(CD){ var bw=Math.max(1,Math.min(9,(W-m.l-m.r)/CD.length*0.62));
    CD.forEach(function(c){ var x=sx(c[0]), u=c[4]>=c[1], cc=u?'#e0423a':'#3a6fe0', yo=sy(c[1]), yc=sy(c[4]);
      s+='<line x1="'+x+'" x2="'+x+'" y1="'+sy(c[2])+'" y2="'+sy(c[3])+'" stroke="'+cc+'" stroke-width="1"/><rect x="'+(x-bw/2)+'" y="'+Math.min(yo,yc)+'" width="'+bw+'" height="'+Math.max(1,Math.abs(yc-yo))+'" fill="'+cc+'"/>'; });
    var jX=0,jN=0; CD.forEach(function(c,i){ if(c[2]>CD[jX][2])jX=i; if(c[3]<CD[jN][3])jN=i; });
    var lab2=function(c,top){ var x=sx(c[0]), v=top?c[2]:c[3], y=sy(v), anc=x<W*0.2?'start':x>W*0.8?'end':'middle'; return '<text x="'+x+'" y="'+(top?y-7:y+15)+'" font-size="11.5" fill="'+(top?'#e0423a':'#3a6fe0')+'" text-anchor="'+anc+'">'+(top?'최고 ':'최저 ')+mmtFmt(v,cur)+'</text>'; };
    s+=lab2(CD[jX],true)+lab2(CD[jN],false); }
  else if(yB!=null){ var cid='mmb'+Math.random().toString(36).slice(2,7);
    s+='<clipPath id="'+cid+'u"><rect x="0" y="0" width="'+W+'" height="'+Math.max(0,yB)+'"/></clipPath><clipPath id="'+cid+'d"><rect x="0" y="'+yB+'" width="'+W+'" height="'+Math.max(0,H-yB)+'"/></clipPath>'
     +'<path d="'+path+'" fill="none" stroke="#e0423a" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" clip-path="url(#'+cid+'u)"/>'
     +'<path d="'+path+'" fill="none" stroke="#3a6fe0" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" clip-path="url(#'+cid+'d)"/>'+lab(iMax,true)+lab(iMin,false); }
  else s+='<path d="'+path+'" fill="none" stroke="'+col+'" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'+lab(iMax,true)+lab(iMin,false);
  s+=''
   +(CD?'':'<circle cx="'+sx(last[0])+'" cy="'+sy(last[1])+'" r="4.5" fill="'+col+'" stroke="#fff" stroke-width="2"/>')
   +'<line class="cx" x1="0" x2="0" y1="'+m.t+'" y2="'+(H-m.b)+'" stroke="#141210" stroke-width="1" opacity="0"/><circle class="cd" r="4.5" fill="#141210" opacity="0"/></svg>';
  box.innerHTML=s;
  var el=box.querySelector('svg'), chgEl=document.querySelector('#main .mmt-chg'), tip={set textContent(v){ if(!chgEl)return; if(!chgEl.dataset.sc){ chgEl.dataset.sc=1; chgEl.dataset.o=chgEl.innerHTML; } chgEl.innerHTML='<b class="sc"></b>'; chgEl.firstChild.textContent=v; }};
  function mv(e){ var r=el.getBoundingClientRect(), t=t0+((e.clientX-r.left)/r.width*W-m.l)/(W-m.l-m.r)*(t1-t0), b=pts[0];
    pts.forEach(function(a){ if(Math.abs(a[0]-t)<Math.abs(b[0]-t))b=a; });
    var cx=el.querySelector('.cx'), cd=el.querySelector('.cd'); cx.setAttribute('x1',sx(b[0]));cx.setAttribute('x2',sx(b[0]));cx.setAttribute('opacity','.3'); cd.setAttribute('cx',sx(b[0]));cd.setAttribute('cy',sy(b[1]));cd.setAttribute('opacity','1');
    var cc=CD&&CD.filter(function(c){return c[0]===b[0]})[0];
    if(cc){ tip.textContent=(intra?mmtKst(b[0]):mmtKst(b[0],true))+'  시 '+mmtTick(cc[1],cur,(hi-lo)/40)+' 고 '+mmtTick(cc[2],cur,(hi-lo)/40)+' 저 '+mmtTick(cc[3],cur,(hi-lo)/40)+' 종 '+mmtFmt(cc[4],cur); return; }
    tip.textContent=(intra?mmtKst(b[0]):mmtKst(b[0],true))+'  '+mmtFmt(b[1],cur)+(base?'  ('+((b[1]/base-1)*100>=0?'+':'−')+Math.abs((b[1]/base-1)*100).toFixed(2)+'%)':''); }
  // 내 선 그리기(사용자 2026-10-29): '✎ 선'을 켜고 차트 위를 끌면 직선, 종목별로 이 기기에 저장
  var NS='http://www.w3.org/2000/svg', tk=mmTk(), inv=function(e){ var r=el.getBoundingClientRect(), x=(e.clientX-r.left)/r.width*W, y=(e.clientY-r.top)/r.height*H; return [t0+(x-m.l)/(W-m.l-m.r)*(t1-t0), hi-(y-m.t)/(H-m.t-m.b)*(hi-lo)]; };
  // 선 종류: tr 추세선(두 점) · h 수평선(한 가격) · par 평행 채널(선 긋고 한 번 더 누른 곳에 평행선) / 색 4가지
  function ln(g,x1,y1,x2,y2,c,w,da,op){ var e=document.createElementNS(NS,'line'); e.setAttribute('x1',x1);e.setAttribute('y1',y1);e.setAttribute('x2',x2);e.setAttribute('y2',y2);e.setAttribute('stroke',c);e.setAttribute('stroke-width',w||1.8);e.setAttribute('stroke-linecap','round'); if(da)e.setAttribute('stroke-dasharray',da); if(op)e.setAttribute('opacity',op); g.appendChild(e); }
  function dot(g,x,y,c){ var e=document.createElementNS(NS,'circle'); e.setAttribute('cx',x);e.setAttribute('cy',y);e.setAttribute('r','2.6');e.setAttribute('fill',c); g.appendChild(e); }
  function drawL(l,tmp){ var g=document.createElementNS(NS,'g'); g.setAttribute('class',tmp?'ml tmp':'ml'); var c=l.c||'#9a6200', xe=W-m.r;
    if(l.k==='h'){ var y=sy(l.a[1]); ln(g,m.l,y,xe,y,c,1.5,'6 4'); var tx=document.createElementNS(NS,'text'); tx.setAttribute('x',W-2);tx.setAttribute('y',y+4);tx.setAttribute('font-size','10');tx.setAttribute('font-weight','800');tx.setAttribute('fill',c);tx.setAttribute('text-anchor','end'); tx.textContent=mmtTick(l.a[1],cur,(hi-lo)/40); g.appendChild(tx); }
    else { var x1=sx(l.a[0]),y1=sy(l.a[1]),x2=sx(l.b[0]),y2=sy(l.b[1]); var offs=[0]; if(l.k==='par'&&l.off!=null) offs.push(l.off);
      offs.forEach(function(o,ix){ var Y1=sy(l.a[1]+o), Y2=sy(l.b[1]+o); ln(g,x1,Y1,x2,Y2,c,ix?1.5:1.8,null,ix?'.85':null);
        if(!tmp&&Math.abs(x2-x1)>4){ var k=(Y2-Y1)/(x2-x1); ln(g,x2,Y2,xe,Y2+k*(xe-x2),c,1.2,'4 4','.6'); } });
      if(l.k==='par'&&l.off!=null){ var p=document.createElementNS(NS,'path'); p.setAttribute('d','M'+x1+','+y1+'L'+x2+','+y2+'L'+x2+','+sy(l.b[1]+l.off)+'L'+x1+','+sy(l.a[1]+l.off)+'Z'); p.setAttribute('fill',c); p.setAttribute('opacity','.07'); g.insertBefore(p,g.firstChild); }
      dot(g,x1,y1,c); dot(g,x2,y2,c); }
    el.insertBefore(g, el.querySelector('.cx')); return g; }
  var lineAt=function(l,t){ return l.a[1]+(l.b[1]-l.a[1])*(t-l.a[0])/((l.b[0]-l.a[0])||1); };
  mmLines(tk).forEach(function(l){ if(l.k==='h'||l.b[0]>=t0-86400*3) drawL(l); });
  var dr=null, P0=window.__mmPend&&window.__mmPend.tk===tk?window.__mmPend:null;
  el.addEventListener('pointerdown',function(e){ var T=window.__mmT||{}; if(!T.draw)return; e.preventDefault(); try{el.setPointerCapture(e.pointerId)}catch(x){} var p=inv(e), c=T.pc||'#9a6200', k=T.pk||'tr';
    if(window.__mmPend&&window.__mmPend.tk===tk){ var q=window.__mmPend; q.l.off=p[1]-lineAt(q.l,p[0]); var Ls=mmLines(tk); Ls.push(q.l); mmLines(tk,Ls); window.__mmPend=null; mmtDraw(); mmToolsSync(); return; }
    dr={l:{k:k,a:p,b:p,c:c}}; dr.g=drawL(dr.l,true); },true);
  el.addEventListener('pointermove',function(e){ if(!dr)return; e.stopImmediatePropagation(); var p=inv(e); if(dr.l.k==='h') dr.l.a=p; else dr.l.b=p; dr.g.remove(); dr.g=drawL(dr.l,true); },true);
  el.addEventListener('pointerup',function(e){ if(!dr)return; var l=dr.l; dr.g.remove(); dr=null;
    if(l.k==='h'){ var Ls=mmLines(tk); Ls.push({k:'h',a:l.a,c:l.c}); mmLines(tk,Ls); drawL(Ls[Ls.length-1]); mmToolsSync(); return; }
    var dx=Math.abs(sx(l.b[0])-sx(l.a[0])), dy=Math.abs(sy(l.b[1])-sy(l.a[1])); if(dx+dy<=14) return; if(l.b[0]<l.a[0]){ var q=l.a; l.a=l.b; l.b=q; }
    if(l.k==='par'){ window.__mmPend={tk:tk,l:l}; drawL(l,true); mmToolsSync(); return; }
    var Ls=mmLines(tk); Ls.push(l); mmLines(tk,Ls); drawL(l); mmToolsSync(); },true);
  el.addEventListener('pointermove',function(e){ if(!(window.__mmT&&window.__mmT.draw)) mv(e); }); el.addEventListener('pointerdown',function(e){ if(!(window.__mmT&&window.__mmT.draw)) mv(e); });
  el.addEventListener('pointerleave',function(){ el.querySelector('.cx').setAttribute('opacity','0'); el.querySelector('.cd').setAttribute('opacity','0'); if(chgEl&&chgEl.dataset.sc){ chgEl.innerHTML=chgEl.dataset.o||''; delete chgEl.dataset.sc; } });
  return {up:up, last:last, RG:RG};
}
var __mmO={};
function mmOhlc(tk,cb){ if(__mmO[tk]&&__mmO[tk].d) return cb(__mmO[tk].d); if(__mmO[tk]){ __mmO[tk].q.push(cb); return; } __mmO[tk]={q:[cb]};
  var v=''; try{ v=(window.__SYNC__||'')+'-'+String(Math.floor(Date.now()/3600000)); }catch(e){}
  fetch('live/ohlc/'+tk.replace(/[^A-Za-z0-9]/g,'-')+'.json?v='+v).then(function(x){return x.ok?x.json():null}).catch(function(){return null}).then(function(d){ var o=__mmO[tk]; o.d=d||{d:[],w:[]}; var q=o.q; o.q=[]; q.forEach(function(f){ try{f(o.d)}catch(e){} }); }); }
function mmTs(d){ return Date.parse(d+'T21:00:00Z')/1000; }
// 매물대: 최근 1년 일별 종가의 고점·저점 꺾인 자리를 ±4%로 묶음(자세한 차트와 같은 계산)
function mmZones(tk,now){ var H=(DATA.H[tk]||[]).filter(function(a){return !a[2]}); if(H.length<30) return null; var lastD=H[H.length-1][0], y1=new Date(Date.parse(lastD+'T00:00:00Z')-370*864e5).toISOString().slice(0,10);
  var ser=H.filter(function(a){return a[0]>=y1}).map(function(a){return {d:a[0],v:a[1]}}); if(ser.length<20) return null;
  var ch=ser.slice(1).map(function(a,i){return Math.abs(a.v/ser[i].v-1)}).sort(function(x,y){return x-y}), med=ch[Math.floor(ch.length/2)]||0.02, th=Math.min(0.14,Math.max(0.06,med*5));
  var piv=[], dir=0, ex=ser[0], hiP=ser[0], loP=ser[0];
  ser.slice(1).forEach(function(a){ if(dir===0){ if(a.v>hiP.v)hiP=a; if(a.v<loP.v)loP=a; if(a.v<hiP.v*(1-th)){piv.push({v:hiP.v,d:hiP.d,k:'H'});ex=a;dir=-1;} else if(a.v>loP.v*(1+th)){piv.push({v:loP.v,d:loP.d,k:'L'});ex=a;dir=1;} return; }
    if(dir>0){ if(a.v>ex.v)ex=a; else if(a.v<ex.v*(1-th)){piv.push({v:ex.v,d:ex.d,k:'H'});ex=a;dir=-1;} return; }
    if(a.v<ex.v)ex=a; else if(a.v>ex.v*(1+th)){piv.push({v:ex.v,d:ex.d,k:'L'});ex=a;dir=1;} });
  var cl=[]; piv.slice().sort(function(x,y){return x.v-y.v}).forEach(function(p){ var c=cl[cl.length-1]; if(c&&p.v<=c.a*1.04){c.p.push(p);c.b=p.v;} else cl.push({a:p.v,b:p.v,p:[p]}); });
  cl.forEach(function(c){ if(c.b/c.a<1.015){ var md=(c.a+c.b)/2; c.a=md*0.9925; c.b=md*1.0075; } c.n=c.p.length; var nh=c.p.filter(function(p){return p.k==='H'}).length, nl=c.n-nh;
    c.why=(nh&&nl?'고점·저점':nh?'고점':'저점')+' '+c.n+'번 꺾인 자리('+c.p.slice().sort(function(x,y){return x.d<y.d?-1:1}).map(function(p){return (p.d.slice(0,4)!==lastD.slice(0,4)?'작년 ':'')+(+p.d.slice(5,7))+'/'+(+p.d.slice(8))}).join('·')+')'; });
  var gHi=Math.max.apply(0,ser.map(function(x){return x.v})), gLo=Math.min.apply(0,ser.map(function(x){return x.v})), rc=new Date(Date.parse(lastD+'T00:00:00Z')-120*864e5).toISOString().slice(0,10), r45=new Date(Date.parse(lastD+'T00:00:00Z')-45*864e5).toISOString().slice(0,10);
  var sc=function(c){ return c.n+(c.p.some(function(p){return p.d>=rc})?1:0)+(c.p.some(function(p){return p.d>=r45})?1:0)+(c.p.some(function(p){return p.v===gHi||p.v===gLo})?1:0); };
  var U=cl.filter(function(c){return c.a>now*1.003&&c.a<now*1.6}).sort(function(x,y){return x.a-y.a}), D=cl.filter(function(c){return c.b<now*0.997&&c.b>now*0.5}).sort(function(x,y){return y.b-x.b});
  var p2=function(L,z){ return L.filter(function(c){return c!==z}).sort(function(x,y){return sc(y)-sc(x)||L.indexOf(x)-L.indexOf(y)})[0]; };
  return {up:U[0], dn:D[0], up2:U[0]&&p2(U,U[0]), dn2:D[0]&&p2(D,D[0])}; }
// 1년 추세선(로그 직선) — 지금 가격이 그 선보다 몇 % 위·아래인지
function mmLT(tk){ var H=(DATA.H[tk]||[]).filter(function(a){return !a[2]}); if(H.length<60) return null; var lastD=H[H.length-1][0], y1=new Date(Date.parse(lastD+'T00:00:00Z')-370*864e5).toISOString().slice(0,10);
  var P=H.filter(function(a){return a[0]>=y1}).map(function(a){return [mmTs(a[0]),Math.log(a[1])]}); var n=P.length, mx=0, my=0; P.forEach(function(p){mx+=p[0];my+=p[1]}); mx/=n; my/=n; var a=0,b=0; P.forEach(function(p){a+=(p[0]-mx)*(p[1]-my); b+=(p[0]-mx)*(p[0]-mx)}); var k=b?a/b:0;
  return function(t){ return Math.exp(my+k*(t-mx)); }; }
function mmFacts(main,r,now,Z,LT,RG,cur){ main.querySelectorAll('.mm2').forEach(function(e){e.remove()}); if(!r)return;
  var f=function(v){ var a=Math.abs(v); return mmtTick(v,cur,cur==='%'?0.01:a>=1000?10:a>=100?1:a>=10?0.1:0.01); }, zf=function(c){return c?f(c.a)+'~'+f(c.b):''}, ltp=LT?((now/LT(Date.now()/1000)-1)*100):null;
  var rgU=RG?RG.up(RG.tb):null, rgD=RG?RG.dn(RG.tb):null, dd=RG?(function(){var d=new Date(RG.ta*1000+9*36e5);return (d.getUTCMonth()+1)+'/'+d.getUTCDate()})():'';
  var lv=document.createElement('div'); lv.className='mm-lv mm2';
  [[Z&&Z.up,'up','▲ 저항',zf(Z&&Z.up)],[Z&&Z.dn,'dn','▼ 지지',zf(Z&&Z.dn)],[RG,'',RG?(RG.dir<0?'단기 하락':'단기 상승'):'',RG?f(rgU)+'/'+f(rgD):''],[ltp!=null,'','1년 추세',ltp!=null?((ltp>=0?'+':'−')+Math.abs(ltp).toFixed(1)+'%'):'']].forEach(function(c){ if(!c[0])return; var d=document.createElement('div'); if(c[1])d.className=c[1]; d.innerHTML='<small></small><b></b>'; d.children[0].textContent=c[2]; d.children[1].textContent=c[3]; lv.appendChild(d); });
  var rows=[]; var where=RG?(now>rgU?' 채널 위로 벗어남':now<rgD?' 채널 아래로 이탈':' 채널 안'):''; rows.push(['지금 자리',(RG?'단기 '+(RG.dir<0?'하락':'상승')+where+'('+dd+' '+(RG.dir<0?'고점':'저점')+' 이후 흐름)':'')+(ltp!=null?(RG?' · ':'')+'1년 추세보다 '+(ltp>=0?'+':'−')+Math.abs(ltp).toFixed(1)+'%':'')]);
  if(Z&&Z.up) rows.push(['넘어야 할 곳',zf(Z.up)+(Z.up2?' → 그다음 '+zf(Z.up2):'')+' · '+Z.up.why]);
  if(Z&&Z.dn) rows.push(['버텨야 할 곳',zf(Z.dn)+(Z.dn2?' → 그다음 '+zf(Z.dn2):'')+' · '+Z.dn.why]);
  if(RG) rows.push([RG.dir<0?'전환 신호':'경계 신호', RG.dir<0?(now>rgU?('하락 추세선('+f(rgU)+')을 넘어선 상태 → 이 위에서 종가로 버티고 다음 눌림에서 저점을 높이면 상승 전환 · 다시 '+f(rgU)+' 아래로 밀리면 실패'):('종가로 '+f(rgU)+' 위(채널 위 선)면 하락 추세 탈출 · '+f(rgD)+' 아래면 더 약해짐')):('종가로 '+f(rgD)+' 아래(채널 아래 선)면 상승 추세 이탈 · '+f(rgU)+' 근처는 과열')]);
  var sm=document.createElement('div'); sm.className='mm-sum mm2'; sm.innerHTML='<b class="ttl">추세 한눈에</b>'+rows.map(function(x,i){return '<p><em>'+'①②③④'[i]+' '+x[0]+'</em><span></span></p>'}).join('')+'<p class="lg">캔들 <i style="background:#e0423a"></i>오름 <i style="background:#3a6fe0"></i>내림 · <i style="background:#c4453a"></i><i style="background:#2f8a4c"></i> 추세 채널 · <i style="background:#8a877f"></i> 1년 추세 · 띠 = 매물대(진하면 1차)</p>';
  rows.forEach(function(x,i){ sm.querySelectorAll('p span')[i].textContent=x[1]; });
  var anchor=main.querySelector('.mmt'); anchor.after(lv); lv.after(sm); }
var __mmL=null, __mmLq=null;
function mmLong(cb){ if(__mmL) return cb(__mmL); if(__mmLq){ __mmLq.push(cb); return; } __mmLq=[cb];
  var v=''; try{ v=(window.__SYNC__||'')+String(Math.floor(Date.now()/3600000)); }catch(e){}
  fetch('live/long.json?v=2-'+v).then(function(x){return x.ok?x.json():null}).catch(function(){return null}).then(function(d){ __mmL=d||{d:{}}; var q=__mmLq; __mmLq=null; q.forEach(function(f){ try{f(__mmL)}catch(e){} }); }); }
function mmtDraw(){
  var main=document.getElementById('main'); if(!main)return; var T=window.__mmT, r=mmtRow(); if(!r)return;
  var wrap=main.querySelector('.mmt'); if(!wrap){ wrap=document.createElement('div'); wrap.className='mmt'; wrap.innerHTML='<div class="mmt-ttl"></div><div class="mmt-top"><p class="mmt-chg"></p></div><div class="mmt-tools"><button type="button" class="mmt-tg mmt-trd">추세</button><button type="button" class="mmt-tg mmt-zn">매물대</button><button type="button" class="mmt-tg mmt-drw">✎ 선</button><label class="mmt-det mmt-tg"><input type="checkbox">자세히</label><button type="button" class="mmt-tg mmt-fs" aria-label="전체 화면"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button><button type="button" class="mmt-tg mmt-q" aria-label="종목 찾기">🔍</button><a class="mmt-tg mmt-ext" href="#">사파리로 크게 ↗</a><button type="button" class="mmt-tg mmt-x" aria-label="닫기">✕</button></div><div class="mmt-pen"><button type="button" data-k="tr" class="on">／추세</button><button type="button" data-k="h">―수평</button><button type="button" data-k="par">▱평행</button><i></i><button type="button" class="pc on" data-c="#9a6200" style="--c:#9a6200"></button><button type="button" class="pc" data-c="#c4453a" style="--c:#c4453a"></button><button type="button" class="pc" data-c="#2f6fd6" style="--c:#2f6fd6"></button><button type="button" class="pc" data-c="#141210" style="--c:#141210"></button><button type="button" class="mmt-clr">지우기</button><p class="mmt-hint"></p></div><div class="mmt-find"><input type="search" placeholder="종목 이름·티커" autocomplete="off"><div class="mmt-res"></div></div><div class="mmt-stage"><div class="mmt-box"></div></div><div class="mmt-per"></div>';
    var hd=main.querySelector('.hd'); hd.after(wrap);
    var pr=wrap.querySelector('.mmt-per'); MMT_PER.forEach(function(p){ var b=document.createElement('button'); b.type='button'; b.textContent=p[1]; b.dataset.p=p[0]; b.addEventListener('click',function(){ T.per=p[0]; mmtDraw(); }); pr.appendChild(b); });
    wrap.querySelector('.mmt-trd').addEventListener('click',function(){ T.tr=!T.tr; mmtDraw(); });
    wrap.querySelector('.mmt-zn').addEventListener('click',function(){ T.zn=!T.zn; mmtDraw(); });
    wrap.querySelector('.mmt-drw').addEventListener('click',function(){ T.draw=!T.draw; mmToolsSync(); var b=main.querySelector('.mmt-box'); if(b) b.classList.toggle('drawing',T.draw); });
    wrap.querySelector('.mmt-clr').addEventListener('click',function(){ var Ls=mmLines(mmTk()); Ls.pop(); mmLines(mmTk(),Ls); window.__mmPend=null; mmtDraw(); mmToolsSync(); });
    wrap.querySelectorAll('.mmt-pen [data-k]').forEach(function(b){ b.addEventListener('click',function(){ T.pk=b.dataset.k; window.__mmPend=null; mmToolsSync(); }); });
    wrap.querySelectorAll('.mmt-pen .pc').forEach(function(b){ b.addEventListener('click',function(){ T.pc=b.dataset.c; mmToolsSync(); }); });
    wrap.querySelector('.mmt-fs').addEventListener('click',function(){ mmFull(true); });
    wrap.querySelector('.mmt-x').addEventListener('click',function(){ mmFull(false); });
    // 큰 화면에서 종목 찾기(사용자 2026-10-29)
    var fd=wrap.querySelector('.mmt-find'), fi=fd.querySelector('input'), fr=fd.querySelector('.mmt-res');
    function list(){ var q=fi.value.trim().toLowerCase(); var L=DATA.P.filter(function(r){ return !q||(r.name+' '+r.ticker).toLowerCase().indexOf(q)>=0; }).slice(0,q?12:10);
      fr.innerHTML=''; L.forEach(function(r){ var b=document.createElement('button'); b.type='button'; b.innerHTML='<b></b> <small></small>'; b.firstChild.textContent=r.name.replace(/\(.*\)$/,''); b.lastChild.textContent=r.ticker.replace('^','');
        b.addEventListener('click',function(){ fd.classList.remove('on'); fi.value=''; location.hash=r.ticker.replace(/[^A-Za-z0-9]/g,'-'); }); fr.appendChild(b); }); }
    wrap.querySelector('.mmt-q').addEventListener('click',function(){ var on=!fd.classList.contains('on'); fd.classList.toggle('on',on); if(on){ list(); setTimeout(function(){ fi.focus(); },30); } });
    fi.addEventListener('input',list); fi.addEventListener('keydown',function(e){ if(e.key==='Enter'){ var b=fr.querySelector('button'); if(b) b.click(); } if(e.key==='Escape') fd.classList.remove('on'); });
    var ex=wrap.querySelector('.mmt-ext'); if(ex){ ex.href='kakaotalk://web/openExternal?url='+encodeURIComponent(location.href); if(MM_KAKAO) wrap.classList.add('kakao'); }
    var cb=wrap.querySelector('input'); cb.addEventListener('change',function(){ T.det=cb.checked; var dl=main.querySelector('.mmt-det'); if(dl) dl.classList.toggle('on',T.det); main.classList.toggle('mmt-detail',T.det); mmtDraw(); }); }
  mmTools(); var TL=main.querySelector('.mmt-tools'); mmToolsSync();
  TL.querySelector('input').checked=T.det; main.classList.toggle('mmt-detail',T.det); main.classList.add('mmt-on');
  wrap.dataset.tk=r.ticker;
  if(document.documentElement.classList.contains('mm-land')||document.documentElement.classList.contains('mm-full')){ if(!wrap.style.height) setTimeout(mmFit,0); }
  var ttl=wrap.querySelector('.mmt-ttl'); if(ttl){ ttl.textContent=r.name+'  '+mmtFmt(Number(r.price),r.currency); }
  wrap.querySelectorAll('.mmt-per button').forEach(function(b){ b.setAttribute('aria-pressed',String(b.dataset.p===T.per)); });
  var box=wrap.querySelector('.mmt-box'), chg=wrap.querySelector('.mmt-chg'), cur=r.currency, now=Number(r.price);
  var pe=main.querySelector('.hd .pr'); var lv=pe&&pe.textContent.match(/[\d,]+\.?\d*/); if(pe&&pe.classList.contains('mm-fh')&&lv) now=Number(lv[0].replace(/,/g,''));
  function setChg(base,label){ delete chg.dataset.sc; if(base==null){chg.textContent='';return} var dv=now-base, dp=dv/base*100, c=dv>=0?'#e0423a':'#3a6fe0'; chg.innerHTML='<span></span> <b style="color:'+c+'"></b>'; chg.firstChild.textContent=label; chg.lastChild.textContent=(cur==='%')?((dv>=0?'+':'−')+Math.round(Math.abs(dv)*100)+'bp'):((dv>=0?'+':'−')+mmtFmt(Math.abs(dv),cur)+' ('+Math.abs(dp).toFixed(1)+'%)'); }
  var DET=!!T.det, ZN=mmZones(r.ticker,now), LT=mmLT(r.ticker), OV={tr:DET||!!T.tr, zn:DET||!!T.zn, lt:DET};
  var opt0={ov:OV, zones:ZN, lt:LT};
  var RG3=(function(){ var d=mmtDaily(r.ticker), from=Date.now()/1000-92*86400; var p=d.filter(function(a){return a[0]>=from}); p.push([Date.now()/1000,now]); return mmRG(p); })();
  var done=function(res,base){ if(DET) mmFacts(main,r,now,ZN,LT,RG3,cur); else mmFacts(main,null); };
  if(T.per==='1d'){
    mmIntra(function(D){ var x=D&&D.d&&D.d[r.ticker]; if(!x||!x.p||x.p.length<2){ box.innerHTML='<p class="mmt-empty">오늘 흐름 자료가 아직 없습니다 · 장 시작 후 5분마다 채워집니다</p>'; setChg(r.prev_close,'어제보다'); done(null); return; }
      var pts=x.p.map(function(a){return [x.s+a[0]*60,a[1]]}); if(Math.abs(pts[pts.length-1][1]-now)>1e-9 && pe&&pe.classList.contains('mm-fh')) pts.push([Date.now()/1000,now]);
      var cd=null; if(DET){ cd=[]; var bk=null; pts.forEach(function(p){ var k=Math.floor(p[0]/900)*900; if(!bk||bk[0]!==k){ bk=[k,p[1],p[1],p[1],p[1]]; cd.push(bk); } else { bk[2]=Math.max(bk[2],p[1]); bk[3]=Math.min(bk[3],p[1]); bk[4]=p[1]; } }); cd.forEach(function(c){ c[0]+=450; }); }
      var rs=x.reg&&x.reg[0]||x.s, re=x.reg&&x.reg[1]||x.s+57600; var res=mmtChart(box,pts,x.pc,cur,{rs:rs,re:re,x0:rs-330*60,x1:re+240*60},{ov:OV,zones:ZN,lt:null,cdl:cd}); setChg(x.pc,'어제보다'); done(res); });
    return; }
  // 1주~10년: 캔들 자료(일봉 1년·주봉 10년)를 받아서 — 기본은 그 종가로 선, 자세히는 캔들. 둘 다 고가·저가로 눈금을 잡아 모양이 같음
  var tkNow=r.ticker; mmOhlc(tkNow,function(O){ if(mmTk()!==tkNow||T.per==='1d')return;
    var YRS={'1w':7/365,'1m':31/365,'3m':92/365,'1y':366/365,'5y':5,'10y':10}[T.per], from=Date.now()/1000-YRS*365.25*86400;
    var src=(T.per==='5y'||T.per==='10y')?O.w:O.d; var cd=(src||[]).map(function(a){return [mmTs(a[0]),a[1],a[2],a[3],a[4]]});
    if(cd.length>=2){ var prevC=cd.filter(function(c){return c[0]<from}); cd=cd.filter(function(c){return c[0]>=from});
      var pd=r.price_date, lc=cd[cd.length-1]; if(lc&&pd){ var ld=new Date(lc[0]*1000).toISOString().slice(0,10); if(ld===pd||T.per==='5y'||T.per==='10y'){ lc[4]=now; lc[2]=Math.max(lc[2],now); lc[3]=Math.min(lc[3],now); } else if(pd>ld){ cd.push([mmTs(pd),lc[4],Math.max(lc[4],now),Math.min(lc[4],now),now]); } }
      if(cd.length>=2){ var pts=cd.map(function(c){return [c[0],c[4]]}), base=prevC.length?prevC[prevC.length-1][4]:cd[0][1];
        var res=mmtChart(box,pts,base,cur,null,{ov:OV,zones:ZN,lt:LT,cdl:DET?cd:null,rng:cd,noTr:(T.per==='5y'||T.per==='10y')});
        var lab=MMT_PER.filter(function(p){return p[0]===T.per})[0][2]; if((T.per==='5y'||T.per==='10y')&&!prevC.length&&cd[0][0]>Date.now()/1000-(YRS-0.5)*365*86400) lab='상장 이후';
        setChg(base,lab); done(res); return; } }
    mmtDrawOld(); });
  return;
}
function mmtDrawOld(){ var main=document.getElementById('main'), T=window.__mmT, r=mmtRow(); if(!r)return; var wrap=main.querySelector('.mmt'), box=wrap.querySelector('.mmt-box'), chg=wrap.querySelector('.mmt-chg'), cur=r.currency, now=Number(r.price);
  var pe=main.querySelector('.hd .pr'); var lv=pe&&pe.textContent.match(/[\d,]+\.?\d*/); if(pe&&pe.classList.contains('mm-fh')&&lv) now=Number(lv[0].replace(/,/g,''));
  function setChg(base,label){ delete chg.dataset.sc; if(base==null){chg.textContent='';return} var dv=now-base, dp=dv/base*100, c=dv>=0?'#e0423a':'#3a6fe0'; chg.innerHTML='<span></span> <b style="color:'+c+'"></b>'; chg.firstChild.textContent=label; chg.lastChild.textContent=(cur==='%')?((dv>=0?'+':'−')+Math.round(Math.abs(dv)*100)+'bp'):((dv>=0?'+':'−')+mmtFmt(Math.abs(dv),cur)+' ('+Math.abs(dp).toFixed(1)+'%)'); }
  if(T.per==='5y'||T.per==='10y'){ // 5년: 하루 한 번 받는 주간 종가(live/long.json) + 최근 일별
    var YR=T.per==='10y'?10:5; mmLong(function(Lg){ if((T.per!=='5y'&&T.per!=='10y')||mmTk()!==r.ticker)return; var wk=(Lg&&Lg.d&&Lg.d[r.ticker])||[], dly=mmtDaily(r.ticker), t0=dly.length?dly[0][0]:Infinity;
      var from=Date.now()/1000-YR*365.25*86400; var pts=wk.map(function(a){return [Date.parse(a[0]+'T21:00:00Z')/1000,a[1]]}).filter(function(a){return a[0]<t0&&a[0]>=from}).concat(dly); pts.push([Date.now()/1000,now]);
      if(pts.length<3){ box.innerHTML='<p class="mmt-empty">5년 자료를 불러오는 중입니다 · 잠시 뒤 다시 열어 주세요</p>'; chg.textContent=''; return; }
      mmtChart(box,pts,pts[0][1],cur,null); setChg(pts[0][1],(pts[0][0]<Date.now()/1000-(YR-0.5)*365*86400)?YR+'년 전보다':'상장 이후'); });
    return; }
  var all=mmtDaily(r.ticker); var tNow=Date.now()/1000; all.push([tNow,now]);
  var days={'1w':7,'1m':31,'3m':92,'1y':366}[T.per]; var from=tNow-days*86400; var pts=all.filter(function(a){return a[0]>=from});
  if(pts.length<2) pts=all.slice(-2);
  var prev=all.filter(function(a){return a[0]<from}); var base=prev.length?prev[prev.length-1][1]:pts[0][1];
  mmtChart(box,pts,base,cur,null); setChg(base,MMT_PER.filter(function(p){return p[0]===T.per})[0][2]);
}

function mmtStyleDetail(){ // 자세한 차트: 추세선은 가늘고 옅게, 주가 선은 맨 위에 흰 테두리로 또렷하게
  var svg=document.querySelector('#main .ch > svg'); if(!svg||svg.dataset.st)return; svg.dataset.st=1;
  var A=function(e,n){return e.getAttribute(n)||''};
  svg.querySelectorAll('line').forEach(function(l){ var st=A(l,'stroke'), d=A(l,'stroke-dasharray');
    if(st==='var(--color-fg)'&&(d==='6 0'||A(l,'stroke-width')==='1.8')){ l.setAttribute('stroke-width','1'); l.setAttribute('opacity','.3'); }
    else if(st==='var(--color-fg)'){ l.setAttribute('opacity','.18'); }
    else if(st==='var(--color-bad)'||st==='var(--color-ok)'){ l.setAttribute('stroke-width','1.1'); l.setAttribute('opacity', d?'.3':'.5'); } });
  svg.querySelectorAll('rect').forEach(function(r){ if(A(r,'opacity')==='0.08') r.setAttribute('opacity','.05'); });
  svg.querySelectorAll('text').forEach(function(t){ if(/^고점/.test(t.textContent)) t.setAttribute('opacity','.75'); });
  // 차트 위 설명은 왼쪽 위에 작게(사용자 2026-10-29): '그래프 기간 …' → '기간 +10.0%', 평균 목표가도 그 아래 왼쪽으로
  svg.querySelectorAll('text').forEach(function(t){ var m=t.textContent.match(/^그래프 기간\s*([−+\-]?[\d.,]+%)/); if(m){ t.textContent='기간 '+m[1]; t.setAttribute('font-size','11.5'); t.setAttribute('font-weight','700'); t.setAttribute('opacity','.85'); }
    if(/^↑?\s*평균 목표가/.test(t.textContent)&&+t.getAttribute('y')<40){ t.setAttribute('x','8'); t.setAttribute('text-anchor','start'); t.setAttribute('y','29'); t.setAttribute('font-size','10.5'); } });
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
  var svg=document.querySelector('#main .ch > svg'); if(!svg||svg.dataset.tg)return; var gl=document.querySelector('#main p.gl'); if(!gl)return;
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
// 가로·전체 화면을 '실제로 보이는 영역'(visualViewport)에 딱 맞춤 — 카톡처럼 위·아래 바가 화면을 덮는 앱 안 브라우저 대응(사용자 2026-10-29)
function mmFit(){ var h=document.documentElement, w=document.querySelector('#main .mmt'); if(!w)return; var on=h.classList.contains('mm-land')||h.classList.contains('mm-full');
  if(!on){ ['top','left','width','height'].forEach(function(k){ w.style[k]=''; }); return; }
  var v=window.visualViewport; var T=v?v.offsetTop:0, Lf=v?v.offsetLeft:0, Wd=v?v.width:innerWidth, Ht=v?v.height:innerHeight;
  var key=[T,Lf,Wd,Ht].map(Math.round).join(','); if(w.dataset.fit===key)return; w.dataset.fit=key;
  w.style.top=T+'px'; w.style.left=Lf+'px'; w.style.width=Wd+'px'; w.style.height=Ht+'px'; w.style.right='auto'; w.style.bottom='auto';
  clearTimeout(window.__mmFt); window.__mmFt=setTimeout(function(){ try{mmtDraw()}catch(e){} },40); }
try{ if(window.visualViewport){ visualViewport.addEventListener('resize',function(){ setTimeout(mmFit,30); }); visualViewport.addEventListener('scroll',function(){ setTimeout(mmFit,30); }); } }catch(e){}
var MM_KAKAO=/KAKAOTALK/i.test(navigator.userAgent||'');
function mmLand(){ var on=false; try{ on=matchMedia('(orientation: landscape)').matches&&innerHeight<560&&!!document.querySelector('#main .mmt'); }catch(e){}
  var h=document.documentElement; if(h.classList.contains('mm-land')===on) return; h.classList.toggle('mm-land',on); if(on){ window.__mmSy=scrollY; } else if(window.__mmSy!=null){ var y=window.__mmSy; window.__mmSy=null; setTimeout(function(){ scrollTo(0,y); },300); } setTimeout(function(){ mmFit(); try{mmtDraw()}catch(e){} },60); }
addEventListener('resize',function(){ clearTimeout(window.__mmLt); window.__mmLt=setTimeout(mmLand,120); }); addEventListener('orientationchange',function(){ setTimeout(mmLand,250); });
// 차트 위에서는 손가락·마우스 휠이 페이지를 움직이지 않게(사용자 2026-10-29) — 차트 훑기만
(function(){ function inChart(e){ var t=e.target; return t&&t.closest&&t.closest('#main .mmt-box > svg, #main .ch > svg'); }
  var st=null;
  document.addEventListener('touchstart',function(e){ st=inChart(e)&&e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY,ly:e.touches[0].clientY,t:Date.now(),sc:false}:null; },{passive:true,capture:true});
  document.addEventListener('touchmove',function(e){ if(!inChart(e))return; e.preventDefault(); if(!st||window.__mmT&&window.__mmT.draw||document.documentElement.classList.contains('mm-land')||document.documentElement.classList.contains('mm-full'))return;
    var t=e.touches[0], dx=Math.abs(t.clientX-st.x), dy=Math.abs(t.clientY-st.y);
    if(!st.sc && dy>56 && dy>dx*2.2) st.sc=true; // 위아래로 크게 당겼을 때만 페이지 이동
    if(st.sc) window.scrollBy(0, st.ly-t.clientY); st.ly=t.clientY; },{passive:false,capture:true});
  document.addEventListener('wheel',function(e){ if(inChart(e)) e.preventDefault(); },{passive:false,capture:true}); })();
// 전체 화면(버튼): 기본 차트를 화면 가득. 안드로이드는 가로 고정까지 시도
function mmFull(on){ var h=document.documentElement; h.classList.toggle('mm-full',on); try{mmTools()}catch(e){} setTimeout(mmFit,50);
  try{ if(on){ var q=h.requestFullscreen&&h.requestFullscreen(); if(q&&q.then) q.then(function(){ try{ screen.orientation.lock('landscape').catch(function(){}); }catch(e){} }).catch(function(){}); }
       else if(document.fullscreenElement&&document.exitFullscreen){ document.exitFullscreen().catch(function(){}); } }catch(e){}
  setTimeout(function(){ try{mmtDraw()}catch(e){} },80); }
document.addEventListener('fullscreenchange',function(){ if(!document.fullscreenElement&&document.documentElement.classList.contains('mm-full')) mmFull(false); });
addEventListener('keydown',function(e){ if(e.key==='Escape'&&document.documentElement.classList.contains('mm-full')) mmFull(false); });
// 모서리 도구: 기본 차트에서는 차트 위에, 자세한 차트에서는 그 차트 위에(같은 자리)
function mmDtipSlot(){ var ch=document.querySelector('#main .ch'); if(ch&&!ch.querySelector('.mm-dtip')) mmDtip('','', '', ''); }
function mmTools(){ var main=document.getElementById('main'), w=main&&main.querySelector('.mmt'), t=w&&w.querySelector('.mmt-tools'); if(!t){ t=main&&main.querySelector('.ch > .mmt-tools'); } if(!t)return;
  if(document.documentElement.classList.contains('mm-full')&&w){ var tp=w.querySelector('.mmt-top'); if(tp&&t.previousElementSibling!==tp) tp.after(t); return; }
  var tg=w&&w.querySelector('.mmt-stage'); if(tg&&t.parentNode!==tg) tg.insertBefore(t,tg.firstChild); }
function mmDtip(d,p,rel,rc){ var main=document.getElementById('main'), ch=main&&main.querySelector('.ch'); if(!ch)return; var el=main.querySelector('.mm-dtip');
  if(!el){ el=document.createElement('p'); el.className='mm-dtip'; } var sv=ch.querySelector(':scope > svg'); if(sv&&el.nextSibling!==sv) ch.insertBefore(el,sv);
  el.innerHTML='<span></span> <b></b> <em></em>'; el.children[0].textContent=d; el.children[1].textContent=p; el.children[2].textContent=rel||''; el.children[2].style.color=rc&&rc.indexOf('ok')>=0?'#1f7a3f':''; }
function mmLines(tk,v){ var k='mm-lines'; try{ var all=JSON.parse(localStorage.getItem(k)||'{}'); if(v===undefined) return all[tk]||[]; if(v&&v.length) all[tk]=v; else delete all[tk]; localStorage.setItem(k,JSON.stringify(all)); }catch(e){ if(v===undefined) return (window.__mmLn=window.__mmLn||{})[tk]||[]; (window.__mmLn=window.__mmLn||{})[tk]=v; } return v; }
function mmToolsSync(){ var t=document.querySelector('#main .mmt-tools'); if(!t)return; var T=window.__mmT||{}; var pen=document.querySelector('#main .mmt-pen'); if(pen){ pen.style.display=T.draw&&!document.querySelector('#main.mmt-detail')?'':'none'; var pk=T.pk||'tr', pc=T.pc||'#9a6200';
    pen.querySelectorAll('[data-k]').forEach(function(b){ b.classList.toggle('on',b.dataset.k===pk); }); pen.querySelectorAll('.pc').forEach(function(b){ b.classList.toggle('on',b.dataset.c===pc); });
    var n=mmLines(mmTk()).length, cl=pen.querySelector('.mmt-clr'); cl.style.display=n?'':'none'; cl.textContent='되돌리기';
    pen.querySelector('.mmt-hint').textContent=window.__mmPend?'평행선 놓을 곳을 한 번 누르세요':pk==='h'?'원하는 가격 높이를 누르거나 끌어 놓으세요':pk==='par'?'먼저 추세선을 긋고, 평행선 자리를 누르세요':'두 점을 잇듯 끌어서 그으세요'; } var d=t.querySelector('.mmt-drw'), c=t.querySelector('.mmt-clr'); if(d) d.classList.toggle('on',!!T.draw);
  var tr=t.querySelector('.mmt-trd'); if(tr) tr.classList.toggle('on',!!T.tr); var zn=t.querySelector('.mmt-zn'); if(zn) zn.classList.toggle('on',!!T.zn); var de=t.querySelector('.mmt-det'); if(de) de.classList.toggle('on',!!T.det); var ch=document.querySelector('#main .mmt-chg'); }
var MM_DR={'1d':'1m','1w':'1m','1m':'1m','3m':'3m','1y':'12m','5y':'5y','10y':'10y'};
function mmMergeLong(Lg){ if(!Lg||!Lg.d||window.__mmMerged)return; window.__mmMerged=1; try{ Object.keys(Lg.d).forEach(function(t){ var H=DATA.H[t]||(DATA.H[t]=[]); var first=H.length?H[0][0]:'9999'; var add=Lg.d[t].filter(function(a){return a[0]<first}).map(function(a){return [a[0],a[1],0]}); if(add.length) DATA.H[t]=add.concat(H); }); }catch(e){} }
function mmSetRange(){ var T=window.__mmT||{}; if(!T.det)return; var k=MM_DR[T.per]||'3m';
  var go=function(){ var b=document.querySelector('#main .rg [data-k="'+k+'"]'); if(b&&b.getAttribute('aria-pressed')!=='true') b.click(); };
  if(k==='5y'||k==='10y'){ mmLong(function(Lg){ var was=window.__mmMerged; mmMergeLong(Lg); go(); if(!was){ var b=document.querySelector('#main .rg [data-k="'+k+'"]'); if(b) b.click(); } }); } else go(); }
// 기간 줄은 두 모드 모두 차트 아래 같은 자리
function mmPerPlace(){ var main=document.getElementById('main'), per=main&&main.querySelector('.mmt-per'); if(!per)return; var det=main.classList.contains('mmt-detail');
  var after=main.querySelector('.mmt-stage'); if(after&&per.previousElementSibling!==after) after.after(per); }
// 추세 가이드 요약(사용자 2026-10-29): 긴 설명 대신 4줄 — 지금 자리 / 넘어야 할 곳 / 버텨야 할 곳 / 전환 신호, 선 읽는 법은 한 줄
function mmGuide(main,gl){ if(!gl||main.querySelector('.mm-sum'))return; var t=gl.textContent.replace(/\s+/g,' ');
  var g=function(re){var m=t.match(re);return m}, R=g(/위 저항 후보\s*([\d,.~]+)[^(]*\(([^)]*)\)/), R2=g(/더 위 저항\s*([\d,.~]+)/), S=g(/아래 지지 후보\s*([\d,.~]+)[^(]*\(([^)]*)\)/), S2=g(/더 아래 지지\s*([\d,.~]+)/);
  var C=g(/단기 (하락|상승) 채널\(([\d.]+) (고점|저점) 이후[^)]*\)\s*·\s*상단\s*([\d,.]+)[^·]*·\s*하단\s*([\d,.]+)/), L=g(/장기 추세선보다\s*([−+\-]?[\d.]+%)/), pos=/아래 경계보다 낮음/.test(t)?'평소보다 많이 눌린 자리':/위 경계보다 높음/.test(t)?'평소보다 많이 오른 자리':'평소 범위 안';
  var dd=function(x){ var p=x.split('.'); return p.length===3?(+p[1])+'/'+(+p[2]):x; };
  var rows=[];
  rows.push(['지금 자리', (C?'단기 '+C[1]+' 채널 안('+dd(C[2])+' '+C[3]+' 이후)':'')+(L?(C?' · ':'')+'1년 추세보다 '+L[1]+' — '+pos:'')]);
  if(R) rows.push(['넘어야 할 곳', R[1]+(R2?' → 그다음 '+R2[1]:'')]);
  if(S) rows.push(['버텨야 할 곳', S[1]+(S2?' → 그다음 '+S2[1]:'')]);
  if(C) rows.push([C[1]==='하락'?'전환 신호':'경계 신호', C[1]==='하락'?('종가로 '+C[4]+' 위(채널 상단)면 하락 추세 탈출 · '+C[5]+' 아래(하단)면 더 약해짐'):('종가로 '+C[5]+' 아래(채널 하단)면 상승 추세 이탈 · '+C[4]+' 위(상단)는 과열 구간')]);
  var box=document.createElement('div'); box.className='mm-sum';
  box.innerHTML='<b class="ttl">추세 한눈에</b>'+rows.map(function(r,i){return '<p><em>'+'①②③④'[i]+' '+r[0]+'</em><span></span></p>'}).join('')+'<p class="lg">선: <i style="background:#c4453a"></i><i style="background:#2f8a4c"></i> 단기 채널 · <i style="background:#bdb9b0"></i> 1년 추세 · 띠 = 매물대(진하면 1차, 옅으면 그다음)</p>';
  rows.forEach(function(r,i){ box.querySelectorAll('p span')[i].textContent=r[1]; });
  var lv=main.querySelector('.mm-lv'); (lv||main.querySelector('.ch')).after(box); }
function mmAsof(){ var main=document.getElementById('main'), a=document.getElementById('asof'); if(!main||!a||!a.textContent.trim())return; var old=document.querySelector('.mm-asof2'); if(old) old.remove(); var kd=main.querySelector('.hd .kind'), pr=main.querySelector('.hd .pr'); var m=a.textContent.match(/(\d{1,2}:\d{2})\s*기준/); if(!kd||!m||(pr&&pr.classList.contains('mm-fh'))) return; var t=' · '+m[1]+' 기준'; if(kd.textContent.indexOf(t)<0) kd.textContent=kd.textContent.replace(/ · \d{1,2}:\d{2} 기준$/,'')+t; return; var e=document.querySelector('.mm-asof2'); var card=main.closest('section,.card,.panel')||main; if(!e){ e=document.createElement('p'); e.className='mm-asof2'; card.parentNode.insertBefore(e,card); } var t='● '+a.textContent.trim(); if(e.textContent!==t) e.textContent=t; }
(function(){ var h=document.documentElement, t=null, idle=null;
  function off(){ h.classList.add('mm-hx-off'); setTimeout(function(){ window.__mmFitN=0; try{mmFitCard()}catch(e){} if(h.classList.contains('mm-lock')) scrollTo(0,0); },480); } function on(){ if(h.classList.contains('mm-land')||h.classList.contains('mm-full')) return; h.classList.remove('mm-hx-off'); }
  function act(){ clearTimeout(idle); if(!h.classList.contains('mm-hx-off')){ clearTimeout(t); t=setTimeout(off,1500); } idle=setTimeout(on,20000); }
  t=setTimeout(off,5000); idle=setTimeout(on,25000);
  ['pointerdown','scroll','keydown','wheel','touchstart'].forEach(function(e){ addEventListener(e,act,{passive:true,capture:true}); }); })();
// 종목 찾기 목록을 시세 보드 '종목별 시세' 한 줄 카드로(사용자 2026-10-29): 이름+티커·층위 / 가격+52주 막대 / 1일 등락 크게·고점 대비 / ›, 목록은 상자 안 스크롤
function mmList(){ var L=document.getElementById('list'); if(!L)return; var byT={}; try{ DATA.P.forEach(function(r){ byT[r.ticker.replace('^','')]=r; }); }catch(e){ return; }
  L.querySelectorAll('button.row').forEach(function(b){ if(b.dataset.mm)return; var sm=b.querySelector('small'), tk=sm&&sm.textContent.trim(), r=byT[tk]; if(!r)return; b.dataset.mm=1;
    var d1=b.querySelector('.d1'), dd=b.querySelector('.dd'), p=Number(r.price), lo=Number(r.lo_52w), hi=Number(r.hi_52w), pos=(hi>lo)?Math.max(0,Math.min(100,(p-lo)/(hi-lo)*100)):50, cur=r.currency;
    var nm=r.name.replace(/\(([^)]*)\)$/,'').trim()||r.name, f=function(v){ return isNaN(v)?'':mmtTick(v,cur,cur==='%'?0.01:v>=1000?1:v>=100?0.01:0.01); };
    b.innerHTML='<span class="l"><b></b><i></i></span><span class="m"><em></em><span class="bar"><s style="left:'+pos.toFixed(0)+'%"></s></span><span class="rg"><u></u><u></u></span></span><span class="r"><strong></strong><small></small></span><span class="go">›</span>';
    b.querySelector('.l b').textContent=nm; b.querySelector('.l i').textContent=tk+' · '+r.category; b.querySelector('.m em').textContent=f(p)+(cur==='%'?'%':'');
    var u=b.querySelectorAll('.rg u'); u[0].textContent=f(lo); u[1].textContent=f(hi);
    var st=b.querySelector('.r strong'); st.textContent=d1?d1.textContent:''; st.className=d1?d1.className.replace('d1','').trim():''; b.querySelector('.r small').textContent=dd?dd.textContent:''; });
  var box=L; if(!box.dataset.box){ box.dataset.box=1; var h=document.createElement('p'); h.className='mm-lhint'; h.textContent='↕ 상자 안에서 내려 보면 전체 종목이 있습니다'; box.after(h); } }
// 종목 바꾸기(사용자 2026-10-29 2+3안): 목록 카드는 아래에서 올라오는 시트로, 차트 위엔 최근 본 종목 칩
function mmSheet(){ var side=document.querySelector('section.side'); if(!side||document.querySelector('.mm-sheet'))return;
  var sh=document.createElement('div'); sh.className='mm-sheet'; sh.innerHTML='<div class="mm-shbg"></div><div class="mm-shbox"><div class="mm-shhd"><i></i><b>종목 바꾸기</b><button type="button" class="mm-shx" aria-label="닫기">✕</button></div><div class="mm-shbody"></div></div>';
  document.body.appendChild(sh); sh.querySelector('.mm-shbody').appendChild(side);
  

  document.body.style.paddingBottom='';
  var open=function(o){ document.documentElement.classList.toggle('mm-shon',o); if(o){ var b=sh.querySelector('.mm-shbody'); b.scrollTop=0; } };
  (function(){ var box=sh.querySelector('.mm-shbox'), body=sh.querySelector('.mm-shbody'), y0=null, dy=0, fromBody=false;
    box.addEventListener('touchstart',function(e){ var t=e.touches[0]; fromBody=!!e.target.closest('.mm-shbody'); if(fromBody&&body.scrollTop>0){ y0=null; return; } y0=t.clientY; dy=0; box.style.transition='none'; },{passive:true});
    box.addEventListener('touchmove',function(e){ if(y0==null)return; dy=e.touches[0].clientY-y0; if(dy<=0){ if(fromBody){ y0=null; box.style.transform=''; box.style.transition=''; } return; } e.preventDefault(); box.style.transform='translateY('+dy+'px)'; },{passive:false});
    box.addEventListener('touchend',function(){ if(y0==null)return; y0=null; box.style.transition=''; box.style.transform=''; if(dy>90) open(false); dy=0; }); })();
  ['.wrap > p.foot','.wrap > p.mm-foot'].forEach(function(q){ var ft=document.querySelector(q); if(ft){ var c=ft.cloneNode(true); c.className='mm-foot2'; sh.querySelector('.mm-shbody').appendChild(c); } });
  window.__mmShOpen=open; sh.querySelector('.mm-shbg').addEventListener('click',function(){ open(false); }); sh.querySelector('.mm-shx').addEventListener('click',function(){ open(false); });
  side.addEventListener('click',function(e){ if(e.target.closest&&e.target.closest('#list button.row')){ setTimeout(function(){ open(false); scrollTo({top:0,behavior:'smooth'}); },120); } },true);
  addEventListener('hashchange',function(){ open(false); }); }
function mmShBar(){ var mn=document.getElementById('main'); if(!mn||!mn.querySelector('.mmt-per')||mn.querySelector('.mm-shbar'))return; var bar=document.createElement('button'); bar.type='button'; bar.className='mm-shbar'; bar.innerHTML='<span>🔍</span> 종목 바꾸기 <small></small>'; try{ bar.querySelector('small').textContent=DATA.P.length+'종목 · 층위별'; }catch(e){}
  bar.addEventListener('click',function(){ if(window.__mmShOpen) window.__mmShOpen(true); }); mn.appendChild(bar); }
function mmRecent(){ var main=document.getElementById('main'); if(!main||!main.querySelector('.hd'))return; var tk=mmTk(); if(!tk)return; var R=[]; try{ R=JSON.parse(localStorage.getItem('mm-recent')||'[]'); }catch(e){}
  if(R[0]!==tk){ R=[tk].concat(R.filter(function(x){return x!==tk})).slice(0,8); try{ localStorage.setItem('mm-recent',JSON.stringify(R)); }catch(e){} }
  if(R.length<3) ['QQQ','SOXL','NVDA','^TNX','SOXX'].forEach(function(x){ if(R.indexOf(x)<0&&R.length<6) R.push(x); });
  var box=main.querySelector('.mm-rec'); if(!box){ box=document.createElement('div'); box.className='mm-rec'; main.insertBefore(box,main.firstChild); }
  var key=R.join(',')+'|'+tk; if(box.dataset.k===key) return; box.dataset.k=key; box.innerHTML='<span class="lb">최근</span>';
  var byT={}; try{ DATA.P.forEach(function(r){ byT[r.ticker]=r; }); }catch(e){}
  R.forEach(function(t){ var r=byT[t]; if(!r)return; var b=document.createElement('button'); b.type='button'; b.textContent=t.replace('^','').replace(/=F$/,''); if(t===tk) b.className='on'; b.title=r.name;
    b.addEventListener('click',function(){ location.hash=t.replace(/[^A-Za-z0-9]/g,'-'); }); box.appendChild(b); }); }
// 첫 화면에 차트 카드만 딱(사용자 2026-10-29): 카드 아래가 아래 아이콘 독 바로 위에 오도록 차트 높이를 맞춤
try{ addEventListener('resize',function(){ clearTimeout(window.__mmFr); window.__mmFr=setTimeout(function(){ window.__mmFitN=0; try{mmFitCard()}catch(e){} },350); }); if(window.visualViewport) visualViewport.addEventListener('resize',function(){ clearTimeout(window.__mmFr); window.__mmFr=setTimeout(function(){ window.__mmFitN=0; try{mmFitCard()}catch(e){} },350); }); }catch(e){}
function mmFitCard(){ var h=document.documentElement; if(h.classList.contains('mm-land')||h.classList.contains('mm-full'))return; var m=document.getElementById('main'), sv=m&&m.querySelector('.mmt-box > svg'); if(!m||!sv)return;
  var dockTop=innerHeight; [].slice.call(document.querySelectorAll('nav,div')).forEach(function(e){ var cs=getComputedStyle(e); if(cs.position!=='fixed')return; var r=e.getBoundingClientRect(); if(r.width>300&&r.top>innerHeight*0.6&&r.height>30&&r.top<dockTop) dockTop=r.top; });
  var hero=document.querySelector('header.mm-hero'), heroH=(hero&&!h.classList.contains('mm-hx-off'))?hero.getBoundingClientRect().height+(parseFloat(getComputedStyle(hero).marginBottom)||0):0;
  var top=m.getBoundingClientRect().top+scrollY-heroH, non=m.offsetHeight-sv.getBoundingClientRect().height, want=Math.round(Math.max(240,Math.min(680,dockTop-4-top-non)));
  h.classList.toggle('mm-lock', want>240&&want<680); if(h.classList.contains('mm-hx-off')&&h.classList.contains('mm-lock')&&scrollY) scrollTo(0,0);
  var cur=Math.round(sv.getBoundingClientRect().height); if(Math.abs(want-cur)>6&&(window.__mmFitN=(window.__mmFitN||0)+1)<4){ window.__mmFitH=want; window.__mmH=want; try{mmtDraw()}catch(e){} } }
function mmtTidy(){ var main=document.getElementById('main'); if(!main||!main.querySelector('.hd'))return; var w=main.querySelector('.mmt'); if(!w||w.dataset.tk!==mmTk()) mmtDraw(); }

function tidy(){
  try{ var RN={'1개월':'1달','3개월':'3달','6개월':'6달','12개월':'1년'}; document.querySelectorAll('#main .rg .pb-chip').forEach(function(b){ var k=b.textContent.trim(); if(RN[k]) b.textContent=RN[k]; }); }catch(e){}
  var main=document.getElementById('main'); if(!main)return; try{mmtTidy()}catch(e){console.log(e)} try{mmtStyleDetail()}catch(e){} try{mmAsof()}catch(e){} try{mmList()}catch(e){} try{mmSheet()}catch(e){} try{mmShBar()}catch(e){} try{mmRecent()}catch(e){} try{mmFitCard()}catch(e){} try{mmTools()}catch(e){} try{mmDtipSlot()}catch(e){} try{mmPerPlace()}catch(e){} try{mmtAxisTags()}catch(e){console.log(e)}
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
  try{ mmGuide(main,gl); }catch(e){console.log(e)}
  if(gl&&!gl.closest('details')){ var nt=main.querySelector('p.nt'); var d=document.createElement('details'); d.className='mm-fold'; d.innerHTML='<summary><span>추세 한눈에</span></summary>'; gl.before(d); d.appendChild(gl); if(nt)d.appendChild(nt); }
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


PIV_JS = r'''        // 최근 1년 일별 종가에서 꼭짓점(되돌림 기준은 종목 변동성에 맞춰 6~14%) → 가까운 꼭짓점끼리 ±4% 묶음
        const lastD = full[full.length - 1].d, y1d = new Date(lastD + 'T00:00:00Z'); y1d.setUTCDate(y1d.getUTCDate() - 370); const yc = y1d.toISOString().slice(0, 10);
        const ser = full.filter((a) => a.kind !== 'm' && a.d >= yc);
        const chg = ser.slice(1).map((a, i) => Math.abs(a.v / ser[i].v - 1)).sort((x, y) => x - y), med = chg.length ? chg[Math.floor(chg.length / 2)] : 0.02;
        const th = Math.min(0.14, Math.max(0.06, med * 5));
        const piv = []; let dir = 0, ex = ser[0], hiP = ser[0], loP = ser[0];
        ser.slice(1).forEach((a) => {
          if (dir === 0) { if (a.v > hiP.v) hiP = a; if (a.v < loP.v) loP = a;
            if (a.v < hiP.v * (1 - th)) { piv.push({ v: hiP.v, d: hiP.d, k: 'H' }); ex = a; dir = -1; } else if (a.v > loP.v * (1 + th)) { piv.push({ v: loP.v, d: loP.d, k: 'L' }); ex = a; dir = 1; } return; }
          if (dir > 0) { if (a.v > ex.v) ex = a; else if (a.v < ex.v * (1 - th)) { piv.push({ v: ex.v, d: ex.d, k: 'H' }); ex = a; dir = -1; } return; }
          if (a.v < ex.v) ex = a; else if (a.v > ex.v * (1 + th)) { piv.push({ v: ex.v, d: ex.d, k: 'L' }); ex = a; dir = 1; }
        });
        const ps = piv.slice().sort((x, y) => x.v - y.v), cl = [];
        ps.forEach((p) => { const c = cl[cl.length - 1]; if (c && p.v <= c.a * 1.04) { c.p.push(p); c.b = p.v; } else cl.push({ a: p.v, b: p.v, p: [p] }); });
        cl.forEach((c) => { if (c.b / c.a < 1.015) { const md = (c.a + c.b) / 2; c.a = md * 0.9925; c.b = md * 1.0075; } c.n = c.p.length;
          const nh = c.p.filter((p) => p.k === 'H').length, nl = c.n - nh, ds = c.p.slice().sort((x, y) => x.d.localeCompare(y.d)).map((p) => (p.d.slice(0, 4) !== lastD.slice(0, 4) ? '작년 ' : '') + Number(p.d.slice(5, 7)) + '/' + Number(p.d.slice(8))).join('·');
          c.why = (nh && nl ? '고점·저점' : nh ? '고점' : '저점') + ' ' + c.n + '번 꺾인 자리(' + ds + ')'; });
        const upC = cl.filter((c) => c.a > nowV * 1.003 && c.a < nowV * 1.6).sort((x, y) => x.a - y.a), dnC = cl.filter((c) => c.b < nowV * 0.997 && c.b > nowV * 0.5).sort((x, y) => y.b - x.b);
        const above = upC[0], below = dnC[0];
        // 2차: 꺾인 횟수 + 최근 4달 안이면 +1 + 1년 최고·최저면 +1 → 점수 높은 곳(같으면 가까운 곳)
        const gHi = Math.max(...ser.map((x) => x.v)), gLo = Math.min(...ser.map((x) => x.v)), rc = new Date(lastD + 'T00:00:00Z'); rc.setUTCDate(rc.getUTCDate() - 120); const rcs = rc.toISOString().slice(0, 10);
        const r45 = new Date(lastD + 'T00:00:00Z'); r45.setUTCDate(r45.getUTCDate() - 45); const r45s = r45.toISOString().slice(0, 10);
        const sc = (c) => c.n + (c.p.some((p) => p.d >= rcs) ? 1 : 0) + (c.p.some((p) => p.d >= r45s) ? 1 : 0) + (c.p.some((p) => p.v === gHi || p.v === gLo) ? 1 : 0);
        const pick2 = (L, z) => L.filter((c) => c !== z).sort((x, y) => sc(y) - sc(x) || (L.indexOf(x) - L.indexOf(y)))[0];
        const above2 = above && pick2(upC, above), below2 = below && pick2(dnC, below);'''


def run(root):
    done = []
    p = os.path.join(root, 'p-trend.html')
    if os.path.exists(p):  # 종목 차트: 휴대폰에서 차트를 크게(사용자 2026-10-29)
        s = open(p, encoding='utf-8').read(); o = s
        NEWH = '(window.__mmH || Math.round(Math.min(430, Math.max(280, W * 0.86))))'
        s = s.replace(NEWH, '@@NEWH@@')
        for old in ('Math.round(Math.min(300, Math.max(200, W * 0.42)))', 'Math.round(Math.min(440, Math.max(300, W * 0.95)))', 'Math.round(Math.min(380, Math.max(260, W * 0.78)))', 'Math.round(Math.min(430, Math.max(280, W * 0.86)))'):
            s = s.replace(old, NEWH)
        s = s.replace('@@NEWH@@', NEWH)
        # 금리(%) 표시: 소수 둘째 자리, 'USD' 대신 '%'(사용자 2026-10-29 채권·유가 층위)
        s = s.replace("const fmtShort = (x, cur) => { if (x == null) return ''; const d = cur === 'USD'", "const fmtShort = (x, cur) => { if (x == null) return ''; const d = cur === '%' ? 2 : cur === 'USD'")
        s = s.replace("+ ' ' + r.currency", "+ (r.currency === '%' ? '%' : ' ' + r.currency)")
        s = s.replace("const rank = (c) => (/지수|ETF/.test(c) ? 0 :", "const rank = (c) => (/레버리지·테마/.test(c) ? 0.3 : /지수|ETF/.test(c) ? 0 : /금리|유가/.test(c) ? 0.5 :")  # 채권·유가 층위는 지수 바로 뒤
        s = s.replace("Math.pow(10, Math.max(0, Math.floor(Math.log10(Math.abs(v))) - 3))", "Math.pow(10, Math.max((typeof r !== 'undefined' && r && r.currency === '%') ? -3 : 0, Math.floor(Math.log10(Math.abs(v))) - 3))")  # 금리는 소수까지
        # 휴대폰 스크롤 때 주소창이 숨었다 나오며 생기는 '높이만 바뀐' resize로 차트 전체를 다시 그려 깜빡이던 것 막기(사용자 2026-10-29)
        s = s.replace("let rt0 = null; addEventListener('resize', () => { clearTimeout(rt0); rt0 = setTimeout(draw, 150); });", "let rt0 = null, rw0 = innerWidth; addEventListener('resize', () => { if (innerWidth === rw0 && !window.__mmForce) return; rw0 = innerWidth; window.__mmForce = 0; clearTimeout(rt0); rt0 = setTimeout(draw, 150); });")
        # 자세한 차트: 손가락 따라다니며 깜빡이던 말풍선 상자 없애고, 차트 위 고정 한 줄(mmDtip)에 표시(사용자 2026-10-29)
        s = s.replace("const tip = hv.append('g');", "const tip = hv.append('g').style('display', 'none');", 1)
        s = s.replace("t3.text(rel).attr('fill', relc);", "t3.text(rel).attr('fill', relc); try { mmDtip(t1.text(), t2.text(), rel, relc); } catch (e) {}", 1)
        # 자세한 차트도 5년·10년, 버튼에 기간 표시(data-k) — 기간 고르기는 아래 공통 줄에서(사용자 2026-10-29)
        s = s.replace("[['1m', '1개월'], ['3m', '3개월'], ['6m', '6개월'], ['12m', '12개월']].forEach(([k, l]) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'pb-chip'; b.textContent = l;", "[['1m', '1개월'], ['3m', '3개월'], ['6m', '6개월'], ['12m', '12개월'], ['5y', '5년'], ['10y', '10년']].forEach(([k, l]) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'pb-chip'; b.textContent = l; b.dataset.k = k;", 1)
        s = s.replace("const cutDays = { '1m': 31, '3m': 92, '6m': 184, '12m': 370 }[openRange];", "const cutDays = { '1m': 31, '3m': 92, '6m': 184, '12m': 370, '5y': 1830, '10y': 3660 }[openRange] || 370;", 1)
        s = s.replace(".text(openRange === '12m' || openRange === '6m' ? String(t.getUTCFullYear()).slice(2)", ".text(openRange === '5y' || openRange === '10y' ? String(t.getUTCFullYear()) : openRange === '12m' || openRange === '6m' ? String(t.getUTCFullYear()).slice(2)", 1)
        # 매물대: 오래 머문 가격대 → 최근 1년 고점·저점 꺾인 자리를 ±4%로 묶어 여러 번 부딪힌 곳(사용자 2026-10-29)
        i0 = s.find("        const lo2 = d3.min(dly, (a) => a.v), hi2 = d3.max(dly, (a) => a.v), nb = 14")
        i1 = s.find("const above = near.filter((z) => z.a > nowV).sort((x, y) => y.n - x.n)[0];", i0)
        if i0 > 0 and i1 > 0:
            i1 += len("const above = near.filter((z) => z.a > nowV).sort((x, y) => y.n - x.n)[0];")
            s = s[:i0] + PIV_JS + s[i1:]
            s = s.replace("${below.n}거래일 머문 구간</span>`;", "${below.why}</span>` + (below2 ? `<span class=\"ln\">▪ 더 아래 지지 <b>${zf(below2)}</b> · ${below2.why}</span>` : '');", 1)
            s = s.replace("${above.n}거래일 머문 구간</span>`;", "${above.why}</span>` + (above2 ? `<span class=\"ln\">▪ 더 위 저항 <b>${zf(above2)}</b> · ${above2.why}</span>` : '');", 1)
            s = s.replace("[[below, 'var(--color-ok)', '아래 지지 후보'], [above, 'var(--color-bad)', '위 저항 후보']].forEach(([z, colz, lab]) => {\n          if (!z) return;\n          const y1 = clampY(z.b), y2 = clampY(z.a);\n          g.insert('rect', ':first-child').attr('x', m.l).attr('width', W - m.r - m.l).attr('y', y1).attr('height', Math.max(3, y2 - y1)).attr('fill', colz).attr('opacity', .08);",
                          "[[below2, 'var(--color-ok)', '더 아래', .045], [above2, 'var(--color-bad)', '더 위', .045], [below, 'var(--color-ok)', '아래 지지 후보', .08], [above, 'var(--color-bad)', '위 저항 후보', .08]].forEach(([z, colz, lab, zop]) => {\n          if (!z) return;\n          const y1 = clampY(z.b), y2 = clampY(z.a);\n          g.insert('rect', ':first-child').attr('x', m.l).attr('width', W - m.r - m.l).attr('y', y1).attr('height', Math.max(3, y2 - y1)).attr('fill', colz).attr('opacity', zop);\n          if (zop < .06) return;", 1)
        s = re.sub(r'const MYLINES = \{.*?\};\n', 'const MYLINES = {};\n', s, count=1)  # 내 관점 관문선은 사이트에서 생략(사용자 2026-10-29)
        if s != o: open(p, 'w', encoding='utf-8').write(s); done.append('trend-height')
    for f, cfg in PAGES.items():
        p = os.path.join(root, f)
        if not os.path.exists(p): continue
        s = o = open(p, encoding='utf-8').read()
        s = re.sub(r'<style data-ptidy>[\s\S]*?</style><script data-ptidy>[\s\S]*?</script>', '', s)
        js = COMMON_JS + cfg['js'] + "\n(function(){var q=0;function go(){try{tidy()}catch(e){}}go();document.addEventListener('DOMContentLoaded',go);window.addEventListener('load',go);try{new MutationObserver(function(){if(q)return;q=1;setTimeout(function(){q=0;go()},150)}).observe(document.documentElement,{subtree:true,childList:true})}catch(e){}})();"
        if cfg.get('sync'):
            js = COMMON_JS + cfg['js'] + "\n(function(){var q=0,n=0,t0=0,busy=0;function go(){try{tidy()}catch(e){}}go();document.addEventListener('DOMContentLoaded',go);window.addEventListener('load',go);try{new MutationObserver(function(){if(busy)return;var now=Date.now();if(now-t0>300){t0=now;n=0}if(++n>8){if(!q){q=1;setTimeout(function(){q=0;go()},120)}return}busy=1;try{go()}finally{busy=0}}).observe(document.documentElement,{subtree:true,childList:true})}catch(e){}})();"
        add = '<style data-ptidy>' + CSS_COMMON + cfg['css'] + '</style><script data-ptidy>' + js + '</script>'
        s = s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add
        if s != o: open(p, 'w', encoding='utf-8').write(s); done.append(f)
    return done
