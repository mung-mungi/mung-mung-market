// 시황 '공포·탐욕 지수' 막대를 시장 경고등 '공포 ↔ 환희' 막대와 같은 보는 법으로(사용자 2026-11-02)
// 왼쪽 파랑 = 겁먹음 · 오른쪽 주황 = 들뜸, 눈금 25 극단 공포 · 50 중립(진한 눈금) · 75 극단 탐욕. 숫자 색도 같은 규칙.
(function(){try{
if(!/p-brief\.html/.test(location.pathname))return;
function emo(p){return p<25?'#1f4e9a':p<45?'#2f5fa8':p<55?'#8a857a':p<75?'#e8913a':'#d0451b'}
function fix(){var box=document.getElementById('mood');if(!box)return;var mb=box.querySelector('.mb'),ml=box.querySelector('.ml'),mv=box.querySelector('.mv');if(!mb||!ml)return;
 if(mb.classList.contains('mm-fg')&&mb.querySelector('.mm-fg-t'))return;
 mb.classList.add('mm-fg');ml.classList.add('mm-fg');var em=mb.querySelector('em');var v=em?parseFloat(em.style.left):NaN;
 [[25,''],[50,'avg'],[75,'']].forEach(function(t){var e=document.createElement('i');e.className='mm-fg-t '+t[1];e.style.left=t[0]+'%';mb.appendChild(e)});
 ml.textContent='';[[25,'극단 공포',''],[50,'중립','avg'],[75,'극단 탐욕','']].forEach(function(t){var s=document.createElement('span');s.className=t[2];s.style.left=t[0]+'%';s.textContent=t[1];ml.appendChild(s)});
 if(!box.querySelector('.mm-fg-cap')){var c=document.createElement('p');c.className='mm-fg-cap';c.textContent='왼쪽(파랑) = 겁먹음 · 오른쪽(주황) = 들뜸 · 경고등 페이지와 같은 방향';ml.after(c)}
 if(!isNaN(v)){var col=emo(v);if(em)em.style.borderColor=col;if(mv)mv.style.color=col}}
var k=0;(function t(){fix();if(++k<20)setTimeout(t,500)})();
var m=document.getElementById('mood');if(m&&window.MutationObserver)new MutationObserver(function(){setTimeout(fix,30)}).observe(m,{childList:true});
// 기사 칸 '시장 경고등 · 🟡 주의 · 불 1/10' 알약을 점수로(사용자 2026-11-02 '진행') — 브리핑이 쓴 불 개수 표기는 점수제 이전 방식이라 같은 날 점수와 단계가 어긋남
// 시황 날짜 D의 기준 = D보다 앞선 마지막 미국 마감일 점수(d/lights/fresh.json score_hist)
var SH=null,BC=[[0,'#2e9d5b','평온','🟢'],[3,'#c99a06','주의','🟡'],[4.5,'#e07b16','경계','🟠'],[6,'#c8501c','긴장','🟠'],[7.5,'#b3261e','위험','🔴']];
function lts(){if(!SH)return;document.querySelectorAll('#days .bf-day').forEach(function(c){var L=c.querySelector('.bf-lights');if(!L||L.dataset.sc)return;var D=c.id.replace('day-','');
 var m=L.textContent.match(/(\d{1,2})\/(\d{1,2})\s*마감/),k=-1;
 if(m){var t=D.slice(0,4)+'-'+('0'+m[1]).slice(-2)+'-'+('0'+m[2]).slice(-2);for(var i=0;i<SH.length;i++)if(SH[i][0]===t)k=i}
 if(k<0)for(var i=0;i<SH.length;i++)if(SH[i][0]<D)k=i;if(k<0)return;
 var v=SH[k][1],b=BC[0];BC.forEach(function(x){if(v>=x[0])b=x});var dd=k>0?Math.round((v-SH[k-1][1])*10)/10:0;
 L.dataset.sc=1;L.style.setProperty('--lc',b[1]);L.textContent='시장 경고등 · '+b[3]+' '+b[2]+' · '+v.toFixed(1)+'/12점'+(dd?(dd>0?' ▲':' ▼')+Math.abs(dd).toFixed(1):'');
 var sm=document.createElement('small');sm.textContent=(+SH[k][0].slice(5,7))+'/'+(+SH[k][0].slice(8))+' 마감 기준';L.appendChild(sm)})}
fetch('d/lights/fresh.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j||!j.score_hist)return;SH=j.score_hist;var q=0;(function t(){lts();if(++q<20)setTimeout(t,500)})();var d=document.getElementById('days');if(d&&window.MutationObserver)new MutationObserver(function(){clearTimeout(lts.t);lts.t=setTimeout(lts,60)}).observe(d,{childList:true,subtree:true})}).catch(function(){});
}catch(e){}})();
