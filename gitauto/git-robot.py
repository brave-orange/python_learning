import socket,os
import json,time
from config import *
from urllib import *

def headers(data):
        header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        result = {}
        for line in header_content:
            k, v = line.split(': ')
            result[quote(k)] = quote(v)
        return result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind(('0.0.0.0',10987))
s.listen(10)
print "waiting connect"
while True:
    sock, addr = s.accept()
    res = sock.recv(4096).decode('utf-8')
    header = headers(res)
    if "X-Gitlab-Token" in header.keys():
        if header["X-Gitlab-Token"] == "istillloveyou":
            if header["X-Gitlab-Event"] == "Push%20Hook":
                os.system("cd %s && git pull origin master" % config["project_path"])
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print "**************************************************************"
    '''
    data = res.split()    
    body = ""
    method = data[0]
    if method == "POST":
        if data[4] == "Coding.net":
            if data[-1] != "":
                body = res.split('\r\n\r\n', 1)[1]
    if body != "":
        body_json = json.loads(body)
        
        if body_json["token"] == "istillloveyou":
    '''        
           



