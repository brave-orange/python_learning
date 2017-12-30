#去除字符串首位空格

def trim(s):
    strlen = len(s)
    head = 0
    tail = 0
    a = 0

    while a < strlen:
        if s[a] != ' ':
            head = a
            break
        else:
            a = a + 1
			
    a = strlen -1
    while a > 0:
        if s[a] != ' ':
            tail = a
            break
        else:
            a = a - 1
    return s[head:tail]
	
print(trim("   gfdgdgd    "))