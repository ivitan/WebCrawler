import requests
res = requests.get('http://esf.sh.fang.com/')
#获取上海在售二手房源网页首页（http://esf.sh.fang.com/）的响应包，命名为res
res.text
#输出res的文本内容

from bs4 import BeautifulSoup
domain = 'http://esf.sh.fang.com'
#将上海在售二手房源网页首页url（http://esf.sh.fang.com/）赋值给domain
soup = BeautifulSoup(res.text,'html.parser')
#创建BeautifulSoup对象对res响应包进行解析，结果命名为soup
for house in soup.select('.shop_list dl dd h4 a'):
#循环遍历获取网页首页所有房源详细内容页的url,循环变量名为house（提示：检查定位路径定位查找的节点是否为空）
    if house:
    #（提示：如果存在返回的标签节点有空的情况，需要进行判断！）
            print(domain+house['href'])#利用domain与存储房屋详细内容的相对url的标签节点构建房屋的url
            #打印输出查看url
            print('========================'
            #输出======表示间隔

import requests
from bs4 import BeautifulSoup
res =requests.get('http://esf.sh.fang.com/chushou/3_331876564.htm')
#将以上获得的第一个房源的详细内容页进行请求访问
soup = BeautifulSoup(res.text,'html.parser')
#对响应包res的网页文本进行解析，解析结果命名为soup
res.text

info ={}
#定义字典变量info，用于存放每套房子相关数据
info['标题']=soup.select('.title h1')[0].text.strip()
#查找房子标题，以“标题”为key名存入info
info #查看info

info['总价']=soup.select('.price_esf')[0].text
#查找总价，以“总价”为key名存入info
info #查看info

k=['总价','单价','建筑面积','朝向','楼层','装修','户型','标题']
for item in soup.select('.trl-item1'):
#item表示包括户型，朝向，单价，楼层，装修等相关数据的标签，思考：观察这些数据都在哪个标签下？
     key=item.select('.font14')[0].text.strip()
     value=item.select('.tt')[0].text.strip()
            #key计划用于表示房屋的字段，问，key在哪个标签节点？这些key作为字段，有没有问题
            #value计划用于表示房屋相关字段对应数
     info[key]=value
print(info)
print(list(info.values()))
print(k)
print(dict(zip(k,list(info.values()))))

def getHouseDetail(url):
    info={}
    info_adj={}
    res=requests.get(url)
    #根据url请求网页内容
    soup = BeautifulSoup(res.text,'html.parser')
    #解析详细内容页，结果命名为soup
    info['标题']=soup.select('.title h1')[0].text.strip()
    #获取房屋名并加入info字典，key值命名为“标题
    info['总价']=soup.select('.price_esf')[0].text
    #获取房屋总价并加入info字典，key值命名为“总价
    for item in soup.select('.trl-item1'):
    #用item做为循环变量名，代表当前网页class为trl-item1的所有标签节点
        key=item.select('.font14')[0].text.strip()
        #key表示item标签下所有class为font14的标签节点文本内容
        print(key)
        value=item.select('.tt')[0].text.strip()
        #value示item标签下所有class为tt的标签节点文本内容
        info[key]=value
        #将info里面所有key赋值给value
        k=['总价','单价','建筑面积','朝向','楼层','装修','户型','标题']
    info_adj=dict(zip(k,list(info.values())))
    #print(info_adj)
    return info_adj

getHouseDetail('http://esf.sh.fang.com/chushou/3_328597533.htm')

import requests
from bs4 import BeautifulSoup
houseary=[]
#定义列表用于存储所有房屋的相关数据
domain='http://esf.sh.fang.com'
#domain为http://esf.sh.fang.com域名
res=requests.get('http://esf.sh.fang.com')
#请求访问http://esf.sh.fang.com首页，获得响应包res
soup=BeautifulSoup(res.text,'html.parser')
#创建BeatifulSoup对象并进行解析
for link in soup.select('.shop_list dl dd h4 a'):
#循环遍历获取网页首页中存有的标签节点，循环变量命名为link
    url=domain+link['href']
    #利用domain与存储房屋详细内容的相对url的标签节点构建房屋的url
    houseary.append(getHouseDetail(url))
    #调用getHouseDetail函数获取每一房屋相关数据并追加到houseary

len(houseary)
#求总共获取到多少套房屋信息

mport pandas
df = pandas.DataFrame(houseary)
#将获取到的所有房屋信息转换成数据框的结构
df

df.to_excel('house.xlsx')
#存储到当前工作空间目录下，文件命名为house.xlsx
