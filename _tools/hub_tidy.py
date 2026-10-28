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
