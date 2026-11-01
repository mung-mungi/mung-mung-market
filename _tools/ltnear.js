// 시장 경고등 '지금 시장은' 통일 양식(사용자 2026-11-01)
// 근접(기준의 90% 이상, ltui의 5단계 색 4 '근접')은 반불(◐)로 보여 주고, 유가는 100달러 이상이면 '높은 자리'로 근접 처리.
// 영역마다 '지금' 한 줄, 맨 위에 '지금 시장은' 총평을 숫자로 자동 생성. 단계 계산(켜진 불)은 그대로.
(function(){var WTI=null,TW={};try{fetch('d/lights/thresholds.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(j){j.forEach(function(t){TW[t.name]=t.why||''});run()}}).catch(function(){})}catch(e){}try{fetch('d/lights/oil.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j.length){WTI=Number(j[j.length-1].wti);run()}}).catch(function(){})}catch(e){}
var C={r:['#b3261e','#fbe8e5'],o:['#a14d00','#fdf0e1'],y:['#8a6a00','#fbf4dc'],g:['#2e7d4f','#e7f3ec']};
function nm(li){return ((li.querySelector('b')||{}).textContent||'').trim()}
function val(li){return ((li.querySelector('.l-now')||{}).textContent||'').trim()}
function st(li){return li.classList.contains('on')||li.dataset.lv==='5'?'on':li.dataset.lv==='4'?'near':'off'}
function short(n){return /10년물 5%/.test(n)?'10년물':/30년물/.test(n)?'30년물':/VIX/.test(n)?'VIX':/기간구조/.test(n)?'기간구조':/풋콜/.test(n)?'풋콜 비율':/하이일드/.test(n)?'하이일드':n.replace(/ 이상$/,'').replace(/ 높음$/,'').replace(/\(최근 5일\)/,'').trim()}
var AN={'반도체·AI':'반도체','옵션·공포':'옵션 시장','채권·금리':'금리','신용':'신용','유가':'유가'};
function nowTxt(area,L,oilNear){var on=L.filter(function(x){return x.s==='on'}),nr=L.filter(function(x){return x.s==='near'});
 if(area==='반도체·AI'){if(on.length>=2)return['r','반도체에 공포가 몰렸습니다. 시장 전체보다 먼저 아픈 곳입니다.'];if(on.length)return['o',short(on[0].n)+' '+on[0].v+' — 반도체가 흔들리고 있습니다.'];if(nr.length)return['y','반도체가 문턱에 다가갔습니다. 다음 급락이 오면 켜집니다.'];return['g','반도체는 아직 조용합니다.']}
 if(area==='유가'){if(on.length)return['r','한 달 새 '+on[0].v+' 급등 — 물가와 금리를 함께 자극합니다.'];if(oilNear)return['o','급등은 아니어도 '+Math.round(WTI)+'달러로 100달러 위에 머물러 물가·금리 부담이 계속됩니다.'];return['g','유가 부담은 크지 않습니다.']}
 if(area==='채권·금리'){if(on.length)return['r',on.map(function(x){return short(x.n)}).join('·')+' 켜짐 — 성장주에 직접 부담입니다.'];if(nr.length)return['o',nr.map(function(x){return short(x.n)+' '+x.v}).join(' · ')+' — 문턱 바로 아래입니다. 한 번만 밀려도 켜집니다.'];return['g','금리 쪽은 조용합니다.']}
 if(area==='신용'){if(on.length)return['r','약한 회사의 돈줄이 조이고 있습니다. 위험이 번지는 신호입니다.'];if(nr.length)return['o','스프레드가 문턱에 다가갔습니다.'];return['y','회사채 전체 평균은 조용합니다. AI 빚 기업·사모신용 쪽 쏠림은 따로 확인합니다.']}
 if(area==='옵션·공포'){var p=[];L.slice().sort(function(a,b){return (a.s==='on'?0:1)-(b.s==='on'?0:1)}).forEach(function(x){if(x.s==='off')return;p.push(/풋콜/.test(x.n)?'하락 보험(풋)을 많이 삽니다':/VIX/.test(x.n)?'VIX '+x.v+(x.s==='on'?'로 20을 넘었습니다':'로 20 문턱입니다'):/기간구조/.test(x.n)?(x.s==='on'?'당장의 불안이 더 큽니다':'단기 불안이 커지는 중입니다'):short(x.n))});if(!p.length)return['g','옵션 시장은 차분합니다.'];return[on.length?'o':'y',p.join(', ')+'.']}
 return null}
