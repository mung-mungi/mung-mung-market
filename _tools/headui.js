// 페이지 맨 위 '오늘 한눈에' 양식 통일(사용자 2026-10-29): 날짜 칩 모양, 본문 글자, 바로가기 줄은 배너 아래로
(function(){function fx(){
 document.querySelectorAll('.mm-take').forEach(function(t){if(t.classList.contains('np')||t.classList.contains('tk-on')||t.classList.contains('o-on'))return;t.classList.add('hu');
  var f=t.firstElementChild;if(f&&f.tagName==='B'&&!f.classList.contains('mm-chipx')&&/\d/.test(f.textContent)&&/(기준|집계|마감|잠정|월|일)/.test(f.textContent)&&f.textContent.length<40)f.classList.add('mm-chipx');
});
 var hero=document.querySelector('.mm-hero');if(hero){document.querySelectorAll('nav[class$="-nav"]:not(.ib)').forEach(function(n){if(n.dataset.hu)return;if(n.compareDocumentPosition(hero)&Node.DOCUMENT_POSITION_FOLLOWING){n.dataset.hu=1;var t=document.querySelector('.mm-take');(t&&t.nextElementSibling&&t.nextElementSibling.classList.contains('hu-more')?t.nextElementSibling:(t||hero)).after(n)}})}}
var k=0;(function go(){try{fx()}catch(e){}if(++k<12)setTimeout(go,500)})()})();

// 테크 행사 '오늘 한눈에': 이번 주 · 한 줄 평 · 다음 행사 3줄(사용자 2026-10-29)
(function(){function fx(){var t=document.querySelector('#take.pg-take');if(!t||t.querySelector('.tg3'))return;var chip=t.querySelector(':scope>b:first-child');var tx=t.textContent.replace(chip?chip.textContent:'','').replace(/\s+/g,' ').trim();
 var nx=(tx.match(/다음 큰 행사는\s*(.+?)입니다/)||[])[1];var m=tx.match(/^이번 주\s*(.+?)(?:이|가)? 열리는 가운데\s*(.+?)(?:이|가) 한꺼번에 나와\s*(.+?)\./);if(!nx||!m)return;
 function split(s){return s.split(/,\s*|과\s+|와\s+/).map(function(x){return x.trim()}).filter(Boolean)}
 function chips(l,date){return '<span class="chips">'+l.map(function(x){var d=date&&x.match(/^(\d+\/\d+)\s+(.+)$/);return '<span>'+(d?'<em>'+d[1]+'</em>'+d[2]:x)+'</span>'}).join('')+'</span>'}
 var ul=document.createElement('ul');ul.className='tg3';ul.innerHTML='<li><i>이번 주</i><span>'+chips([m[1]].concat(split(m[2])))+'</span></li><li><i>한 줄 평</i><span><b class="k">'+m[3]+'</b></span></li><li><i>다음 행사</i><span>'+chips(split(nx),1)+'</span></li>';t.appendChild(ul);t.classList.add('tg-rows')}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,500)})()})();
