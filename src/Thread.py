#!/usr/bin/env python
# encoding=utf-8
    
    '''
import time, threading ,random
def func1():
    i = 0
    while i < 10:
        
        s = random.random()*3
        print("Thread1(No.%d):sleep %0.2f" % (i,s))
        time.sleep(s)
        i += 1
        
def func2():
    i = 0
    while i < 10:
        s = random.random()*3
        print("Threa2(No.%d):sleep %0.2f" % (i,s))
        time.sleep(s)
        i += 1
        
if __name__ == '__main__':
    t1 = threading.Thread(target = func1)
    t2 = threading.Thread(target = func2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    '''
import threading, multiprocessing
from multiprocessing import Pool
def loop():
    x = 0
    while True:
        x = x ^ 1
        
if __name__=='__main__':
    p = Pool()
     
    for i in range(8):
        p.apply_async(loop)
        
    p.close()
    p.join()
    
    
    
    
    
    
    
    