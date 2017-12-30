import os, os.path
class SearchFile:
    def __init__(slef,path,str):
        slef.path = path
        slef.str = str
    def finddir(slef):
        r = [x for x in os.listdir(slef.path)]
        return r
        
    def findall(slef,path_now):
        if(os.path.isfile(path_now)):
            if slef.str in os.path.split(path_now)[1]:
                print("文件名：%s" % os.path.split(path_now)[1],"     路径：%s" % path_now.replace(slef.path,''))
            else:
                print('')
        else:
            path_list = os.listdir(path_now)
            
            x = 0
            while x <  len(path_list):
                a = os.path.join(path_now,path_list[x])
                path_list[x] = a
                x += 1
            
            
            if len(path_list):
                for path_now in path_list:
                    slef.findall(path_now)
            
s = SearchFile('F:\\src\\python','py')

s.findall('F:\\src\\python')