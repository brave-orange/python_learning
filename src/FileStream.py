#f = open('./code.py','r')
#f.read()
with open('./code.py', mode='r' ,encoding='UTF-8') as f:
    s = f.read(1000)
    while (s):
        print(s)
        s = f.read(1000)