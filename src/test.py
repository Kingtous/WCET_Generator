import os
import re as r #正则表达式库
import sys
from readalf import readalf
from getHeader1 import getHeader
from getFunc import getFunc
from Delete_Note import Delete_Note
from Function_declaration import getFunction_declaration
from replace_call import replace_call
from getBasicBlockSlice import getBasicBlockSlice
from Create_every_bb import Create_every_bb

Enter_File_Name=input("Input file name:")
hashtag_rule=r.compile(u'(\/\*(\s|.)*?\*\/)|(\/\/.*)')
file = open(Enter_File_Name, 'r')
content = file.readlines()
head=getHeader(content)  #head：alf代码总的函数声明
file.close()
#print(head)
DATA=readalf(Enter_File_Name)#DATA：将代码保存为一个字符串放白奴和
#print(head)
#print(DATA)
list_func=getFunc(DATA)#将DATA里的每一个func提取出来组合为一个列表（含注释）
#for i in range(0,len(list_func)):
    #print(list_func[i])
#print(list_func)
Delete_Note(list_func)#将list_func的注释清除
#print(list_func)
Every_func_mid_declaration=getFunction_declaration(list_func)
#print(Every_func_mid_declaration)
for i in range(0,len(list_func)):
    list_func_temp=[]
    list_func_temp.append(list_func[i])
    dict_temp=getBasicBlockSlice(list_func_temp)
    #print(dict_temp)
    replace_call(dict_temp)
    #print(dict_temp)
    Create_every_bb(dict_temp,Every_func_mid_declaration,head)

print('Create "alf"file Success!')
# print(Every_func_mid_declaration)
# print(list_func)
