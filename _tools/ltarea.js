// '영역별 경고등' 카드를 경고등 3판 자료(d/lights/fresh.json)로 다시 그림(사용자 2026-11-09 '아랫단 영역별에도 오늘 내용 반영')
// 예전 카드는 옛 기준표(지표 13개)로 그려져 위 점수 카드(층위 7개 등)와 숫자가 달랐음. 모양(클래스)은 그대로 두고 내용만 바꿈
(function(){
if(!/p-lights\.html/.test(location.pathname))return;
var F=null,ORD=['반도체·AI','유가','채권·금리','신용','옵션·공포'];
var DESC={'반도체·AI':'우리 기조(AI 밸류체인)의 체온입니다. 칩 설계부터 네오클라우드까지 6개 층과 하루 급락을 봅니다.','유가':'기름값 수준·급등 속도와 중동 위험 웃돈(브렌트-WTI)·유가 출렁임(OVX)으로 전쟁 프리미엄을 봅니다.','채권·금리':'금리 수준(5%·5.5%)과 2주 급등 속도, 금리가 움직인 이유, 국채 입찰을 봅니다.','신용':'돈 빌리기가 어려워지는지 — 하이일드·투자등급·CCC 스프레드, 사모신용, MMF로 숨는 돈을 봅니다.','옵션·공포':'옵션 시장의 공포 — VIX·VVIX(공포 강도), 기간구조, 풋콜을 봅니다.'};
var LINK={'반도체·AI':['p-prices.html','시세 보드에서 보기'],'유가':['p-policy.html','주요 뉴스에서 보기'],'채권·금리':['p-bond.html','채권 온도계에서 보기'],'신용':['p-bond.html','채권 온도계에서 보기'],'옵션·공포':['p-opt.html','옵션 온도계에서 보기']};
var LVI={'안전':0,'양호':1,'보통':2,'근접':3,'켜짐':4};
function col(r){return r>=.7?'#b3261e':r>=.55?'#c8501c':r>=.39?'#e07b16':r>=.25?'#c99a06':'#2e9d5b'}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function fv(i){var v=Math.round(i.val*100)/100;return (i.unit==='달러'?v+'달러':v+(i.unit||''))}
function now(a,x){var on=x.items.filter(function(i){return i.lv==='켜짐'}),nr=x.items.filter(function(i){return i.lv==='근접'});
 if(x.ratio>=.6)return on.length?on.map(function(i){return i.name.replace(' 고점 대비','')}).slice(0,4).join('·')+' 등 '+on.length+'개가 켜져 꽉 찼습니다.':'문턱 앞 지표가 많아 거의 꽉 찼습니다.';
 if(x.ratio>=.25)return (on.length?'켜진 불 '+on.length+'개':'')+(on.length&&nr.length?' + ':'')+(nr.length?'문턱 앞 '+nr.map(function(i){return i.name.replace(/\(.*?\)/,'')}).slice(0,3).join('·'):'')+' — 조금씩 차오르는 중입니다.';
 return '대부분 평소 수준입니다.'}
function render(){var box=document.getElementById('areas');if(!box||!F||!F.area_scores)return;if(box.dataset.v3===F.date)return;
 var EXP=window.__MM_EXP||{};box.textContent='';
 ORD.concat(Object.keys(F.area_scores).filter(function(k){return ORD.indexOf(k)<0})).forEach(function(a){var x=F.area_scores[a];if(!x)return;var c=col(x.ratio);
  var d=el('div','area');d.dataset.ad=1;d.style.setProperty('--ac',c);var hd=el('div','hd');hd.appendChild(el('b','',a));var on=x.items.filter(function(i){return i.lv==='켜짐'}).length;hd.appendChild(el('span','cnt',on+' / '+x.items.length+' 켜짐 · '+Math.round(x.ratio*100)+'% 참'));d.appendChild(hd);
  d.appendChild(el('p','a-desc',DESC[a]||''));
  var nw=el('div','mm-ln-now');nw.style.setProperty('--nc',c);nw.style.setProperty('--nb',x.ratio>=.39?'#fbe8e5':'#f6f4ef');nw.appendChild(el('b','','지금'));nw.appendChild(el('span','',now(a,x)));d.appendChild(nw);
  var ul=el('ul');x.items.forEach(function(i){var L=LVI[i.lv]||0;var li=el('li',L===4?'on l-on':'');li.dataset.lv=L+1;li.dataset.lt=1;li.dataset.t=1;li.dataset.lx=1;li.appendChild(el('span','l-dot'));li.appendChild(el('b','',i.name));li.appendChild(el('span','l-now',fv(i)));
   li.appendChild(el('span','l-th',i.pctl!=null?'10년 중 '+Math.round(i.pctl)+'% 자리 · 켜짐 ≥ '+(Math.round(i.th*100)/100):'기준 ≥ '+i.th+(i.unit==='%p'?'%p':i.unit==='달러'?'달러':i.unit||'')));
   var lv=el('span','l-lv');for(var k=0;k<5;k++)lv.appendChild(el('i'));lv.appendChild(el('em','',i.lv));li.appendChild(lv);
   var ex=EXP[i.id];if(ex){var nm=i.name.replace(/\(.*?\)/,'').trim(),cc=nm.charCodeAt(nm.length-1);li.appendChild(el('span','l-q',nm+(cc>=44032&&cc<=55203&&(cc-44032)%28?'이란?':'란?')));li.appendChild(el('span','l-ex',ex[0]));li.addEventListener('click',function(){this.classList.toggle('lxo')})}ul.appendChild(li)});d.appendChild(ul);
  var lk=LINK[a];if(lk){var A=el('a','',lk[1]+' →');A.href=lk[0];A.dataset.lx=1;d.appendChild(A)}box.appendChild(d)});
 box.dataset.v3=F.date}
fetch('d/lights/fresh.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j||!j.ver3)return;F=j;var k=0;(function go(){try{render()}catch(e){}if(++k<25)setTimeout(go,500)})();
 try{var t=null;new MutationObserver(function(){var b=document.getElementById('areas');if(b&&b.dataset.v3!==F.date){clearTimeout(t);t=setTimeout(render,80)}}).observe(document.body,{childList:true,subtree:true})}catch(e){}}).catch(function(){});
})();
