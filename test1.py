
def find_num(n,nums):
    if nums[n:] == "":
        num = 0
    else:
        num = int(nums[n:])
    if n == 2:
        if int(nums[0:n] ) > 26:
            return 0
    if num < 26:
        return 1
    else:
        return find_num(1,nums[n:])+find_num(2,nums[n:])


print(find_num(1,"226")+find_num(2,"226"))





