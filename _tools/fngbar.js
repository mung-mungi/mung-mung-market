// 시황 '공포·탐욕 지수' 막대를 시장 경고등 '공포 ↔ 환희' 막대와 같은 보는 법으로(사용자 2026-11-02)
// 왼쪽 파랑 = 겁먹음 · 오른쪽 주황 = 들뜸, 눈금 25 극단 공포 · 50 중립(진한 눈금) · 75 극단 탐욕. 숫자 색도 같은 규칙.
(function(){try{
if(!/p-brief\.html/.test(location.pathname))return;
function emo(p){return p<25?'#1f4e9a':p<45?'#2f5fa8':p<55?'#8a857a':p<75?'#e8913a':'#d0451b'}
function fix(){var box=document.getElementById('mood');if(!box)return;var mb=box.querySelector('.mb'),ml=box.querySelector('.ml'),mv=box.querySelector('.mv');if(!mb||!ml)return;
 if(mb.classList.contains('mm-fg')&&mb.querySelector('.mm-fg-t'))return;
 mb.classList.add('mm-fg');ml.classList.add('mm-fg');var em=mb.querySelector('em');var v=em?parseFloat(em.style.left):NaN;
 [[25,''],[50,'avg'],[75,'']].forEach(function(t){var e=document.createElement('i');e.className='mm-fg-t '+t[1];e.style.left=t[0]+'%';mb.appendChild(e)});
 ml.textContent='';[[25,'극단 공포',''],[50,'중립','avg'],[75,'극단 탐욕','']].forEach(function(t){var s=document.createElement('span');s.className=t[2];s.style.left=t[0]+'%';s.textContent=t[1];ml.appendChild(s)});
 if(!box.querySelector('.mm-fg-cap')){var c=document.createElement('p');c.className='mm-fg-cap';c.textContent='왼쪽(파랑) = 겁먹음 · 오른쪽(주황) = 들뜸 · 경고등 페이지와 같은 방향';ml.after(c)}
 if(!isNaN(v)){var col=emo(v);if(em)em.style.borderColor=col;if(mv)mv.style.color=col}}
var k=0;(function t(){fix();if(++k<20)setTimeout(t,500)})();
var m=document.getElementById('mood');if(m&&window.MutationObserver)new MutationObserver(function(){setTimeout(fix,30)}).observe(m,{childList:true});
}catch(e){}})();
