#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-12-28 下午6:48
# @Author  : Vitan
# @File    : anjuke.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery.pyquery import PyQuery as pq
from bs4 import  BeautifulSoup
import pandas
import time,random

broswer = webdriver.Chrome()
wait = WebDriverWait(broswer,10)
houseInfo = []
def get_urls():
    urls = []
    star_url = 'https://cd.5i5j.com/ershoufang/n'
    for i in range(1,70):
        url = star_url+str(i)
#         print(url)
        urls.append(url)
    return urls

def HouseUrl(url):
    time.sleep(random.random()*10)
    broswer.get(url)
    html = broswer.page_source
    main = 'https://cd.5i5j.com'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cur')))
    HouseUrls = []
    soup = BeautifulSoup(html,'lxml')
    for link in soup.select('.pList .listCon .listTit a'):
        HouseUrl = main+link['href']
        HouseUrls.append(HouseUrl)
    return HouseUrls

def get_detail(url):
    time.sleep(random.random() * 20)
    broswer.get(url)
    html = broswer.page_source
    soup = BeautifulSoup(html,'lxml')
    info = {}
    info['标题'] = soup.select('.house-tit')[0].text
    info['总价'] = soup.select('.jlinfo')[0].text
    info['单价'] = soup.select('.jlinfo')[1].text
    info['户型'] = soup.select('.jlinfo')[2].text
    info['面积'] = soup.select('.jlinfo')[3].text
    info['楼层'] = soup.select('.zushous li')[1].text
    info['朝向'] = soup.select('.zushous li')[2].text 
    info['装修'] = soup.select('.zushous li')[3].text
    info['类型'] = soup.select('.zushous li')[5].text
    k = ['标题','总价','单价','面积','楼层','朝向','装修','类型']
    info_adj = dict(zip(k,list(info.values())))
    houseInfo.append(info_adj)
    print(houseInfo)
    return houseInfo

def save_to_csv(houseInfo):
    df = pandas.DataFrame(houseInfo)
    df.to_csv('chengdu.csv')

def main():
    urls = get_urls()
    for url in urls:
        url = HouseUrl(url)
        for Hurl in url:
            houseInfo=get_detail(Hurl)
            save_to_csv(houseInfo)
    print(url)

if __name__ == '__main__':
    main()

