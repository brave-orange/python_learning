#能直接作用于for循环的数据类型、带有yield的function都叫做可迭代对象：Iterable
#使用isinstance()判断是不是可迭代对象
#生成器可以被Next()函数一直调用返回下一个值被称作迭代器：Iterator
#使用isinstance()判断是不是可迭代器
#生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。

#把list、dict、str等Iterable变成Iterator可以使用iter()函数：


def f(x):
    return x*x
    
r = map(f , [1,2,3,4,5,6,7,8,9])   #执行f函数，并返回值为迭代器


list(r)      #函数让它把整个序列都计算出来并返回一个list。
