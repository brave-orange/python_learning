class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1


class Man(object):
    __slots__ = ["name","age","height","NO"]    #只允许添加括号内的几个属性
    #def __init__(self,width)  #构造函数中也不能地柜限制之外的属性  
       # self.width = width
    def __init__(self,height):
        self.height = height

m = Man(150)  
   
'''   
s = Student("bob")
s1 = Student("bob1")
s2 = Student("bob2")
s3 = Student("bob3")
s.count = 100
print(s.count)
'''