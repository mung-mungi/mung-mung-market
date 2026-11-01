// 우리가 평소 부르는 이름으로 보이기(사용자 2026-11-02) — 화면 글자만 바꿈(원본 자료·티커는 그대로).
// 예: 알파벳 → 구글. 받침이 같은 이름끼리만 넣어야 조사(은/는·이/가)가 안 어긋남. 새 이름은 아래 M에 한 줄 추가.
(function(){try{
var M=[['알파벳','구글']];
var re=new RegExp(M.map(function(x){return x[0]}).join('|'),'g'),to={};M.forEach(function(x){to[x[0]]=x[1]});
var SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,INPUT:1,NOSCRIPT:1};
function fixText(t){var v=t.nodeValue;if(!v||v.length<2)return;re.lastIndex=0;if(!re.test(v))return;re.lastIndex=0;t.nodeValue=v.replace(re,function(m){return to[m]})}
function fix(n){if(!n)return;if(n.nodeType===3){var p=n.parentNode;if(p&&!SKIP[p.nodeName])fixText(n);return}
 if(n.nodeType!==1&&n.nodeType!==9&&n.nodeType!==11)return;if(SKIP[n.nodeName])return;
 if(n.nodeType===1&&n.textContent.indexOf(M[0][0])<0&&M.length===1)return;
 var w=document.createTreeWalker(n,4,null),t;while((t=w.nextNode())){if(!SKIP[t.parentNode.nodeName])fixText(t)}}
// perf.js가 화면 감시를 한 프레임에 한 번으로 묶으면서 바뀐 목록을 비워 넘기므로, 바뀔 때마다 전체를 가볍게 다시 훑음(0.3초에 한 번까지)
var last=0,tm=0;function sweep(){tm=0;last=Date.now();var b=document.body;if(!b||b.textContent.indexOf(M[0][0])<0)return;fix(b)}
function later(){if(tm)return;var w=Math.max(0,300-(Date.now()-last));tm=setTimeout(sweep,w)}
function go(){sweep();if(document.title)document.title=document.title.replace(re,function(m){return to[m]});
 new MutationObserver(later).observe(document.body,{childList:true,subtree:true,characterData:true});
 addEventListener('load',later);setTimeout(later,1500);setTimeout(later,4000)}
if(document.body)go();else document.addEventListener('DOMContentLoaded',go);
}catch(e){}})();
