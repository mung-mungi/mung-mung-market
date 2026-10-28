# 첫 화면 정리(사용자 2026-10-29 지시): '오늘 한눈에' 제목·날짜 칩 빼기, 묶음 제목 줄이기, 펼친 설명 글꼴을 본문과 맞추고 문장마다 줄바꿈
# 여러 번 돌려도 같음(이미 바뀌었으면 그대로). kit/home.html과 사이트 index.html 둘 다에 씀
import sys

CSS_SH_OLD = '.sh{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:0 0 10px;font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--muted)}'
CSS_SH_NEW = '.sh{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin:0 0 6px;font-size:13px;font-weight:700;letter-spacing:.04em;color:var(--muted)}'
CSS_ADD = ('\n/* hub_tidy */.today .lab{display:none!important}'
           '.today .c{font-family:var(--sans)!important;font-size:14.5px!important;font-weight:500!important;color:var(--fg)!important;'
           'line-height:1.55!important;letter-spacing:-.01em!important;white-space:pre-line;margin:8px 0 0!important;padding-top:8px;border-top:1px dashed var(--line)}')
JS_OLD = "bold($('t-c'),t.comment||'')"
JS_NEW = "bold($('t-c'),(t.comment||'').replace(/(다\\.)\\s+/g,'$1\\n'))"


def tidy(s):
    s = s.replace('      <p class="sh">오늘 한눈에</p>\n', '').replace('<p class="sh">오늘 한눈에</p>', '')
    s = s.replace('매일 아침 핵심 · 하루 한 번 이상 갱신<span>', '매일 아침 핵심<span>')
    s = s.replace('흐름 확인 · 며칠~몇 주 흐름과 소식<span>', '흐름 확인<span>')
    s = s.replace(CSS_SH_OLD, CSS_SH_NEW)
    if '/* hub_tidy */' not in s and '</style>' in s:
        s = s.replace('</style>', CSS_ADD + '\n</style>', 1)
    s = s.replace(JS_OLD, JS_NEW)
    return s


if __name__ == '__main__':
    for p in sys.argv[1:]:
        o = open(p, encoding='utf-8').read(); s = tidy(o)
        if s != o: open(p, 'w', encoding='utf-8').write(s)
        print(p, 'changed' if s != o else 'same')


# 시황 기록: 화제의 인물 발언은 3명까지 보이고 나머지는 '더 보기'로 접기(사용자 2026-10-29)
BRIEF_ANCHOR = "s.appendChild(ul);if(kind==='eco'"
BRIEF_ADD = ("if(kind==='ppl'&&ul.children.length>3){const n=ul.children.length-3,rest=()=>[...ul.children].slice(3);rest().forEach(li=>li.hidden=true);"
             "const mb=document.createElement('button');mb.type='button';mb.className='bf-pmore';mb.textContent='더 보기 ▾ ('+n+'명)';"
             "mb.onclick=()=>{const o=mb.dataset.o!=='1';mb.dataset.o=o?'1':'';rest().forEach(li=>li.hidden=!o);mb.textContent=o?'접기 ▴':'더 보기 ▾ ('+n+'명)'};"
             "ul.after(mb)}")
BRIEF_CSS = ('<style data-pmore>.bf-pmore{display:block;margin:6px 0 0;padding:7px 12px;font:inherit;font-size:14px;font-weight:700;color:var(--accent,#9a6200);'
             'background:color-mix(in srgb,var(--accent,#9a6200) 9%,transparent);border:1px solid color-mix(in srgb,var(--accent,#9a6200) 25%,transparent);'
             'border-radius:10px;cursor:pointer;box-shadow:0 2px 0 color-mix(in srgb,var(--accent,#9a6200) 18%,transparent)}.bf-pmore:active{transform:translateY(1px)}</style>')


def tidy_brief(s):
    s = tidy_deep(s)
    s = tidy_paper(s)
    s = tidy_tiles(s)
    s = tidy_units(s)
    if "'더 보기 ▾ ('" in s or BRIEF_ANCHOR not in s:
        return s
    s = s.replace(BRIEF_ANCHOR, "s.appendChild(ul);" + BRIEF_ADD + ";if(kind==='eco'", 1)
    return s.replace('</body>', BRIEF_CSS + '</body>', 1) if '</body>' in s else s + BRIEF_CSS


