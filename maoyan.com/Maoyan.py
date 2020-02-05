import requests
import re
import json
from requests.exceptions import RequestException

def get_one_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
    response = requests.get(url,headers = headers)
    html = response.text
    return html

def parse_one_page(html):
    pattern = re.compile('<dd.*?title="(.*?)".*?star">'
    + '(.*?)</p>.*?releasetime">(.*?)'
    + '</p>.*?integer">(.*?)<.*?fraction">(.*?)</i>',re.S)
    movies = re.findall(pattern,html)
    for item in movies:
        yield {
            '电影名':item[0],
            '主演':item[1].strip()[3:],
            '上映时间':item[2][5:],
            '评分':item[3]+item[4]
        }

def write_to_txt(content):
    # 采用 append 追加模式，字符集为utf8
    with open('movies.txt','a',encoding='utf8') as f:
        # 采用json的dumps方法来初始化字符串
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

# 第1-10页url
for i in range(0,10):
    url = 'https://maoyan.com/board/4?offset=' + str(i * 10)
    # 构建 url，调用1、2、3步骤
    html = get_one_page(url)
    movies= parse_one_page(html)
    for item in movies:
        write_to_txt(item)


mport requests
import re
import json
import pandas
from requests.exceptions import RequestException

def get_one_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
    response = requests.get(url,headers = headers)
    html = response.text
    return html

def parse_one_page(html):
    pageary = []
    pattern = re.compile('<dd.*?title="(.*?)".*?star">'
        + '(.*?)</p>.*?releasetime">(.*?)'
        + '</p>.*?integer">(.*?)<.*?fraction">(.*?)</i>',re.S)
    movies = re.findall(pattern,html)
    for item in movies:
        dict = {
            '电影名':item[0],
            '主演':item[1].strip()[3:],
            '上映时间':item[2][5:],
            '评分':item[3]+item[4]
        }
        pageary.append(dict)
    return pageary

ary = []
for i in range(0,10):
    url = 'https://maoyan.com/board/4?offset=' + str(i * 10)
    html = get_one_page(url)
    pageary = parse_one_page(html)
    ary = ary + pageary
df = pandas.DataFrame(ary)
df.to_csv('movies.csv')
