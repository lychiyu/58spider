# -*- coding: utf-8 -*-
# 获取58二手市场的所有分类链接


import requests
from bs4 import BeautifulSoup

# 二手市场首页链接
start_url = "http://bj.58.com/sale.shtml"

User_Agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {
    'User-Agent': User_Agent,
}


def get_cate_urls(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    links = soup.select('ul.ym-submnu > li > b > a')
    for link in links:
        page_url = 'http://bj.58.com' + link.get('href')
        yield page_url


urls = set(get_cate_urls(start_url))
