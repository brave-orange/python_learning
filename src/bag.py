# #背包问题
# #价值
# v = [1,3,5,4]
# #重量
# w = [3,5,7,6]
# #包的承重量
# bag = 10
# size = len(v)
# # dp = [[0 for _ in range(10)] for _ in range(size)]
# max_value = 0
# for i in range(size):
#     j = bag - w[i] 
#     r = 0
#     value = v[i]
#     while j >= 0 and r < size:
#         j = j - w[r]  #剩余容量
#         if j <= 0:
#             break
#         value = value + v[r]  #当前价值
#         if value > max_value:
#             max_value = value
#         print(i,r,j,max_value)
#         r = r+1

# print(max_value)

        
#背包问题
#价值
v = [1,3,5,4]
#重量
w = [3,5,7,6]
#包的承重量
bag = 10
size = len(v)
# dp = [[0 for _ in range(bag+1)] for _ in range(size+1)]
# for i in range(1,size):
#     weight = w[i]
#     value = v[i]
#     for j in range(1,bag):
#         print(j)
#         if j>=weight:
#             dp[i][j] = max(dp[i-1][j],dp[i-1][j-weight] +value)
#         else:
#             dp[i][j] = dp[i-1][j]

# print(dp)
n = size
c = bag
value = [[0 for j in range(c + 1)] for i in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, c + 1):
        value[i][j] = value[i - 1][j]  #不放进去的情况
        # 背包总容量够放当前物体，遍历前一个状态考虑是否置换
        if j >= w[i - 1] and value[i][j] < value[i - 1][j - w[i - 1]] + v[i - 1]:
            print(i,j)
            value[i][j] = value[i - 1][j - w[i - 1]] + v[i - 1]
# for x in value:
#     print(x)
print(value)

        
