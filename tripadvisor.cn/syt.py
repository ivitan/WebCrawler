#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-10-31 下午8:43
# @Author  : Vitan
# @File    : syt.py

'''
names = ['leo','jack','james']
colors = ['red','green','blue','yellow']
for name,color in zip(names,colors):
    print(name,'-->',color)
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import TimeoutException
import pyquery as pq


broswer = webdriver.Chrome()
broswer.set_window_size(1920,1080)
wait = WebDriverWait(broswer,10)

def view_first(url):
    try:
        broswer.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nav.next.taLnk.ui_button.primary')))
        get_view()
    except TimeoutException:
        return None

def view_next(page):
    try:
        next = broswer.find_element_by_css_selector('#taplc_location_reviews_list_resp_ar_responsive_0 > div > div:nth-child(15) > div > div > div > a:nth-child(2)')
        next.click()
        get_view()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.nav.next.taLnk.ui_button.primary')))
    except NoSuchAttributeException:
        view_next(page)

def get_view():
    html = broswer.page_source
    doc = pq(html)
    items = doc('.listContainer')
    for i in items:
        view = {
            'name':i.find('.info_text > div:nth-child(1)').text(),
            'title':i.find('#rn545940292 > span').text(),
            'txt':i.find('.prw_rup.prw_reviews_text_summary_hsx > div > p').text()
        }
        print(view)

def main():
    url = 'https://www.tripadvisor.cn/Attraction_Review-g298555-d1580078-Reviews-Chimelong_Paradise-Guangzhou_Guangdong.html'
    view_first(url)

if __name__ == '__main__':
    main()
