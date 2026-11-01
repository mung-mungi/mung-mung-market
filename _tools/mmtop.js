// 시장 경고등 맨 위 '한눈에'(사용자 2026-11-01): 지금 시장은 한 줄 → 층위별 신호등 6칸(누르면 아래로 상세) → 업종 회전 지도(점·타일 누르면 관련 기업)
// 자료: d/stress/stress.json(build_stress.py, Actions) + d/lights/fresh.json. 위험 쪽 점수 0 평온~100 불안, 심리 쪽 0 공포~100 환희
(function(){
var S=null,F=null,OPEN=null,SEL=null,VIEW='map',HL=['SOXX','XLK'];
var EN={SOXX:'Semiconductors',XLK:'Technology',XLC:'Communication Services',XLY:'Consumer Discretionary',XLI:'Industrials',XLF:'Financials',XLE:'Energy',XLV:'Health Care',XLP:'Consumer Staples',XLU:'Utilities'};
function j(u){return fetch(u+'?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function md(d){if(!d)return'';var a=String(d).split('-');return a.length===3?(+a[1])+'/'+(+a[2]):d}
function sg(v,n){return v==null?'—':(v>0?'+':v<0?'−':'')+Math.abs(v).toFixed(n==null?1:n)}
function risk(p){return p==null?['자료 대기','#8a857a']:p<55?['평온','#2e9d5b']:p<70?['주의','#c99a06']:p<85?['불안 커짐','#e07b16']:['위험','#b3261e']}
function emo(p){return p==null?['자료 대기','#8a857a']:p<25?['극단적 공포','#1f4e9a']:p<45?['공포','#2f5fa8']:p<55?['중립','#8a857a']:p<75?['낙관','#e8913a']:['환희','#d0451b']}
function stg(s){return {'평온':'#2e9d5b','주의':'#c99a06','경계':'#e07b16','긴장':'#c8501c','위험':'#b3261e'}[s]||'#8a857a'}
var CH={ofr:['빠름·예민','fast'],stlfsi:['균형','bal'],nfci:['느긋·관대','slow'],anfci:['경기 걸러낸 판','bal'],kcfsi:['느림·월간','slow'],vix:['가장 빠름','fast'],move:['빠름·예민','fast'],cnn:['대중·역발상','ctr'],aaii:['잡음 큼·역발상','ctr'],bofa_bb:['역발상','ctr'],bofa_fms:['역발상','ctr']};
var ENDS={cnn:['0~25 극단적 공포','50','75~100 극단적 탐욕'],aaii:['약세가 20%p 이상 많음','평소','강세가 20%p 이상 많음'],bofa_bb:['0~2 극단적 비관 · 살 때','5 중립','8~10 극단적 낙관 · 팔 때'],bofa_fms:['5% 이상 · 겁먹음','4.5%','4% 아래 · 너무 낙관']};
var HOW={cnn:'숫자가 작을수록 겁먹은 것',aaii:'"앞으로 6개월 내린다" 응답이 많을수록 겁먹은 것',bofa_bb:'숫자가 클수록 들뜬 것',bofa_fms:'현금이 적을수록 들뜬 것(살 돈이 남지 않음)'};
function I(id){return (S.items||[]).filter(function(x){return x.id===id})[0]}
function val(x){if(!x)return'—';var v=x.value;if(x.id==='cnn')return Math.round(v)+'';if(x.id==='aaii')return '약세 '+v+'%';if(x.unit==='%')return v+'%';if(x.unit==='/10')return v+' / 10';return (typeof v==='number'?(Math.abs(v)<10?v.toFixed(2):v.toFixed(1)):v)+''}
var NM={ofr:'OFR 금융 스트레스',stlfsi:'세인트루이스 연은 스트레스',nfci:'시카고 연은 금융여건',anfci:'시카고 연은 조정 금융여건',kcfsi:'캔자스시티 연은 스트레스',vix:'VIX 주식 변동성',move:'MOVE 채권 변동성',cnn:'CNN 공포·탐욕',aaii:'AAII 개인 설문',bofa_bb:'BofA 강세·약세',bofa_fms:'BofA 펀드매니저 현금'};
function barRow(x,isEmo){var r=el('div','mm-st-row');var h=el('div','h');h.appendChild(el('b','',NM[x.id]||(x.org+' '+x.name)));var c=CH[x.id];if(c)h.appendChild(el('span','mm-st-chip '+c[1],c[0]));if(x.freq)h.appendChild(el('span','mm-st-chip fq',x.freq.replace('(기사)','')));
 var v=el('span','v',val(x));v.appendChild(el('small','',md(x.date)));h.appendChild(v);r.appendChild(h);
 var p=isEmo?x.emo:x.pct;var col=isEmo?emo(p)[1]:risk(p)[1];var b=el('div','mm-st-bar'+(isEmo?' emo':''));b.style.setProperty('--c',col);var i=el('i');i.style.left=Math.max(2,Math.min(98,p||0))+'%';b.appendChild(i);var em=el('em','',isEmo?(emo(p)[0]+' '+p):p+'');em.style.left=Math.max(8,Math.min(92,p||0))+'%';b.appendChild(em);r.appendChild(b);
 var e=ENDS[x.id];var ends=el('div','mm-st-ends');(e||['10년 중 가장 평온','평소','가장 불안']).forEach(function(t){ends.appendChild(el('span','',t))});r.appendChild(ends);
 var tx=(HOW[x.id]?'<b>'+HOW[x.id]+'</b> · ':'')+(x.read||'');if(x.parts){var ps=Object.keys(x.parts).map(function(k){return k+' '+sg(x.parts[k],2)});tx+=' · 영역별: '+ps.join(', ')}
 var pp=el('p');pp.innerHTML=tx.replace(/</g,'&lt;').replace(/&lt;b>/g,'<b>').replace(/&lt;\/b>/g,'</b>');r.appendChild(pp);return r}
function panelSystem(d){d.appendChild(el('h3','','금융 시스템은 멀쩡한가'));d.appendChild(el('p','s','연준·재무부가 수십~백여 개 지표를 묶은 공식 지수. 눈금이 달라 \'최근 10년 중 몇 % 자리\'로 맞췄습니다(0 평온 · 50 평소 · 100 가장 불안).'));
 var OR=['ofr','stlfsi','nfci','anfci','kcfsi'];(S.items||[]).filter(function(x){return x.kind==='official'}).sort(function(a,b){return OR.indexOf(a.id)-OR.indexOf(b.id)}).forEach(function(x){d.appendChild(barRow(x))});
 var lim=new Date(Date.now()-40*864e5).toISOString().slice(0,10);var sub=(S.items||[]).filter(function(x){return x.kind==='sub'&&x.date>=lim});if(sub.length){d.appendChild(el('p','mm-st-key','시카고 연은 하위지수(10년 중 % 자리): '+sub.map(function(x){return x.name.replace('NFCI ','').replace(' 하위지수','')+' '+x.pct+' ('+md(x.date)+')'}).join(' · ')))}
 d.appendChild(el('p','mm-st-key','빠름·예민 = 시장 가격으로 매일 계산, 먼저 울리지만 헛울림도 · 균형 = 금리·스프레드 중심 매주 · 느긋·관대 = 은행·그림자금융까지 100여 개, 진짜 위기가 아니면 잘 안 움직임'))}
function panelPrice(d){d.appendChild(el('h3','','시장은 얼마나 출렁일 거라 보나'));d.appendChild(el('p','s','옵션 가격에 담긴 앞으로 1달 출렁임 예상. 최근 10년 중 몇 % 자리인지로 봅니다.'));['vix','move'].forEach(function(k){var x=I(k);if(x)d.appendChild(barRow(x))});
 var v=I('vix'),m=I('move');if(v&&m)d.appendChild(el('div','mm-st-say',(m.pct>v.pct?'채권 쪽 흔들림(MOVE '+m.value+')이 주식(VIX '+v.value+')보다 앞서 있습니다 — 금리 불안이 먼저입니다.':'주식 쪽 흔들림(VIX '+v.value+')이 채권(MOVE '+m.value+')보다 앞서 있습니다.')))}
function panelEmo(d,who){var ids=who==='retail'?['cnn','aaii']:['bofa_bb','bofa_fms'];var sc=S.scores||{};
 d.appendChild(el('h3','',who==='retail'?'개인은 겁먹었나, 들떴나':'기관은 겁먹었나, 들떴나'));d.appendChild(el('p','s','모두 같은 눈금 — 왼쪽 파랑 공포 ◀ 중립 ▶ 오른쪽 주황 환희. 끝으로 갈수록 거꾸로 읽습니다(모두 겁먹으면 바닥 근처, 모두 들뜨면 꼭지 근처).'));
 var vs=el('div','mm-st-vs');[['개인',sc.retail],['기관',sc.inst]].forEach(function(a){var e=emo(a[1]);var c=el('div');c.style.setProperty('--c',e[1]);c.style.setProperty('--b',a[1]<45?'#edf2fa':a[1]>=55?'#fdeee6':'#f1ede4');c.appendChild(el('i','',a[0]));c.appendChild(el('b','',a[1]==null?'—':a[1]+''));c.appendChild(el('small','',e[0]));vs.appendChild(c)});d.appendChild(vs);
 ids.forEach(function(k){var x=I(k);if(x)d.appendChild(barRow(x,true))});
 d.appendChild(el('div','mm-st-say',mix(sc)));d.appendChild(el('p','mm-st-key','BofA·AAII는 원자료가 비공개·유료라 새벽 브리핑이 기사에서 옮겨 적습니다(주 1회 안팎). 점수는 각 지표 눈금을 0~100으로 옮긴 환산값입니다.'))}
function mix(sc){var r=sc.retail,i=sc.inst;if(r==null||i==null)return'';if(r<45&&i>=55)return'개인 공포 + 기관 낙관 = 아직 바닥 신호는 아닙니다. 기관이 비중을 줄이기 시작하면(기관 점수가 50 쪽으로 내려오면) 한 번 더 흔들릴 수 있는 자리입니다.';if(r<45&&i<45)return'개인·기관 모두 겁먹었습니다 — 역사적으로 바닥 근처에서 자주 나온 조합입니다.';if(r>=55&&i>=55)return'개인·기관 모두 들떴습니다 — 꼭지 근처에서 자주 나온 조합이라 조심할 자리입니다.';return'개인과 기관 심리가 한쪽으로 쏠리지 않았습니다.'}
function secCol(x,y){return x>=0&&y>=0?'#2e7d4f':x>=0?'#c99a06':y<0?'#b3261e':'#2f5fa8'}
function quad(x,y){return x>=0&&y>=0?'선도':x>=0?'약해지는 중':y<0?'소외':'살아나는 중'}
function mapSvg(){var SE=S.sectors||[];var W=358,H=330,m=8;var xs=[],ys=[];SE.forEach(function(s){s.trail.forEach(function(p){xs.push(p[0]);ys.push(p[1])})});
 var x0=Math.min(-10,Math.min.apply(null,xs)-2),x1=Math.max(10,Math.max.apply(null,xs)+2),ya=Math.max(12,Math.max.apply(null,ys.map(Math.abs))+2);
 var X=function(v){return m+(v-x0)/(x1-x0)*(W-2*m)},Y=function(v){return m+(ya-v)/(2*ya)*(H-2*m)};var cx=X(0),cy=Y(0);
 var s='<svg viewBox="0 0 '+W+' '+H+'" font-family="-apple-system,Apple SD Gothic Neo,sans-serif">';
 s+='<rect x="'+cx+'" y="'+m+'" width="'+(W-m-cx)+'" height="'+(cy-m)+'" fill="#e7f3ec"/><rect x="'+cx+'" y="'+cy+'" width="'+(W-m-cx)+'" height="'+(H-m-cy)+'" fill="#fbf4dc"/><rect x="'+m+'" y="'+cy+'" width="'+(cx-m)+'" height="'+(H-m-cy)+'" fill="#fbe8e5"/><rect x="'+m+'" y="'+m+'" width="'+(cx-m)+'" height="'+(cy-m)+'" fill="#edf2fa"/>';
 [[W-m-6,m+18,'end','#2e7d4f','선도'],[W-m-6,H-m-8,'end','#8a6a00','약해지는 중'],[m+6,H-m-8,'start','#b3261e','소외'],[m+6,m+18,'start','#2f5fa8','살아나는 중']].forEach(function(a){s+='<text x="'+a[0]+'" y="'+a[1]+'" text-anchor="'+a[2]+'" font-size="14" font-weight="800" fill="'+a[3]+'" opacity=".85">'+a[4]+'</text>'});
 s+='<line x1="'+cx+'" y1="'+m+'" x2="'+cx+'" y2="'+(H-m)+'" stroke="#b9b1a2" stroke-dasharray="3 3"/><line x1="'+m+'" y1="'+cy+'" x2="'+(W-m)+'" y2="'+cy+'" stroke="#b9b1a2" stroke-dasharray="3 3"/>';
 var on=function(t){return HL.indexOf(t)>=0||SEL===t};
 SE.slice().sort(function(a,b){return (on(a.t)?1:0)-(on(b.t)?1:0)}).forEach(function(se){var p=se.trail,l=p[p.length-1],c=secCol(l[0],l[1]),b=on(se.t);var pts=p.map(function(q){return X(q[0]).toFixed(1)+','+Y(q[1]).toFixed(1)}).join(' ');
  s+='<polyline points="'+pts+'" fill="none" stroke="'+(b?c:'#b9b1a2')+'" stroke-width="'+(b?3.2:1.2)+'" stroke-opacity="'+(b?.85:.35)+'" stroke-linecap="round" stroke-linejoin="round"/>';
  if(b)p.slice(0,-1).forEach(function(q,i){s+='<circle cx="'+X(q[0]).toFixed(1)+'" cy="'+Y(q[1]).toFixed(1)+'" r="'+(2+i*0.5)+'" fill="'+c+'" opacity=".7"/>'})});
 var placed=[];function hit(a){return placed.some(function(b){return a.x0<b.x1&&a.x1>b.x0&&a.y0<b.y1&&a.y1>b.y0})}
 var pts=SE.map(function(se){var l=se.trail[se.trail.length-1];return {se:se,c:secCol(l[0],l[1]),px:X(l[0]),py:Y(l[1]),big:on(se.t)}});
 pts.forEach(function(p){placed.push({x0:p.px-7,x1:p.px+7,y0:p.py-7,y1:p.py+7})});
 pts.sort(function(a,b){return (b.big?1:0)-(a.big?1:0)||a.py-b.py}).forEach(function(p){if(!p.big)return;var fs=p.big?13.5:12,tw=p.se.n.length*fs*0.98+4,best=null;
  [[1,0],[-1,0],[1,-13],[-1,-13],[1,13],[-1,13],[0,-16],[0,18]].some(function(o){var ax=o[0]===1?p.px+9:o[0]===-1?p.px-9-tw:p.px-tw/2,ay=p.py+4+o[1];if(ax<10||ax+tw>W-10)return false;var bb={x0:ax,x1:ax+tw,y0:ay-fs+2,y1:ay+3};if(!hit(bb)){best={x:ax,y:ay,bb:bb};return true}return false});
  if(!best){var ax2=Math.min(W-10-tw,Math.max(10,p.px+9));best={x:ax2,y:p.py+4,bb:{x0:ax2,x1:ax2+tw,y0:p.py-8,y1:p.py+7}}}placed.push(best.bb);p.lx=best.x;p.ly=best.y});
 pts.forEach(function(p){var se=p.se,sel=SEL===se.t;
  s+='<g class="dot'+(sel?' sel':'')+'" data-t="'+se.t+'" role="button"><circle cx="'+p.px.toFixed(1)+'" cy="'+p.py.toFixed(1)+'" r="16" fill="transparent"/>'+(sel?'<circle cx="'+p.px.toFixed(1)+'" cy="'+p.py.toFixed(1)+'" r="13" fill="none" stroke="#262626" stroke-width="2.5"/>':'')+'<circle cx="'+p.px.toFixed(1)+'" cy="'+p.py.toFixed(1)+'" r="'+(sel?8:p.big?7.5:4.5)+'" fill="'+(p.big?p.c:'#c9c3b6')+'" stroke="#fff" stroke-width="2"/>'+(p.big?'<text x="'+p.lx.toFixed(1)+'" y="'+p.ly.toFixed(1)+'" font-size="14" font-weight="800" fill="#262626" paint-order="stroke" stroke="#fff" stroke-width="3">'+se.n+'</text>':'')+'</g>'});
 return s+'</svg>'}
function tileCol(m){return m<=-10?['#b3261e','#fff']:m<=-5?['#e06a55','#fff']:m<0?['#f2c4ba','#262626']:m<5?['#bfe3ca','#262626']:m<10?['#4fae73','#fff']:['#2e7d4f','#fff']}
function panelSector(d){var sc=S.scores||{};d.appendChild(el('h3','','돈은 어디서 빠져서 어디로 갔나'));
 d.appendChild(el('p','s','가로 = 최근 3달 S&P보다 강했나 · 세로 = 최근 1달 힘이 붙었나 · 굵은 선 = 지난 4주 지나온 길. 아래 업종 버튼을 누르면 그 업종이 굵게 뜨고, 점이나 타일을 누르면 관련 기업이 열립니다.'));
 var tg=el('div','mm-st-tog');[['map','회전 지도'],['tile','타일']].forEach(function(a){var b=el('button',VIEW===a[0]?'on':'',a[1]);b.type='button';b.onclick=function(e){e.stopPropagation();VIEW=a[0];draw()};tg.appendChild(b)});d.appendChild(tg);
 if(VIEW==='map'){var cp=el('div','mm-st-chips');(S.sectors||[]).forEach(function(se){var l=se.trail[se.trail.length-1],c=secCol(l[0],l[1]);var b=el('button',HL.indexOf(se.t)>=0?'on':'',se.n);b.type='button';b.style.setProperty('--c',c);b.onclick=function(e){e.stopPropagation();var i=HL.indexOf(se.t);if(i>=0)HL.splice(i,1);else HL.push(se.t);draw()};cp.appendChild(b)});
  var ab=el('button','all',HL.length>=(S.sectors||[]).length?'기본(반도체·기술)':'전체 보기');ab.type='button';ab.onclick=function(e){e.stopPropagation();HL=HL.length>=(S.sectors||[]).length?['SOXX','XLK']:(S.sectors||[]).map(function(x){return x.t});draw()};cp.appendChild(ab);d.appendChild(cp);
  var mp=el('div','mm-st-map');mp.innerHTML=mapSvg();d.appendChild(mp);var ax=el('div','mm-st-ax');ax.appendChild(el('span','','◀ 3달 동안 약했음'));ax.appendChild(el('span','','3달 동안 강했음 ▶'));d.appendChild(ax);
  mp.querySelectorAll('.dot').forEach(function(g){g.addEventListener('click',function(e){e.stopPropagation();var t=g.dataset.t;SEL=SEL===t?null:t;if(SEL&&HL.indexOf(t)<0)HL.push(t);draw()})})}
 else{var tl=el('div','mm-st-tiles');(S.sectors||[]).slice().sort(function(a,b){return a.m1-b.m1}).forEach(function(se){var c=tileCol(se.m1);var b=el('button','mm-st-tile'+(SEL===se.t?' sel':''));b.type='button';b.style.background=c[0];b.style.color=c[1];b.appendChild(el('b','',se.n));b.appendChild(el('span','',sg(se.m1)+'%'));b.appendChild(el('small','','고점 '+sg(se.dd,0)+'%'));b.onclick=function(e){e.stopPropagation();SEL=SEL===se.t?null:se.t;draw()};tl.appendChild(b)});
  if(sc.spy_m1!=null){var sp=el('div','mm-st-tile');sp.style.background='#ece9e2';sp.appendChild(el('b','','S&P'));sp.appendChild(el('span','',sg(sc.spy_m1)+'%'));sp.appendChild(el('small','','지수'));tl.appendChild(sp)}d.appendChild(tl)}
 if(SEL)d.appendChild(compBox(SEL));else d.appendChild(el('div','mm-st-say',secSay(sc)))}
function secSay(sc){var SE=S.sectors||[];if(sc.atk==null||sc.def==null)return'';var g=sc.def-sc.atk;var lead=SE.filter(function(x){var l=x.trail[x.trail.length-1];return l[0]>=0&&l[1]>=0}).map(function(x){return x.n}),out=SE.filter(function(x){var l=x.trail[x.trail.length-1];return l[0]<0&&l[1]<0}).map(function(x){return x.n});
 return '최근 1달 공격 업종 '+sg(sc.atk)+'% vs 방어 업종 '+sg(sc.def)+'%'+(sc.spy_m1!=null?' (S&P '+sg(sc.spy_m1)+'%)':'')+'. '+(g>=8?'돈이 방어 업종으로 숨었습니다. ':g<=-8?'돈이 공격 업종으로 몰리고 있습니다. ':'업종 흐름이 크게 갈리지 않았습니다. ')+(lead.length?'선도: '+lead.join('·')+'. ':'')+(out.length?'소외: '+out.join('·')+'.':'')}
function compBox(t){var se=(S.sectors||[]).filter(function(x){return x.t===t})[0];var cs=(S.comps||{})[t]||[];var w=el('div','mm-st-co');if(!se)return w;var l=se.trail[se.trail.length-1],f=se.trail[0],c=secCol(l[0],l[1]);
 var ch=el('div','ch');var dt=el('span');dt.style.cssText='flex:0 0 14px;display:block;width:14px;height:14px;min-width:14px;max-width:14px;border-radius:50%;padding:0;background:'+c;ch.appendChild(dt);var hb=el('b','',se.n+' 관련 기업');if(EN[t]){var en=el('small','',' · '+EN[t]);en.style.cssText='font:600 12px sans-serif;color:#8a857a';hb.appendChild(en)}ch.appendChild(hb);var bd=el('span','',quad(l[0],l[1])+(quad(f[0],f[1])!==quad(l[0],l[1])?' · 4주 전 '+quad(f[0],f[1]):''));bd.style.setProperty('--c',c);bd.style.setProperty('--b',c==='#2e7d4f'?'#e7f3ec':c==='#c99a06'?'#fbf4dc':c==='#b3261e'?'#fbe8e5':'#edf2fa');ch.appendChild(bd);w.appendChild(ch);
 var sm=el('div','sum');[['업종 1달',sg(se.m1)+'%'],['고점 대비',sg(se.dd,0)+'%'],['S&P보다',(S.scores&&S.scores.spy_m1!=null?sg(se.m1-S.scores.spy_m1)+'%p':'—')]].forEach(function(a){var d=el('div');d.appendChild(el('small','',a[0]));var b=el('b','',a[1]);b.style.color=a[1].indexOf('−')===0?'#b3261e':'#2e7d4f';d.appendChild(b);sm.appendChild(d)});w.appendChild(sm);
 if(cs.length){var up=cs.filter(function(x){return x.m1>0}).length;var best=cs[cs.length-1],worst=cs[0];w.appendChild(el('div','mm-st-say',cs.length+'곳 중 '+up+'곳 상승 · 가장 강한 곳 '+best.n+' '+sg(best.m1)+'% · 가장 약한 곳 '+worst.n+' '+sg(worst.m1)+'%'))}
 var mx=Math.max.apply(null,cs.map(function(x){return Math.abs(x.m1)}).concat([5]));
 cs.slice().sort(function(a,b){return b.m1-a.m1}).forEach(function(x){var r=el('div','mm-st-cr');var nm=el('div','nm');nm.appendChild(el('b','',x.n));nm.appendChild(el('small','',x.t+' · '+x.r));r.appendChild(nm);var br=el('div','br');var i=el('i');var col=x.m1<=-20?'#b3261e':x.m1<=-10?'#e06a55':x.m1<0?'#c99a06':x.m1<10?'#4fae73':'#2e7d4f';i.style.background=col;var wd=Math.abs(x.m1)/mx*50;if(x.m1<0){i.style.right='50%';i.style.width=wd+'%'}else{i.style.left='50%';i.style.width=wd+'%'}br.appendChild(i);var mid=el('i');mid.style.cssText='left:50%;width:1px;background:#cfc8ba';br.appendChild(mid);r.appendChild(br);var v=el('div','v',sg(x.m1)+'%');v.style.color=col;v.appendChild(el('small','','하루 '+sg(x.d1)+'%'));r.appendChild(v);w.appendChild(r)});
 var lk=el('div','mm-st-links');[['📈 종목 차트','p-trend.html'],['🧾 실적 결과','p-earn.html'],['🎯 목표주가','p-targets.html'],['🩳 공매도','p-short.html']].forEach(function(a){var x=el('a','',a[0]);x.href=a[1];lk.appendChild(x)});w.appendChild(lk);w.appendChild(el('p','mm-st-key','1달 등락 순 · 막대 가운데 선 기준 왼쪽 하락, 오른쪽 상승'));return w}
function draw(){var root=document.querySelector('.mm-st');var mast=document.querySelector('.lw-mast');if(!S||!mast)return;if(!root){root=el('section','mm-st');mast.after(root)}root.textContent='';
 var sc=S.scores||{};var date=(I('vix')||{}).date||'';
 var hd=el('div','mm-st-head');hd.appendChild(el('small','','지금 시장은 · '+md(date)+' 마감'));var r=sc.retail,i=sc.inst,g=(sc.def!=null&&sc.atk!=null)?sc.def-sc.atk:0;
 var a=(r<45&&i>=55)?'개인은 겁먹고 기관은 아직 낙관':(r<45&&i<45)?'개인·기관 모두 겁먹음':(r>=55&&i>=55)?'개인·기관 모두 들뜸':'개인 '+emo(r)[0]+' · 기관 '+emo(i)[0];
 var worst=(S.sectors||[]).slice().sort(function(x,y){return x.m1-y.m1})[0];var b=g>=8?'돈은 '+(worst?worst.n:'공격 업종')+'에서 방어 업종으로 숨었습니다':g<=-8?'돈이 공격 업종으로 몰립니다':'업종 흐름은 고릅니다';
 hd.appendChild(el('b','',a+' — '+b));root.appendChild(hd);
 var gr=el('div','mm-st-g');var lightsOn=F?F.on:null,near=F&&F.near?F.near.length:0;var vix=I('vix'),mv=I('move'),cnn=I('cnn'),aa=I('aaii'),bb=I('bofa_bb'),fm=I('bofa_fms');
 var T=[['system','금융 시스템',risk(sc.system),'공식 지수 '+(S.items||[]).filter(function(x){return x.kind==='official'}).length+'개 · '+sc.system+'점'],
  ['price','시장 가격',risk(sc.price),'VIX '+(vix?vix.value:'—')+' · MOVE '+(mv?mv.value:'—')],
  ['retail','개인 심리',emo(sc.retail),'CNN '+(cnn?Math.round(cnn.value):'—')+' · AAII 약세 '+(aa?aa.value+'%':'—')],
  ['inst','기관 심리',emo(sc.inst),'BofA '+(bb?bb.value:'—')+' · 현금 '+(fm?fm.value+'%':'—')],
  ['sector','업종 쏠림',g>=8?['방어로 대피','#b3261e']:g>=4?['방어 쏠림','#e07b16']:g<=-8?['공격 쏠림','#e07b16']:['고른 흐름','#2e9d5b'],'공격 '+sg(sc.atk)+'% · 방어 '+sg(sc.def)+'%'],
  ['lights','우리 경고등',[F?F.stage:'—',stg(F&&F.stage)],'불 '+(lightsOn==null?'—':lightsOn)+'개 · 근접 '+near]];
 T.forEach(function(t){var bt=el('button','mm-st-t'+(OPEN===t[0]?' on':''));bt.type='button';bt.style.setProperty('--c',t[2][1]);var tp=el('div','tp');tp.appendChild(el('i'));tp.appendChild(document.createTextNode(t[1]));bt.appendChild(tp);bt.appendChild(el('div','st',t[2][0]));bt.appendChild(el('div','sm',t[3]));
  bt.onclick=function(){if(t[0]==='lights'){var bg=document.getElementById('big');if(bg)bg.scrollIntoView({behavior:'smooth',block:'start'});return}OPEN=OPEN===t[0]?null:t[0];draw();if(OPEN){var d=document.querySelector('.mm-st-d.on');if(d)setTimeout(function(){var y=d.getBoundingClientRect().top;if(y>window.innerHeight*0.7)window.scrollBy({top:y-window.innerHeight*0.35,behavior:'smooth'})},30)}};gr.appendChild(bt)});root.appendChild(gr);
 if(!OPEN)root.appendChild(el('p','mm-st-cap','칸을 누르면 바로 아래에 자세히 펼쳐집니다 · 우리 경고등은 아래 카드로 이동'));
 var d=el('div','mm-st-d'+(OPEN?' on':''));if(OPEN==='system')panelSystem(d);else if(OPEN==='price')panelPrice(d);else if(OPEN==='retail')panelEmo(d,'retail');else if(OPEN==='inst')panelEmo(d,'inst');else if(OPEN==='sector')panelSector(d);root.appendChild(d)}
Promise.all([j('d/stress/stress.json'),j('d/lights/fresh.json')]).then(function(a){S=a[0];F=a[1];var k=0;(function go(){try{draw()}catch(e){}if(!document.querySelector('.mm-st')&&++k<20)setTimeout(go,300)})()})
})();
