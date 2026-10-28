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
