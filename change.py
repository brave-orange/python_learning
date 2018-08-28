'''
批量修改目录下文件的需要改动的内容

'''

import os
def getAllfileAndDirPath(sourcePath):
    if not os.path.exists(sourcePath):
        return
    listName = os.listdir(sourcePath)
    for name in listName:
        absPath = os.path.join(sourcePath,name)
        if os.path.isfile(absPath):
            if absPath.find('.') != -1 and absPath[absPath.find('.') :] == ".php":
                with open(absPath,'rb+') as f:
                    t = f.read().decode('utf8')
                    t = t.replace("shanghai.com.cn","onmycard.com.cn")
                    f.seek(0,0)
                    f.write(t.encode('utf8'))
                print("修改%s完成" % absPath)
        if os.path.isdir(absPath):
            getAllfileAndDirPath(absPath)

getAllfileAndDirPath(r'test')