function run(){var A=document.getElementById('areas'),big=document.getElementById('big');if(!A||!big)return;var areas=[...A.querySelectorAll('.area')];if(!areas.length)return;
 if(areas.some(function(a){return !a.querySelector('li[data-lt]')||a.querySelector('li[data-lt]:not([data-lv])')})){clearTimeout(run.t);run.t=setTimeout(function(){try{run()}catch(e){}},250);return} // 5단계 색이 다 붙은 뒤(다시 그려지는 중이면 잠시 뒤 재시도)
 var oilNear=WTI!=null&&WTI>=100,nearAll=[],hot=[],warm=[],status={};
 areas.forEach(function(a){var t=((a.querySelector('.hd b')||{}).textContent||'').trim();var L=[...a.querySelectorAll('li[data-lt]')].map(function(li){var s=st(li);if(t==='유가'&&s==='off'&&oilNear)s='near';return{n:nm(li),v:val(li),s:s}});
  var on=L.filter(function(x){return x.s==='on'}).length,nr=L.filter(function(x){return x.s==='near'});status[t]=L;
  nr.forEach(function(x){nearAll.push(t==='유가'&&x.s==='near'&&oilNear?'유가 '+Math.round(WTI)+'달러(수준)':short(x.n)+' '+x.v)});
  if(on)hot.push(t);else if(nr.length)warm.push(t);
  var c=a.querySelector('.cnt');if(c){c.textContent=on+' / '+L.length+' 켜짐'+(nr.length?' · 근접 '+nr.length:'');c.classList.toggle('mm-ln-nc',!on&&nr.length>0);if(!on&&nr.length)a.style.setProperty('--ac','#e07b16')}
  var old=a.querySelector('.mm-ln-now');if(old)old.remove();var n=nowTxt(t,L,oilNear);if(n){var d=document.createElement('div');d.className='mm-ln-now';d.style.setProperty('--nc',C[n[0]][0]);d.style.setProperty('--nb',C[n[0]][1]);var b=document.createElement('b');b.textContent='지금';var sp=document.createElement('span');sp.textContent=n[1];d.append(b,sp);var after=a.querySelector('.a-desc')||a.querySelector('.hd');after.after(d)}});
 // 위 동그라미: 근접은 반불
 var D=[...document.querySelectorAll('#big-dots .dot')];D.forEach(function(i){i.classList.remove('mm-half')});
 Object.keys(status).forEach(function(t){status[t].forEach(function(x){if(x.s!=='near')return;var i=D.find(function(d){return d.title===x.n&&!d.classList.contains('on')});if(i)i.classList.add('mm-half')})});
 // 영역별 3칸 동그라미(사용자 2026-11-01): 불 1개당 1칸, 근접 1개당 반 칸(최대 3칸). 줄을 누르면 왜 켜졌는지 펼침
 var dots=document.getElementById('big-dots');if(dots){dots.classList.add('mm-ln-one');[...dots.querySelectorAll('.mm-ln-row,.mm-ln-cap,.mm-ln-ar,.mm-ln-key')].forEach(function(e){e.remove()});
  var nOn=0,nNr=0,nAll=0,OPEN=window.__mmLnOpen||(window.__mmLnOpen={});
  var box=document.createElement('div');box.className='mm-ln-ar';
  Object.keys(status).forEach(function(t){var L=status[t];var on=L.filter(function(x){return x.s==='on'}),nr=L.filter(function(x){return x.s==='near'});nOn+=on.length;nNr+=nr.length;nAll+=L.length;
   var sc=Math.min(3,on.length+nr.length*0.5);var rw=document.createElement('div');rw.className='mm-ln-r'+(on.length?' hot':nr.length?' warm':'');rw.setAttribute('role','button');
   var nm=document.createElement('b');nm.textContent=t;rw.appendChild(nm);var dd=document.createElement('span');dd.className='d3';var ro=Math.min(3,on.length),ns=Math.min(3-ro,nr.length*0.5);for(var q=1;q<=3;q++){var i=document.createElement('i');if(q<=ro)i.className='on';else if(q-ro<=ns)i.className='nf';else if(q-ro-0.5<=ns)i.className='nr';dd.appendChild(i)}rw.appendChild(dd);
   var st=document.createElement('span');st.className='st';st.textContent=on.length?'켜짐 '+on.length+(nr.length?' · 근접 '+nr.length:''):nr.length?'근접 '+nr.length:'조용';rw.appendChild(st);
   var ex=document.createElement('div');ex.className='mm-ln-ex';var hit=on.concat(nr);
   if(!hit.length){var p0=document.createElement('p');p0.textContent=L.length+'개 모두 기준에서 멉니다.';ex.appendChild(p0)}
   hit.forEach(function(x){var p=document.createElement('p');var k=document.createElement('span');k.className=x.s==='on'?'k on':'k nr';k.textContent=x.s==='on'?'켜짐':'근접';p.appendChild(k);var tt=document.createElement('b');tt.textContent=x.n+' '+x.v;p.appendChild(tt);
    var why=(t==='유가'&&x.s==='near'&&oilNear)?'급등 기준(한 달 +15%)은 아니지만 WTI가 '+Math.round(WTI)+'달러로 100달러 위에 머물러 물가·금리 부담이 이어집니다.':(TW[x.n]||'');if(x.s==='near'&&!(t==='유가'&&oilNear))why='기준의 90% 넘게 다가왔습니다. '+why;
    if(why){var w=document.createElement('span');w.className='w';w.textContent=why;p.appendChild(w)}ex.appendChild(p)});
   var rest=L.length-hit.length;if(hit.length&&rest>0){var pr=document.createElement('p');pr.className='rest';pr.textContent='나머지 '+rest+'개는 꺼짐';ex.appendChild(pr)}
   if(OPEN[t])rw.classList.add('op');rw.addEventListener('click',function(){rw.classList.toggle('op');OPEN[t]=rw.classList.contains('op')});
   box.appendChild(rw);box.appendChild(ex)});
  dots.appendChild(box);
  var cp=document.createElement('span');cp.className='mm-ln-cap';var aO=Object.keys(status).filter(function(t){return status[t].some(function(x){return x.s==='on'})}).length,aN=Object.keys(status).filter(function(t){return !status[t].some(function(x){return x.s==='on'})&&status[t].some(function(x){return x.s==='near'})}).length,aT=Object.keys(status).length;cp.innerHTML=aT+'개 영역 중 <i class="on"></i><em>켜짐 '+aO+'</em> · <i class="nr"></i><u>문턱 앞 '+aN+'</u> · <i></i>조용 '+(aT-aO-aN)+' <span style="color:#9a948a;font-weight:600">(불 '+nOn+' · 근접 '+nNr+' / 전체 '+nAll+'개)</span>';dots.appendChild(cp);
  var ky=document.createElement('span');ky.className='mm-ln-key';ky.textContent='영역마다 3칸: 켜진 불 1개 = 빨간 1칸, 근접 1개 = 주황 반 칸 · 줄을 누르면 이유가 펼쳐집니다';dots.appendChild(ky)}
 // 큰 숫자는 '켜진 영역 n / 전체 영역'(사용자 2026-11-01: 3/12는 직관적이지 않음)
 var areasAll=Object.keys(status),aOn=areasAll.filter(function(t){return status[t].some(function(x){return x.s==='on'})}),aNr=areasAll.filter(function(t){return aOn.indexOf(t)<0&&status[t].some(function(x){return x.s==='near'})});
 var bn=document.getElementById('big-n');if(bn){var want=aOn.length+' / '+areasAll.length;if(bn.dataset.mm!==want||bn.textContent.indexOf('영역')<0){bn.dataset.mm=want;bn.innerHTML='';bn.appendChild(document.createTextNode(want));var u=document.createElement('small');u.className='mm-ln-u';u.textContent=' 영역';bn.appendChild(u)}}
 var bc=document.getElementById('big-chg');if(bc){var nOnL=0;areasAll.forEach(function(t){nOnL+=status[t].filter(function(x){return x.s==='on'}).length});var tx='켜진 영역: '+(aOn.join('·')||'없음')+' · 불 '+nOnL+'개'+(aNr.length?' · 문턱 앞 영역: '+aNr.join('·'):'');if(bc.textContent!==tx)bc.textContent=tx}
 var bs=document.getElementById('big-st');if(bs&&/무게/.test(bs.textContent))bs.textContent=bs.textContent.replace(/\s*\(무게[^)]*\)/,'');
 var stp=document.querySelectorAll('#big-steps span small');var LB=['켜진 곳 없음','영역 1곳','영역 2곳','한 곳에 불 몰림','영역 3곳+'];stp.forEach(function(x,i){if(LB[i]&&x.textContent!==LB[i])x.textContent=LB[i]});
 var o=big.querySelector('.mm-ln-near');if(o)o.remove();
 if(!big.querySelector('.mm-ln-leg')){var dots=document.getElementById('big-dots');if(dots){var lg=document.createElement('div');lg.className='mm-ln-leg';lg.innerHTML='<span><i style="background:var(--color-bad,#b3261e);border-color:var(--color-bad,#b3261e)"></i>켜짐</span><span><i style="background:linear-gradient(90deg,#e07b16 50%,transparent 50%);border-color:#e07b16"></i>근접(반불)</span><span><i></i>꺼짐</span>';dots.after(lg)}}
 // 맨 위 총평
 var h=big.querySelector('.mm-ln-head');if(h)h.remove();h=document.createElement('div');h.className='mm-ln-head';
 var nearNames=[];Object.keys(status).forEach(function(t){status[t].forEach(function(x){if(x.s==='near')nearNames.push(t==='유가'?'유가':/10년물/.test(x.n)?'10년물':/30년물/.test(x.n)?'30년물':/VIX/.test(x.n)?'VIX':/기간구조/.test(x.n)?'기간구조':short(x.n))})});
 nearNames=nearNames.filter(function(x,i,a){return a.indexOf(x)===i});
 var l1=hot.length?'공포는 '+hot.map(function(t){return AN[t]||t}).join('·')+'에 몰렸고':'아직 켜진 영역은 없고',l2=nearNames.length?nearNames.slice(0,4).join('·')+'는 문턱 바로 앞입니다':'다른 곳은 조용합니다';
 var y10=(status['채권·금리']||[]).find(function(x){return/10년물 5%/.test(x.n)});
 var sub='터진 곳 '+hot.length+'곳, 문턱에서 대기 중 '+warm.length+'곳'+(y10&&y10.s==='near'?' — 10년물이 5%를 넘으면 한 번에 번질 수 있는 자리':y10&&y10.s==='on'?' — 핵심 불(10년물 5%)이 켜져 있습니다':'');
 var sm=document.createElement('small');sm.textContent='지금 시장은';var sp2=document.createElement('span');sp2.textContent=sub;h.append(sm,document.createTextNode(l1+', '+l2),sp2);big.insertBefore(h,big.firstChild)}
var k=0;(function go(){try{run()}catch(e){}if(++k<20)setTimeout(go,400)})();
if(window.MutationObserver){var r=document.getElementById('areas');if(r)new MutationObserver(function(){setTimeout(function(){try{run()}catch(e){}},60)}).observe(r,{childList:true});var bd=document.getElementById('big-dots');if(bd)new MutationObserver(function(m){if(m.some(function(x){return [...x.addedNodes].some(function(n){return n.classList&&n.classList.contains('grp')})}))setTimeout(function(){try{run()}catch(e){}},60)}).observe(bd,{childList:true})}})();
