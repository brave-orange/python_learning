def a(c):   
    print("hello")
    return c
@a
def b():
    print("jam")
    
    
b()   #等于执行a(b)