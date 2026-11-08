// 채권 온도계(사용자 2026-11-02): 채권·금리 페이지를 옵션 온도계 양식으로 — 숫자칸에 10년물, '오늘 한눈에' = 단계·점수 + 왜 이 단계 + 지표 5줄(값 · 5단계 막대),
// 옛 '불 n개 그대로' 카드(#bt-card)와 경고등 카드 안 글 목록(#lights)은 위 5줄과 겹쳐 숨김. 점수는 시장 경고등과 같은 점수제(d/lights/fresh.json).
(function(){if(!/p-bond\.html/.test(location.pathname))return;
var F=null,Y=null;
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
// 2026-11-02 사용자: 장단기·하이일드는 지금 중요도 낮음, '금리가 왜 움직였나'(피난형 등)가 핵심 → 10년물·움직인 이유·30년물·국채 입찰 + 하이일드는 참고
var ROW=[['y10','10년물','5% 넘으면 켜짐 · 무게 2배'],['why','금리 움직인 이유',''],['y30','30년물 · 재정','5.5% 넘으면 켜짐'],['auc','국채 입찰','최근 2주 부진 2번이면 켜짐'],['hy','하이일드(참고)','4.5%p 넘으면 켜짐 · 신용 불안']];
var LV={'안전':1,'양호':2,'보통':3,'근접':4,'켜짐':5},LN=['','안전','양호','보통','근접','켜짐'];
var BR=[[0,'평온','#2e9d5b','🟢'],[.25,'주의','#c99a06','🟡'],[.392,'경계','#e07b16','🟠'],[.55,'긴장','#c8501c','🟠'],[.7,'위험','#b3261e','🔴']];
function stg(sc,mx){var r=BR[0];BR.forEach(function(b){if(sc>=b[0]*mx-1e-9)r=b});return r}
function items(){var m={};Object.keys(F.area_scores||{}).forEach(function(a){F.area_scores[a].items.forEach(function(i){m[i.id]=i})});return m}
function fv(i){if(i.id==='why')return i.kind||'—';if(i.id==='auc')return '부진 '+Number(i.val)+'번';var v=Number(i.val),u=i.unit==='%p'?'%p':'%';return (v>0&&i.id!=='y10'&&i.id!=='y30'&&i.id!=='hy'?'+':'')+v.toFixed(2)+u}
function pct(i){var v=Number(i.val),t=Number(i.th);if(i.op==='<')return null;return t>0?Math.round(v/t*100):null}
function md(d){var a=String(d).split('-');return (+a[1])+'/'+(+a[2])}
function chg(k){if(!Y)return '';var r=Y.filter(function(x){return x[k]!=null});if(r.length<2)return '';var d=Math.round((r[r.length-1][k]-r[r.length-2][k])*100);return (d>0?'+':d<0?'−':'±')+Math.abs(d)+'bp'}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function take(){var tk=document.getElementById('take');if(!tk||!F)return;var M=items(),sc=0,mx=0,on=[],nr=[];
 ROW.forEach(function(r){var i=M[r[0]];if(!i)return;sc+=Number(i.pt||0);mx+=Number(i.w||1);if(i.lv==='켜짐')on.push(r[1]);if(i.lv==='근접')nr.push(r[1]+' '+(pct(i)||'')+'%')});
 if(!mx)return;sc=Math.round(sc*10)/10;var g=stg(sc,mx);
 /* 경고등 3판 영역 점수(10점 만점)·같은 단계 구간으로(사용자 2026-11-09 점검 '잣대 하나로') */
 var A3=F.ver3&&F.area_scores&&F.area_scores['채권·금리'];if(A3&&F.bands){sc=Math.round(A3.ratio*100)/10;mx=10;var bi=0;F.bands.forEach(function(b,k){if(sc>=b[0])bi=k});g=[F.bands[bi][0],F.bands[bi][1],['#1a7f37','#b08a00','#e07b16','#c8501c','#c62828'][bi],['🟢','🟡','🟠','🟠','🔴'][bi]]}
 var key=F.date+':'+sc;var w=tk.parentNode.querySelector('.mm-bo');if(w&&w.dataset.k===key)return;
 if(!w){w=el('div','mm-bo');tk.after(w)}w.dataset.k=key;w.textContent='';tk.classList.add('mm-bo-src');
 var top=el('div','mm-bo-top');var s=el('span','st',g[3]+' '+g[1]);s.style.color=g[2];top.appendChild(s);var c=el('span','sc');c.innerHTML=(A3?'영역 점수':'점수')+' <span class="n"></span> / '+mx;c.querySelector('.n').textContent=sc.toFixed(1);top.appendChild(c);w.appendChild(top);
 var W=M.why;if(W&&W.kind){var y10=M.y10?Number(M.y10.val).toFixed(2):'';var TX={'피난형':'금리는 내렸지만 물가 덕이 아니라 피난 때문입니다 — 기술주에서 빠진 돈이 국채로 간 것이라 좋은 신호로 보기 어렵습니다.','물가 안정형':'물가 기대가 내려 금리가 내렸습니다 — 기술주에 우호적인 하락입니다.','재정 우려형':'장기물이 앞서 오릅니다 — 나라 빚 걱정이 붙은 상승이라 성장주에 가장 부담입니다.','긴축형':'단기물이 앞서 오릅니다 — 금리 인하가 늦춰질 걱정이 붙은 상승입니다.','급등':'금리가 2주 새 빠르게 올랐습니다 — 성장주 몸값에 바로 부담입니다.','금리 상승':'금리가 오르는 중입니다 — 성장주 몸값에 부담입니다.','보합':'최근 2주 금리는 크게 안 움직였습니다 — 지금은 10년물 '+y10+'%라는 높이 자체가 부담입니다.','금리 하락':'금리가 내렸고 주식도 버팁니다 — 부담이 조금 덜어졌습니다.'};
  var nw=el('p','mm-bo-now');nw.appendChild(el('span','q',W.kind));nw.appendChild(document.createTextNode(TX[W.kind]||''));w.appendChild(nw)}
 var why=el('p','mm-bo-why');why.appendChild(el('span','q','왜 이 단계? '));why.appendChild(document.createTextNode(on.length||nr.length?('켜진 불 '+on.length+'개'+(on.length?'('+on.join('·')+')':'')+(nr.length?' + 문턱 바로 앞 '+nr.length+'개('+nr.join(' · ')+')':'')+' — 켜지기 직전인 불까지 미리 더한 경고입니다.'):'금리·신용 쪽 지표가 모두 문턱에서 멀리 있습니다.'));w.appendChild(why);
 var ul=el('ul','mm-bo-rows');ROW.forEach(function(r){var i=M[r[0]];if(!i)return;var k=LV[i.lv]||1;var li=el('li');
  var a=el('span','k');a.appendChild(el('span','nm',r[1]));a.appendChild(el('span','ds',r[0]==='why'?String(i.note||'').replace(/^[^—]*—\s*/,''):r[2]));li.appendChild(a);
  var v=el('span','v',fv(i));v.dataset.lv=k;var cg=r[0]==='y10'?chg('us10y'):r[0]==='y30'?chg('us30y'):'';if(cg)v.appendChild(el('span','cg',cg));li.appendChild(v);
  var m=el('span','lv');m.dataset.lv=k;for(var n=0;n<5;n++)m.appendChild(el('i'));m.appendChild(el('em','',LN[k]));li.appendChild(m);ul.appendChild(li)});
 w.appendChild(ul);w.appendChild(el('p','mm-bo-ft','막대 = 문턱까지 얼마나 왔나(안전·양호·보통·근접·켜짐) · '+md(F.date)+' 마감'))}
function hero(){if(!Y)return;var s=document.querySelector('.mm-hero .hx-side');if(!s)return;var r=Y.filter(function(x){return x.us10y!=null});if(!r.length)return;var v=r[r.length-1].us10y.toFixed(2);
 if(s.dataset.bo===v)return;s.dataset.bo=v;s.innerHTML='<b></b><small>10년물 %</small>';s.firstChild.textContent=v}
// 위쪽 바로가기 알약(사용자 2026-11-02: 국채 입찰처럼 요즘 중요한데 찾기 힘든 칸) — 가로 밀기 대신 줄바꿈, 누르면 그 칸으로
var J=[['lights-card','경고등 점수',null],[/^지금 금리/,'지금 금리',null],[/^국채 입찰/,'국채 입찰','hot'],[/^금리가 왜/,'금리가 왜 움직였나',null],[/^국채 금리 흐름/,'금리 흐름',null],[/^장단기/,'장단기 금리차',null],[/^한국·미국/,'한미 금리',null]];
function card(k){if(typeof k==='string')return document.getElementById(k);var h=[].find.call(document.querySelectorAll('h2'),function(x){return k.test(x.textContent.trim())});return h&&(h.closest('section,.card,article')||h)}
function jump(){var bo=document.querySelector('.mm-bo');if(!bo)return;var box=bo.closest('section,.card,article')||bo.parentNode;var have=J.map(function(a){return [card(a[0]),a[1],a[2]]}).filter(function(a){return a[0]});if(have.length<3)return;
 var nav=document.querySelector('.mm-bj'),sig=have.map(function(a){return a[1]}).join(',');if(nav&&nav.dataset.sig===sig&&nav.previousElementSibling===box)return;if(nav)nav.remove();
 nav=el('nav','mm-bj');nav.dataset.sig=sig;nav.setAttribute('aria-label','바로가기');
 have.forEach(function(a){var x=el('a',a[2]?'hot':'',a[1]);x.href='#';x.setAttribute('role','button');
  if(a[2]&&F){var it=items().auc;if(it)x.appendChild(el('em','',' · 최근 부진 '+Number(it.val)+'번'))}
  x.onclick=function(e){e.preventDefault();var t=card(J.find(function(z){return z[1]===a[1]})[0]);if(t)scrollTo({top:t.getBoundingClientRect().top+scrollY-10,behavior:'smooth'})};nav.appendChild(x)});
 box.after(nav)}
function all(){try{take()}catch(e){}try{hero()}catch(e){}try{jump()}catch(e){}}
Promise.all([j('d/lights/fresh.json'),j('d/bond/yields_daily.json')]).then(function(a){F=a[0];Y=a[1];all()});
var k=0;(function go(){all();if(++k<30)setTimeout(go,400)})();
try{new MutationObserver(all).observe(document.body,{childList:true,subtree:true})}catch(e){}
})();
