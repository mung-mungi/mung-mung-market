// 종목 찾기 한글·별명·영문·초성(사용자 2026-11-02): '구글'→알파벳, '삼전'→삼성전자, 'nvidia'→엔비디아, 'ㅇㄴㄷㅇ'→엔비디아. 띄어쓰기 무시.
(function(){
var A={SOXX:'반도체etf 필반 필라델피아',SOXL:'속슬 레버리지 3배',NVDA:'nvidia 엔비 엔비댜',AMD:'에이엠디',INTC:'intel',AVGO:'broadcom 브컴',MRVL:'marvell 마블',
'2454.TW':'mediatek',MU:'micron',
'000660.KS':'하이닉스 닉스 skhynix hynix 에스케이하이닉스','005930.KS':'삼전 삼성 samsung',SNDK:'sandisk',WDC:'westerndigital 웨디',STX:'seagate',
'285A.T':'kioxia',SIMO:'siliconmotion','8299.TWO':'phison',TSM:'티에스엠씨 대만반도체 티섬',TSEM:'tower 타워',GFS:'globalfoundries 글파 글로벌파운드리스',
CDNS:'cadence',SNPS:'synopsys',AMAT:'appliedmaterials 어플라이드',LRCX:'lamresearch 램',KLAC:'케이엘에이',ASML:'에이에스엠엘',TER:'teradyne',CAMT:'camtek',
FORM:'formfactor',MKSI:'mks',UCTT:'ultraclean',AMKR:'amkor 앰코테크놀로지','8150.TW':'chipmos',LITE:'lumentum',COHR:'coherent',AAOI:'appliedoptoelectronics',
AXTI:'axt',FN:'fabrinet',GLW:'corning',VIAV:'viavi',ALAB:'asteralabs 아스테라',SMTC:'semtech',CRDO:'credo',RMBS:'rambus',APH:'amphenol',TEL:'teconnectivity 티이',
ANET:'arista 아리스타네트웍스',CSCO:'cisco',LUMN:'lumen',CLS:'celestica',SMCI:'supermicro 슈마 슈퍼마이크로컴퓨터',DELL:'델테크놀로지스',VRT:'vertiv',
GEV:'gevernova 지이버노바 버노바',BE:'bloomenergy 블룸',CAT:'caterpillar 캣',NVTS:'navitas',ON:'onsemi 온세미컨덕터',MPWR:'monolithicpower 엠피에스',
TXN:'texasinstruments 텍사스 티아이',PWR:'quanta 콴타',FLR:'fluor',CRWV:'coreweave 코어',NBIS:'nebius',IREN:'iren 아이리스에너지',EQIX:'equinix',
DLR:'digitalrealty',GDS:'gds',MSFT:'microsoft 마소 엠에스',GOOGL:'google 구글 alphabet',GOOG:'google 구글 alphabet',AMZN:'amazon aws 아마존웹서비스',
META:'facebook 페이스북 메타플랫폼스',ORCL:'oracle',AAPL:'apple 아이폰',TSLA:'tesla',IBM:'아이비엠',NET:'cloudflare',PLTR:'palantir 팔란',PANW:'paloalto',
NOW:'servicenow',QQQ:'큐큐큐 나스닥'};
var CH='ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ';
function cho(s){var o='';for(var i=0;i<s.length;i++){var c=s.charCodeAt(i)-44032;o+=(c>=0&&c<11172)?CH[Math.floor(c/588)]:s[i]}return o}
function nz(s){return String(s||'').toLowerCase().replace(/[\s·\-_.()]/g,'')}
window.__mmq=function(r,q){if(!q)return true;var t=String(r.ticker||''),h=nz(r.name)+' '+nz(t)+' '+nz(t.split('.')[0])+' '+nz(A[t]||''),k=nz(q);if(!k)return true;
 if(h.indexOf(k)>=0)return true;if(/^[ㄱ-ㅎ]+$/.test(k))return cho(nz(r.name)+' '+nz(A[t]||'')).indexOf(k)>=0;return false};
})();
