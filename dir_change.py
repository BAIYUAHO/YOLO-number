#导入os模块和time模块
import os
import time
#利用os模块的方法，用start记录最开始你要监控的文件夹里面有哪些文件


def dirchange():
    p = './data/images'
    startdir = os.listdir(p)
    while True:

        #如果一开始监控的文件夹和30秒以后的文件夹里面的内容不同了，就把30秒以后的文件夹记录到end中
        if startdir != os.listdir(p):
            startdir = os.listdir(p)
            end = os.listdir(p)
            n = len(end)-1
            p0 = p+'/'+ end[n]
            print(p0)

        else:
            startdir = os.listdir(p)
        #每隔30秒进行一次监控
        time.sleep(0.5)