# 인물 발언 행간: 첫 문단만 보이고 나머지는 '행간 더 읽기'로 접기(사용자 2026-10-29 — 길어지면 펼치기)
DEEP_ANCHOR = "bx.appendChild(p)});s.appendChild(bx);more.appendChild(s)}"
DEEP_NEW = ("bx.appendChild(p)});s.appendChild(bx);if(bx.children.length>1){const rest=()=>[...bx.children].slice(1),n=bx.children.length-1;rest().forEach(e=>e.hidden=true);"
            "const mb=document.createElement('button');mb.type='button';mb.className='bf-pmore';mb.textContent='행간 더 읽기 ▾';"
            "mb.onclick=()=>{const o=mb.dataset.o!=='1';mb.dataset.o=o?'1':'';rest().forEach(e=>e.hidden=!o);mb.textContent=o?'접기 ▴':'행간 더 읽기 ▾'};s.appendChild(mb)}more.appendChild(s)}")


def tidy_deep(s):
    if "'행간 더 읽기 ▾'" in s or DEEP_ANCHOR not in s:
        return s
    return s.replace(DEEP_ANCHOR, DEEP_NEW, 1)


# 목표주가 '최근 목표가 변경' 안내문: 한 줄로 짧게(사용자 2026-10-29 — 설명은 친절하되 주저리 없이)
TGT_OLD = ('<p class="sub">최근 일주일 사이 목표주가나 투자의견을 바꾼 기관과 그 이유(코멘트). 이유가 확인된 변경을 맨 위에 둡니다. '
           '<b class="newb">NEW</b> = 가장 최근 업데이트에 들어온 변경. 누르면 그 종목 화면으로 갑니다.</p>')
TGT_NEW = ('<p class="sub">이유가 확인된 변경부터 · <b class="newb">NEW</b> 새로 들어온 것</p>')


def tidy_targets(s):
    import re
    s = s.replace(TGT_OLD, TGT_NEW)
    return re.sub(r'<p class="sub">바꾼 이유가 확인된 것부터[^<]*<b class="newb">NEW</b>[^<]*</p>', TGT_NEW, s)


# 데일리 시황 맨 위 요약을 신문 1면처럼(사용자 2026-10-29): 제호 · 판 정보 · 첫 문장 = 큰 제목 · 나머지 = 본문(첫 글자 크게)
PAPER = r'''<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&display=swap"><style data-paper>
#take.np{display:block!important;padding:12px 14px 12px!important;background:#f3f2ee!important;border:1px solid #cfccc4!important;border-radius:4px!important;box-shadow:none!important;color:#262626!important}
#take.np::before{content:none!important;display:none!important}
#take.np .np-mast{display:flex;align-items:flex-end;justify-content:space-between;gap:8px;font-family:"Noto Serif KR",ui-serif,serif;font-weight:900;font-size:23px;line-height:1;letter-spacing:-.04em;color:#222;padding:0 0 6px;border-bottom:3px solid #333}#take.np .np-mast em{font:600 10.5px/1.3 -apple-system,"Apple SD Gothic Neo",sans-serif;font-style:normal;letter-spacing:0;color:#77746d;text-align:right}
#take.np .np-mast small{display:none}
#take.np .np-line{display:flex;justify-content:space-between;gap:8px;font:500 11px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#77746d;padding:4px 0;border-bottom:1px solid #8f8c85;margin:2px 0 10px}
#take.np .np-hd{font-family:"Noto Serif KR",ui-serif,Georgia,serif;font-weight:900;font-size:clamp(16px,4.7vw,21px);line-height:1.4;letter-spacing:-.045em;color:#1a1a1a;margin:0;word-break:keep-all}
#take.np .np-body{font-family:"Noto Serif KR",ui-serif,Georgia,serif;font-weight:500;font-size:15px;line-height:1.75;text-align:left;word-break:keep-all;color:#333;margin:10px 0 0!important;padding-top:10px;border-top:1px solid #cfccc4}
#take.np .np-body b,#take.np .np-body strong{font-weight:700;color:#111}
#take.np .np-more{display:block;width:100%;margin:10px 0 0;padding:6px 0 0;border:0;border-top:1px solid #cfccc4;background:none;font:600 12.5px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#66635c;text-align:right;cursor:pointer}
</style><script data-paper>(function(){var k=0;function go(){var t=document.getElementById('take');if(!t||t.classList.contains('np'))return;var dl=t.querySelector('.bf-dl'),bd=t.querySelector('[data-field=comment]');
if(!bd||!bd.textContent.trim()){if(++k<40)setTimeout(go,250);return}
var a=dl?(dl.querySelector('b')||{}).textContent||'':'',u=dl?(dl.querySelector('.bf-us')||{}).textContent||'':'';a=a.replace(/\s*\([^)]*\)/,'');
var h=bd.innerHTML,hd,rest;if(t.dataset.hd){hd=t.dataset.hd;rest=h}else{var i=h.search(/다\.(\s|$)/);if(i>0){hd=h.slice(0,i+2);rest=h.slice(i+2).trim()}else{hd=h;rest=''}var tmp=document.createElement('div');tmp.innerHTML=hd;hd=tmp.textContent.replace(/\.$/,'')}
t.classList.add('np');t.innerHTML='<div class="np-mast"><span>멍뭉일보</span><em>AI 밸류체인<br>아침판</em></div><div class="np-line"><span>'+a+'</span><span>'+u+'</span></div><h2 class="np-hd"></h2>'+(rest?'<p class="np-body" hidden>'+rest+'</p><button type="button" class="np-more">기사 펼치기 ▾</button>':'');var he=t.querySelector('.np-hd');String(hd).replace(/\*\*/g,'').split(/\s*(?:,|…|\.\.\.)\s*/).filter(Boolean).forEach(function(x,k){if(k)he.appendChild(document.createElement('br'));he.appendChild(document.createTextNode(x.trim()))});var pb=t.querySelector('.np-body');if(pb)pb.innerHTML=pb.innerHTML.replace(/다\.\s+/g,'다.<br>');var mb=t.querySelector('.np-more');if(mb)mb.onclick=function(){var p=t.querySelector('.np-body'),o=p.hidden;p.hidden=!o;mb.textContent=o?'접기 ▴':'기사 펼치기 ▾'}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go()})();</script>'''


