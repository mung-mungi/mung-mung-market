import json
import os
import re
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
    s = tidy_statgo(s)
    s = tidy_splash(s)
    s = s.replace('      <p class="sh">오늘 한눈에</p>\n', '').replace('<p class="sh">오늘 한눈에</p>', '')
    s = s.replace('매일 아침 핵심 · 하루 한 번 이상 갱신<span>', '매일 아침 핵심<span>')
    s = s.replace('흐름 확인 · 며칠~몇 주 흐름과 소식<span>', '흐름 확인<span>')
    s = s.replace(CSS_SH_OLD, CSS_SH_NEW)
    # CSS_ADD는 메인 첫 </style>에 넣던 규칙인데, 그 자리가 늘 '이전·홈 버튼'(navfab) 통째 부품 안이라 다시 입힐 때마다 지워져
    # 실제로는 한 번도 적용되지 않았음. 정리 3일차(2026-11-01)에 그 부품이 공용 파일로 빠지면서 처음 적용될 뻔 → 지금 화면 그대로 두려고 끔
    s = s.replace(CSS_ADD + '\n</style>', '</style>')
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
    s = tidy_np2(s)
    s = tidy_macrogo(s)
    s = tidy_rng(s)
    s = tidy_rngui(s)
    s = tidy_deep(s)
    s = tidy_paper(s)
    s = tidy_tiles(s)
    s = tidy_units(s)
    s = tidy_fng(s)
    s = tidy_dend(s)
    s = tidy_ddate(s)
    s = tidy_briefui(s)
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
    s = tidy_tgrow(s)
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
</style><script data-paper>(function(){var k=0;function go(){var t=document.getElementById('take');if(!t||t.querySelector('.np-mast'))return;var dl=t.querySelector('.bf-dl'),bd=t.querySelector('[data-field=comment]');
if(!bd||!bd.textContent.trim()){if(++k<40)setTimeout(go,250);return}
var a=dl?(dl.querySelector('b')||{}).textContent||'':'',u=dl?(dl.querySelector('.bf-us')||{}).textContent||'':'';a=a.replace(/\s*\([^)]*\)/,'');
var h=bd.innerHTML,hd,rest;if(t.dataset.hd){hd=t.dataset.hd;rest=h}else{var i=h.search(/다\.(\s|$)/);if(i>0){hd=h.slice(0,i+2);rest=h.slice(i+2).trim()}else{hd=h;rest=''}var tmp=document.createElement('div');tmp.innerHTML=hd;hd=tmp.textContent.replace(/\.$/,'')}
t.classList.add('np');t.innerHTML='<div class="np-mast"><span>멍뭉일보</span><em>AI 밸류체인<br>아침판</em></div><div class="np-line"><span>'+a+'</span><span>'+u+'</span></div><h2 class="np-hd"></h2>'+(rest?'<p class="np-body" hidden>'+rest+'</p><button type="button" class="np-more">기사 펼치기 ▾</button>':'');var he=t.querySelector('.np-hd');String(hd).replace(/\*\*/g,'').split(/\s*(?:,|…|\.\.\.)\s*/).filter(Boolean).forEach(function(x,k){if(k)he.appendChild(document.createElement('br'));he.appendChild(document.createTextNode(x.trim()))});var pb=t.querySelector('.np-body');if(pb)pb.innerHTML=pb.innerHTML.replace(/다\.\s+/g,'다.<br>');var mb=t.querySelector('.np-more');if(mb)mb.onclick=function(){var p=t.querySelector('.np-body'),o=p.hidden;p.hidden=!o;mb.textContent=o?'접기 ▴':'기사 펼치기 ▾'}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();var tk0=document.getElementById('take');if(tk0)new MutationObserver(function(){if(!tk0.querySelector('.np-mast')){k=0;go()}}).observe(tk0,{childList:true})})();</script>'''


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
    s = tidy_earnui(s)
    s = tidy_irlib(s)
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
    s = tidy_perf(s)
    s = tidy_splash(s)
    s = tidy_navorder(s)
    s = tidy_dock(s)
    s = tidy_headui(s)
    s = tidy_rdbox(s)
    return ibdrag_place(s)


def ibdrag_place(s):
    if 'class="ib"' not in s:
        return s
    # 정리 3일차: _tools/ibdrag.* 공용 파일(IBDRAG 글은 기록용으로 남김). 이미 있으면 그 자리 그대로 바꿔 끼움(순서 유지)
    add = core_ref('ibdrag', 'ibdrag.css') + core_ref('ibdrag', 'ibdrag.js')
    m = re.search(r'(?:<style data-ibdrag>.*?</style>|<link data-ibdrag[^>]*>)\s*(?:<script data-ibdrag(?:\s[^>]*)?>.*?</script>)', s, re.S)
    if m:
        return s[:m.start()] + add + s[m.end():]
    s = core_strip(s, 'ibdrag')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 실적 결과 '이번 주 발표 예정': 날짜 아래 구간(새벽 장후·아시아·저녁 장전)마다 한 줄씩, 글자 모양 하나로 통일(사용자 2026-10-29 — 산만함 정리)
UPS = (r'''<style data-ups>body .ups{gap:0!important}body .ups .ud{display:block!important;padding:7px 0!important}'''
       r'''body .ups .ud>em{display:block;width:auto!important;font:800 13px/1.3 -apple-system,"Apple SD Gothic Neo",sans-serif!important;color:var(--accent)!important;margin:0 0 3px}'''
       r'''body .ups .ur{display:grid;grid-template-columns:4.1em 1fr;gap:4px;align-items:baseline;padding:2px 0}'''
       r'''body .ups .ud .ur>.slot,body .ups .ud .ur>.slot.pre,body .ups .ud .ur>.slot.post,body .ups .ud .ur>.slot.asia{all:unset!important;font:700 11.5px/1.5 -apple-system,"Apple SD Gothic Neo",sans-serif!important;color:var(--muted)!important;white-space:nowrap!important}'''
       r'''body .ups .ud .ur>.slot.pre{color:var(--accent)!important}'''
       r'''body .ups .un{display:flex;flex-wrap:wrap;gap:1px 7px}'''
       r'''body .ups .un>*{all:unset;font:500 13.5px/1.5 -apple-system,"Apple SD Gothic Neo",sans-serif;color:var(--faint,#9a978f);white-space:nowrap}'''
       r'''body .ups .un>button{color:var(--fg);font-weight:700;cursor:pointer}'''
       r'''body .ups .un>button i{font-style:normal;font-size:10.5px;color:var(--up);margin-left:1px}</style>'''
       r'''<script data-ups>(function(){function fix(){var u=document.getElementById('ups');if(!u)return;u.querySelectorAll('.ud').forEach(function(d){if(d.dataset.tidy)return;d.dataset.tidy=1;'''
       r'''var kids=[].slice.call(d.childNodes),row=null,names=null;kids.forEach(function(n){if(n.nodeType===1&&n.tagName==='EM')return;'''
       r'''if(n.nodeType===1&&n.classList.contains('slot')){row=document.createElement('div');row.className='ur';names=document.createElement('div');names.className='un';row.appendChild(n);row.appendChild(names);d.appendChild(row);return}'''
       r'''if(n.nodeType!==1){if(n.textContent.trim()==='')n.remove();return}if(!names){row=document.createElement('div');row.className='ur';row.appendChild(document.createElement('span'));names=document.createElement('div');names.className='un';row.appendChild(names);d.appendChild(row)}'''
       r'''if(n.tagName==='SPAN')n.textContent=n.textContent.replace(/\s*·\s*$/,'');if(n.tagName==='BUTTON'&&/✓/.test(n.textContent)){n.textContent=n.textContent.replace(/\s*✓\s*/,'');var c=document.createElement('i');c.textContent='✓';n.appendChild(c)}names.appendChild(n)})})}'''
       r'''var k=0;(function go(){fix();var u=document.getElementById('ups');if(u&&!u.__mo){u.__mo=1;new MutationObserver(function(){fix()}).observe(u,{childList:true})}if(++k<20&&!(u&&u.children.length))setTimeout(go,300)})()})();</script>''')


def tidy_ups(s):
    if 'id="ups"' not in s:
        return s
    s = re.sub(r'<(style|script) data-ups>.*?</\1>', '', s, flags=re.S)
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
    s = re.sub(r'<(style|script) data-sumrow>.*?</\1>', '', s, flags=re.S)
    if 'sumrow' not in s:
        return s
    return s.replace('</body>', SUMROW + '</body>', 1) if '</body>' in s else s + SUMROW


# 옵션 온도계: 기간구조 카드를 차트들 맨 아래(설명 카드 앞)로 내려 VIX 3개월 바로 밑에 풋콜(CBOE)이 오게(사용자 2026-10-29)
def tidy_optui(s):
    s = re.sub(r'<(style|script) data-optui>.*?</\1>', '', s, flags=re.S)
    if 'id="earn-card"' not in s and 'id="take-txt"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-optui>' + open(os.path.join(d, 'optui.css'), encoding='utf-8').read() + '</style><script data-optui>' + open(os.path.join(d, 'optui.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


def tidy_opt(s):
    s = tidy_optui(s)
    m = re.search(r'\s*<section class="ot-card" id="term-card">.*?</section>', s, re.S)
    r = s.find('<section class="ot-card ot-sec" id="rule-card">')
    if not m or r < 0 or m.start() > s.find('id="earn-card"'):
        return s
    blk = m.group(0)
    s = s[:m.start()] + s[m.end():]
    r = s.find('<section class="ot-card ot-sec" id="rule-card">')
    return s[:r] + blk.strip() + '\n\n  ' + s[r:]


# 데일리 시황 펼친 카드: 시장 이야기를 맨 앞 신문 기사로, 나머지 섹션은 제목만 보이는 접이식 신문 목차로(사용자 2026-10-29 — 전체 글이 너무 김)
NP2 = (r"""<style data-np2>body #days .bf-more{gap:0!important;row-gap:0!important;background:#f3f2ee;border-top:3px solid #333;margin-top:8px;padding:10px 12px 6px;border-radius:2px}"""
       r"""body #days .bf-more .bf-toc{display:none!important}"""
       r"""body #days .bf-more .np-lead{border:0!important;border-top:1px solid #cfccc4!important;background:none!important;padding:12px 0 6px!important;margin:0!important}"""
       r"""body #days .bf-more .np-lead>.k{display:block;font:900 21px/1.3 "Noto Serif KR","Nanum Myeongjo",serif!important;color:#111!important;letter-spacing:-.01em;padding-bottom:6px;margin-bottom:8px;border-bottom:1px solid #cfccc4}"""
       r"""body #days .bf-more .np-lead>.k::before{content:"시황 해설";display:block;font:700 11px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#7a766d;letter-spacing:.08em;margin-bottom:2px}"""
       r"""body #days .bf-more .np-lead p{font-size:16.5px!important;line-height:1.75!important;color:#222!important;margin:0 0 10px!important}"""
       r"""body #days .bf-more .np-lead .bf-hlt{background:none!important;font-weight:800;box-shadow:inset 0 -.42em 0 #e4dfd2}"""
       r"""body #days .bf-day.on>.bf-com{display:none!important}body #days .np-lead .np-x{display:none!important}body #days .np-lead.op .np-x{display:block!important}"""
       r"""body #days .np-lead .np-rd{all:unset;display:block;margin:2px 0 8px;font:600 13px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#66635c;cursor:pointer}"""
       r"""body #days .bf-more .bf-sec li{font-size:16px!important;line-height:1.6!important}body #days .bf-more .bf-sec .it{font-size:16.5px!important}body #days .bf-more .bf-sec .sub2,body #days .bf-more .bf-sec .q{font-size:15px!important}body #days .bf-day>.bf-hl{font-size:19px!important}"""
       r"""body #days .bf-more .bf-cite{font-size:11px!important;opacity:.7}"""
       r"""body #days .bf-more .bf-sec.npf{border:0!important;border-top:1px solid #cfccc4!important;background:none!important;border-radius:0!important;padding:0!important;margin:0!important}"""
       r"""body #days .bf-more .bf-sec.npf>.k{display:flex!important;justify-content:space-between;align-items:center;cursor:pointer;padding:9px 2px!important;margin:0!important;font:800 16.5px/1.35 "Noto Serif KR","Nanum Myeongjo",serif!important;color:#222!important;border:0!important;background:none!important}"""
       r"""body #days .bf-more .bf-sec.npf>.k::after{content:"▾";font:400 13px sans-serif;color:#7a766d}body #days .bf-more .bf-sec.npf.op>.k::after{content:"▴"}"""
       r"""body #days .bf-more .bf-sec.npf.op{padding-bottom:10px!important}"""
       # 접힌 칸도 앞 3~4줄은 미리 보이고 아래는 옅게 흐려지며 '펼쳐서 더 보기'(사용자 2026-11-01) — 짧은 칸(npx)은 그대로 다 보임
       r"""body #days .bf-more .bf-sec.npf:not(.op):not(.npx){max-height:156px;overflow:hidden;position:relative;cursor:pointer}"""
       r"""body #days .bf-more .bf-sec.npf:not(.op):not(.npx)::after{content:"펼쳐서 더 보기 ▾";position:absolute;left:0;right:0;bottom:0;height:60px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:7px;font:700 13.5px/1 -apple-system,\"Apple SD Gothic Neo\",sans-serif;color:#8a6410;background:linear-gradient(to bottom,rgba(243,242,238,0),#f3f2ee 62%);pointer-events:none}"""
       r"""body #days .bf-more .bf-sec.npf.npx>.k{cursor:default}body #days .bf-more .bf-sec.npf.npx>.k::after{content:none}</style>"""
       r"""<script data-np2>(function(){var NQ=[];/* 속도(2026-11-03): 칸마다 따로 높이를 재면 칸 수만큼 화면 배치를 다시 계산 → 한 프레임에 모아 한 번에 재고 한 번에 표시 */function fix(){document.querySelectorAll('#days .bf-more').forEach(function(m){if(m.dataset.np2)return;m.dataset.np2=1;var st=m.querySelector('.bf-story');if(st){st.classList.add('np-lead');var aft=m.querySelector(':scope>.bf-sec[id$="-changes"]')||m.querySelector(':scope>.bf-sec.iss');if(aft)aft.after(st);var ps=st.querySelectorAll('p');if(ps.length>2){for(var i=2;i<ps.length;i++)ps[i].classList.add('np-x');var rb=document.createElement('button');rb.type='button';rb.className='np-rd';rb.textContent='기사 이어 읽기 ▾ ('+(ps.length-2)+'단락)';if((window.__npop||{})['lead'+(st.id||'')]){st.classList.add('op');rb.textContent='접기 ▴'}rb.onclick=function(e){e.stopPropagation();st.classList.toggle('op');(window.__npop=window.__npop||{})['lead'+(st.id||'')]=st.classList.contains('op');rb.textContent=st.classList.contains('op')?'접기 ▴':'기사 이어 읽기 ▾ ('+(ps.length-2)+'단락)'};st.appendChild(rb)}}var ex=[m.querySelector(':scope>.bf-macro'),m.querySelector(':scope>.bf-src')].filter(Boolean);if(ex.length){var w=document.createElement('div');w.className='bf-sec';var kk=document.createElement('span');kk.className='k';kk.textContent='수치 · 출처';w.appendChild(kk);ex.forEach(function(e){w.appendChild(e)});m.appendChild(w)}"""
       r"""m.querySelectorAll('.bf-sec').forEach(function(c){if(c.classList.contains('np-lead'))return;c.classList.add('npf');var OP=window.__npop||(window.__npop={});var key=c.id||c.querySelector(':scope>.k')&&c.querySelector(':scope>.k').textContent;if(key in OP?OP[key]:c.classList.contains('iss'))c.classList.add('op');var k=c.querySelector(':scope>.k');if(k)k.addEventListener('click',function(e){e.stopPropagation();if(c.classList.contains('npx'))return;c.classList.toggle('op');OP[key]=c.classList.contains('op')});c.addEventListener('click',function(e){if(c.classList.contains('op')||c.classList.contains('npx')||e.target.closest('a'))return;e.stopPropagation();c.classList.add('op');OP[key]=true});NQ.push(c)})});if(NQ.length&&!NQ.r){NQ.r=1;requestAnimationFrame(function(){NQ.r=0;var a=NQ.splice(0),h=a.map(function(c){return c.scrollHeight});a.forEach(function(c,i){if(h[i]<=172)c.classList.add('npx')})})}}"""
       r"""var k=0;(function go(){fix();if(!document.__np2){var d=document.getElementById('days');if(d){document.__np2=1;new MutationObserver(fix).observe(d,{childList:true,subtree:true})}}if(++k<10)setTimeout(go,500)})()})();</script>""")


def tidy_np2(s):
    s = re.sub(r'<(style|script) data-np2>.*?</\1>', '', s, flags=re.S)
    if 'id="days"' not in s:
        return s
    return s.replace('</body>', NP2 + '</body>', 1) if '</body>' in s else s + NP2


# 데일리 시황 '일별 지수 등락·분위기' 차트: 기본 3개월(사용자 2026-10-29). 브리핑 이전 날짜는 live/idx.json(Actions가 받는 지수 일별 등락)으로 채움, 1·3·6개월 버튼
RNG_ANCHOR = "function drawChart(){\n  const box=$('chart');"
RNG_FN = (r"""let __IDX=null;fetch('live/idx.json',{cache:'no-store'}).then(r=>r.ok?r.json():null).then(j=>{if(j&&j.rows){__IDX=j.rows;try{drawChart()}catch(e){}}}).catch(()=>{});"""
          r"""function __rngui(){const lg=$('legend');if(!lg||document.querySelector('.bf-rng'))return;const w=document.createElement('div');w.className='bf-rng';[[1,'1개월'],[3,'3개월'],[6,'6개월']].forEach(o=>{const b=document.createElement('button');b.type='button';b.textContent=o[1];b.setAttribute('aria-pressed',o[0]===(st.rng||3));"""
          r"""b.onclick=()=>{st.rng=o[0];w.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));drawChart()};w.appendChild(b)});lg.parentNode.insertBefore(w,lg)}"""
          r"""function __cb(){__rngui();const mo=(st.rng||3);const by={};(__IDX||[]).forEach(r=>{by[r.date]=Object.assign({},r)});B.forEach(r=>{by[r.date]=r});"""
          r"""const all=Object.keys(by).sort().map(k=>by[k]);if(!all.length)return B;const L=new Date(all[all.length-1].date+'T00:00:00Z');L.setUTCMonth(L.getUTCMonth()-mo);const c=L.toISOString().slice(0,10);"""
          r"""const rows=all.filter(r=>r.date>c);const acc={};return rows.map(r=>{const o=Object.assign({},r);SER.forEach(s=>{const k=s[0];if(r[k]==null){o[k]=acc[k]==null?null:+((acc[k]-1)*100).toFixed(2);return}if(acc[k]==null){acc[k]=1;o[k]=0;return}acc[k]=acc[k]*(1+r[k]/100);o[k]=+((acc[k]-1)*100).toFixed(2)});return o})}"""
          r"""function __cbnote(){const c=$('chart-card');if(!c||c.dataset.cum)return;const p=c.querySelector('p');const h=c.querySelector('h2,h3');if(h)h.textContent='지수 흐름 · 분위기';if(p){p.textContent='선 = 기간 첫날 대비 누적 등락(%). 아래 띠 = 그날 분위기(초록 위험선호 · 회색 혼조 · 빨강 위험회피). 점을 누르면 그날 기록이 열립니다.';c.dataset.cum=1}}""" "\n")


def tidy_rng(s):
    s = re.sub(r'(?:let __IDX=null;|function __cb\(\)\{)[^\n]*\n(function drawChart\(\)\{)const B=__cb\(\);', r'\1', s)
    s = s.replace("function drawChart(){try{__cbnote()}catch(e){}\n", "function drawChart(){\n")
    if RNG_ANCHOR not in s:
        return s
    s = s.replace(RNG_ANCHOR, RNG_FN + "function drawChart(){const B=__cb();try{__cbnote()}catch(e){}\n  const box=$('chart');", 1)
    # 점 크기: 길어지면 작게
    s = s.replace(".attr('r',3).attr('fill',dash.colors[i])});\n  // hover columns", ".attr('r',B.length>40?1.6:3).attr('fill',dash.colors[i])});\n  // hover columns", 1)
    return s


RNG_UI = (r"""<style data-rng>body .bf-rng{display:flex;gap:4px;margin:2px 0 6px}body .bf-rng button{all:unset;cursor:pointer;font:600 12.5px/1 -apple-system,"Apple SD Gothic Neo",sans-serif;padding:5px 10px;border-radius:999px;border:1px solid var(--color-border-line,#ddd);color:var(--color-fg-muted,#666);box-shadow:0 1px 2px rgba(0,0,0,.06)}"""
          r"""body .bf-rng button[aria-pressed=true]{background:#111;color:#fff;border-color:#111}</style>""")


def tidy_rngui(s):
    s = re.sub(r'<(style|script) data-rng>.*?</\1>', '', s, flags=re.S)
    if 'id="chart-card"' not in s:
        return s
    return s.replace('</body>', RNG_UI + '</body>', 1) if '</body>' in s else s + RNG_UI


# 목표주가: 최근 변경·평균 목표가·기관별·변경 기록 표를 시세 보드 '종목별 시세' 한 줄 카드로 (사용자 2026-10-29)
def tidy_tgrow(s):
    s = re.sub(r'<(style|script) data-tgrow>.*?</\1>', '', s, flags=re.S)
    if 'rc-list' not in s and 'pt-tbl' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-tgrow>' + open(os.path.join(d, 'tgrow.css'), encoding='utf-8').read() + '</style><script data-tgrow>' + open(os.path.join(d, 'tgrow.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 실적 결과 화면 정리(시세 보드 양식) — CSS·JS는 _tools/earnui.css·earnui.js (사용자 2026-10-29)
def tidy_earnui(s):
    s = re.sub(r'<(style|script) data-earnui>.*?</\1>', '', s, flags=re.S)
    if 'id="hits"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-earnui>' + open(os.path.join(d, 'earnui.css'), encoding='utf-8').read() + '</style><script data-earnui>' + open(os.path.join(d, 'earnui.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 실적 결과 > IR 서재(사용자 2026-10-30) — CSS·JS는 _tools/irlib.css·irlib.js, 데이터는 d/ir/ir.json
def tidy_irlib(s):
    s = re.sub(r'<(style|script) data-irlib>.*?</\1>', '', s, flags=re.S)
    if 'id="hits"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-irlib>' + open(os.path.join(d, 'irlib.css'), encoding='utf-8').read() + '</style><script data-irlib>' + open(os.path.join(d, 'irlib.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 홈 '오늘 한눈에' 숫자 칸을 누르면 해당 차트로(사용자 2026-10-29): 나스닥→종목 차트 QQQ, 반도체→SOXX, 10년물→채권·금리, WTI→데일리 시황 금리·유가 차트(WTI)
STATGO = (r"""<style data-statgo>.stats .stat[data-go]{cursor:pointer;transition:transform .08s}.stats .stat[data-go]:active{transform:translateY(1px);background:rgba(154,98,0,.06)}"""
          r""".stats .stat[data-go] .k::after{content:" ›";color:#b9b6ae;font-weight:700}</style>"""
          r"""<script data-statgo>document.addEventListener('click',function(e){var s=e.target.closest&&e.target.closest('.stats .stat[data-go]');if(!s)return;var g=s.dataset.go;if(/\.html/.test(g))return;e.stopPropagation();e.preventDefault();location.href='p-trend.html?per=1y#'+g},true);</script>""")


def tidy_statgo(s):
    s = re.sub(r'<(style|script) data-statgo>.*?</\1>', '', s, flags=re.S)
    if 'class="stats"' not in s and "stats" not in s:
        return s
    return s.replace('</body>', STATGO + '</body>', 1) if '</body>' in s else s + STATGO


# 데일리 시황: 주소 끝이 #wti 등이면 금리·유가 차트에서 그 항목을 골라 보여 줌
MACROGO = (r"""<script data-macrogo>(function(){var h=(location.hash||'').slice(1).toLowerCase();if(!h)return;var L={wti:'WTI',us10y:'10년물',brent:'브렌트',gold:'금',vix:'VIX',dxy:'달러지수'};if(!L[h])return;var k=0;"""
           r"""(function go(){var c=document.getElementById('mchips');var b=c&&[...c.querySelectorAll('button')].find(function(x){return x.textContent.trim().indexOf(L[h])===0});if(b){b.click();var m=document.getElementById('macro-card');if(m){var y=m.getBoundingClientRect().top+scrollY-70;scrollTo(0,y)}return}if(++k<20)setTimeout(go,300)})()})();</script>""")


def tidy_macrogo(s):
    s = re.sub(r'<script data-macrogo>.*?</script>', '', s, flags=re.S)
    if 'id="mchips"' not in s:
        return s
    return s.replace('</body>', MACROGO + '</body>', 1) if '</body>' in s else s + MACROGO


# 시장 경고등 화면 정리 — _tools/ltui.css·ltui.js (사용자 2026-10-29)
def tidy_lights(s):
    s = re.sub(r'<(style|script) data-ltui>.*?</\1>', '', s, flags=re.S)
    if 'id="areas"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-ltui>' + open(os.path.join(d, 'ltui.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'ltui.js'), encoding='utf-8').read() + '</script>'
    # 자동 한 줄·멈춘 값 칩(사용자 2026-10-31) — _tools/ltfresh.*, 자료 d/lights/fresh.json
    add += '<style data-ltui>' + open(os.path.join(d, 'ltfresh.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'ltfresh.js'), encoding='utf-8').read() + '</script>'
    # '지금 시장은' 통일 양식·근접(반불)·반도체·AI 영역(사용자 2026-11-01) — _tools/ltnear.*
    # 맨 위 '한눈에' — 층위별 신호등·업종 회전 지도(사용자 2026-11-01) — _tools/mmtop.*, 자료 d/stress/stress.json
    add += '<style data-ltui>' + open(os.path.join(d, 'mmtop.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'mmtop.js'), encoding='utf-8').read() + '</script>'
    add += '<style data-ltui>' + open(os.path.join(d, 'ltnear.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'ltnear.js'), encoding='utf-8').read() + '</script>'
    # 점수제 큰 카드·1년 점수 흐름(사용자 2026-11-01, 근접 0.8·보통 0.4·양호 0.2) — _tools/ltscore.*
    add += '<style data-ltui>' + open(os.path.join(d, 'ltscore.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'ltscore.js'), encoding='utf-8').read() + '</script>'
    # 바로가기 칩 + 주제 구분띠(사용자 2026-11-02) — _tools/ltjump.*
    add += '<style data-ltui>' + open(os.path.join(d, 'ltjump.css'), encoding='utf-8').read() + '</style><script data-ltui>' + open(os.path.join(d, 'ltjump.js'), encoding='utf-8').read() + '</script>'
    s = s.replace(LT_AREAS_OLD, LT_AREAS_NEW, 1)
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


LT_AREAS_OLD = "const AREAS=[['유가','p-policy.html','p-policy.html']"
LT_AREAS_NEW = "const AREAS=[['반도체·AI','p-trend.html','p-trend.html'],['유가','p-policy.html','p-policy.html']"


# 종목 차트: 주소에 ?per=1y 등이 있으면 그 기간 알약을 눌러 둠(홈 숫자 칸 → 1년 기본, 사용자 2026-10-29)
PERGO = (r"""<script data-pergo>(function(){var m=(location.search||'').match(/per=(1d|1w|1m|3m|1y|5y|10y)/);if(!m)return;var L={'1d':'1일','1w':'1주','1m':'1달','3m':'3달','1y':'1년','5y':'5년','10y':'10년'}[m[1]];try{window.__mmT=window.__mmT||{};window.__mmT.per=m[1]}catch(e){}var k=0;"""
         r"""(function go(){var b=[...document.querySelectorAll('button')].find(function(x){return x.textContent.trim()===L&&x.offsetParent});if(b){if(b.getAttribute('aria-pressed')!=='true'&&!b.classList.contains('on'))b.click();if(++k<4)setTimeout(go,500);return}if(++k<30)setTimeout(go,300)})()})();</script>""")


def tidy_pergo(s):
    s = re.sub(r'<script data-pergo>.*?</script>', '', s, flags=re.S)
    if 'MMT_PER' not in s:
        return s
    return s.replace('</body>', PERGO + '</body>', 1) if '</body>' in s else s + PERGO


# 맨 위 페이지 줄 '핵심' 순서를 홈 '매일 아침 핵심'과 같게 — _tools/navorder.js (사용자 2026-10-29)
def tidy_navorder(s):
    s = core_strip(s, 'navorder')  # 정리 3일차(2026-11-01): 통째 대신 공용 파일 참조, 자리는 그대로
    if 'class="ib"' not in s:
        return s
    i = s.find('</nav>', s.find('class="ib"'))
    if i < 0:
        return s
    return s[:i + 6] + core_ref('navorder', 'navorder.js') + s[i + 6:]


# 실적 일정 맨 위 요약 — _tools/calui.css·calui.js (사용자 2026-10-29)
def tidy_cal(s):
    s = core_strip(s, 'calui')
    if 'id="next"' not in s:
        return s
    add = core_ref('calui', 'calui.css') + core_ref('calui', 'calui.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 페이지 맨 위 '오늘 한눈에' 양식 통일 — _tools/headui.css·headui.js (사용자 2026-10-29)
def tidy_headui(s):
    s = core_strip(s, 'headui')
    # 머리 부품이 공용 파일로 옮겨 가 'mm-hero' 글자가 페이지에 없어도, 머리 참조(data-hero)가 있으면 머리가 있는 페이지(2026-11-01)
    if 'mm-take' not in s and 'mm-hero' not in s and 'data-hero' not in s:
        return s
    add = core_ref('headui', 'headui.css') + core_ref('headui', 'headui.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 나머지 페이지 공통 정리 — _tools/uniui.css·uniui.js (사용자 2026-10-29)
UNI_PAGES = ['p-bond.html', 'p-econ.html', 'p-cal.html', 'p-short.html', 'p-fx.html', 'p-capex.html', 'p-policy.html', 'p-tech.html', 'p-supply.html', 'p-neo.html', 'p-qtr.html', 'p-insider.html']


def tidy_uni(s):
    s = core_strip(s, 'uniui')
    s = core_strip(s, 'krtable')
    if 'id="tw-table-card"' in s:
        k = core_ref('krtable', 'krtable.css') + core_ref('krtable', 'krtable.js')
        s = s.replace('</body>', k + '</body>', 1) if '</body>' in s else s + k
    add = core_ref('uniui', 'uniui.css') + core_ref('uniui', 'uniui.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# '읽는 법' 상자 통일 — _tools/rdbox.css·rdbox.js (사용자 2026-10-29)
def tidy_rdbox(s):
    s = core_strip(s, 'rdbox')
    if 'class="ib"' not in s:
        return s
    add = core_ref('rdbox', 'rdbox.css') + core_ref('rdbox', 'rdbox.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 페이지 줄을 화면 아래 아이콘 독으로 — _tools/dock.css (사용자 2026-10-29)
def tidy_dock(s):
    s = re.sub(r'<style data-dock>.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<link data-dock(?:\s[^>]*)?>', '', s)
    if 'class="ib"' not in s:
        return s
    s = core_strip(s, 'dock')
    add = core_ref('dock', 'dock.css') + core_ref('dock', 'dock.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add



# 공용 파일 참조(2026-11-01 정리 1일차) — 페이지마다 통째로 붙이던 부품을 _tools/ 파일 하나로 불러옴.
# 주소 뒤 ?v= 는 파일 내용으로 만든 값이라, 파일을 고치면 홈 화면 앱도 새 파일을 받음.
def _core_v(name):
    import hashlib
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
DEFER_JS = {'navfab.js', 'push.js', 'stale.js', 'descfold.js'}
def core_ref(marker, name):
    u = '_tools/' + name + '?v=' + _core_v(name)
    if name.endswith('.css'):
        return '<link data-' + marker + ' rel="stylesheet" href="' + u + '">'
    # 속도(2026-11-03): 머리(head)에 들어가지만 첫 화면에 필요 없는 부품은 defer — 내용부터 그리고 실행(순서는 그대로 유지)
    if name in DEFER_JS:
        return '<script data-' + marker + ' defer src="' + u + '"></script>'
    return '<script data-' + marker + ' src="' + u + '"></script>'
def core_strip(s, marker):  # 예전 통째 붙인 것과 새 참조 둘 다 지움
    s = re.sub(r'<(style|script) data-' + marker + r'(?:\s[^>]*)?>.*?</\1>', '', s, flags=re.S)
    return re.sub(r'<link data-' + marker + r'(?:\s[^>]*)?>', '', s)
def vt_refs():
    return core_ref('vt', 'vt.css') + core_ref('vt', 'vt.js')

# 누름 소리(틱) — 2026-11-01 정리 1일차 이어서: 통째 부품을 공용 파일 참조로, 자리는 그대로(본문 끝)
def tidy_tick(s):
    pat = r'<script data-tick(?:\s[^>]*)?>[\s\S]*?</script>'
    m = re.search(pat, s)
    if not m:
        return s
    ref = core_ref('tick', 'tick.js')
    head, tail = s[:m.start()], s[m.end():]
    return head + ref + re.sub(pat, '', tail)  # 첫 자리에 참조 하나, 혹시 겹친 것은 지움


# 페이지 머리 1판·2판 — 2026-11-01 정리 2일차: 통째 부품을 공용 파일 참조로. 조각마다 제자리에서 바꿈.
# 주의 ①: 1판(hero.js)이 제목·날짜칩·면책 문구에 이름표를 붙이고 2판이 받아 꾸밈 → 1판을 지우면 21페이지가 무너짐(가상 진행으로 확인).
# 주의 ②: 조각 사이 줄바꿈을 지우면 일부 페이지가 1~3px 달라짐 → 줄바꿈은 그대로 둠.
HERO_PARTS = [('style', 'hero', 'hero.css'), ('script', 'hero', 'hero.js'), ('script', 'hero-fix', 'herofix.js'),
              ('style', 'hero2', 'hero2.css'), ('script', 'hero2', 'hero2.js')]
# 머리 부품의 원본은 hero.html·hero2.html 하나 — 공용 파일(hero*.css/js, herofix.js)은 여기서 자동으로 맞춤(2026-11-01: 두 곳이 어긋나 이름 변경이 안 먹던 문제)
_HERO_SYNCED = []
def _sync_hero_parts():
    if _HERO_SYNCED: return
    _HERO_SYNCED.append(1)
    d = os.path.dirname(os.path.abspath(__file__))
    for src, parts in (('hero.html', (('style', 'data-hero', 'hero.css'), ('script', 'data-hero', 'hero.js'), ('script', 'data-hero-fix', 'herofix.js'))),
                       ('hero2.html', (('style', 'data-hero2', 'hero2.css'), ('script', 'data-hero2', 'hero2.js')))):
        try: h = open(os.path.join(d, src), encoding='utf-8').read()
        except Exception: continue
        for tag, mk, out in parts:
            m = re.search(r'<%s %s>(.*?)</%s>' % (tag, mk, tag), h, re.S)
            if not m: continue
            fp = os.path.join(d, out)
            try: cur = open(fp, encoding='utf-8').read()
            except Exception: cur = None
            if cur != m.group(1): open(fp, 'w', encoding='utf-8').write(m.group(1))
def tidy_hero(s):
    _sync_hero_parts()
    for tag, m, n in HERO_PARTS:
        ref = core_ref(m, n)
        s = re.sub(r'<%s data-%s>[\s\S]*?</%s>' % (tag, m, tag), lambda x: ref, s, count=1)  # 통째 → 참조
        if n.endswith('.css'):
            s = re.sub(r'<link data-%s rel="stylesheet" href="_tools/%s\?v=\w+">' % (m, re.escape(n)), lambda x: ref, s)
        else:
            s = re.sub(r'<script data-%s src="_tools/%s\?v=\w+"></script>' % (m, re.escape(n)), lambda x: ref, s)
    return s


# 종목 차트 자료(사용자 2026-11-01 '열 때 무거움'): 페이지 안에 통째로 넣던 546KB 자료를 d/trend_embed.json(예비본)으로 빼고,
# 열 때는 5분 갱신 자료(live/trend.json) 하나만 받음. 그게 없거나 예비본보다 오래되면 그때만 예비본을 받음. 5분 안에 다시 열면 휴대폰에 남은 것을 씀
TREND_STUB_MARK = 'd/trend_embed.json'
def tidy_trend(s, root=None):
    i = s.find('const DATA = ')
    if i < 0: return s
    j = s.find('\n', i); line = s[i:j]
    if TREND_STUB_MARK in line: return s
    body = line[len('const DATA = '):].rstrip()
    if body.endswith(';'): body = body[:-1]
    if body.startswith('(function(d){'):
        k = body.find('})(')
        if k < 0 or not body.endswith(')'): return s
        js = body[k + 3:-1]
    else:
        js = body
    try:
        D = json.loads(js.replace('<\\/', '</'))
    except Exception:
        return s
    import hashlib
    raw = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
    v = hashlib.md5(raw.encode()).hexdigest()[:8]
    if root:
        os.makedirs(os.path.join(root, 'd'), exist_ok=True)
        open(os.path.join(root, 'd', 'trend_embed.json'), 'w', encoding='utf-8').write(raw)
    meta = json.dumps({'asof': D.get('asof', ''), 'at': D.get('at', ''), 'label': D.get('label', '')}, ensure_ascii=False)
    stub = ("const DATA = (function(m){function g(u){try{var x=new XMLHttpRequest();x.open('GET',u,false);x.send();if(x.status===200)return JSON.parse(x.responseText)}catch(e){}return null}"
            "var j=g('live/trend.json?t='+Math.floor(Date.now()/300000));"
            "if(j&&j.P&&j.P.length&&j.asof>=m.asof&&(j.at||'')>(m.at||'')){window.__LIVE_TREND__=j.label;return j}"
            "var d=g('" + TREND_STUB_MARK + "?v=" + v + "');if(d&&d.P)return d;if(j&&j.P)return j;return {asof:m.asof,label:m.label,P:[],H:{}}})(" + meta.replace('</', '<\\/') + ");")
    return s[:i] + stub + s[j:]


# 메인 화면 순서·이름(home_order.js)과 시장 띠(market.js)를 최신 파일로(2026-11-01) — 예전엔 동기화 때만 다시 넣었음
def tidy_mkt(s):
    if 'data-mkt' not in s: return s
    d = os.path.dirname(os.path.abspath(__file__))
    MJ = '<script data-mkt>' + open(os.path.join(d, 'market.js'), encoding='utf-8').read() + '</script>'
    MJ += '<script data-mkt>' + open(os.path.join(d, 'home_order.js'), encoding='utf-8').read() + '</script>'
    m = re.search(r'<script data-mkt>[\s\S]*?</script>', s)
    s2 = re.sub(r'<script data-mkt>[\s\S]*?</script>', '', s)
    return s2[:m.start()] + MJ + s2[m.start():] if m else s


# 휴대폰 버벅임 줄이기 — _tools/perf.js를 <head> 맨 앞에(사용자 2026-10-29)
def tidy_perf(s):
    s = core_strip(s, 'perf')
    js = core_ref('perf', 'perf.js')
    m = re.search(r'<head[^>]*>', s)
    if m:
        return s[:m.end()] + js + s[m.end():]
    m = re.search(r'<script', s)
    return s[:m.start()] + js + s[m.start():] if m else js + s


# 처음 열 때 멍뭉이 로딩 화면 — _tools/splash.* (사용자 2026-10-29)
def tidy_splash(s):
    s = core_strip(s, 'splash')
    d = os.path.dirname(os.path.abspath(__file__))
    s = re.sub(r'<link data-hsicon[^>]*>|<meta data-hsicon[^>]*>', '', s)
    s = core_strip(s, 'hshome')
    s = core_strip(s, 'wrapfix')
    s = core_strip(s, 'navfab')
    s = core_strip(s, 'push')
    s = core_strip(s, 'names')
    s = core_strip(s, 'chlog')
    s = core_strip(s, 'stale')
    s = core_strip(s, 'descfold')
    # 홈 화면 앱 다시 시작 → 메인부터 (_tools/homestart.js, 사용자 2026-10-29)
    add = '<link data-hsicon rel="manifest" href="manifest.webmanifest"><meta data-hsicon name="mobile-web-app-capable" content="yes"><meta data-hsicon name="apple-mobile-web-app-capable" content="yes">' + core_ref('hshome', 'homestart.js')
    # 줄바꿈 다듬기 — _tools/wrapfix.* (사용자 2026-10-29, 전 페이지)
    add += core_ref('wrapfix', 'wrapfix.css') + core_ref('wrapfix', 'wrapfix.js')
    # 이전·홈 동그란 버튼 — _tools/navfab.* (사용자 2026-10-29)
    add += core_ref('navfab', 'navfab.css') + core_ref('navfab', 'navfab.js')  # 정리 3일차: 공용 파일 참조
    # 휴대폰 알림 받기 카드(원시그널) — _tools/push.* (사용자 2026-10-30, 메인에서만 동작)
    add += core_ref('push', 'push.css') + core_ref('push', 'push.js')
    # 평소 부르는 이름으로(알파벳 → 구글) — _tools/names.js (사용자 2026-11-02)
    add += core_ref('names', 'names.js')
    # 버전업 표시 + 바뀐 점 설명서, 오래된 자료 경고 칩(사용자 2026-11-02) — _tools/chlog.*, stale.js
    # 'NEW · 바뀐 점'·'새로 바뀐 것' 알약(chlog)은 사용자 요청으로 내림(2026-11-02 "짜친다") — 위 core_strip이 지우고 다시 넣지 않음. 버전 표기(v1.9)는 prep_site가 따로 붙임
    add += core_ref('stale', 'stale.js')
    # 설명 문단 접기 — 첫 줄 + '설명 보기 ▾'(사용자 2026-11-02, 전 페이지 · 메인·데일리 시황 제외는 js에서)
    add += core_ref('descfold', 'descfold.css') + core_ref('descfold', 'descfold.js')
    add += '<link data-hsicon rel="apple-touch-icon" href="img/icon180.png?v=2"><meta data-hsicon name="apple-mobile-web-app-title" content="멍뭉 터미널">' + core_ref('splash', 'splash.css') + core_ref('splash', 'splash.js')
    m = re.search(r'<script data-perf(?:\s[^>]*)?>.*?</script>', s, re.S) or re.search(r'<head[^>]*>', s)
    s = s[:m.end()] + add + s[m.end():] if m else add + s
    # 페이지 넘김 전환(vt) — 예전처럼 </head> 바로 앞, 공용 파일로
    if 'data-vt' in s or '</head>' in s:
        s = core_strip(s, 'vt')
        if re.search(r'</head>', s, re.I):
            s = re.sub(r'</head>', lambda x: vt_refs() + x.group(0), s, count=1, flags=re.I)
        else:  # </head>가 없는 페이지: 예전처럼 <!doctype> 바로 뒤(앞에 두면 화면이 옛 방식으로 그려짐)
            m = re.match(r'\s*<!doctype[^>]*>', s, re.I)
            s = s[:m.end()] + vt_refs() + s[m.end():] if m else vt_refs() + s
    return s


# 메인 전달사항(사용자 2026-10-31) — 들어오면 전체 화면 공지, 닫으면 접힌 한 줄. 내용은 d/notice.html(_tools/notice.*)
def tidy_notice(s):
    s = re.sub(r'<(style|script) data-notice>.*?</\1>', '', s, flags=re.S)
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-notice>' + open(os.path.join(d, 'notice.css'), encoding='utf-8').read() + '</style><script data-notice>' + open(os.path.join(d, 'notice.js'), encoding='utf-8').read() + '</script>'
    # 유튜브 새 영상 배너(사용자 2026-11-02) — _tools/ytban.*, 자료 d/yt.json(Actions yt.yml)
    s = core_strip(s, 'ytban')
    add += core_ref('ytban', 'ytban.css') + core_ref('ytban', 'ytban.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 주인장 자료(사용자 2026-11-01) — 메인 맨 아래 비번 잠금 검토함, 내용은 d/owner.enc.json(암호문)
def tidy_owner(s):
    s = re.sub(r'<(style|script) data-owner>.*?</\1>', '', s, flags=re.S)
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-owner>' + open(os.path.join(d, 'owner.css'), encoding='utf-8').read() + '</style><script data-owner>' + open(os.path.join(d, 'owner.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add

# 공포·탐욕 지수·VIX는 CNN·CBOE 원본(d/fng.json, Actions 6시간)을 우선 씀(사용자 2026-11-01) — 브리핑 기사값이 하루~이틀 밀리는 일이 있었음
FNG = (r"""<script data-fng>(function(){var F=null;var Z=[[0,25,'극단적 공포','#e5484d'],[25,45,'공포','#f08a4b'],[45,55,'중립','#8b8d98'],[55,75,'탐욕','#7cc47f'],[75,101,'극단적 탐욕','#2fa36b']];"""
       r"""function md(d){var a=String(d).split('-');return (+a[1])+'.'+(+a[2])}"""
       r"""function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}"""
       r"""function mood(){var f=F&&F.fng;var box=document.getElementById('mood'),card=document.getElementById('mood-card');if(!f||!box)return;var v=Math.round(f.score);var key=f.date+':'+v;if(box.dataset.fng===key&&box.firstChild)return;"""
       r"""var z=Z.filter(function(q){return v>=q[0]&&v<q[1]})[0]||Z[2];if(card)card.style.display='';box.textContent='';box.dataset.fng=key;"""
       r"""var top=el('div','mt');top.appendChild(el('span','mk','공포·탐욕 지수'));var b=el('b','mv',v+' '+z[2]);b.style.color='color-mix(in srgb,'+z[3]+' 78%,var(--color-fg))';top.appendChild(b);"""
       r"""var a=el('a','ms',md(f.date)+' 마감'+(f.prev_close!=null?' · 전일 '+Math.round(f.prev_close):'')+' · CNN');a.href=f.src||'https://edition.cnn.com/markets/fear-and-greed';a.target='_blank';a.rel='noopener';top.appendChild(a);box.appendChild(top);"""
       r"""var bar=el('div','mb');Z.forEach(function(q){var i=el('i');i.style.flex=String(Math.min(q[1],100)-q[0]);i.style.background=q[3];bar.appendChild(i)});var m=el('em');m.style.left=Math.max(0,Math.min(100,f.score))+'%';bar.appendChild(m);box.appendChild(bar);"""
       r"""var lb=el('div','ml');['0 극단적 공포','50 중립','100 극단적 탐욕'].forEach(function(t){lb.appendChild(el('span','',t))});box.appendChild(lb)}"""
       r"""function vix(){var x=F&&F.vix;var v=document.getElementById('t-vix');if(!x||!v)return;var u=v.querySelector('.u');var t=x.close.toFixed(2);if(v.firstChild&&v.firstChild.nodeType===3){if(v.firstChild.nodeValue!==t)v.firstChild.nodeValue=t}else if(v.textContent!==t){v.textContent=t;if(u)v.appendChild(u)}"""
       r"""var sx=v.parentNode.querySelector('.s');if(sx){var d=x.chg;var s2=Math.abs(d)<0.05?'보합':(d>0?'+':'')+d.toFixed(1)+'%';if(sx.textContent!==s2){sx.textContent=s2;sx.removeAttribute('id');sx.style.visibility='';sx.className='s '+(Math.abs(d)<0.05?'mu':d>0?'up':'dn')}}}"""
       r"""function ap(){try{mood()}catch(e){}try{vix()}catch(e){}}"""
       r"""fetch('d/fng.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j)return;F=j;ap();var k=0;(function go(){ap();if(++k<12)setTimeout(go,500)})();"""
       r"""['mood-card','tiles'].forEach(function(id){var n=document.getElementById(id);if(n)new MutationObserver(ap).observe(n,{childList:true,subtree:true,characterData:true})})}).catch(function(){})})();</script>""")


def tidy_fng(s):
    s = re.sub(r'<script data-fng>.*?</script>', '', s, flags=re.S)
    if 'id="mood-card"' not in s:
        return s
    return s.replace('</body>', FNG + '</body>', 1) if '</body>' in s else s + FNG

# 시황 날짜 카드 사이 '여기서 그날 기사 끝' 표시(사용자 2026-11-01) — 펼친 날 끝에 신문식 마감 줄, 카드 사이 간격·점선
DEND = (r"""<style data-dend>body #days .bf-day+.bf-day{margin-top:30px!important;position:relative}"""
        r"""body #days .bf-day+.bf-day::before{content:"";position:absolute;left:12%;right:12%;top:-16px;border-top:2px dashed #cfc6b2;pointer-events:none}"""
        r"""body #days .mm-dend{display:flex;align-items:center;gap:10px;margin:14px 0 2px;font:800 13.5px/1 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#7a5a12;letter-spacing:.02em}"""
        r"""body #days .mm-dend::before,body #days .mm-dend::after{content:"";flex:1;border-top:3px double #8f8a7e}</style>"""
        r"""<script data-dend>(function(){function md(id){var a=id.replace('day-','').split('-');return (+a[1])+'.'+(+a[2])+' '+'일월화수목금토'[new Date(Date.UTC(+a[0],a[1]-1,+a[2])).getUTCDay()]}"""
        r"""function fix(){document.querySelectorAll('#days .bf-day').forEach(function(c){var m=c.querySelector(':scope>.bf-more');var e=c.querySelector(':scope>.mm-dend');if(!m){if(e)e.remove();return}if(e&&e===c.lastElementChild)return;if(e)e.remove();e=document.createElement('div');e.className='mm-dend';e.textContent='■ '+md(c.id)+' 기사 끝';c.appendChild(e)})}"""
        r"""var k=0;(function go(){fix();var d=document.getElementById('days');if(d&&!d.__dend){d.__dend=1;new MutationObserver(fix).observe(d,{childList:true,subtree:true})}if(++k<10)setTimeout(go,500)})()})();</script>""")


def tidy_dend(s):
    s = re.sub(r'<(style|script) data-dend>.*?</\1>', '', s, flags=re.S)
    if 'id="days"' not in s:
        return s
    return s.replace('</body>', DEND + '</body>', 1) if '</body>' in s else s + DEND


# 시황 날짜 카드 날짜 크게 + 요일 + 한국 기준 '오늘·어제'(사용자 2026-11-02) — _tools/ddate.*
def tidy_ddate(s):
    s = re.sub(r'<(style|script) data-ddate>.*?</\1>', '', s, flags=re.S)
    if 'id="days"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-ddate>' + open(os.path.join(d, 'ddate.css'), encoding='utf-8').read() + '</style><script data-ddate>' + open(os.path.join(d, 'ddate.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 데일리 시황 통일 양식(사용자 2026-11-02 — 신문 컨셉 대신 사이트 공통 카드·고딕·알약) — _tools/briefui.*
def tidy_briefui(s):
    s = re.sub(r'<(style|script) data-briefui>.*?</\1>', '', s, flags=re.S)
    if 'id="days"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-briefui>' + open(os.path.join(d, 'briefui.css'), encoding='utf-8').read() + '</style><script data-briefui>' + open(os.path.join(d, 'briefui.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 채권·금리 페이지 '채권 경고등'도 시장 경고등과 같은 '지금' 양식(사용자 2026-11-01) — _tools/bdnear.*
# 정책·지정학: 타임라인 → 다가오는 일정(3줄 + 펼치기) → 나머지(사용자 2026-11-01) — _tools/polord.*
def tidy_policy(s):
    s = re.sub(r'<(style|script) data-polord>.*?</\1>', '', s, flags=re.S)
    if 'id="up-sec"' not in s or 'id="tl-sec"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-polord>' + open(os.path.join(d, 'polord.css'), encoding='utf-8').read() + '</style><script data-polord>' + open(os.path.join(d, 'polord.js'), encoding='utf-8').read() + '</script>'
    # 타임라인 헤드라인 모드(사용자 2026-11-01): 제목만 이어 보고 누르면 펼침, 흐름 이어 보기, 정리본 — 정책·테크 공용
    s = re.sub(r'<(style|script) data-tlx>.*?</\1>', '', s, flags=re.S)
    add += '<style data-tlx>' + open(os.path.join(d, 'tlx.css'), encoding='utf-8').read() + '</style><script data-tlx>' + open(os.path.join(d, 'tlx.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


def tidy_bond(s):
    s = re.sub(r'<(style|script) data-bdnear>.*?</\1>', '', s, flags=re.S)
    if 'id="lights-card"' not in s:
        return s
    d = os.path.dirname(os.path.abspath(__file__))
    add = '<style data-bdnear>' + open(os.path.join(d, 'bdnear.css'), encoding='utf-8').read() + '</style><script data-bdnear>' + open(os.path.join(d, 'bdnear.js'), encoding='utf-8').read() + '</script>'
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


SEARCH_PAGES = ['p-prices.html', 'p-targets.html', 'p-trend.html']
def tidy_search(s):
    """종목 찾기: 한글 별명·영문·초성까지(사용자 2026-11-02) — _tools/search_ko.js의 __mmq로 바꿔 끼움"""
    s = re.sub(r"\(\s*([A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)?)\.name \+ ' ' \+ \1\.ticker\)\.toLowerCase\(\)\.includes\(q\)",
               lambda m: 'window.__mmq(' + m.group(1) + ',q)', s)
    if 'window.__mmq(' not in s: return s
    s = re.sub(r'<script data-mmq>[\s\S]*?</script>', '', s)
    js = '<script data-mmq>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'search_ko.js'), encoding='utf-8').read() + '</script>'
    return re.sub(r'(<meta charset[^>]*>)', lambda m: m.group(1) + js, s, count=1, flags=re.I) if re.search(r'<meta charset', s, re.I) else js + s


# 페이지 안에 통째로 남은 부품을 그 자리 그대로 공용 파일 참조로 바꿈(사용자 2026-11-02 — 메인 머리 양식·아이디어 페이지 공통 양식)
def inline_to_ref(s, marker, css=None, js=None):
    pat = r'(?:<style data-' + marker + r'(?:\s[^>]*)?>.*?</style>)?\s*(?:<script data-' + marker + r'(?:\s[^>]*)?>(?!\s*</script>).*?</script>)?'
    for m in re.finditer(pat, s, re.S):
        if m.group(0).strip() and ('<style data-' + marker in m.group(0) or '<script data-' + marker in m.group(0)) and ' src=' not in m.group(0).split('>')[0]:
            ref = (core_ref(marker, css) if css and '<style' in m.group(0) else '') + (core_ref(marker, js) if js and '<script' in m.group(0) else '')
            return s[:m.start()] + ref + s[m.end():]
    return s


# 페이지별 '쉽게 읽기' 덧입힘(사용자 2026-11-02): 옵션 온도계 기간구조(optterm) · 시장 경고등 업종 회전 지도 축 설명(rrgaxis)
# 쉽게 읽기·보는 법 통일 덧입힘(2026-11-02): 페이지 → 부품 이름 목록(각각 _tools/<이름>.css·.js)
EASY = {'p-opt.html': ['optterm', 'btscore'], 'p-lights.html': ['rrgaxis'], 'p-bond.html': ['btscore', 'bdopt'],
        'p-brief.html': ['fngbar'], 'index.html': ['todaybtn'], 'p-policy.html': ['chipfold'], 'p-tech.html': ['chipfold']}
# 분류·필터 알약 줄 통일을 사이트 전체로(사용자 2026-11-02) — 넘치는 필터 줄이 있는 페이지만(목표주가 위쪽 고정 목차는 제외)
for _p in ['p-prices.html', 'p-trend.html', 'p-short.html', 'p-targets.html', 'p-earn.html', 'p-qtr.html']:
    EASY[_p] = (EASY.get(_p) or []) + ['chipfold']
# 공매도 추이 '오늘 한눈에' — 확인용 보조지표(사용자 2026-11-02)
EASY['p-short.html'] = EASY['p-short.html'] + ['shtop']
# 단계 옆 '왜 이 단계?' 한 줄(사용자 2026-11-02) — 단계는 점수 그대로, 코멘트로 풀어 줌
EASY['p-opt.html'] = EASY['p-opt.html'] + ['stwhy']; EASY['p-bond.html'] = EASY['p-bond.html'] + ['stwhy']
# '어제보다 바뀐 점' 카드(사용자 2026-11-03, A안)
for _pg in ('p-opt.html', 'p-bond.html', 'p-lights.html'):
    EASY[_pg] = EASY.get(_pg, []) + ['mvban']
# 방금 들어온 소식(사용자 2026-11-02) — 뉴스 두 페이지 맨 위
EASY['p-policy.html'] = EASY['p-policy.html'] + ['newsq_ui']; EASY['p-tech.html'] = EASY['p-tech.html'] + ['newsq_ui']
# 뉴스 타임라인: 높이 고정 상자 대신 '더 보기' + 날짜 바로가기(사용자 2026-11-03)
EASY['p-policy.html'] = EASY['p-policy.html'] + ['tlmore']; EASY['p-tech.html'] = EASY['p-tech.html'] + ['tlmore']
# 경제지표 알림 누르면 그 발표 줄로 + 추세 그래프(사용자 2026-11-04)
EASY['p-econ.html'] = EASY.get('p-econ.html', []) + ['evgo']
# 목표주가 아래쪽 차트 늦게 그리기(2026-11-03): 데이터가 덜 와서 페이지가 짧을 때 잘못 '보임'으로 판정하지 않게 1.5초 뒤(또는 손가락이 처음 닿을 때)부터 지켜봄
LAZYRUN_JS = r"""<script data-lazyrun>window.__lazyRun=function(k,f,el){if(!el||!window.IntersectionObserver)return f();var L=window.__lazyRun.s||(window.__lazyRun.s={}),z=L[k]||(L[k]={});z.f=f;if(z.on)return f();if(z.o)return;z.o=new IntersectionObserver(function(es){if(es.some(function(e){return e.isIntersecting})){z.o.disconnect();z.on=1;requestAnimationFrame(function(){z.f()})}},{rootMargin:"500px 0px"});var arm=function(){if(z.a)return;z.a=1;z.o.observe(el)};setTimeout(arm,1500);['touchstart','wheel','keydown'].forEach(function(t){addEventListener(t,arm,{once:true,passive:true})})};</script>"""
# 실적 결과 가볍게(사용자 2026-11-03, A안): 접힌 노트는 한 줄 카드(+제목·꼬리표)만 화면에 두고, 본문은 펼칠 때 붙임.
# 데이터(seed)·노트 HTML은 그대로 — 자동 실적 업로드·실적 일정·새 소식 목록 도구와 무관. 접힌 동안 본문 안 찾기(.verdict·.row 등)는 보관본까지 같이 찾음
EARNLZ_JS = r"""<script data-earnlz>(function(){var MO=window.MutationObserver,P=Element.prototype,QA=P.querySelectorAll,Q1=P.querySelector,mo=null;
var RX=/([가-힣A-Za-z])\((?=[^)\d\s][^)]+\))/g,SK={SCRIPT:1,STYLE:1,TEXTAREA:1,INPUT:1,CODE:1,PRE:1,NOSCRIPT:1},NUM=/[①②③④⑤⑥⑦⑧⑨⑩]/,SPL=/(?=[①②③④⑤⑥⑦⑧⑨⑩])/,BLK={P:1,DIV:1,LI:1,UL:1,OL:1,TABLE:1,SECTION:1,ARTICLE:1,H1:1,H2:1,H3:1,H4:1},SKS='button,a,select,option,svg,script,style,textarea,input,label,nav';
// 열 때 붙이는 본문에도 페이지를 열 때 하던 손질을 똑같이(감시기가 늦게 붙은 칸을 놓치는 두 가지): 괄호 앞 줄바꿈 자리(wrapfix.js) · ①② 번호마다 줄바꿈(페이지 가독성 스크립트)
function prep(f){try{var w=document.createTreeWalker(f,4),n,L=[];while((n=w.nextNode()))L.push(n);L.forEach(function(n){var p=n.parentNode;if(!p||SK[p.nodeName]||(p.closest&&p.closest('svg,[contenteditable]')))return;RX.lastIndex=0;if(RX.test(n.nodeValue)){RX.lastIndex=0;n.nodeValue=n.nodeValue.replace(RX,'$1​(')}});RX.lastIndex=0}catch(e){}
 try{[].forEach.call(QA.call(f,'p,li,td,dd,blockquote,div,span.sub'),function(el){for(var j=0;j<el.children.length;j++)if(BLK[el.children[j].tagName])return;var t=el.textContent||'',m=t.match(/[①②③④⑤⑥⑦⑧⑨⑩]/g);if(!m||m.length<2||t.length<30||el.closest(SKS))return;
  var tw=document.createTreeWalker(el,4),ns=[],seen=false;while(tw.nextNode())ns.push(tw.currentNode);
  ns.forEach(function(n){var s=n.textContent;if(n.parentElement&&n.parentElement.closest(SKS)){if(s.trim())seen=true;return}var parts=s.split(SPL);if(!parts.some(function(q,i){return NUM.test(q.charAt(0))&&(seen||i>0)})){if(s.trim())seen=true;return}
   var prev=n.previousSibling,g=document.createDocumentFragment();parts.forEach(function(q,i){if(NUM.test(q.charAt(0))&&(seen||i>0)){if(!(i===0&&prev&&prev.nodeName==='BR'))g.appendChild(document.createElement('br'));q=q.replace(/^\s+/,'')}else if(i<parts.length-1)q=q.replace(/\s+$/,'');if(q)g.appendChild(document.createTextNode(q));if(q.trim())seen=true});n.parentNode.replaceChild(g,n)})})}catch(e){}}
function fill(a){if(!a.__lz||a.classList.contains('fold'))return;var f=a.__lz;a.__lz=null;delete a.querySelectorAll;delete a.querySelector;a.appendChild(f);try{if(window.drawViz)drawViz()}catch(e){}prep(a)}
window.__lzHollow=function(){try{if(!mo)mo=new MO(function(ms){ms.forEach(function(m){fill(m.target)})});
 document.querySelectorAll('article[data-date].fold').forEach(function(a){if(a.__lz)return;var k=[].slice.call(a.children),i=0;while(i<k.length&&k[i].matches('.sumrow,.tag,h3'))i++;if(i>=k.length)return;
  var f=document.createDocumentFragment();k.slice(i).forEach(function(c){f.appendChild(c)});a.__lz=f;
  a.querySelectorAll=function(s){var r=[].slice.call(QA.call(this,s));if(this.__lz)r=r.concat([].slice.call(this.__lz.querySelectorAll(s)));return r};
  a.querySelector=function(s){return Q1.call(this,s)||(this.__lz?this.__lz.querySelector(s):null)};
  mo.observe(a,{attributes:true,attributeFilter:['class']})})}catch(e){}};})();</script>"""
def tidy_easy(s, name):
    if name == 'p-econ.html':  # 알림 바로가기(evgo.js)가 이번 주 카드의 발표 줄을 찾게 줄마다 발표 id
        s = s.replace("const li=el('div','mc-ev'+(r.stars===3?' p3':''));\n", "const li=el('div','mc-ev'+(r.stars===3?' p3':''));li.dataset.key=r.id;\n", 1)
        # 아직 안 나온 발표의 예상치는 다른 색 + '예상치'라고(사용자 2026-11-04) — 이번 주 카드·전체 일정표
        s = s.replace("ex.appendChild(document.createTextNode('예상 '));ex.appendChild(mk(el('span',null,fv(r.consensus,r.unit)),'calendar','consensus','id='+enc(r.id)));",
                      "if(r.actual==null&&r.consensus!=null){const cb=el('span','evc');cb.appendChild(document.createTextNode('예상치 '));cb.appendChild(mk(el('b',null,fv(r.consensus,r.unit)),'calendar','consensus','id='+enc(r.id)));ex.appendChild(cb)}else{ex.appendChild(document.createTextNode('예상 '));ex.appendChild(mk(el('span',null,fv(r.consensus,r.unit)),'calendar','consensus','id='+enc(r.id)))}", 1)
        s = s.replace("num('consensus');num('previous');", "{const cc=num('consensus');if(r.actual==null&&r.consensus!=null)cc.classList.add('evc')}num('previous');", 1)
    if name == 'p-earn.html':
        s = s.replace('drawViz();linkTickers();initFind(open);', 'linkTickers();initFind(open);(window.__lzHollow||Object)();drawViz();', 1)
        s = re.sub(r'<script data-earnlz>.*?</script>', '', s, flags=re.S)
        s = re.sub(r'(<script[^>]*>)', lambda m: EARNLZ_JS + m.group(1), s, count=1)
    if name == 'p-brief.html':  # 가볍게(사용자 2026-11-04): 처음엔 최근 7일만 그리고 '지난 날 더 보기'로 14일씩(찾기·분위기 거르기·차트에서 고른 날은 그대로 다 보임)
        s = s.replace("  const rows=ALL.filter(hit).slice().reverse();\n",
                      "  const rows0=ALL.filter(hit).slice().reverse(),LIM=(st.q||st.mood)?1e9:(st.lim||7),oi=rows0.findIndex(r=>r.date===st.open),rows=rows0.slice(0,Math.max(LIM,oi+1)),LEFT=rows0.length-rows.length;\n", 1)
        s = s.replace("    box.appendChild(card);\n  });\n}\ndash.onData(draw);",
                      "    box.appendChild(card);\n  });\n  if(LEFT>0){const mw=document.createElement('div');mw.className='bf-moreday';const mb=document.createElement('button');mb.type='button';mb.textContent='▾ 지난 날 더 보기 · 남은 '+LEFT+'일';mb.onclick=()=>{const y=scrollY;st.lim=(st.lim||7)+14;drawDays();scrollTo(0,y)};mw.appendChild(mb);box.appendChild(mw)}\n}\ndash.onData(draw);", 1)
        if '.bf-moreday{' not in s:
            s = s.replace('</head>', '<style data-moreday>body #days .bf-moreday{display:flex;justify-content:center;margin:14px 0 22px}body #days .bf-moreday button{font:800 15px/1 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#7a5200;background:#fffaf0;border:1px solid #e3cf9f;border-radius:999px;padding:13px 20px;box-shadow:0 2px 0 #ecd6a6;cursor:pointer;-webkit-tap-highlight-color:transparent}body #days .bf-moreday button:active{transform:translateY(1px);box-shadow:none}</style></head>', 1)
    if name == 'p-brief.html':  # 속도(2026-11-03): 시황 그림은 화면에 들어올 때 그림(보이지 않는 지난 날짜 차트까지 열 때 다 그리던 것)
        s = s.replace('requestAnimationFrame(()=>drawCD(cv,cd))', '(window.__lazyCD||requestAnimationFrame)(()=>drawCD(cv,cd),cv)')
        if 'window.__lazyCD=' not in s:
            s = re.sub(r'(<script[^>]*>)', lambda m: '<script data-lazycd>window.__lazyCD=function(f,el){if(!el||!window.IntersectionObserver)return requestAnimationFrame(f);var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){o.disconnect();requestAnimationFrame(f)}})},{rootMargin:"600px 0px"});o.observe(el)};</script>' + m.group(1), s, count=1)
    if name == 'p-targets.html':  # 가볍게(사용자 2026-11-04): '목표가 vs 현재가' 78줄·'평균 목표가 추세' 표 78줄(작은 추세선 포함)도 화면 가까이 올 때 그림
        s = s.replace("    drawVs();\n    fillTake();", "    (window.__lazyRun||((k,f)=>f()))('vs',drawVs,document.getElementById('vsprice'));\n    fillTake();", 1)
        s = s.replace("    drawTrend();\n    drawPicker();", "    (window.__lazyRun||((k,f)=>f()))('trend',drawTrend,document.getElementById('trend-card'));\n    drawPicker();", 1)
    if name == 'p-targets.html':  # 속도(2026-11-03): 아래쪽 차트(종목 선 그래프·월별·업종 열지도·업종 표)는 화면 가까이 올 때 그림
        for a, b in [("    drawHeat();\n    drawCat();", "    (window.__lazyRun||((k,f)=>f()))('heat',drawHeat,document.getElementById('heat-card'));\n    (window.__lazyRun||((k,f)=>f()))('cat',drawCat,document.getElementById('cat-card'));"),
                     ("    drawPicker();\n    redrawTk();\n  });", "    drawPicker();\n    (window.__lazyRun||((k,f)=>f()))('tk',redrawTk,document.getElementById('lines-card'));\n  });")]:
            if a in s: s = s.replace(a, b, 1)
        s = re.sub(r'<script data-lazyrun>.*?</script>', '', s, flags=re.S)
        if True:
            s = re.sub(r'(<script[^>]*>)', lambda m: LAZYRUN_JS + m.group(1), s, count=1)
    for mk in EASY.get(name) or []:
        s = _easy_one(s, mk)
    return s
def _easy_one(s, mk):
    add = core_ref(mk, mk + '.css') + core_ref(mk, mk + '.js')
    if add in s:  # 이미 최신 참조가 있으면 자리를 옮기지 않음(다시 입힐 때마다 바뀌지 않게)
        return s
    s = core_strip(s, mk)
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add


# 시세 보드 기간 1일·1주일 추가 + 왼쪽부터 짧은 순(사용자 2026-11-03) — 원본(통합본 동기화로 덮임) 위에 멱등 치환
# 1주일 = history의 일별 종가 중 기준일 이전 5번째 거래일 종가. history를 계산 입력에 넣지 않고(보드가 history를 기다리지 않게) 계산 안에서 읽음
PPER_MARK = '/*mm-per1w2*/'
PPER_REP = [
    ("<button type=\"button\" class=\"pb-chip\" data-p=\"12m\">12개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"6m\">6개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"3m\">3개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"1m\">1개월</button>",
     "<button type=\"button\" class=\"pb-chip\" data-p=\"1d\">1일</button><button type=\"button\" class=\"pb-chip\" data-p=\"1w\">1주일</button><button type=\"button\" class=\"pb-chip\" data-p=\"1m\">1개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"3m\">3개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"6m\">6개월</button><button type=\"button\" class=\"pb-chip\" data-p=\"12m\">12개월</button>"),
    ("<button type=\"button\" class=\"pb-chip\" data-p=\"1d\">1일</button><button type=\"button\" class=\"pb-chip\" data-p=\"1m\">1개월</button>",
     "<button type=\"button\" class=\"pb-chip\" data-p=\"1d\">1일</button><button type=\"button\" class=\"pb-chip\" data-p=\"1w\">1주일</button><button type=\"button\" class=\"pb-chip\" data-p=\"1m\">1개월</button>"),
    ("const PER = { '1m': ['1개월', '지난 1개월', '한 달 전'],",
     "const PER = { '1d': ['1일', '오늘', '전날'], '1w': ['1주일', '지난 1주일', '1주일 전'], '1m': ['1개월', '지난 1개월', '한 달 전'],"),
    ("const HPL = { '1d': '1일', '1m': '1개월',", "const HPL = { '1d': '1일', '1w': '1주일', '1m': '1개월',"),
    ("({ '1m': 20, '3m': 35, '6m': 50, '12m': 80 }[P] || 25)", "({ '1d': 4, '1w': 10, '1m': 20, '3m': 35, '6m': 50, '12m': 80 }[P] || 25)"),
    ("      return prices.map((r) => {\n        const p = n(r.price);",
     "      " + PPER_MARK + "window.__mmOff = prices.filter((r) => /day|pre|after/.test(r.price_kind || '')).length > prices.length / 2; const W1 = (function () { try { const H = dash.data('history'); if (!H || H.status !== 'ok') return {}; if (window.__mmW1 && window.__mmW1.ref === H.data && window.__mmW1.n === prices.length) return window.__mmW1.m; const by = {}; H.data.forEach((x) => { if (x.kind === 'm') return; (by[x.ticker] = by[x.ticker] || []).push(x); }); const m = {}; prices.forEach((r) => { const a = (by[r.ticker] || []).filter((x) => x.date <= (r.prev_date || r.price_date) && (r.prev_date || x.date < r.price_date)).sort((p, q) => (p.date < q.date ? -1 : 1)); if (a.length >= 5) m[r.ticker] = Number(a[a.length - 5].close); }); window.__mmW1 = { ref: H.data, n: prices.length, m: m }; return m; } catch (e) { return {}; } })();\n      window.__mmOff = prices.filter((r) => /day|pre|after/.test(r.price_kind || '')).length > prices.length / 2;\n      return prices.map((r) => {\n        const p = n(r.price);"),
    ("          chg_1d: pct(p, n(r.prev_close)),\n", "          chg_1d: pct(p, n(r.prev_close)),\n          chg_1w: pct(p, W1[r.ticker]),\n"),
    ("const pick = (k) => rs.map((r) => r[k]).filter((x) => x != null);", "const LEV = ['SOXL', 'SOXS', 'TQQQ', 'SQQQ', 'TECL', 'UPRO', 'SPXL', 'NVDL', 'TSLL']; const pick = (k) => rs.filter((r) => LEV.indexOf(r.ticker) < 0 || rs.every((q) => LEV.indexOf(q.ticker) >= 0)).map((r) => r[k]).filter((x) => x != null);"),
    ("m12 = pick('chg_12m'), d1 = pick('chg_1d');", "m12 = pick('chg_12m'), d1 = pick('chg_1d'), w1 = pick('chg_1w');"),
    ("c.textContent = HP === '1d' ? `${r.n_1d}종목` : `오늘 ${fmtPct(r.avg_1d)}`;", "c.textContent = HP === '1d' ? `${r.n_1d}종목` : `${window.__mmOff ? '장외' : '오늘'} ${fmtPct(r.avg_1d)}`;"),
    ("n_1d: d1.length, avg_1d: avg(d1),", "n_1d: d1.length, avg_1d: avg(d1), n_1w: w1.length, avg_1w: avg(w1),"),
    ("if (/^(best|worst)_\\d+m$/.test(k))", "if (/^(best|worst)_\\d+[mdw]$/.test(k))"),
    (".pb-per{display:flex;flex-wrap:wrap;align-items:center;gap:6px}", ".pb-per{display:flex;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;align-items:center;gap:6px;padding-bottom:4px}.pb-per::-webkit-scrollbar{display:none}.pb-per .pb-chip,.pb-per .lab{flex:none}"),
    ("      ['1m', '3m', '6m', '12m'].forEach((k) => {\n        const v = board_calc.map((r) => r['chg_' + k])",
     "      ['1d', '1w', '1m', '3m', '6m', '12m'].forEach((k) => {\n        const v = board_calc.map((r) => r['chg_' + k])"),
]
def tidy_prices_per(s):
    if 'id="period"' not in s or 'board_calc' not in s:
        return s
    if PPER_MARK not in s:
        for a, b in PPER_REP:
            if a in s:
                s = s.replace(a, b, 1)
    # '강세' 칸이 마이너스면 '가장 덜 빠진', '약세' 칸이 플러스면 '가장 덜 오른' — _tools/pper.js
    s = core_strip(s, 'pper')
    add = core_ref('pper', 'pper.js')
    return s.replace('</body>', add + '</body>', 1) if '</body>' in s else s + add
