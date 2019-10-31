#!/usr/bin/env python
# encoding=utf-8
import requests
from pyquery import PyQuery
import chardet,re
def GetDouBanMovie():
    a = 1
    url = "https://hao.360.cn/"
    r = requests.get(url)
    f = open('cars.txt',mode='w+',encoding=("utf8"))
    doc = PyQuery(r.text)
    for pp in doc("a"):
        pp1 = PyQuery(pp)
        title = pp1.text()
        href = pp1.attr("href")
        if href or str(href).find("javascript:void(0)") < 0:
            s = "链接名：%s       url：%s\n"%(title,href)
            f.write(s.encode("utf8").decode("utf8"))

GetDouBanMovie()