HD_ANCHOR = "const tk=$('take');tk.textContent='';const lastAll=ALL[ALL.length-1];"


def tidy_paper(s):
    if HD_ANCHOR in s and 'tk.dataset.hd' not in s:
        s = s.replace(HD_ANCHOR, HD_ANCHOR + "if(lastAll&&lastAll.headline)tk.dataset.hd=lastAll.headline;", 1)
    if 'data-paper' in s or 'id="take"' not in s:
        return s
    return s.replace('</body>', PAPER + '</body>', 1) if '</body>' in s else s + PAPER


# 데일리 시황 숫자 칸: 3열로 작게(사용자 2026-10-29 — 가독성은 지키고 스크롤 압박 줄이기)
TILES = ('<style data-tiles>body .bf-tiles{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important}'
         'body .bf-tile{padding:8px 9px!important;gap:1px!important;border-radius:10px!important}'
         'body .bf-tile .k{font-size:11.5px!important;line-height:1.3!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
         'body .bf-tile .v{font-size:19px!important;line-height:1.25!important;min-height:0!important;margin:1px 0!important}'
         'body .bf-tile .s{font-size:11.5px!important;line-height:1.3!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
         'body .bf-moodc{padding:8px 12px!important}body .bf-moodc .mt{gap:6px!important}</style>')


def tidy_tiles(s):
    if 'data-tiles' in s or 'bf-tiles' not in s:
        return s
    return s.replace('</body>', TILES + '</body>', 1) if '</body>' in s else s + TILES


# 숫자 칸 단위: '%'·'달러'는 숫자 옆에 작게, 아랫줄은 전날 대비(10년물 bp, WTI·VIX %)(사용자 2026-10-29)
UNITS_CSS = ('<style data-units>body .bf-tile .v .u{font-family:-apple-system,"Apple SD Gothic Neo",sans-serif;font-size:12px;font-weight:600;'
             'color:var(--color-fg-muted,#6f6d68);margin-left:3px;letter-spacing:0}</style>')
