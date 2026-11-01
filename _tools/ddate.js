/* 시황 날짜 카드 머리 날짜 줄(사용자 2026-11-02) — 카드 id(day-YYYY-MM-DD)=미국 날짜, 한국에서 읽는 날=다음 날 아침 */
(function(){
var WD=['일','월','화','수','목','금','토'];
function kstToday(){var n=new Date(Date.now()+9*36e5);return Date.UTC(n.getUTCFullYear(),n.getUTCMonth(),n.getUTCDate())}
function fix(){
  var t0=kstToday();
  document.querySelectorAll('#days .bf-day').forEach(function(c){
    var h=c.querySelector(':scope>.bf-dh');if(!h)return;
    var m=/^day-(\d{4})-(\d{2})-(\d{2})$/.exec(c.id||'');if(!m)return;
    if(h.firstElementChild&&h.firstElementChild.className==='mm-dd'&&h.firstElementChild.dataset.d===c.id)return;
    var old=h.querySelector(':scope>.mm-dd');if(old)old.remove();
    var y=+m[1],mo=+m[2],d=+m[3],u=Date.UTC(y,mo-1,d),wd=new Date(u).getUTCDay();
    var pu=u+864e5,pw=new Date(pu).getUTCDay(),pd=new Date(pu);
    var bg=h.querySelector('.bf-badge.wk'),hol=bg&&/휴장/.test(bg.textContent),wk=!!bg;
    var e=document.createElement('div');e.className='mm-dd';e.dataset.d=c.id;
    var n=document.createElement('span');n.className='mm-dd-n';n.textContent=mo+'.'+String(d).padStart(2,'0');
    var w=document.createElement('span');w.className='mm-dd-w'+(wd===6?' sat':wd===0?' sun':'');w.textContent=WD[wd];
    var s=document.createElement('span');s.className='mm-dd-s';
    s.textContent=(hol?'휴장일':wk?'주말판':'미국장')+' · 한국 '+(pd.getUTCMonth()+1)+'.'+pd.getUTCDate()+'('+WD[pw]+') 아침';
    var r=document.createElement('span'),k=Math.round((t0-pu)/864e5);
    r.className='mm-dd-r'+(k<=0?' now':k>=2?' old':'');r.textContent=k<=0?'오늘 아침':k===1?'어제':k+'일 전';
    e.appendChild(n);e.appendChild(w);e.appendChild(s);e.appendChild(r);
    h.insertBefore(e,h.firstChild);
  });
}
var k=0;(function go(){fix();var d=document.getElementById('days');if(d&&!d.__ddate){d.__ddate=1;new MutationObserver(fix).observe(d,{childList:true,subtree:true})}if(++k<10)setTimeout(go,500)})();
})();
