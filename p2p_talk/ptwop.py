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
        self.k_number = 6
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
        self.nodeId  = hex(long(str)) #python2
        #self.nodeId  = hex(int(str)) #python3
    def addto_k_bucket(self,nodeId,ip,port,distance):   #添加K桶
        if len(self.k_bucket) < self k_number:
            self.k_bucket.append({"KadId":nodeId,"ip"：ip,"port":int(port),"distance":int(int(self.nodeId,16)^,int(nodeId,16))})
        else:
            self.k_bucket.pop(0)
            self.k_bucket.append({"KadId":nodeId,"ip"：ip,"port":int(port),"distance":int(int(self.nodeId,16)^,int(nodeId,16))})

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
        request += "NodeId:"+self.nodeId+"\r\n"#来源ID
        request += "From:"+self.myaddr+"\r\n" #来源ip
        request += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        self.socket.sendto(request,addr)

    def send_pong(self,ip,port):
        response = "Content-Type:PONG\r\n" #回复我还活着
        response += "msg:I'm fine,thinks and you?\r\n" #消息
        response += "NodeId:"+self.nodeId+"\r\n" #来源ID
        response += "From:"+self.myaddr+"\r\n" #来源ip
        response += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))

        self.socket.sendto(response,addr)

    def send_findnode(self,ip,port,nodeId):
        #self.k_bucket.append({"nodeId":nodeId,"ip":ip,"port":int(port),"distance":int(distance,16)})  
        self.addto_k_bucket(nodeId,ip,port)     #这个节点存进zi自己的k桶
        request = "Content-Type:FIND_NODE\r\n"
        request += "NodeId:"+self.nodeId+"\r\n"#来源ID
        request += "From:"+self.myaddr+"\r\n"s
        request += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        self.socket.sendto(request,addr)

    def response_findnode(self,nodeId,ip,port):    #回复k桶数据
        response = "Content-Type:RESPONSE_NODE\r\n"
        response += "NodeId:"+nodeId+"\r\n"#来源ID
        response += "From:"+self.myaddr+"\r\n"
        response += "Port:6666\r\n"   #端口号
        nodes = []
        for k in self.k_bucket:    #找到k桶中离请求点最近的k_number个节点
            distance = k["KadId"]^nodeId
            if len(nodes) < self.k_number:
                nodes.append({"nodeId":nodeId,"ip":ip,"port":int(port),"distance":int(distance,16)}) 
            else:
                for n in nodes:
                    if n["distance"] > distance:
                        nodes[nodes.index(n)] = {"nodeId":nodeId,"ip":ip,"port":int(port),"distance":int(distance,16)}   #替换距离更大的
        msg = json.dumps(nodes)
        response += "Kbucket:"+msg+"\r\n\r\n"
        addr = (ip,int(port))
        self.socket.sendto(response,addr)

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
        if header["Content-Type"] == "PING":    #收到PING数据
            print "收到PING,回复PONG，存入K桶"
            self.send_pong(header["From"],header["Port"])
            
        if header["Content-Type"] == "PONG":    #收到PONG消息
            print "收到PONG,问他要他的邻居"
            self.send_findnode(header["ip"],header["port"],header["NodeId"])    #发送find_node

        if header["Content-Type"] == "FIND_NODE":    #收到寻找节点的请求
            print "收到FIND_NODE,回复他k桶里的东西"
            self.response_findnode(header["ip"],header["port"])

        if header["Content-Type"] == "RESPONSE_NODE":    #收到回复节点消息，更新自己的k桶
            




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

iptable = Iptable()
print 'Waiting for recv......'
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    print "有消息了" 
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=iptable.recv, args=(sock, addr))
    t.start()

