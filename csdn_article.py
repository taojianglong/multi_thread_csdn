import requests
import json
import os
import csv
import random
import socket
from lxml import etree
from multiprocessing import Pool

def get_txt():
    pic_url= []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

    page_url = 'https://blog.csdn.net/qq_38915710'
    # print(page_url)
    html = requests.get(page_url, headers=headers).text
    html_elem = etree.HTML(html)
    links = html_elem.xpath('//div[@class="article-list"]//h4/a/@href')
    return links
    # print(r)

def parse_html(links):
    index = 0
    infos = []
    for link in links:
        # print(link)
        html_page = requests.get(link).text
        html_page_elem = etree.HTML(html_page)
        index += 1
        title = html_page_elem.xpath('//div[@class="article-title-box"]//h1/text()')
        time_infos = html_page_elem.xpath('//div[@class="article-bar-top"]/span[2]/text()')
        # print(title[0])
        # print(time_infos[0].strip()[5:])
        data = {
            'index': index,
            'title': title[0],
            'time':time_infos[0].strip()[5:]
        }
        infos.append(data)
    headers = ['index', 'title', 'time']
    with open('test2.csv', 'w', newline='', encoding='utf-8')as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(infos)

# def csv_write(infos):
#     headers = ['index', 'title', 'time']
#     with open('test2.csv', 'w', newline='')as f:
#         f_csv = csv.DictWriter(f, headers)
#         f_csv.writeheader()
#         f_csv.writerows(infos)

if __name__ == '__main__':
    html = get_txt()
    print(html)
    pool = Pool()
    pool.map(parse_html, [html])
