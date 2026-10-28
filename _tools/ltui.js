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

// 경고등 '~란?' 설명(누르면 펼침)·영역 링크 문구(사용자 2026-10-29)
var LX=[[/유가/,'유가 급등이란?','유가가 짧은 기간에 크게 오르는 것입니다. 물가와 금리를 함께 밀어 올려 주식에 부담이 됩니다.'],
[/장단기/,'장단기 금리 역전이란?','짧은 만기(2년) 국채 금리가 긴 만기(10년)보다 높아지는 것입니다. 시장이 경기 둔화를 예상할 때 나타납니다.'],
[/10년물 5%/,'10년물 5%가 왜 중요?','장기 금리가 5%를 넘으면 미래 이익의 현재 가치가 낮아져 성장주·중소형주에 특히 부담이 큽니다.'],
[/30년물/,'30년물 금리란?','30년 만기 국채 금리입니다. 높을수록 정부 빚과 물가에 대한 걱정이 크다는 뜻입니다.'],
[/2주 급등/,'금리 급등이 왜 위험?','금리가 짧은 기간에 급하게 오르면 시장이 적응할 시간이 없어 주가가 흔들리기 쉽습니다.'],
[/입찰/,'국채 입찰 부진이란?','정부가 국채를 팔 때 사려는 수요가 약한 것입니다. 금리를 더 올려야 팔린다는 신호라 금리 상승 압력이 됩니다.'],
[/하이일드/,'하이일드 스프레드란?','신용이 낮은 회사채가 국채보다 더 얹어 주는 이자입니다. 벌어지면 돈 빌리기가 어려워지고 부도 걱정이 커졌다는 뜻입니다.'],
[/VIX/,'VIX란?','앞으로 한 달 S&P 500이 얼마나 출렁일지 옵션 가격으로 계산한 공포 지수입니다. 20을 넘으면 불안이 커진 구간으로 봅니다.'],
[/기간구조/,'기간구조 뒤집힘이란?','단기 VIX가 3개월 VIX보다 높아지는 것입니다. 먼 미래보다 지금 당장의 불안이 더 크다는 뜻입니다.'],
[/풋콜/,'풋콜 비율이란?','하락에 거는 풋옵션이 상승에 거는 콜옵션보다 얼마나 많이 거래되는지입니다. 높을수록 겁이 많다는 뜻입니다.']];
function lx(){var A=document.getElementById('areas');if(!A)return;A.querySelectorAll('li[data-lt]:not([data-lx])').forEach(function(li){var nm=(li.querySelector('b')||{}).textContent||'';var hit=LX.find(function(x){return x[0].test(nm)});if(!hit)return;li.dataset.lx=1;
 var q=document.createElement('span');q.className='l-q';q.textContent=hit[1];li.appendChild(q);var d=document.createElement('span');d.className='l-ex';d.textContent=hit[2];li.appendChild(d);li.addEventListener('click',function(){li.classList.toggle('lxo')})});
 var AD={'유가':'기름값이 급하게 오르면 물가와 금리를 자극해 주식에 부담이 됩니다.','채권·금리':'금리가 높거나 빨리 오르면 주식, 특히 성장주·중소형주에 부담입니다.','신용':'회사들이 돈을 빌리기 어려워지는지, 부도 걱정이 커지는지 봅니다.','옵션·공포':'투자자들이 얼마나 겁먹었는지 옵션 시장 가격으로 봅니다.'};
 A.querySelectorAll('.area:not([data-ad])').forEach(function(ar){var h=ar.querySelector('.hd');var t=(h&&h.querySelector('b')||{}).textContent||'';if(!h||!AD[t])return;ar.dataset.ad=1;var p=document.createElement('p');p.className='a-desc';p.textContent=AD[t];h.after(p)});
 A.querySelectorAll('.area>a:not([data-lx])').forEach(function(a){a.dataset.lx=1;var h=(a.closest('.area').querySelector('.hd b')||{}).textContent||'';a.textContent=h+' 차트로 보기 →'})}
var k2=0;(function g2(){try{lx()}catch(e){}if(++k2<14)setTimeout(g2,400)})();
if(window.MutationObserver){var r2=document.querySelector('.lw');if(r2)new MutationObserver(function(){try{lx()}catch(e){}}).observe(r2,{childList:true,subtree:true})}

