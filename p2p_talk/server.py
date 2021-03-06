#!/usr/bin/env python
# encoding=utf-8

import socket
import threading,time, struct,os,time,json
import requests,re

class Iptable(object):
    def headers(self,str):        #解析数据包
        header_content = str.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
        result = {}
        for line in header_content:
            k, v = line.split(':')
            result[quote(k)] = quote(v)
        return result
    def __init__(self):
        self.iptables = set()
        self.iptables.add("114.91.184.198")#172.31.0.17
        url = requests.get("http://txt.go.sohu.com/ip/soip")
        text = url.text
        self.myaddr = re.findall(r'\d+.\d+.\d+.\d+',text)[0]
        # self.myaddr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', "eth0"[:15]))[20:24])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("p2p创世节点初始化完成")

        self.send_radio()     #发送广播包得到iptables
        

    def addip(self,ips):
        self.iptables = self.iptables | ips #合并现有ip列表

    def send_radio(self):
        print ("开始发送广播")
        for ip in self.iptables:
            print ("发送给"+ip)
            if ip == self.myaddr:   #不能发送给自己
                print ("暂无其他节点")
                continue
            request = "Content-Type:radio\r\n" #表示是广播请求
            request += "Method:getIptables\r\n" #表示目的是得到IP列表
            request += "From:"+self.myaddr+"\r\n" #来源ip
            request += "Referer:"+ip+"\r\n"  #目标ip
            request += "Port:9005\r\n\r\n"   #端口号
            print (type(request))
            self.socket.connect((ip,9005)) 
            self.socket.send(request)
            self.socket.close()
            print ("发送一条广播")

    def getIptables(self,port,ip,sock):  #发送现有的IP列表
        print ("返回iptables至请求的机器")
        self.socket.connect((ip,port))
        self.iptables.add(ip)
        response = "Content-Type:response\r\n" #表示是对点请求
        response += "Method:refreshIptables\r\n" #表示目的是得到IP列表
        response += "From:"+self.myaddr+"\r\n" #来源ip
        response += "Port:6666\r\n"   #端口号
        iptables_str = "["
        for ip in self.iptables:
            iptables_str += ip + ','
        iptables_str = iptables_str.strip(',');
        iptables_str += "]"
        response += "Iptables:"+iptables_str+"\r\n\r\n"   #端口号
        sock.send(response)

    def refreshIptables(self,header,sock):  #获取更新iptables
        #self.addip(ips)
        print ("更新现有的iptables")
        ip_str = header["Iptables"]
        ips = json.loads(ip_str)
        self.addip(set(ips))
        sock.close()
        print ("网内ip已更新")

    def recv(self,sock,addr):   #处理接收到的请求
        h = sock.recv(1024).decode('utf-8')
        headers = self.headers(h)
        if headers["Content-Type"] == "radio":
            print ("收到广播")
            eval("self."+headers["Method"])(headers["Port"],headers["From"],sock)   #执行操作
        if headers["Content-Type"] == "response":    #返回数据
            print ("收到回复")
            eval("self."+headers["Method"])(header,sock)   #执行操作




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',9005))
s.listen(10)

iptable = Iptable()
print ('Waiting for connection...')

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    print ("有链接")
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=iptable.recv, args=(sock, addr))

    t.start()
    time.sleep(2)

