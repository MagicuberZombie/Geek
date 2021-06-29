import contextlib
import os
import re

import requests
from bs4 import BeautifulSoup


def is_article(href):
    return href and re.compile("page.htm").search(href)


def is_pdf_href(href):
    return href and re.compile(".pdf").search(href)


def download_article(url, filename, dirname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}

    with contextlib.closing(requests.get(url=url, stream=True, headers=headers, timeout=6)) as r:
        with open(os.path.join(dirname, filename), "ab+") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()


download_dir = os.path.join(os.getcwd(), "pdf")
host_server = "http://www.cifu.fudan.edu.cn"
for i in range(1, 12):
    start_page = "http://www.cifu.fudan.edu.cn/12233/list%d.htm" % i
    r = requests.get(start_page)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    article_tables = soup.find_all(href=is_article)
    for table in article_tables:
        with contextlib.closing(requests.get(host_server + table['href'])) as re:
            re.encoding = "utf-8"
            soup2 = BeautifulSoup(re.text, "html.parser")
            target = soup2.find(href=is_pdf_href)
            if target is not None:
                title = target.text.replace('?', '？')
                article_url = host_server + target['href']
                try:
                    download_article(article_url, title, download_dir)
                except OSError as err:
                    print(err)
