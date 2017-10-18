# -*- coding: utf-8 -*-
from multiprocessing import Pool
from category_extract import urls
from page_parse import *


def get_all(url):
    for i in range(1, 101):
        get_detail_links(url, i)


if __name__ == "__main__":
    pool = Pool()
    pool.map(get_all, urls)
    pool.close()
    pool.join()
    for item in urllist.find():
        time.sleep(1)
        parse_detail_page(item['url'])
    print('done')
