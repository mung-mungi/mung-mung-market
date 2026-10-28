// 시장 경고등: 시세 보드 양식(사용자 2026-10-29) — 영역별 한 줄 카드, 관점 접기, 긴 해설 3줄, 성적표 카드
(function(){function fx(){var A=document.getElementById('areas');if(A)
// 영역별: 한 줄 카드로 (이름 | 지금 | 기준)
A.querySelectorAll('li:not([data-lt])').forEach(function(li){var b=li.querySelector('b'),s=li.querySelector('small');var nm=b?b.textContent:'',tx=s?s.textContent:'';if(!b){var q=li.textContent.split(/\s+[—-]\s+/);nm=q[0];tx=q.slice(1).join(' ')}var m=tx.match(/지금\s*(.+?)\s*\(기준\s*(.+?)\)/);if(!nm||!m)return;li.dataset.lt=1;var on=li.dataset.t!=='1'&&!/(^|\s)off/.test(li.className);
 if(/(^|\s)on(\s|$)/.test(li.className)||li.dataset.on==='1')li.classList.add('l-on');li.innerHTML='<span class="l-dot"></span><b>'+nm+'</b><span class="l-now">'+m[1]+'</span><span class="l-th">기준 '+m[2]+'</span>'});
// 관점(MY READ): 제목만, 나머지 접기
var v=document.getElementById('view');if(v&&!v.dataset.lt){v.dataset.lt=1;var body=[...v.children].filter(function(c){return c.tagName!=='H3'&&!c.classList.contains('vk')});var bt=document.createElement('button');bt.type='button';bt.className='l-more';bt.textContent='관점 자세히 ▾';body.forEach(function(c){c.classList.add('l-x')});v.appendChild(bt);bt.onclick=function(){v.classList.toggle('op');bt.textContent=v.classList.contains('op')?'접기 ▴':'관점 자세히 ▾'}}
// 긴 해설: 3줄 + 더 읽기
['chg-one','amp-one','hist-one'].forEach(function(id){var p=document.getElementById(id);if(!p||p.dataset.lt)return;p.dataset.lt=1;p.classList.add('l-clamp');var bt=document.createElement('button');bt.type='button';bt.className='l-more';bt.textContent='더 읽기 ▾';p.after(bt);bt.onclick=function(){p.classList.toggle('op');bt.textContent=p.classList.contains('op')?'접기 ▴':'더 읽기 ▾'}});
// 성적표: 행 카드
var sc=document.getElementById('score');if(sc){sc.querySelectorAll('.r:not(.h):not([data-lt])').forEach(function(r){var c=[...r.children];if(c.length<5)return;r.dataset.lt=1;var lv=c[0].textContent.split('·');var dd=c[4].textContent.split(/\s*최악\s*/);
 r.innerHTML='<span class="s-lv">'+lv[0].trim()+'<small>'+(lv[1]||'').trim()+'</small></span><span class="s-m '+c[2].className+'">'+c[2].textContent+'<small>1달 뒤 평균</small></span><span class="s-p">'+c[3].textContent+'<small>오른 비율</small></span><span class="s-d">'+dd[0].trim()+'<small>최악 '+(dd[1]||'').trim()+' · '+c[1].textContent+'일</small></span>'})}
// 오늘 한눈에 문단 2줄
var tc=document.getElementById('today-chg');if(tc)tc.classList.add('l-clamp2');
}
var k=0;(function go(){try{fx()}catch(e){}if(!document.__ltmo){var r=document.querySelector('.lw');if(r){document.__ltmo=1;new MutationObserver(function(){try{fx()}catch(e){}}).observe(r,{childList:true,subtree:true})}}if(++k<12)setTimeout(go,400)})()})();
