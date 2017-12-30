#利用闭包返回一个计数器函数，每次调用它返回递增整数
i = 0
def createCounter():
    def counter():
        global i
        i += 1
        return i        
    return counter

    
a = createCounter()
print(a(),a(),a(),a(),a(),a(),a(),a())