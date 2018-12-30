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
    star_url = 'https://guangzhou.anjuke.com/sale/p'
    for i in range(1,51):
        url = star_url+str(i)
        print(url)
        urls.append(url)
    return urls

def HouseUrl(url):
    time.sleep(random.random()*10)
    broswer.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.curr')))
    urls = broswer.find_elements_by_css_selector('.houseListTitle') # a 标签
    House = []
    for a in urls:
        urls = a.get_attribute('href')
        House.append(urls)
    return House

def get_detail(url):
    time.sleep(random.random() * 10)
    broswer.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.houseInfoBox')))
    html = broswer.page_source
    soup = BeautifulSoup(html,'lxml')
    info = {}
    info['标题'] = soup.select('.long-title')[0].text
    info['总价'] = soup.select('.basic-info span')[0].text
    info['户型'] = soup.select('.basic-info span')[1].text
    info['面积'] = soup.select('.basic-info span')[2].text
    info['单价'] = soup.select('.houseInfo-content')[2].text
    info['朝向'] = soup.select('.houseInfo-content')[7].text
    info['月供'] = soup.select('.houseInfo-content')[8].text
    info['楼层'] = soup.select('.houseInfo-content')[-7].text
    info['装修'] = soup.select('.houseInfo-content')[-6].text
    k = ['标题','总价','户型','面积','单价','朝向','月供','楼层','装修']
    info_adj = dict(zip(k,list(info.values())))
    houseInfo.append(info_adj)
    print(houseInfo)
    return houseInfo

def save_to_csv(houseInfo):
    df = pandas.DataFrame(houseInfo)
    df.to_csv('Guangzhou.csv')

def main():
    urls = get_urls()
    for url in urls:
        url = HouseUrl(url)
        for Hurl in url:
            houseInfo=get_detail(Hurl)
            save_to_csv(houseInfo)

if __name__ == '__main__':
    main()
