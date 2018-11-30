from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException,TimeoutException
from pyquery.pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import time
import pymongo

driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)

client = pymongo.MongoClient('localhost')
db = client['Qunar']

def lastPage(url):
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.next')))
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    total = int(soup.select('.pager a')[-2].text)
    return total

def search_first(url):
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.next')))

def search_next(page):
    next = driver.find_element_by_css_selector('.next')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.next')))
    next.click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.pager em'),str(page)))
    time.sleep(1)

def get_url():
    doc = pq(driver.page_source)
    doc = doc.find('.sight_item_caption')
    li = []
    for box in doc.items():
        url = 'http://piao.qunar.com'+str(box.find('.name').attr('href'))
        li.append(url)
    return li

def get_comment_last(url):
    # 评论总页数
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mp-pager-next.mp-pager-item')))
    doc = pq(driver.page_source)
    doc = doc.find('#pageContainer')
    li = [i.text() for i in doc.find('.mp-pager-item').items()]
    return int(li[-2])

def get_commet_first(url):
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mp-pager-next.mp-pager-item')))

def get_comment_next(page):
    try:
        next = driver.find_element_by_css_selector('.mp-pager-next.mp-pager-item')
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mp-pager-next.mp-pager-item')))
        next.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.mp-pager em'),str(page)))
        time.sleep(1)
    except TimeoutException:
        get_comment_next(page)
    except WebDriverException:
        get_comment_next(page)

def get_comments():
    doc = pq(driver.page_source)
    doc = doc.find('.mp-comments-list')
    for item in doc.find('.mp-comments-item').items():
        usr = item.find('.mp-comments-username').text()
        date = item.find('.mp-comments-time').text()
        comment = item.find('.mp-comments-desc').text()
        view = {
            'user':usr,
            'date':date,
            'comment':comment
        }
        save_to_mongo(view)

def save_to_mongo(view):
    if db['comment'].insert_one(view):
        print('Saving to MongoDB',view)
        return True
    return False

def main():
    url = 'http://piao.qunar.com/ticket/list_%E6%88%90%E9%83%BD.html#from=home_remen&in_track=qunar_djmp_gnmdd_%E6%88%90%E9%83%BD'
    total = lastPage(url)
    search_first(url)
    all_url = get_url()
    for i in range(2,total+1):
        search_next(i)
        all_url.extend(get_url())

    for url in all_url:
        total = get_comment_last(url)
        get_commet_first(url)
        get_comments()
        for i in range(2,total+1):
            get_comment_next(i)
            get_comments()


if __name__ == '__main__':
    main()
