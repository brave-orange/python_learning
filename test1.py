#!/usr/bin/python
# -*- coding: utf-8 -*-
dp = {}
def find_num(n,nums):
    global dp
    if int(nums[0:n] ) > 26:
        return 0
    if int(nums) < 10:
        return 1
    if nums[n:] in dp.keys():
        return dp[nums[n:]]
    a += 1
    if nums[n:] == "":
        num = 0
    else:
        num = int(nums[n:])
    if num < 10:
        return 1
    dp[nums[n:]] = find_num(1,nums[n:])+find_num(2,nums[n:])
    return dp[nums[n:]]

str= "222222226"
print(find_num(1,str)+find_num(2,str))
print(dp)
