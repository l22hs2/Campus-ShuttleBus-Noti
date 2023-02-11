import re
import requests
from bs4 import BeautifulSoup as bs

# 공지사항 - '셔틀' 검색 결과 페이지
board_url = "https://www.cju.ac.kr/www/selectBbsNttList.do?key=4577&bbsNo=881&integrDeptCode=&searchCtgry=&searchCnd=SJ&searchKrwd=셔틀"

res = requests.get(board_url)
soup = bs(res.text, 'html.parser')
posts = soup.select("#board > table > tbody > tr") # 게시판
pattern = re.compile('&nttNo=[0-9]+') # 게시글 번호 추출 정규식

for post in posts:
    notice = bool(post.select_one("td:nth-child(1) > strong")) # 공지 게시글 여부

    if notice == False: # 공지 게시글이 아니면
        # 게시물 객체
        post = post.select_one("td.subject")

        # 게시물 제목
        title = post.get_text()
        title = title.strip()
        print(title)

        # 게시물 URL
        uri = post.select_one("a")["href"] # uri 전체
        nttNo = pattern.search(uri).group() # 게시글 번호(&nttNo=*) 부분만 추출
        nttNo = nttNo.split('=')[1] # 게시글 번호만 추출

        url = f"https://www.cju.ac.kr/www/selectBbsNttView.do?bbsNo=881&nttNo={nttNo}&&pageUnit=10&searchCnd=SJ&searchKrwd=셔틀&key=4577&pageIndex=1"
        print(url)
        print(nttNo)