UNITS_ANCHOR = "  $('t-date').textContent="
UNITS_JS = ("  try{const P=B[B.length-2];[['t-10y','us10y','bp','%'],['t-wti','wti','%','달러'],['t-vix','vix','%','']].forEach(q=>{const v=$(q[0]);if(!v)return;const sx=v.parentNode.querySelector('.s');"
            "if(q[3]&&!v.querySelector('.u')){const sp=document.createElement('span');sp.className='u';sp.textContent=q[3];v.appendChild(sp)}"
            "const a=last&&last[q[1]],b=P&&P[q[1]];if(sx){if(a==null||b==null){sx.style.visibility='hidden';return}"
            "const d=q[2]==='bp'?Math.round((a-b)*1000)/10:(a/b-1)*100;sx.removeAttribute('id');sx.style.visibility='';sx.textContent=Math.abs(d)<0.05?'보합':(d>0?'+':'')+(q[2]==='bp'?d.toFixed(1)+'bp':d.toFixed(1)+'%');sx.className='s '+cl(Math.abs(d)<0.05?0:d)}})}catch(e){}\n")


def tidy_units(s):
    if 'data-units' in s or UNITS_ANCHOR not in s:
        return s
    # 날짜 줄(t-date)은 위 코드가 VIX 칸 아랫줄을 바꾼 뒤에 다시 쓰지 않도록 대상만 없앰
    s = s.replace(UNITS_ANCHOR, UNITS_JS.replace("sx.removeAttribute('id');", "") + "  if(0)$('t-date').textContent=", 1)
    return s.replace('</body>', UNITS_CSS + '</body>', 1) if '</body>' in s else s + UNITS_CSS


# 실적 결과 회사 바로가기: 이름 길이만큼만 차지하는 작은 알약을 촘촘히(사용자 2026-10-29 — 공간 아끼기)
HITS = ('<style data-hits>body .hits{display:flex!important;flex-wrap:wrap!important;gap:3px!important;align-items:center}'
        'body .hits>.hday,body .hits>.hmore,body .hits>.hrest{flex-basis:100%}'
        'body .hits>.hday{flex-basis:auto;font-size:11.5px!important;padding:1px 7px!important;margin-right:2px}'
        'body .hits .hrest:not([hidden]){display:flex!important;flex-wrap:wrap!important;gap:3px!important}body .hits .hrest[hidden]{display:none!important}'
        'body .hits button:not(.hmore){display:inline-flex!important;align-items:center!important;gap:3px!important;padding:2px 7px!important;'
        'border-radius:999px!important;min-height:0!important;line-height:1.3!important;box-shadow:0 1px 0 rgba(0,0,0,.08)}'
        'body .hits button:not(.hmore) b{font-size:12px!important;font-weight:700;letter-spacing:-.03em}'
        'body .hits button:not(.hmore) span{display:none!important}'
        'body .hits .hmore{flex-basis:auto!important;border-radius:999px!important;padding:2px 9px!important;font-size:12px!important}</style>')


def tidy_hits(s):
    s = tidy_ups(s)
    s = tidy_sumrow(s)
    if 'data-hits' in s or 'id="hits"' not in s:
        return s
    return s.replace('</body>', HITS + '</body>', 1) if '</body>' in s else s + HITS


# 맨 위 페이지 줄(.ib): 아이패드·카톡 안 브라우저에서 옆으로 밀어도 안 움직이는 문제 → 손가락 끌기를 직접 처리, '핵심·흐름·점검' 묶음 글자는 숨김(사용자 2026-10-29)
IBDRAG = (r'''<style data-ibdrag>.ib{-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;touch-action:pan-x pan-y}.ib .tg{display:none!important}</style>'''
          r'''<script data-ibdrag>(function(){function on(n){if(!n||n.__drag)return;n.__drag=1;var x0,y0,s0,mode=null;'''
          r'''n.addEventListener('touchstart',function(e){var t=e.touches[0];x0=t.clientX;y0=t.clientY;s0=n.scrollLeft;mode=null},{passive:true});'''
          r'''n.addEventListener('touchmove',function(e){var t=e.touches[0],dx=t.clientX-x0,dy=t.clientY-y0;if(mode===null&&(Math.abs(dx)>6||Math.abs(dy)>6))mode=Math.abs(dx)>Math.abs(dy)?'x':'y';'''
          r'''if(mode==='x'){var before=n.scrollLeft;n.scrollLeft=s0-dx;if(n.scrollLeft!==before||Math.abs(dx)>10){e.preventDefault()}}},{passive:false});'''
          r'''n.addEventListener('touchend',function(){if(mode==='x'){var a=n.querySelectorAll('a');a.forEach(function(l){l.__noclick=Date.now()})}mode=null},{passive:true});'''
          r'''n.addEventListener('click',function(e){var l=e.target.closest&&e.target.closest('a');if(l&&l.__noclick&&Date.now()-l.__noclick<350){e.preventDefault();e.stopPropagation()}},true)}'''
          r'''function go(){document.querySelectorAll('.ib').forEach(on)}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();setTimeout(go,1500)})();</script>''')


