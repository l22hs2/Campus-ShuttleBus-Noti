import re
import requests
from bs4 import BeautifulSoup as bs
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='bus', charset='utf8')
cur = conn.cursor()


# 공지사항 - '셔틀' 검색 결과 페이지
keyword = "셔틀"
board_url = f"https://www.cju.ac.kr/www/selectBbsNttList.do?key=4577&bbsNo=881&integrDeptCode=&searchCtgry=&searchCnd=SJ&searchKrwd={keyword}"

res = requests.get(board_url)
soup = bs(res.text, 'html.parser')
posts = soup.select("#board > table > tbody > tr") # 게시판
pattern = re.compile('&nttNo=[0-9]+') # 게시글 번호 추출 정규식

for post in posts:
    notice = bool(post.select_one("td:nth-child(1) > strong")) # 공지 게시글 여부 (불필요한 게시글)

    if notice == False: # 공지 게시글이 아니면
        # 게시물 객체
        post = post.select_one("td.subject")

        # 게시물 URL
        uri = post.select_one("a")["href"] # uri 전체
        nttNo = pattern.search(uri).group() # 게시글 번호(&nttNo=*) 부분만 추출
        nttNo = nttNo.split('=')[1] # 게시글 번호만 추출

        # 새로운 게시글인지 확인
        cur.execute(f"select 0 from post where num={nttNo}")

        # 이미 존재하는 게시글이면
        if cur.fetchone(): 
            break

        # 새로운 게시글이면
        else:
            cur.execute(f"INSERT INTO post VALUES({nttNo}, now())")
            # 게시물 제목
            title = post.get_text().strip()
            print(title)

            url = f"https://www.cju.ac.kr/www/selectBbsNttView.do?bbsNo=881&nttNo={nttNo}&key=4577"
            print(url)

            print(nttNo)

conn.commit()
conn.close()
        