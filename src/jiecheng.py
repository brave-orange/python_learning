#递归计算阶乘和
def method(num):
    if num == 1:
        return 1
    else:
	    return num*method(num-1)

		
def method2(num):
    if num == 1:
        return 1
    else:
        return method(num)+method2(num-1)
		
		
		
print(method2(100))