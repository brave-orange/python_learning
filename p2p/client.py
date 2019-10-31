# -*- coding: utf-8 -*-
import socket,time,threading,json

def headers(self,data):        #解析数据包
    data = str(data, encoding = "utf8")
    header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
    result = {}
    for line in header_content:
        k, v = line.split(':',1)
        result[k.strip(" ")] = v.strip(" ")
    return result
def send_ping(socket,addr,msg=""): #send ping
    #socket.sendto("ping".encode('UTF_8'),addr)
    request = "Content-Type:PING\r\n"
    request += "msg:Are you OK!"+msg+"\r\n\r\n" #消息
    socket.sendto(request.encode("utf-8"),addr)
    print("send_ping")
    print ("发送ping到"+addr[0])

def recv_ping(socket,addr):  #接收客户端的ping
    global nodes
    while True:
        msg,addr = socket.recvfrom(2048)
        h = headers(msg)
        if(addr not in nodes):
            nodes.append(addr)
            print("add_new node")
        msg = "Content-Type:PONG\r\n"
        msg += "Msg:hello\r\n\r\n" 
        socket.sendto(msg,addr)
def get_nodes(socket,addr):  #ask to server
    request = "Content-Type:FIND_NODE\r\n"
    request += "msg:Are you OK!\r\n\r\n" #消息
    print("向请求邻居")
    print (request)
    socket.sendto(request.encode("utf-8"),addr)
def headers(data):        #解析数据包
    print(data)
    data = data.decode("utf-8")
    header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
    result = {}
    for line in header_content:
        k, v = line.split(':',1)
        result[k.strip(" ")] = v.strip(" ")
    return result

def nodes_back(socket,addr):    #服务端返回节点列表
    response = "Content-Type:RESPONSE_NODE\r\n"
    
    socket.sendto()
def recv(receive,server_addr):
    while True:
        global nodes
        data,addr = receive.recvfrom(2048)  #收到服务器的回应
        header = headers(data)
        if header["Content-Type"] == "PONG" and addr == server_addr: #收到回应的话每隔几秒发送心跳信息
                t2 = threading.Thread(target=heart, args=(receive,addr)) 
                t2.start()
        if header["Content-Type"] == "RESPONSE_NODE":
            print("收到列表")
            node_list = json.loads(header["nodes"])
            global nodes
            nodes = []
            for value in node_list:
                t = tuple(value)
                if value not in nodes and t != myaddr:
                    nodes.append(t)
        if header["Content-Type"] == "PONG" and addr != server_addr:
            msg = "Content-Type:NAT\r\n"
            msg += "msg:success\r\n\r\n"
            receive.sendto(msg.encode("utf-8"),addr)
        if header["Content-Type"] == "PING":
            msg = "Content-Type:PONG\r\n"
            msg += "msg:success\r\n\r\n"
            receive.sendto(msg.encode("utf-8"),addr)

def heart(socket,addr):  #发送心跳
    msg = "Content-Type:HEART\r\n"
    msg += "msg:i'm alive!\r\n\r\n"
    while True:
        socket.sendto(msg.encode("utf-8"),addr)
        time.sleep(3)
nodes = []
myaddr = ()
if __name__ == "__main__":
    addr = ('114.91.184.198',9005)
    receive = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    send_ping(receive, addr)    #say hello与服务器建立连接
    t = threading.Thread(target=recv, args=(receive,addr)) 
    t.start()
    get_nodes(receive, addr)    #获取节点列表
    while True:
        print (nodes)
        if len(nodes)>0:
            for i in range(1,len(nodes)):
                if nodes[i] != myaddr:
                    send_ping(receive,nodes[i],nodes[i][0])
        time.sleep(3)