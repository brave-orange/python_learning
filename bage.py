#!/usr/bin/python
# coding:utf-8
import numpy as np
m = 10
n = 6
w = [2, 2, 3, 1, 5, 2]
v = [2, 3, 1, 5, 4, 3]
vec = np.zeros([n+1,m+1],int)

for i in range(1,n+1):
    for j in range(1,m+1):

        if w[i-1] > j:   #剩余容量不够装第i个商品
            vec[i][j] = vec[i-1][j]
        else:
            tmp1 = v[i-1] + vec[i - 1][j - w[i-1]]
            tmp2 = vec[i - 1][j]
            vec[i][j] = tmp1 if tmp1 > tmp2 else tmp2
        j = j + 1

print(vec)