def tidy_ibdrag(s):
    if 'data-ibdrag' in s or 'class="ib"' not in s:
        return s
    return s.replace('</body>', IBDRAG + '</body>', 1) if '</body>' in s else s + IBDRAG


# 실적 결과 '이번 주 발표 예정': 날짜 아래 구간(새벽 장후·아시아·저녁 장전)마다 한 줄씩, 글자 모양 하나로 통일(사용자 2026-10-29 — 산만함 정리)
UPS = (r'''<style data-ups>body .ups{gap:0!important}body .ups .ud{display:block!important;padding:7px 0!important}'''
       r'''body .ups .ud>em{display:block;width:auto!important;font:800 13px/1.3 -apple-system,"Apple SD Gothic Neo",sans-serif!important;color:var(--accent)!important;margin:0 0 3px}'''
       r'''body .ups .ur{display:grid;grid-template-columns:4.6em 1fr;gap:6px;align-items:baseline;padding:2px 0}'''
       r'''body .ups .ud .ur>.slot,body .ups .ud .ur>.slot.pre,body .ups .ud .ur>.slot.post,body .ups .ud .ur>.slot.asia{all:unset!important;font:700 11.5px/1.5 -apple-system,"Apple SD Gothic Neo",sans-serif!important;color:var(--muted)!important;white-space:nowrap!important}'''
       r'''body .ups .ud .ur>.slot.pre{color:var(--accent)!important}'''
       r'''body .ups .un{display:flex;flex-wrap:wrap;gap:1px 9px}'''
       r'''body .ups .un>*{all:unset;font:500 13.5px/1.5 -apple-system,"Apple SD Gothic Neo",sans-serif;color:var(--faint,#9a978f);white-space:nowrap}'''
       r'''body .ups .un>button{color:var(--fg);font-weight:700;cursor:pointer}'''
       r'''body .ups .un>button i{font-style:normal;font-size:11px;color:var(--up);margin-left:2px}</style>'''
       r'''<script data-ups>(function(){function fix(){var u=document.getElementById('ups');if(!u)return;u.querySelectorAll('.ud').forEach(function(d){if(d.dataset.tidy)return;d.dataset.tidy=1;'''
       r'''var kids=[].slice.call(d.childNodes),row=null,names=null;kids.forEach(function(n){if(n.nodeType===1&&n.tagName==='EM')return;'''
       r'''if(n.nodeType===1&&n.classList.contains('slot')){row=document.createElement('div');row.className='ur';names=document.createElement('div');names.className='un';row.appendChild(n);row.appendChild(names);d.appendChild(row);return}'''
       r'''if(n.nodeType!==1){if(n.textContent.trim()==='')n.remove();return}if(!names){row=document.createElement('div');row.className='ur';row.appendChild(document.createElement('span'));names=document.createElement('div');names.className='un';row.appendChild(names);d.appendChild(row)}'''
       r'''if(n.tagName==='SPAN')n.textContent=n.textContent.replace(/\s*·\s*$/,'');if(n.tagName==='BUTTON'&&/✓/.test(n.textContent)){n.textContent=n.textContent.replace(/\s*✓\s*/,'');var c=document.createElement('i');c.textContent='✓';n.appendChild(c)}names.appendChild(n)})})}'''
       r'''var k=0;(function go(){fix();var u=document.getElementById('ups');if(u&&!u.__mo){u.__mo=1;new MutationObserver(function(){fix()}).observe(u,{childList:true})}if(++k<20&&!(u&&u.children.length))setTimeout(go,300)})()})();</script>''')


def tidy_ups(s):
    if 'data-ups' in s or 'id="ups"' not in s:
        return s
    return s.replace('</body>', UPS + '</body>', 1) if '</body>' in s else s + UPS


