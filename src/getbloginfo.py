'''
爬取csdn上区块链模块的文章信息
'''

import requests
from pyquery import PyQuery
 
def GetDouBanMovie():
    a = 1
    for i in range(0,250,25):
        url = "https://blog.csdn.net/nav/blockchain"
        r = requests.get(url)
        f = open('blog.txt',mode='a+')
        for blog in PyQuery(r.content)(".list_con"):
            title = PyQuery(blog).find(".csdn-tracking-statistics").find('a').html()
            title.replace('\n','')
            num = PyQuery(blog).find(".num").html()
            s = "%s: 博客:%s  阅读量:%s \n"%(a,title,num)
            f.write(s)
            a += 1

GetDouBanMovie()