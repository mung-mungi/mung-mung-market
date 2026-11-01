// 채권 온도계(사용자 2026-11-02): 채권·금리 페이지를 옵션 온도계 양식으로 — 숫자칸에 10년물, '오늘 한눈에' = 단계·점수 + 왜 이 단계 + 지표 5줄(값 · 5단계 막대),
// 옛 '불 n개 그대로' 카드(#bt-card)와 경고등 카드 안 글 목록(#lights)은 위 5줄과 겹쳐 숨김. 점수는 시장 경고등과 같은 점수제(d/lights/fresh.json).
(function(){if(!/p-bond\.html/.test(location.pathname))return;
var F=null,Y=null;
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
var ROW=[['inv','장단기 금리차','10년−2년 · 0 밑(역전)이면 켜짐'],['y10','10년물','5% 넘으면 켜짐 · 무게 2배'],['jump','10년물 2주 변화','+0.25%p 넘게 오르면 켜짐'],['y30','30년물','5.5% 넘으면 켜짐'],['hy','하이일드 가산금리','4.5%p 넘으면 켜짐 · 신용 불안']];
var LV={'안전':1,'양호':2,'보통':3,'근접':4,'켜짐':5},LN=['','안전','양호','보통','근접','켜짐'];
var BR=[[0,'평온','#2e9d5b','🟢'],[.25,'주의','#c99a06','🟡'],[.375,'경계','#e07b16','🟠'],[.5,'긴장','#c8501c','🟠'],[.625,'위험','#b3261e','🔴']];
function stg(sc,mx){var r=BR[0];BR.forEach(function(b){if(sc>=b[0]*mx-1e-9)r=b});return r}
function items(){var m={};Object.keys(F.area_scores||{}).forEach(function(a){F.area_scores[a].items.forEach(function(i){m[i.id]=i})});return m}
function fv(i){var v=Number(i.val),u=i.unit==='%p'?'%p':'%';return (v>0&&i.id!=='y10'&&i.id!=='y30'&&i.id!=='hy'?'+':'')+v.toFixed(2)+u}
function pct(i){var v=Number(i.val),t=Number(i.th);if(i.op==='<')return null;return t>0?Math.round(v/t*100):null}
function md(d){var a=String(d).split('-');return (+a[1])+'/'+(+a[2])}
function chg(k){if(!Y)return '';var r=Y.filter(function(x){return x[k]!=null});if(r.length<2)return '';var d=Math.round((r[r.length-1][k]-r[r.length-2][k])*100);return (d>0?'+':d<0?'−':'±')+Math.abs(d)+'bp'}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function take(){var tk=document.getElementById('take');if(!tk||!F)return;var M=items(),sc=0,mx=0,on=[],nr=[];
 ROW.forEach(function(r){var i=M[r[0]];if(!i)return;sc+=Number(i.pt||0);mx+=Number(i.w||1);if(i.lv==='켜짐')on.push(r[1]);if(i.lv==='근접')nr.push(r[1]+' '+(pct(i)||'')+'%')});
 if(!mx)return;sc=Math.round(sc*10)/10;var g=stg(sc,mx),key=F.date+':'+sc;var w=tk.parentNode.querySelector('.mm-bo');if(w&&w.dataset.k===key)return;
 if(!w){w=el('div','mm-bo');tk.after(w)}w.dataset.k=key;w.textContent='';tk.classList.add('mm-bo-src');
 var top=el('div','mm-bo-top');var s=el('span','st',g[3]+' '+g[1]);s.style.color=g[2];top.appendChild(s);var c=el('span','sc');c.innerHTML='점수 <span class="n"></span> / '+mx;c.querySelector('.n').textContent=sc.toFixed(1);top.appendChild(c);w.appendChild(top);
 var why=el('p','mm-bo-why');why.appendChild(el('span','q','왜 이 단계? '));why.appendChild(document.createTextNode(on.length||nr.length?('켜진 불 '+on.length+'개'+(on.length?'('+on.join('·')+')':'')+(nr.length?' + 문턱 바로 앞 '+nr.length+'개('+nr.join(' · ')+')':'')+' — 켜지기 직전인 불까지 미리 더한 경고입니다.'):'금리·신용 쪽 지표가 모두 문턱에서 멀리 있습니다.'));w.appendChild(why);
 var ul=el('ul','mm-bo-rows');ROW.forEach(function(r){var i=M[r[0]];if(!i)return;var k=LV[i.lv]||1;var li=el('li');
  var a=el('span','k');a.appendChild(el('span','nm',r[1]));a.appendChild(el('span','ds',r[2]));li.appendChild(a);
  var v=el('span','v',fv(i));v.dataset.lv=k;var cg=r[0]==='y10'?chg('us10y'):r[0]==='y30'?chg('us30y'):'';if(cg)v.appendChild(el('span','cg',cg));li.appendChild(v);
  var m=el('span','lv');m.dataset.lv=k;for(var n=0;n<5;n++)m.appendChild(el('i'));m.appendChild(el('em','',LN[k]));li.appendChild(m);ul.appendChild(li)});
 w.appendChild(ul);w.appendChild(el('p','mm-bo-ft','막대 = 문턱까지 얼마나 왔나(안전·양호·보통·근접·켜짐) · '+md(F.date)+' 마감'))}
function hero(){if(!Y)return;var s=document.querySelector('.mm-hero .hx-side');if(!s)return;var r=Y.filter(function(x){return x.us10y!=null});if(!r.length)return;var v=r[r.length-1].us10y.toFixed(2);
 if(s.dataset.bo===v)return;s.dataset.bo=v;s.innerHTML='<b></b><small>10년물 %</small>';s.firstChild.textContent=v}
function all(){try{take()}catch(e){}try{hero()}catch(e){}}
Promise.all([j('d/lights/fresh.json'),j('d/bond/yields_daily.json')]).then(function(a){F=a[0];Y=a[1];all()});
var k=0;(function go(){all();if(++k<30)setTimeout(go,400)})();
try{new MutationObserver(all).observe(document.body,{childList:true,subtree:true})}catch(e){}
})();
