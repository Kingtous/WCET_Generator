import os
import re as r
def readalf(string):
    '''

    :param string:alf文件名
    :return: alf文件（一个长字符串）
    '''
    alfdata=''
    data_path=string
    data = open(data_path,'r')
    # body=open(data_path+ '.txt', 'w')
    line = data.readline()
    while line:             #直到读取完文件
         # body.write(line)
         if line[-1]!='\n':
              alfdata=alfdata+line
         else:
              alfdata=alfdata+line[:-1]
         line = data.readline()  #读取一行文件，包括换行符

    data.close()

    return alfdata

