#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-11-19 下午7:05
# @Author  : Vitan
# @File    : MaoTuView.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import TimeoutException
import pyquery as pq
import pymongo

client = pymongo.MongoClient('localhost')
db = client['MaoTuView']

broswer = webdriver.Chrome()
broswer.set_window_size(1920,1080)
wait = WebDriverWait(broswer,10)

def search_first(url):
    try:
        broswer.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.unified.pagination')))
        total = int(broswer.find_element_by_xpath('//*[@id="FILTERED_LIST"]/div[36]/div/div/div/a[6]').get_attribute('data-page-number'))
        place()
        return total
    except TimeoutException:
        return total

def search_next(page):
    try:
        next = broswer.find_element_by_css_selector('.nav.next.rndBtn.ui_button.primary.taLnk')
        next.click()
        place()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="FILTERED_LIST"]/div[36]/div/div/a[2]')))
    except NoSuchAttributeException:
        search_next(page)

def place():
    anchors = broswer.find_elements_by_css_selector('.listing_info > div.listing_title > a')
    for a in anchors:
        if 'Review' in a.get_attribute('href'):
            url = a.get_attribute('href')
            return url

def view_first(url):
    try:
        broswer.get(url)
        total = int(broswer.find_element_by_xpath('//*[@id="taplc_location_reviews_list_resp_ar_responsive_0"]/div/div[13]/div/div/div/a[5]').get_attribute('data-page-number'))
        get_view()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nav.next.taLnk.ui_button.primary')))
        return total
    except TimeoutException:
        return view_first(url)

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
    items = doc('#taplc_location_reviews_list_resp_ar_responsive_0')
    for i in items:
        view = {
            'name':i.find('.info_text > div:nth-child(1)').text(),
            'title':i.find('#rn545940292 > span').text(),
            'txt':i.find('.prw_rup.prw_reviews_text_summary_hsx > div > p').text()
        }
        print(view)
        save_to_mongo(view)

def save_to_mongo(view):
    if db['MaotuYingView'].insert_one(view):
        print('Saving to MongoDB',view)
        return True
    return False

def main():
    url = 'https://www.tripadvisor.cn/Attractions-g298555-Activities-Guangzhou_Guangdong.html'
    total = search_first(url)
    for page in range(2, total + 1):
        search_next(page)

if __name__ == '__main__':
    main()