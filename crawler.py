import account

import re
import requests
from bs4 import BeautifulSoup as bs
from sshtunnel import SSHTunnelForwarder

# DB 연결
server = SSHTunnelForwarder(
    (account.host),
    ssh_username = account.ssh_username,
    ssh_pkey = account.ssh_pkey,
    ssh_password = account.ssh_password,
    remote_bind_address = account.remote_bind_address
)
server.start()

try:
    conn = account.connect(server)
    cur = conn.cursor()

    # 공지사항 - '셔틀' 검색 결과 페이지
    keyword = "셔틀"
    board_url = f"https://www.cju.ac.kr/www/selectBbsNttList.do?key=4577&bbsNo=881&integrDeptCode=&searchCtgry=&searchCnd=SJ&searchKrwd={keyword}"

    res = requests.get(board_url)
    soup = bs(res.text, 'html.parser')
    posts = soup.select("#board > table > tbody > tr") # 게시판
    pattern = re.compile('&nttNo=[0-9]+') # 게시글 번호 추출 정규식

    for post in posts:
        notice = bool(post.select_one("td:nth-child(1) > strong")) # 게시글이 공지글인지 체크 (불필요한 게시글)

        if notice == False: # 공지글이 아니면
            # 게시물 객체
            post = post.select_one("td.subject")

            # 게시물 URL
            uri = post.select_one("a")["href"] # uri 전체
            nttNo = pattern.search(uri).group() # 게시글 번호(&nttNo=*) 부분만 추출
            nttNo = nttNo.split('=')[1] # 게시글 번호만 추출

            # 새로운 게시글인지 확인
            cur.execute(f"select 0 from shuttle where post_num={nttNo}")

            # 이미 존재하는 게시글이면
            if cur.fetchone(): 
                break

            # 새로운 게시글이면
            else:
                cur.execute(f"INSERT INTO shuttle VALUES({nttNo}, now())") # 메시지 전송 테스트를 위한 주석
                # 게시물 제목
                title = post.get_text().strip()
                print(title)

                msg = f"{title}"
                url = f"https://www.cju.ac.kr/www/selectBbsNttView.do?bbsNo=881&nttNo={nttNo}&key=4577"
                button = {"inline_keyboard" : [[{"text" : "\U0001F68C  자세히 보기", "url" : url}]]}

                data = {"chat_id" : account.chat_id, "text": msg, "parse_mode": 'markdown', "reply_markup" : button}
                url = f"https://api.telegram.org/bot{account.token}/sendMessage?"
                requests.post(url, json=data)

except:
    print("오류 발생")

finally:
    conn.commit()
    conn.close()
    server.stop()