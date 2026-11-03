// 시세 보드 '지난 n 강세·약세' 이름표를 숫자 방향에 맞춤(사용자 2026-11-03): 강세 칸이 마이너스면 '가장 덜 빠진 분야', 약세 칸이 플러스면 '가장 덜 오른 분야'
(function(){
function fix(){var t=document.getElementById('take-line');if(!t)return;t.querySelectorAll('.two>div').forEach(function(d,i){var sm=d.querySelector('small'),v=d.querySelector('.sv');if(!sm||!v)return;var w=sm.querySelector('.per-word');var x=parseFloat(v.textContent.replace('−','-').replace('+',''));if(isNaN(x))return;
 var lab=i===0?(x<0?' 가장 덜 빠진 분야':' 강세'):(x>0?' 가장 덜 오른 분야':' 약세');var tn=w?w.nextSibling:null;if(tn&&tn.nodeType===3){if(tn.nodeValue!==lab)tn.nodeValue=lab}})}
var k=0;(function go(){try{fix()}catch(e){}if(++k<40)setTimeout(go,500)})();
var t0=null;new MutationObserver(function(){clearTimeout(t0);t0=setTimeout(function(){try{fix()}catch(e){}},60)}).observe(document.documentElement,{childList:true,subtree:true,characterData:true});
})();
