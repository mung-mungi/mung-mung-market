// 페이지 맨 위 '오늘 한눈에' 양식 통일(사용자 2026-10-29): 날짜 칩 모양, 본문 글자, 바로가기 줄은 배너 아래로
(function(){function fx(){
 document.querySelectorAll('.mm-take').forEach(function(t){if(t.classList.contains('np')||t.classList.contains('tk-on')||t.classList.contains('o-on'))return;t.classList.add('hu');
  var f=t.firstElementChild;if(f&&f.tagName==='B'&&!f.classList.contains('mm-chipx')&&/\d/.test(f.textContent)&&/(기준|집계|마감|잠정|월|일)/.test(f.textContent)&&f.textContent.length<40)f.classList.add('mm-chipx');
});
 var hero=document.querySelector('.mm-hero');if(hero){document.querySelectorAll('nav[class$="-nav"]:not(.ib)').forEach(function(n){if(n.dataset.hu)return;if(n.compareDocumentPosition(hero)&Node.DOCUMENT_POSITION_FOLLOWING){n.dataset.hu=1;var t=document.querySelector('.mm-take');(t&&t.nextElementSibling&&t.nextElementSibling.classList.contains('hu-more')?t.nextElementSibling:(t||hero)).after(n)}})}}
var k=0;(function go(){try{fx()}catch(e){}if(++k<12)setTimeout(go,500)})()})();
