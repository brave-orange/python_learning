#!/usr/bin/env python
# encoding=utf-8

import socket
import threading,time,fcntl, struct,os,random,json
'''
kad算法
'''
class Iptable(object):

    def __init__(self):
        
        self.k_bucket = list() #k桶（k_bucket[0]中存放距离在1~n的节点…………）
        self.k_number = 6
        self.k_bucket.append({"KadId":"0xbda0e659f6c5","ip":"172.31.0.17","port":6666})
        self.myaddr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', "eth0"[:15]))[20:24])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#无状态socket
        if self.myaddr == "172.31.0.17":
            self.nodeId = "0xbda0e659f6c5"
        else:
            self.makeId() #随机ID
        self.port = 6666
        #self.iptables.add("172.31.0.17") 
        print self.nodeId
        for kad in self.k_bucket:
            kad["distance"] = int(self.nodeId,16)^int(kad["KadId"],16)
            self.send_ping(kad["ip"],kad["port"])   #发送ping
        #self.myaddr = urlopen('http://ip.42.pl/raw').read()#获取本机ip
        
        print "p2p节点初始化完成"
        

    def makeId(self):   #生成随机ID
        str = ""
        for i in range(15):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch

        #self.nodeId  = hex(long(str)) #python2
        self.nodeId  = hex(int(str)) #python3
    def addto_k_bucket(self,nodeId,ip,port):   #添加一个节点到K桶
        if len(self.k_bucket) < self.k_number:
            self.k_bucket.append({"KadId":nodeId,"ip":ip,"port":int(port),"distance":int(int(self.nodeId,16)^int(nodeId,16))})
        else:
            self.k_bucket.pop(0)
            self.k_bucket.append({"KadId":nodeId,"ip":ip,"port":int(port),"distance":int(int(self.nodeId,16)^int(nodeId,16))})
    def headers(self,data):        #解析数据包
        header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
        result = {}
        for line in header_content:
            k, v = line.split(':',1)
            result[k.strip(" ")] = v.strip(" ")
        return result

    def send_ping(self,ip,port):
        if(ip != self.myaddr):
            request = "Content-Type:PING\r\n" #表示是看看是不是活得
            request += "msg:Are you OK!\r\n" #消息
            request += "NodeId:"+self.nodeId+"\r\n"#来源ID
            request += "From:"+self.myaddr+"\r\n" #来源ip
            request += "Port:6666\r\n\r\n"   #端口号
            addr = (ip,int(port))
            self.socket.sendto(request,addr)
            print "发送ping到"+ip
            

    def send_pong(self,ip,port,nodeId):
        response = "Content-Type:PONG\r\n" #回复我还活着
        response += "msg:I'm fine,thinks and you?\r\n" #消息
        response += "NodeId:"+self.nodeId+"\r\n" #来源ID
        response += "From:"+self.myaddr+"\r\n" #来源ip
        response += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        self.addto_k_bucket(nodeId,ip,port)     #这个节点存进zi自己的k桶
        print "回复PONG到"+ip
        self.socket.sendto(response,addr)

    def send_findnode(self,ip,port,nodeId):
        #self.k_bucket.append({"nodeId":nodeId,"ip":ip,"port":int(port),"distance":int(distance,16)})  
        
        request = "Content-Type:FIND_NODE\r\n"
        request += "NodeId:"+self.nodeId+"\r\n"#来源ID
        request += "From:"+self.myaddr+"\r\n"
        request += "Port:6666\r\n\r\n"   #端口号
        addr = (ip,int(port))
        print"向"+ip+"请求邻居"
        print request
        self.socket.sendto(request,addr)

    def response_findnode(self,ip,port,nodeId):    #回复k桶数据
        response = "Content-Type:RESPONSE_NODE\r\n"
        response += "NodeId:"+nodeId+"\r\n"#来源ID
        response += "From:"+self.myaddr+"\r\n"
        response += "Port:6666\r\n"   #端口号
        nodes = []
        for k in self.k_bucket:    #找到k桶中离请求点最近的k_number个节点
            
            distance = int(k["KadId"],16)^int(nodeId,16)
            if distance == 0:
                continue
            if len(nodes) < self.k_number:
                nodes.append({"nodeId":k["KadId"],"ip":ip,"port":k["port"],"distance":distance}) 
            else:
                max_node = nodes[0]
                for n in nodes:
                    if n["distance"] > max_node["distance"]:
                        max_node = n
                if distance < max_node["distance"]:
                    nodes[nodes.index(max_node)] = {"nodeId":k["KadId"],"ip":ip,"port":int(port),"distance":idistance}   #替换距离更大的
        msg = json.dumps(nodes)
        response += "Kbucket:"+msg+"\r\n\r\n"
        addr = (ip,int(port))
        print"向"+ip+"回复邻居"
        print response
        self.socket.sendto(response,addr)
    
    def refresh_k_bucket(self,nodes_str): #收到节点数据刷新k桶
        nodes = json.loads(nodes_str)

        for k in nodes:
            print self.k_bucket;
            for value in self.k_bucket:
                distance = int(k["nodeId"],16)^int(value["KadId"],16)
                if distance == 0:
                    continue
                if len(self.k_bucket) < self.k_number:
                    self.k_bucket.append({"KadId": k["nodeId"],"ip":k["ip"],"port": k["port"],"distance":distance}) 
                else:
                    max_node = nodes[0]
                    for n in self.k_bucket:
                        if n["distance"] > max_node["distance"]:
                            max_node = n
                    if distance < max_node["distance"]:
                        self.k_bucket[nodes.index(max_node)] = {"KadId": k["nodeId"],"ip":k["ip"],"port":int(port),"distance":distance}
        print "已刷新K桶"
        print self.k_bucket

    def recv(self,header):   #处理接收到的请求
        header = self.headers(header)
        print header

        if header["Content-Type"] == "PING":    #收到PING数据
            print "收到PING,回复PONG，存入K桶"
            self.send_pong(header["From"],header["Port"],header["NodeId"])
            
        if header["Content-Type"] == "PONG":    #收到PONG消息
            print "收到PONG,问他要他的邻居"
            self.send_findnode(header["From"],header["Port"],header["NodeId"])    #发送find_node

        if header["Content-Type"] == "FIND_NODE":    #收到寻找节点的请求
            print "收到FIND_NODE,回复他k桶里的东西"
            self.response_findnode(header["From"],header["Port"],header["NodeId"])

        if header["Content-Type"] == "RESPONSE_NODE":    #收到回复节点消息，更新自己的k桶
            self.refresh_k_bucket(header["Kbucket"])


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0",6666))
iptable = Iptable()
#print(iptable.nodeId)

print 'Waiting for connection...'

while True:
    # 接受一个新连接:
    header,address = s.recvfrom(2048)
    print "有消息了" 
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=iptable.recv, args=(header,))
    t.start()

