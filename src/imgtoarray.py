'''
图片转换为一维矩阵
'''
from scipy.misc import imread
from numpy import *
img = imread('sad.png')
data = zeros((1,img.shape[2]*img.shape[1]*img.shape[0]))

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        for t in range(img.shape[2]):
            print(i,j,t)
            data[0,3*i*j+t] = img[i][j][t]
print(data.shape)