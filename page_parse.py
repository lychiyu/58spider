# -*- coding: utf-8 -*-
# 爬取并解析每一个商品的详情页的链接并存入mongo数据库

import time
import requests
import pymongo
from bs4 import BeautifulSoup

from config import *

client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
db = client[MONGO_DB]
urllist = db['urllist']
product = db['product']

User_Agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {
    'User-Agent': User_Agent,
}


# 获取发布的商品详情页链接
def get_detail_links(url, who, pagenum):
    # http://bj.58.com/shouji/0/pn2
    real_url = '{}{}/pn{}/'.format(url, str(who), str(pagenum))
    res = requests.get(real_url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    # 个人发布的商品列表页面解析
    if who == 0:
        # 判断是否有内容
        if soup.find('td', 't'):
            links = soup.select('td.t > a')
            for link in links:
                link = link.get('href')
                # 剔除精品链接
                if link.find('zhuan') >= 0:
                    link = link.split('?')[0]
                    # 存入数据库中
                    urllist.insert_one({'url': link})
                    print(link)
        else:
            pass

    # 商家发布的商品列表页面解析
    else:
        # infolist > div:nth-child(5) > div > div.left > a.title.t
        # 判断是否有内容
        if soup.find('a', 't'):
            links = soup.select('div.business_desc > div.left > a.title.t')
            for link in links:
                link = link.get('href')
                # 剔除精品链接
                if link.find(url) >= 0:
                    link = link.split('?')[0]
                    # 存入数据库中
                    urllist.insert_one({'url': link})
                    print(link)
        else:
            pass


def parse_detail_page(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    # 解析转转商品详情页页面
    if url.find('zhuan') >= 0:
        # 判断转转商品是否下架
        if soup.find('span', 'soldout_btn'):
            pass
        else:
            title = soup.select('h1.info_titile')[0].text
            price = soup.select('span.price_now > i')[0].text
            area = soup.select('div.palce_li > span > i')[0].text.split('-')[1]
            # 存入数据库
            product.insert_one({'title': title, 'price': price, 'area': area})
            print(title, price, area)
    # 解析商家商品详情页
    else:
        # 判断是否是404页面或下架页面
        if soup.find('p', 'et') or soup.select('div#Notice'):
            pass
        else:
            title = soup.select('div.col_sub.mainTitle > h1')[0].text
            price = soup.select('span.price.c_f50')[0].text
            date = soup.select('li.time')[0].text
            area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
            # 保存至数据库
            product.insert_one({'title': title, 'price': price, 'area': area[0], 'date': date})
            print(title, price, area[0], date)
