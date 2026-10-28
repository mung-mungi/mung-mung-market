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
PAPER = r'''<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&family=UnifrakturMaguntia&display=swap"><style data-paper>
#take.np{display:block!important;padding:14px 16px 16px!important;background:#fbf8f1!important;border:1px solid #d9d0bd!important;border-radius:6px!important;box-shadow:0 2px 0 rgba(60,45,20,.08),0 8px 18px rgba(60,45,20,.08)!important;color:#1d1a15!important}
#take.np::before{content:none!important;display:none!important}
#take.np .np-mast{text-align:center;font-family:"UnifrakturMaguntia","Old English Text MT",ui-serif,Georgia,serif;font-weight:400;font-size:32px;letter-spacing:.01em;line-height:1.1;padding:2px 0 6px;border-bottom:3px double #1d1a15}
#take.np .np-mast small{display:block;font:700 10.5px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;letter-spacing:.32em;color:#7a6a4c;margin-bottom:3px}
#take.np .np-line{display:flex;justify-content:space-between;gap:8px;font:600 11.5px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#5d5240;padding:5px 0;border-bottom:1px solid #1d1a15;margin-bottom:12px}
#take.np .np-hd{font-family:"Noto Serif KR",ui-serif,Georgia,serif;font-weight:900;font-size:22px;line-height:1.35;letter-spacing:-.02em;margin:0 0 10px;text-wrap:balance}
#take.np .np-body{font-family:"Noto Serif KR",ui-serif,Georgia,serif;font-weight:500;font-size:15.5px;line-height:1.75;text-align:left;word-break:keep-all;margin:0;padding-top:10px;border-top:1px solid #d9d0bd}
#take.np .np-body::first-letter{float:left;font-weight:900;font-size:44px;line-height:.9;padding:5px 7px 0 0;color:#8a1c1c}
#take.np .np-body b,#take.np .np-body strong{font-weight:700;background:linear-gradient(transparent 62%,rgba(214,170,60,.35) 0)}
#take.np .np-more{display:block;width:100%;margin:10px 0 0;padding:7px 0 0;border:0;border-top:1px solid #1d1a15;background:none;font:700 13px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#8a1c1c;text-align:right;cursor:pointer;letter-spacing:.02em}
#take.np .np-hd{margin-bottom:0}#take.np .np-body:not([hidden])+.np-more{margin-top:10px}
#take.np .np-body{margin-top:10px!important}
#take.np .np-foot{margin-top:10px;padding-top:6px;border-top:1px solid #1d1a15;font:600 11px/1.4 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#7a6a4c;text-align:right;letter-spacing:.04em}
</style><script data-paper>(function(){var k=0;function go(){var t=document.getElementById('take');if(!t||t.classList.contains('np'))return;var dl=t.querySelector('.bf-dl'),bd=t.querySelector('[data-field=comment]');
if(!bd||!bd.textContent.trim()){if(++k<40)setTimeout(go,250);return}
var a=dl?(dl.querySelector('b')||{}).textContent||'':'',u=dl?(dl.querySelector('.bf-us')||{}).textContent||'':'';a=a.replace(/\s*\([^)]*\)/,'');
var h=bd.innerHTML,i=h.search(/다\.(\s|$)/),hd,rest;if(i>0){hd=h.slice(0,i+2);rest=h.slice(i+2).trim()}else{hd=h;rest=''}
var tmp=document.createElement('div');tmp.innerHTML=hd;hd=tmp.textContent.replace(/\.$/,'');
t.classList.add('np');t.innerHTML='<div class="np-mast"><small>AI VALUE CHAIN DAILY</small>The Mungmung Times</div><div class="np-line"><span>'+a+'</span><span>'+u+'</span></div><h2 class="np-hd"></h2>'+(rest?'<p class="np-body" hidden>'+rest+'</p><button type="button" class="np-more">기사 펼치기 ▾</button>':'');t.querySelector('.np-hd').textContent=hd;var mb=t.querySelector('.np-more');if(mb)mb.onclick=function(){var p=t.querySelector('.np-body'),o=p.hidden;p.hidden=!o;mb.textContent=o?'접기 ▴':'기사 펼치기 ▾'}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go()})();</script>'''


def tidy_paper(s):
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
