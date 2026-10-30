# IR 서재 원본 폴더

한 건당 JSON 파일 하나: `YYYYMMDD_티커_분기.json` (예: `20261029_AMZN_3Q26.json`)
칸: name, ticker, q, date(YYYY-MM-DD), time(장전·장후·아시아), title, body, src, pdf_kr, pdf_orig, pdf_slides, by
PDF는 릴리스 `ir-YYYYMMDD`에 영어 이름(`티커_분기_kr.pdf` / `_orig.pdf` / `_slides.pdf`)으로 첨부.
새 파일 추가만 하고 기존 파일은 고치지 않는다. 목록(d/ir/ir.json)과 회사별 최근 4분기 정리는 자동 작업(ir-library)이 한다.
