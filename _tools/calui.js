// 실적 일정 맨 위 요약(이번 주·오늘·아시아 추적)을 칸·줄 맞춘 모양으로(사용자 2026-10-29)
(function(){function fx(){var n=document.getElementById('next');if(!n)return;var t=n.textContent;if(n.dataset.sig===t)return;var d=[].slice.call(n.children);if(d.length<2)return;
 function part(i){var x=d[i];if(!x)return null;var b=x.querySelector('b');return {k:b?b.textContent.trim():'',v:x.textContent.replace(b?b.textContent:'','').trim()}}
 var w=part(0),td=part(1),as=part(2);var wN=(w&&w.v.match(/(\d+)곳/)||[])[1],tN=(td&&td.v.match(/(\d+)곳/)||[])[1];
 var slots=td?(td.v.match(/(장후|아시아|장전)\s*([\d:]+~?)/g)||[]):[];
 var items=as?as.v.split(/\s*·\s*/).map(function(s){var m=s.match(/^(\d+\/\d+)\s+([\d:]+)\s+(.+)$/);return m?{d:m[1],t:m[2],n:m[3]}:null}).filter(Boolean):[];
 var now=new Date(),y=now.getFullYear();
 var h='<div class="cn-top"><div class="cn-tile"><small>이번 주</small><b>'+(wN||'—')+'<i>곳</i></b></div><div class="cn-tile"><small>오늘</small><b>'+(tN||'—')+'<i>곳</i></b></div></div>';
 if(slots.length)h+='<div class="cn-sl"><small>오늘 발표 시각</small><div>'+slots.map(function(s){var m=s.match(/(장후|아시아|장전)\s*([\d:]+)/);return '<span class="'+(m[1]==='장전'?'pre':'')+'"><em>'+m[1]+'</em>'+m[2]+'</span>'}).join('')+'</div></div>';
 if(items.length)h+='<div class="cn-as"><small>아시아 실시간 추적</small><ul>'+items.map(function(it){var p=it.d.split('/'),hm=it.t.split(':');var dt=new Date(y,+p[0]-1,+p[1],+hm[0],+hm[1]);var past=dt<now;return '<li class="'+(past?'past':'')+'"><span class="d">'+it.d+'</span><span class="t">'+it.t+'</span><b>'+it.n+'</b><i>'+(past?'✓ 나옴':'예정')+'</i></li>'}).join('')+'</ul></div>';
 var box=n.querySelector('.cn');if(!box){box=document.createElement('div');box.className='cn';n.appendChild(box)}box.innerHTML=h;n.classList.add('cn-on');n.dataset.sig=n.textContent.replace(box.textContent,'')===t?t:t}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,400)})();
try{new MutationObserver(function(){try{var n=document.getElementById('next');if(n&&!n.querySelector('.cn'))fx()}catch(e){}}).observe(document.body,{childList:true,subtree:true})}catch(e){}})();
