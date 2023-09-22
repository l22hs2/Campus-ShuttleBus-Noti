# coding=euc-kr
import os
import re
import datetime

import pymysql
import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

# ���� �ð� ���
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"=== {now} ===")

try:
    load_dotenv()

    # DB ����
    conn = pymysql.connect(host=os.environ.get('db_host'), user=os.environ.get('db_user'), password=os.environ.get('db_password'), db=os.environ.get('db'), charset='utf8')
    cur = conn.cursor()
    
    # �������� Ű���� �˻� ��� ������
    keyword = "����"
    board_url = f"https://www.cju.ac.kr/www/selectBbsNttList.do?key=4577&bbsNo=881&integrDeptCode=&searchCtgry=&searchCnd=SJ&searchKrwd={keyword}"

    res = requests.get(board_url) # �������� ������
    soup = bs(res.text, 'html.parser') # �Ľ�
    posts = soup.select("#board > table > tbody > tr") # �Խ���
    pattern = re.compile('&nttNo=[0-9]+') # �Խñ� ��ȣ ���� ���Խ�

    cnt = 0

    for post in posts:
        notice = bool(post.select_one("td:nth-child(1) > strong")) # �ش� �Խñ��� ���������� üũ (���ʿ��� �Խñ�)

        if notice == False: # �������� �ƴϸ�
            # �Խù� ��ü
            post = post.select_one("td.subject")

            # �Խù� URL
            uri = post.select_one("a")["href"] # uri ��ü
            nttNo = pattern.search(uri).group() # �Խñ� ��ȣ(&nttNo=*) �κи� ����
            nttNo = nttNo.split('=')[1] # �Խñ� ��ȣ�� ����

            # ���ο� �Խñ����� Ȯ�� (DB�� �ش� �Խñ� ��ȣ�� �ִ���)
            cur.execute(f"select 0 from shuttle where post_num={nttNo}")

            # �̹� �����ϴ� �Խñ��̸�
            if cur.fetchone():
                break
            # ������ ���� �ٷ��� �޽��� ���� ����
            if cnt >= 3:
                break

            # ���ο� �Խñ��̸�
            else:
                cnt += 1
                cur.execute(f"INSERT INTO shuttle VALUES({nttNo}, now())") # �Խñ� ��Ͽ� �߰�
                conn.commit()
                # �Խù� ����
                title = post.get_text().strip()
                print(title)

                msg = f"*{title}*" # �޽��� ����
                url = f"https://www.cju.ac.kr/www/selectBbsNttView.do?bbsNo=881&nttNo={nttNo}&key=4577" # �Խñ� ��ũ
                button = {"inline_keyboard" : [[{"text" : "\U0001F68C  �ڼ��� ����", "url" : url}]]} # �Խñ� �̵� ��ư �Ӽ�
                
                # ���� ä��
                data = {"chat_id" : os.environ.get('chat_id'), "text": msg, "parse_mode": 'markdown', "reply_markup" : button} # api �Ӽ�
                
                # ���� ä��
                # data = {"chat_id" : os.environ.get('personal_chat_id'), "text": msg, "parse_mode": 'markdown', "reply_markup" : button} # api �Ӽ�

                url = f"https://api.telegram.org/bot{os.environ.get('token')}/sendMessage?"
                requests.post(url, json=data) # �޽��� ����
    conn.close()

except Exception as e:
    print("���� �߻�")
    print(e)

    msg = "\U0001F6A8 *û�ִ� ��Ʋ ����* - ���� �߻�"
    data = {"chat_id" : os.environ.get('personal_chat_id'), "text": msg, "parse_mode": 'markdown'} # api �Ӽ�
    url = f"https://api.telegram.org/bot{os.environ.get('token')}/sendMessage?"
    requests.post(url, json=data) # �޽��� ����

finally:
    # ���� �ð� ���
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- {now} ---")