// 지금 값이 기준에 얼마나 가까운지 5단계 색(사용자 2026-10-29): 1 안전 … 5 켜짐
var LV=['','안전','양호','보통','근접','위험'];
function lv(){document.querySelectorAll('#areas li[data-lt]:not([data-lv])').forEach(function(li){var nw=li.querySelector('.l-now'),th=li.querySelector('.l-th');if(!nw||!th)return;
 var n=parseFloat(nw.textContent.replace(/[^\d.\-−]/g,'').replace('−','-')),t=parseFloat(th.textContent.replace(/[^\d.\-−]/g,'').replace('−','-'));if(isNaN(n)||isNaN(t))return;
 var lt=/</.test(th.textContent),x;if(lt){x=t===0?1-(n/0.5):(t/n)}else{x=t>0?n/t:0}var on=lt?n<t:n>=t;
 var k=on?5:x>=0.9?4:x>=0.8?3:x>=0.6?2:1;li.dataset.lv=k;var m=document.createElement('span');m.className='l-lv';m.innerHTML='<i></i><i></i><i></i><i></i><i></i><em>'+LV[k]+'</em>';th.after(m)});
 document.querySelectorAll('#areas .area:not([data-lvk])').forEach(function(a){if(!a.querySelector('li[data-lv]'))return;a.dataset.lvk=1})}
var k3=0;(function g3(){try{lv()}catch(e){}if(++k3<14)setTimeout(g3,400)})();
if(window.MutationObserver){var r3=document.querySelector('.lw');if(r3)new MutationObserver(function(){try{lv()}catch(e){}}).observe(r3,{childList:true,subtree:true})}

// 오늘 한눈에(경고등) 정리: 단계 크게 → 달라진 것 · 흐름 · 참고 3줄(사용자 2026-10-29)
function tk(){var box=document.querySelector('.lw-take');if(!box)return;var t1=box.querySelector('.tk1'),t2=box.querySelector('.tk2'),cg=document.getElementById('today-chg'),as=document.getElementById('asof');if(!t2||!cg)return;
 var sig=(t1?t1.textContent:'')+'|'+t2.textContent+'|'+cg.textContent;if(box.dataset.sig===sig)return;
 var s2=t2.textContent,c=cg.textContent.replace(/\s+/g,' ');var on=(s2.match(/(\d+)\s*\/\s*(\d+)/)||[]);var st=(s2.match(/·\s*(\S+)\s*단계/)||[])[1]||'';
 var em=(c.match(/^(\S+)/)||[''])[0];var why=(c.match(/단계\(([^)]+)\)/)||[])[1]||'';var mv=(c.match(/불\s*(\d+)\s*→\s*(\d+)개/)||[]);var chg=(c.match(/(꺼짐|켜짐):\s*([^.]+)\./)||[]);
 var ref=(c.match(/지난 1년([^.]+)\./)||[])[1]||'';var tr=t1?t1.textContent.replace(/\s+/g,' ').trim():'';var dir=(tr.match(/^[↘↗→]\s*\S+\s*\S+\s*\S+/)||[tr])[0];var avg=(tr.match(/([\d.]+)개\s*→\s*([\d.]+)개/)||[]);
 if(!on[1]||!st){return}
 box.dataset.sig=sig;var w=box.querySelector('.tk-new');if(!w){w=document.createElement('div');w.className='tk-new';box.appendChild(w)}
 var col=getComputedStyle(cg).borderLeftColor||'';
 w.innerHTML='<div class="tk-top"><span class="tk-st" style="--tc:'+col+'">'+em+' '+st+'</span><span class="tk-n">불 <em class="tk-b">'+on[1]+'</em> / '+on[2]+'</span></div>'+(why?'<p class="tk-why">'+why.replace(/에서 내려옴/,'에서 한 단계 내려왔습니다').replace(/에서 올라옴/,'에서 한 단계 올라갔습니다')+'</p>':'')+
 '<ul class="tk-rows">'+(chg[1]?'<li><i>달라진 것</i><span>'+chg[2]+' <em class="tk-s '+(chg[1]==='꺼짐'?'off':'on')+'">'+chg[1]+'</em>'+(mv[1]?' ('+mv[1]+' → '+mv[2]+'개)':'')+'</span></li>':'')+
 (tr?'<li><i>흐름</i><span>'+dir.replace(/불\s*/,'')+(avg[1]?' · 평균 '+avg[1]+' → '+avg[2]+'개':'')+'</span></li>':'')+
 (ref?'<li><i>참고</i><span>'+ref.trim().replace(/^불이 줄어든 날 뒤 1달은/,'불이 줄어든 날 뒤 1달, 나스닥100')+'</span></li>':'')+'</ul>';
 box.classList.add('tk-on')}
var k4=0;(function g4(){try{tk()}catch(e){}if(++k4<14)setTimeout(g4,400)})();
if(window.MutationObserver){var r4=document.querySelector('.lw-take');if(r4)new MutationObserver(function(){try{tk()}catch(e){}}).observe(r4,{childList:true,subtree:true,characterData:true})}
