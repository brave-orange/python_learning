#使用sorted排序
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
    return t[0]
a = sorted(L,key = by_name,reverse=True)   #reverse:反向
print(a)
  