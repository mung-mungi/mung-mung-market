// 시세 보드 '지난 n 강세·약세' 이름표를 숫자 방향에 맞춤(사용자 2026-11-03): 강세 칸이 마이너스면 '가장 덜 빠진 분야', 약세 칸이 플러스면 '가장 덜 오른 분야'
(function(){
function off(){var on=!!window.__mmOff;var k=document.querySelector('#tiles .pb-tile[data-tile="d1"] .k');if(k){var w=on?'1일 중앙값 · 장외':'1일 중앙값';if(k.textContent!==w)k.textContent=w}
 var hd=document.querySelector('#take-line .hd');if(hd){var c=hd.querySelector('.mm-off');if(on&&!c){c=document.createElement('span');c.className='mm-off';c.textContent='장외';c.title='미국 정규장 밖(데이장·프리마켓·애프터) 가격입니다. 전날 정규장 종가와 비교합니다.';c.style.cssText='display:inline-block;margin-left:6px;vertical-align:middle;font:800 12px/1.6 -apple-system,sans-serif;color:#2f5fa8;background:#e8f0fb;border:1px solid #c5d6f0;border-radius:999px;padding:0 8px';hd.appendChild(c)}else if(!on&&c)c.remove()}}
function fix(){var t=document.getElementById('take-line');if(!t)return;try{off()}catch(e){}t.querySelectorAll('.two>div').forEach(function(d,i){var sm=d.querySelector('small'),v=d.querySelector('.sv');if(!sm||!v)return;var w=sm.querySelector('.per-word');var x=parseFloat(v.textContent.replace('−','-').replace('+',''));if(isNaN(x))return;
 var lab=i===0?(x<0?' 가장 덜 빠진 분야':' 강세'):(x>0?' 가장 덜 오른 분야':' 약세');var tn=w?w.nextSibling:null;if(tn&&tn.nodeType===3){if(tn.nodeValue!==lab)tn.nodeValue=lab}})}
var k=0;(function go(){try{fix()}catch(e){}if(++k<40)setTimeout(go,500)})();
var t0=null;new MutationObserver(function(){clearTimeout(t0);t0=setTimeout(function(){try{fix()}catch(e){}},60)}).observe(document.documentElement,{childList:true,subtree:true,characterData:true});
})();
