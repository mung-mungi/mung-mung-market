// 단계 옆 '왜 이 단계?' 한 줄(사용자 2026-11-02) — 단계는 전체 점수 그대로(불은 켜지기 전에 미리 경고하는 것),
// 다만 불이 적게 켜졌는데 '위험'이면 보는 사람이 헷갈리므로 켜진 불 + 문턱 앞 지표를 한 줄로 풀어 줌. 자료 d/lights/fresh.json
(function(){
var P=/p-opt\.html/.test(location.pathname)?'opt':/p-bond\.html/.test(location.pathname)?'bond':null;if(!P)return;
var IDS={opt:['vix','term','pc'],bond:['inv','y10','jump','y30','hy']}[P];
var SH={vix:'VIX',term:'기간구조',pc:'풋콜',inv:'장단기차',y10:'10년물',jump:'10년물 2주 급등',y30:'30년물',hy:'하이일드'};
var F=null;
function ratio(i){var v=Number(i.val),t=Number(i.th);if(i.val==null)return 0;if(i.op==='<'||i.op==='<=')return t===0?1-(v/0.5):t/v;return t>0?v/t:0}
function text(){var it=[];Object.keys(F.area_scores||{}).forEach(function(a){F.area_scores[a].items.forEach(function(i){if(IDS.indexOf(i.id)>=0)it.push(i)})});
 var on=it.filter(function(i){return i.lv==='켜짐'}),nr=it.filter(function(i){return i.lv==='근접'});if(!on.length&&!nr.length)return null;
 var a=[];if(on.length)a.push('켜진 불 '+on.length+'개('+on.map(function(i){return SH[i.id]||i.name}).join('·')+')');
 if(nr.length)a.push('문턱 바로 앞 '+nr.length+'개('+nr.map(function(i){var r=ratio(i);return (SH[i.id]||i.name)+(r>0&&r<1.5?' '+Math.round(r*100)+'%':'')}).join(' · ')+')');
 return a.join(' + ')+(nr.length?' — 켜지기 직전인 불까지 미리 더한 경고입니다.':'.')}
function put(after,cls){if(!after)return;var n=after.nextElementSibling;var t=text();if(!t)return;if(n&&n.classList.contains('mm-why')){if(n.dataset.t!==t){n.dataset.t=t;n.lastChild.textContent=t}return}
 var e=document.createElement('p');e.className='mm-why '+(cls||'');e.dataset.t=t;var b=document.createElement('b');b.textContent='왜 이 단계?';e.appendChild(b);e.appendChild(document.createTextNode(t));after.after(e)}
function run(){if(!F)return;
 if(P==='opt'){var st=document.querySelector('.o-top .o-st');if(st)put(st.closest('.o-top'),'top');put(document.querySelector('#bt-card .mm-bs-n'))}
 else put(document.querySelector('#lights-card .mm-bd-sc .r'))}
fetch('d/lights/fresh.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).then(function(j){F=j;var k=0;(function go(){try{run()}catch(e){}if(++k<30)setTimeout(go,500)})()}).catch(function(){});
})();
