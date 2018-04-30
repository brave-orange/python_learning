import time
import random
#arr = [5,12,6,25,34,15,8,9,7,2,31,22,74]
arr = []
for i in range(0,999):
    arr.append(random.randrange(1 , round(time.time()/100),1))
def quicksort(left,right):
    if left > right:
        return
    a = arr[left]
    i = left
    j = right
    while i != j:
        while arr[j] >= a and i < j:
            j = j-1
        while arr[i] <= a and i < j:
            i = i+1
        if i < j:
            t = arr[i]
            arr[i] = arr[j]
            arr[j] = t
            
    arr[left] = arr[i]
    arr[i] = a        
    quicksort(left,i-1)
    quicksort(i+1,right)

quicksort(0,998)

print (arr)
