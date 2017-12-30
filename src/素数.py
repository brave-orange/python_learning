#利用fitter（）筛选出素数集合

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
#使用生成器无限的数列


def _not_divisible(n):    #筛选函数
    return lambda x: x % n > 0   #相当于if (x%n)>0:return 0 else: return 1
    
def primes():
    it =  _odd_iter()
    while True:
        n = next(it)
        yield n   
        it = filter(_not_divisible(n),it)        #将非素数筛选出去
 


for i in primes():
    if i < 1000:
        print(i)
    else:
        break
    
'''
def a():
    n = 1
    while True:
        n = n + 2
        yield n
     
        

n = a()
print(next(n))  
print(next(n))  
print(next(n))        
'''
