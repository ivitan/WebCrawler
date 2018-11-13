from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import TimeoutException
from pyquery.pyquery import PyQuery

broswer = webdriver.PhantomJS()
# Element is not currently visible and may not be manipulated"
broswer.set_window_size(1920, 1080)
wait = WebDriverWait(broswer,10)

def search_first(url):
    try:
        broswer.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.pi.pg-last')))
        total = int(broswer.find_element_by_css_selector('.pi.pg-last').get_attribute('data-page'))
        return total
    except TimeoutException:
        return total

def search_next(page):
    try:
        next = broswer.find_element_by_css_selector('.pi.pg-next')
        next.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.pg-current'),str(page)))
    except NoSuchAttributeException:
        search_next(page)

def view_first(url):
    broswer.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.pi.pg-last')))
    total = int(broswer.find_element_by_css_selector('.pi.pg-last'))
    return total

def view_next(page):
    next = broswer.find_element_by_css_selector('.pi.pg-next')
    next.click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.pg-current'),str(page)))

def main():
    url = 'http://www.mafengwo.cn/jd/10088/gonglve.html'
    total = search_first(url)
    for page in range(2,total+1):
        search_next(page)
        print('Clicking',page,'页')

if __name__=='__main__':
    main()