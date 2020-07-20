
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('db.sqlite3')
query = 'CREATE TABLE navershop (title TEXT, link TEXT)'
conn.execute(query)
conn.commit()
conn.close()

res = requests.get('https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery=%20%EC%84%A0%EB%AC%BC&pagingIndex=1&pagingSize=40&productSet=checkout&query=%20%EC%84%A0%EB%AC%BC&sort=rel&timestamp=&viewType=list')

if res.status_code == 200 :
    soup = BeautifulSoup(res.content, 'html.parser')
    links = soup.find_all('a', class_ = 'basicList_link__1MaTN')
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        title = ''
        link = ''
        for link in links:
            title = str.strip(link.get_text())
            link = link.get('href')
            cur.execute('INSERT INTO navershop (title, link) VALUES (?,?)', (title, link))
        con.commit()
    print('crawling_naver_shopping :', type(links), len(links))
