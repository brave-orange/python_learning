#递归计算杨辉三角

def yanghui(i,j):
    if i == 1 and j == 1:
        return 1
    if i < 0 or j > i:
        return 0
    else:
        return yanghui(i-1,j-1) + yanghui(i-1,j)
        
print(yanghui(6,5))