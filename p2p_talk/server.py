#!/usr/bin/env python
# encoding=utf-8
import socket
import threading,time

def tcplink(sock, addr):
    name=""
    print('Accept new connection from %s:%s...' % addr)
    for i in range(0, len(person)):
        print(person[i])
        if addr == person[i]['addr']:
            if person[i]['name'] == "":
                print("send hello")
                sock.send(b'sys:What is your name?')
                data = sock.recv(2048).decode('utf-8')
                person[i]['name'] = data
                name = data
            break
    online_list = "******************online_list********************\n" 
    for i in range(0, len(person)):        
        online_list += "%d : name:%s           ip:%s \n" %  (i,person[i]['name'],person[i]['addr'][0])
    online_list += "\n\n\n input the %+number(%1) to choose somebody to talk \n input '%public' to talk with all of people,\n input '%refresh' to reload online_list \n input '%-1' to quit,input '%-2' to quit talk." 
    online_list += "*************************************************\n\n\n" 
    sock.send(online_list.encode('utf-8'))
    mode = 0    ##代表当前聊天模式 0：功能选择，1：P2P对话模式，2：广播模式
    target = ""
    while True:
        data = sock.recv(2048).decode('utf-8') 
        if data[0] == '%':
            c = data[1:]
            if c == "public":
                sock.send(b'sys:Ok,you can talk with all of people now.')
                mode = 2
            elif c == "refresh":
                online_list = "******************online_list********************\n" 
                for i in range(0, len(person)):        
                    online_list += "%d : name:%s           ip:%s \n" %  (i,person[i]['name'],person[i]['addr'][0])
                online_list += "\n\n\n input the %+number(%1) to choose somebody to talk \n input '%public' to talk with all of people,\n input '%refresh' to reload online_list \n input %-1 to quit." 
                online_list += "*************************************************\n\n\n" 
                sock.send(online_list.encode('utf-8'))
            elif c == "-1":
                sock.send("bye!".encode('utf-8'))
                sock.close()
                mode = 0;
                break
            elif c == "-2":
                sock.send("sys:already quit talk.".encode('utf-8'))
                mode = 0 
            else:
                c1 = int(c)
                target = person[c1]
                mode = 1
        else:
            if mode == 1:
                str = "%s(%s):%s\n time:%s" % (name,addr,data,time.time())
                target_sock = target['sock']
                target_sock.send(str.encode('utf-8'))
            elif mode == 2:
                str = "[Radio]%s(%s):%s\n time:%s" % (name,addr,data,time.time())
                for i in range(0, len(person)):
                    target_sock = person[i]['sock']
                    target_sock.send(str.encode('utf-8'))
            elif mode == 0:
                online_list = "******************online_list********************\n" 
                for i in range(0, len(person)):        
                    online_list += "%d : name:%s           ip:%s \n" %  (i,person[i]['name'],person[i]['addr'][0])
                online_list += "\n\n\n input the %+number(%1) to choose somebody to talk \n input '%public' to talk with all of people,\n input '%refresh' to reload online_list \n input %-1 to quit." 
                online_list += "*************************************************\n\n\n" 
                sock.send(online_list.encode('utf-8'))
                
                
        
    print(person)




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
person = [] #存储来的人

s.bind(('0.0.0.0',6666))
s.listen(10)
print('Waiting for connection...')

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    person.append({'addr':addr,'sock':sock,'name':''})
    
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

