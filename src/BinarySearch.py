#递归二分查找

a=[i for i in range(1,100000000)]
def search(a,left,right,num):
    mid = round((left+right)/2)
    print(mid)
    if a[mid]>num:
        return search(a,left,mid,num)
    elif a[mid]<num:
        return search(a,mid,right,num)
    else:
        return mid
        
print(search(a,0,99999999,5))
