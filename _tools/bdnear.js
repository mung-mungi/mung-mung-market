// 채권·금리 페이지 '채권 경고등'에 근접(반불)·'지금' 한 줄·시장 전체 단계 알약(사용자 2026-11-01)
(function(){var L=null,T=null,F=null;
function j(u){return fetch(u+'?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
Promise.all([j('d/lights/lights_log.json'),j('d/lights/thresholds.json'),j('d/lights/fresh.json')]).then(function(a){L=a[0];T=a[1];F=a[2];go()});
var MAP={'장단기 금리 역전':'inv','10년물 5% 이상':'y10','10년물 2주 급등':'jump','30년물 5.5% 이상':'y30','하이일드 스프레드 4.5%p 이상':'hy'};
function ratio(t,v){if(v==null)return 0;if(t.op==='<'||t.op==='<=')return t.value===0?1-(v/0.5):t.value/v;return t.value>0?v/t.value:0}
// 점수제(사용자 2026-11-01): 켜짐 = 무게 전부 · 근접 0.8 · 보통 0.4 · 양호 0.2
function bsc(){if(!F||!F.area_scores)return'';var ids=Object.keys(MAP).map(function(k){return MAP[k]}),sc=0,mx=0;Object.keys(F.area_scores).forEach(function(a){F.area_scores[a].items.forEach(function(i){if(ids.indexOf(i.id)>=0){sc+=i.pt;mx+=i.w}})});return ' · 점수 '+(Math.round(sc*10)/10)+'/'+mx}
function run(){var card=document.getElementById('lights-card'),ul=document.getElementById('lights'),dots=document.getElementById('b-dots');if(!card||!ul||!dots||!L||!T)return false;
 var lis=[...ul.querySelectorAll('li')];if(!lis.length)return false;var TH={};T.forEach(function(t){TH[t.id]=t});var d=L[L.length-1].date;var cur={};L.forEach(function(r){if(r.date===d)cur[r.id]=r});
 var st=[],nears=[];lis.forEach(function(li){var name=Object.keys(MAP).find(function(k){return li.textContent.indexOf(k)>=0});var id=name&&MAP[name],r=id&&cur[id],t=id&&TH[id];var s='off';
  if(r&&t){s=Number(r.on)===1?'on':ratio(t,Number(r.val))>=0.9?'near':'off'}st.push(s);li.classList.toggle('mm-nr',s==='near');
  if(s==='near'){li.innerHTML=li.innerHTML.replace(/→ 꺼짐\s*$/,'→ <b style="color:#c76a0c">근접</b>');nears.push((/10년물 5%/.test(name)?'10년물 ':/30년물/.test(name)?'30년물 ':/하이일드/.test(name)?'하이일드 ':name+' ')+(t.unit==='%p'?Number(r.val).toFixed(2)+'%p':Number(r.val).toFixed(2)+'%'))}});
 var D=[...dots.querySelectorAll('.dot')];var od={on:0,near:1,off:2},ss=st.slice().sort(function(a,b){return od[a]-od[b]});D.forEach(function(i,k){i.classList.remove('on','mm-nr');if(ss[k]==='on')i.classList.add('on');if(ss[k]==='near')i.classList.add('mm-nr')});
 var on=st.filter(function(x){return x==='on'}).length,nr=nears.length;var tt=document.getElementById('b-title');if(tt&&!tt.querySelector('.mm-cnt')){tt.insertAdjacentHTML('afterbegin','<span class="mm-cnt" style="display:block;font-size:14px;color:#6f6a60;font-weight:700;margin-bottom:2px">'+st.length+'개 중 켜짐 '+on+' · 근접 '+nr+bsc()+'</span>')}
 var o=card.querySelector('.mm-bd-now');if(o)o.remove();var n=on?['#b3261e','#fbe8e5','채권 쪽 불이 켜졌습니다. 성장주에 직접 부담입니다.']:nr?['#a14d00','#fdf0e1',nears.join(' · ')+' — 문턱 바로 아래입니다. 한 번만 밀려도 켜집니다.']:['#2e7d4f','#e7f3ec','금리·신용 쪽은 조용합니다.'];
 var e=document.createElement('div');e.className='mm-bd-now';e.style.setProperty('--nc',n[0]);e.style.setProperty('--nb',n[1]);e.innerHTML='<b>지금</b><span></span>';e.querySelector('span').textContent=n[2];ul.before(e);
 var ex=card.querySelector('.mm-bd-all');if(ex)e.after(ex);if(F&&F.stage&&!ex){var a=document.createElement('a');a.className='mm-bd-all';a.href='p-lights.html';var em={'평온':'🟢','주의':'🟡','경계':'🟠','긴장':'🟠','위험':'🔴'}[F.stage]||'';a.textContent='시장 전체 경고등 '+em+' '+F.stage+(F.score!=null?' · '+F.score.toFixed(1)+'/'+F.score_max+'점':' · 불 '+F.on+'개')+' →';e.after(a)}
 return true}
function go(){var k=0;(function t(){try{run()}catch(e){}if(++k<25)setTimeout(t,400)})();
 ['lights','b-dots','b-title'].forEach(function(id){var n=document.getElementById(id);if(n&&window.MutationObserver)new MutationObserver(function(m){if(m.some(function(x){return [...x.addedNodes].some(function(a){return !(a.classList&&(a.classList.contains('mm-cnt')||a.classList.contains('mm-bd-now')))&&!(a.nodeName==='B')})})){clearTimeout(go.t);go.t=setTimeout(function(){try{run()}catch(e){}},80)}}).observe(n,{childList:true})})}})();
