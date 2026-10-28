// '읽는 법'은 모든 페이지에서 공매도 '이렇게 읽습니다' 상자 모양으로 통일(사용자 2026-10-29)
(function(){function mk(p){if(p.dataset.rd||p.closest('details')||p.closest('.u-fold')||p.closest('.o-fold'))return;p.dataset.rd=1;
 var b0=p.firstElementChild;if(b0&&/^읽는 법/.test(b0.textContent.trim())&&p.firstChild===b0)b0.remove();p.innerHTML=p.innerHTML.replace(/^\s*읽는 법\s*[:·—-]?\s*/,'');
 var old=p.nextElementSibling;if(old&&/(u-more|o-more)/.test(old.className))old.remove();p.classList.remove('u-clamp','o-clamp','op');
 var b=document.createElement('button');b.type='button';b.className='rd-btn';b.innerHTML='이렇게 읽습니다 <span>눌러서 펼치기</span>';p.parentNode.insertBefore(b,p);p.classList.add('rd-body');
 b.onclick=function(){var o=!b.classList.contains('op');b.classList.toggle('op',o);p.classList.toggle('op',o);b.querySelector('span').textContent=o?'접기':'눌러서 펼치기'}}
function fx(){document.querySelectorAll('p.how,p[class$="-how"],.ot-card .how,p.sp-how').forEach(mk);
 document.querySelectorAll('p,div.note').forEach(function(p){if(p.dataset.rd||p.children.length>12)return;var t=p.textContent.trim();if(/^읽는 법\s*[:·—]/.test(t)||(p.firstElementChild&&p.firstElementChild.tagName==='B'&&p.firstElementChild.textContent.trim()==='읽는 법'&&p.firstChild===p.firstElementChild))mk(p)})}
var k=0;(function go(){try{fx()}catch(e){}if(++k<16)setTimeout(go,500)})();
try{var mo=new MutationObserver(function(){try{fx()}catch(e){}});mo.observe(document.body,{childList:true,subtree:true});setTimeout(function(){mo.disconnect()},20000)}catch(e){}})();
