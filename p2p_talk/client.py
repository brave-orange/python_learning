#!/usr/bin/env python
# encoding=utf-8
import socket
import threading,time
from multiprocessing import Process
import os
def recv_message(sock):

    while True:
        data = sock.recv(2048).decode('utf-8')
        print(data)
        time.sleep(5)

def send_message(sock):
    while True:
        data = input('speak:')
        sock.send(data.encode('utf-8'))
        time.sleep(5)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("114.91.184.198",9005))        


recv1 = threading.Thread(target=recv_message, args=(s,))
send1 = threading.Thread(target=send_message, args=(s,))
recv1.start()
time.sleep(2)
send1.start()
recv1.join()
send1.join()





