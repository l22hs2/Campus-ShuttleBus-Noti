# coding=euc-kr
import os
import re
import datetime

import pymysql
import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

# 시작 시간 출력
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"=== {now} ===")

try:
    load_dotenv()

    # DB 연결
    conn = pymysql.connect(host=os.environ.get('db_host'), user=os.environ.get('db_user'), password=os.environ.get('db_password'), db=os.environ.get('db'), charset='utf8')
    cur = conn.cursor()
    
    # 공지사항 키워드 검색 결과 페이지
    keyword = "결행"
    board_url = f"https://www.cju.ac.kr/www/selectBbsNttList.do?key=4577&bbsNo=881&integrDeptCode=&searchCtgry=&searchCnd=SJ&searchKrwd={keyword}"

    res = requests.get(board_url) # 공지사항 페이지
    soup = bs(res.text, 'html.parser') # 파싱
    posts = soup.select("#board > table > tbody > tr") # 게시판
    pattern = re.compile('&nttNo=[0-9]+') # 게시글 번호 추출 정규식

    cnt = 0

    for post in posts:
        notice = bool(post.select_one("td:nth-child(1) > strong")) # 해당 게시글이 공지글인지 체크 (불필요한 게시글)

        if notice == False: # 공지글이 아니면
            # 게시물 객체
            post = post.select_one("td.subject")

            # 게시물 URL
            uri = post.select_one("a")["href"] # uri 전체
            nttNo = pattern.search(uri).group() # 게시글 번호(&nttNo=*) 부분만 추출
            nttNo = nttNo.split('=')[1] # 게시글 번호만 추출

            # 새로운 게시글인지 확인 (DB에 해당 게시글 번호가 있는지)
            cur.execute(f"select 0 from shuttle where post_num={nttNo}")

            # 이미 존재하는 게시글이면
            if cur.fetchone():
                break
            # 오류로 인한 다량의 메시지 전송 방지
            if cnt >= 3:
                break

            # 새로운 게시글이면
            else:
                cnt += 1
                cur.execute(f"INSERT INTO shuttle VALUES({nttNo}, now())") # 게시글 목록에 추가
                conn.commit()
                # 게시물 제목
                title = post.get_text().strip()
                print(title)

                msg = f"*{title}*" # 메시지 내용
                url = f"https://www.cju.ac.kr/www/selectBbsNttView.do?bbsNo=881&nttNo={nttNo}&key=4577" # 게시글 링크
                button = {"inline_keyboard" : [[{"text" : "\U0001F68C  자세히 보기", "url" : url}]]} # 게시글 이동 버튼 속성
                
                # 서비스 채널
                data = {"chat_id" : os.environ.get('chat_id'), "text": msg, "parse_mode": 'markdown', "reply_markup" : button} # api 속성
                
                # 점검 채널
                # data = {"chat_id" : os.environ.get('personal_chat_id'), "text": msg, "parse_mode": 'markdown', "reply_markup" : button} # api 속성

                url = f"https://api.telegram.org/bot{os.environ.get('token')}/sendMessage?"
                requests.post(url, json=data) # 메시지 전송
    conn.close()

except Exception as e:
    print("오류 발생")
    print(e)

    msg = "\U0001F6A8 *청주대 셔틀 정보* - 오류 발생"
    data = {"chat_id" : os.environ.get('personal_chat_id'), "text": msg, "parse_mode": 'markdown'} # api 속성
    url = f"https://api.telegram.org/bot{os.environ.get('token')}/sendMessage?"
    requests.post(url, json=data) # 메시지 전송

finally:
    # 종료 시간 출력
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- {now} ---")