# 실적 결과 노트 요약 줄: 한 덩어리 글 → ① AI 판정 한 줄 ② 체크 칩(매출·EPS·가이던스)+주가 반응 ③ 나머지 작은 글씨(사용자 2026-10-29 — 산만함 정리)
SUMROW = (r'''<style data-sumrow>body .sumrow{align-items:flex-start!important}body .sumrow .ar{font-size:0!important;flex:none;align-self:flex-start;padding-top:4px}'''
          r'''body .sumrow .ar::after{content:"▾";font-size:15px;color:var(--muted)}body .sumrow[aria-expanded=true] .ar::after{content:"▴"}'''
          r'''body .sumrow .nm{font-family:inherit!important;font-weight:800!important}body .sumrow .sm.sx{display:block;margin-top:5px;font-size:13.5px!important;line-height:1.5!important;color:var(--fg)!important}'''
          r'''body .sm.sx .sx-ai{display:block}body .sm.sx .sx-ai b{font-weight:800;margin-right:5px}body .sm.sx .sx-ai b.g{color:var(--up)}body .sm.sx .sx-ai b.y{color:#a26a0c}body .sm.sx .sx-ai b.r{color:var(--down)}'''
          r'''body .sm.sx .sx-ck{display:flex;flex-wrap:wrap;gap:3px;margin-top:5px}body .sm.sx .sx-ck i{font-style:normal;font-size:11.5px;font-weight:700;padding:1px 5px;border-radius:5px;background:color-mix(in srgb,var(--up) 11%,transparent);color:var(--up)}'''
          r'''body .sm.sx .sx-ck i.n{background:color-mix(in srgb,var(--down) 11%,transparent);color:var(--down)}body .sm.sx .sx-ck i.m{background:var(--panel-2,#f1f0ec);color:var(--fg)}body .sm.sx .sx-ck i.m.dn{color:var(--down)}body .sm.sx .sx-ck i.m.up{color:var(--up)}'''
          r'''body .sm.sx .sx-et{display:block;margin-top:4px;font-size:12.5px;color:var(--muted);line-height:1.5}</style>'''
          r'''<script data-sumrow>(function(){function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}'''
          r'''function fix(){document.querySelectorAll('.sumrow .sm:not(.sx)').forEach(function(sm){var raw=sm.textContent.trim();if(!raw)return;var parts=raw.split(/\s+·\s+/),ai='',chk=[],react=[],etc=[];'''
          r'''parts.forEach(function(p,i){if(i===0&&/^\d{1,2}\/\d{1,2}$/.test(p))return;var m=p.match(/^AI 관점\s*(호재|중립|경고)\s*(?:\((.*)\))?$/);if(m){var c=m[1]==='호재'?'g':m[1]==='중립'?'y':'r';ai='<b class="'+c+'">AI '+m[1]+'</b>'+esc(m[2]||'');return}'''
          r'''if(/(프리마켓|시간외|장중|종가)\s*[+\-−–~]/.test(p)&&p.length<30){var neg=/[\-−–]\d/.test(p)&&!/\+/.test(p);react.push('<i class="m '+(neg?'dn':'up')+'">'+esc(p)+'</i>');return}'''
          r'''if(/[✅❌]/.test(p)){var re=/([^\s✅❌()]+)\s*(✅|❌)\s*(\([^)]*\))?/g,x,any=false;while((x=re.exec(p))){any=true;chk.push('<i class="'+(x[2]==='✅'?'':'n')+'">'+esc(x[1])+' '+(x[2]==='✅'?'✓':'✗')+'</i>');if(x[3])etc.push(esc(x[1]+' '+x[3].slice(1,-1)))}if(any)return}'''
          r'''etc.push(esc(p))});var h='';if(ai)h+='<span class="sx-ai">'+ai+'</span>';if(chk.length||react.length)h+='<span class="sx-ck">'+chk.join('')+react.join('')+'</span>';if(etc.length)h+='<span class="sx-et">'+etc.join(' · ')+'</span>';'''
          r'''if(h){sm.innerHTML=h;sm.classList.add('sx');var br=sm.previousElementSibling;if(br&&br.tagName==='BR')br.remove()}})}'''
          r'''var k=0;(function go(){fix();if(!document.__sxmo){document.__sxmo=1;new MutationObserver(function(){fix()}).observe(document.body,{childList:true,subtree:true})}if(++k<10)setTimeout(go,400)})()})();</script>''')


def tidy_sumrow(s):
    if 'data-sumrow' in s or 'sumrow' not in s:
        return s
    return s.replace('</body>', SUMROW + '</body>', 1) if '</body>' in s else s + SUMROW
