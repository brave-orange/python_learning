#!/usr/bin/env python
# encoding=utf-8

import socket
import threading,time,fcntl, struct,os,random
'''
kad算法
'''

class Iptable(object):

    def __init__(self):
        
        
        self.makeId() #随机ID
        #self.iptables.add("172.31.0.17")   #("120.92.165.154")
        self.k_bucket = list()
        self.k_bucket.append({"KadId":"0xbda0e659f6c5","ip"："172.31.0.17","port":6666})
        for kad in self.k_bucket:
            kad["distance"] = int(self.nodeId,16)^int(kad["KadId"],16)
            self.send_ping(kad["ip"],kad["port"])   #发送ping
        #self.myaddr = urlopen('http://ip.42.pl/raw').read()#获取本机ip
        self.myaddr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', "eth0"[:15]))[20:24])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#无状态socket
        print "p2p创世节点初始化完成"
        

    def makeId(self):
        str = ""
        for i in range(15):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        #self.nodeId  = hex(long(str)) #python2
        self.nodeId  = hex(int(str)) #python3
    def headers(self,data):        #解析数据包
        header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
        result = {}
        for line in header_content:
            print line
            k, v = line.split(':')
            result[k.strip(" ")] = v.strip(" ")
        return result

    def send_ping(self,ip,port):
        request = "Content-Type:PING\r\n" #表示是看看是不是活得
        request += "msg:Are you OK!\r\n" #消息
        request += "From:"+self.myaddr+"\r\n" #来源ip
        request += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        self.socket.sendto(msg,addr)
    def send_pong(self,ip,port):
        request = "Content-Type:PONG\r\n" #回复我还活着
        request += "msg:I'm fine,thinks adn you?\r\n" #消息
        request += "From:"+self.myaddr+"\r\n" #来源ip
        request += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        self.socket.sendto(msg,addr)

    def send_radio(self):
        print "开始发送广播"
        for ip in self.iptables:
            if ip == self.myaddr:   #不能发送给自己
                print "暂无其他节点"
                continue
            request = "Content-Type:radio\r\n" #表示是广播请求
            request += "Method:getIptables\r\n" #表示目的是得到IP列表
            request += "From:"+self.myaddr+"\r\n" #来源ip
            request += "Referer:"+ip+"\r\n"  #目标ip
            request += "Port:6666\r\n\r\n"   #端口号
            self.socket.connect((ip,6666)) 
            self.socket.send(request)
            print "发送一条广播"

    def getIptables(self,port,ip,sock):  #发送现有的IP列表
        print "返回iptables至请求的机器"
        self.socket.connect((ip,int(port)))
        self.iptables.add(ip)
        response = "Content-Type:response\r\n" #表示是对点请求
        response += "Method:refreshIptables\r\n" #表示目的是得到IP列表
        response += "From:"+self.myaddr+"\r\n" #来源ip
        response += "Port:6666\r\n"   #端口号
        iptables_str = "["
        for ip in self.iptables:
            iptables_str = iptables_str + '"' + ip + '",'
        iptables_str = iptables_str.strip(',');
        iptables_str += "]"
        response += "Iptables:"+iptables_str+"\r\n\r\n"   #端口号
        print response
        sock.send(response)
        sock.close()
        print "线程结束"

    def refreshIptables(self,header,sock):  #获取更新iptables
        #self.addip(ips)
        print "更新现有的iptables"
        ip_str = header['Iptables']
        ips = json.loads(ip_str)
        self.addip(set(ips))
        print "网络内ip已更新"
        return "线程结束"

    def recv(self,sock,addr):   #处理接收到的请求

        h = sock.recv(1024).decode('utf-8')
        header = self.headers(h)
        
        print header
        if header["Content-Type"] == "radio":
            print "收到广播"
            eval("self."+header["Method"])(header["Port"],header["From"],sock)   #执行操作
        if header["Content-Type"] == "response":    #返回数据
            print "收到回复"
            eval("self."+header["Method"])(header,sock)   #执行操作
        if header["Content-Type"] == "PING":    #PING数据
            print "收到PING"
            eval("self."+header["Method"])(header,sock)   #执行操作
        if header["Content-Type"] == "PONG":    #PONG消息
            print "收到PONG"
            eval("self."+header["Method"])(header,sock)   #执行操作




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

iptable = Iptable()
print(iptable.nodeId)
'''
print 'Waiting for connection...'
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    print "有新连接了" 
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=iptable.recv, args=(sock, addr))
    t.start()

'''
