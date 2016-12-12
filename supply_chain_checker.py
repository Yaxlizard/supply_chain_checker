# -*- encoding: utf8 -*-
import requests
import urllib2
from lxml import etree
import math
import re

s = requests.session()
url = 'http://www.dianxiaomi.com/user/login.htm'
account = raw_input('please enter your account: ')
password = raw_input('please enter your password: ')
data = {'account':account,
        'password':password,
        }
headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
s.post(url,data=data,headers=headers)

def getPage():
    getNum = s.get('http://www.dianxiaomi.com/product/index.htm').text
    html = etree.HTML(getNum)
    productNum = int(html.xpath('//*[@id="state_3"]')[0].text)
    pages = math.ceil(productNum/50.0)   #向上取整得到页数,店小秘最大显示100行产品，这里只要50行
    return int(pages)   #只显示整数部分 

def detect(dic):
    list = []
    pattern = re.compile(u'立即订购|立即购买|加入进货单')
    for name in dic:
        openweb = urllib2.urlopen(dic[name])
#1688的编码还是GB2312，要转成unicode，再匹配unicode的中文字符串
        webpage = openweb.read().decode('GB2312','ignore')
        result = pattern.search(webpage)
        if not result:
            list.append(name)
    return list

pages = getPage()
print u'一共有%d页，请等待。。。' %pages
n = 1
for p in range(1,pages+1):
    print u'第%d页：' %n
    dic = {}
    linkLst = []
    idLst = []
    create_tail = 'pageNo=%d&pageSize=50&shopId=-1&fullCid=&state=3&productState=1&searchType=0&searchValue=&sortName=&sortValue=0' %p
    url = 'http://www.dianxiaomi.com/product/pageList.htm?'+create_tail
    wholepage = s.get(url)
    print type(wholepage.text)
    html = etree.HTML(wholepage.text)
    print html
    links = html.xpath('//tr/td[2]/p/a/@href') 
    print len(links)
    for i in links:
        linkLst.append(i)
    ids = html.xpath('//tr/td[3]/span[1]/a')
    print len(ids)
    for j in ids:
        idLst.append(j.text)
    dic = dict(zip(idLst,linkLst))
    del idLst,linkLst
    list = detect(dic)
    for id in list:
        print u'以下商品可能需要重找货源: %s' %id
    n += 1
print u'检索结束'


    
        
        
        
    
    
    
        

        
