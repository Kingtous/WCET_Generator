import os
import re as r #正则表达式库
import sys,getopt
from help import ShowOptions
from readalf import readalf
from getInit import getInitialHeader
from getFunc import getFunc
from Delete_Note import Delete_Note
from Function_declaration import getFunction_declaration
from replace_call import replace_call
from getBasicBlockSlice import getBasicBlockSlice
from Create_every_bb import Create_every_bb
from Create_every_bb import Create_every_task
from WCET_Generator import WCET_Output

def Generate_evealf(input_filename, output_filename):#'w':'Generate WCET for the file imported.'
    '''
    以basicblock为单位生成每个节点的WECT
    :param input_filename: 输入文件名
    :param output_filename: 输出文件名
    :return:
    '''
    try:

        Enter_File_Name =input_filename

    except:
        print('Please Input ALF file u\'d like to analyze.\nAborted.')
        sys.exit(0)

    WCETList = {}
    call_result={}
    if os.path.isfile(Enter_File_Name):
        #hashtag_rule = r.compile(u'(\/\*(\s|.)*?\*\/)|(\/\/.*)')
        file = open(Enter_File_Name, 'r')
        content = file.readlines()
        Total_Function_Declarations = getInitialHeader(content)  # Total_Function_Declarations：alf代码总的函数声明
        file.close()
        DATA = readalf(Enter_File_Name)  # DATA：将代码保存为一个字符串

        list_func_body = getFunc(DATA)  # 将DATA里的每一个func提取出来组合为一个列表（含注释）
        Delete_Note(list_func_body)  # 将list_func的注释清除
        Every_func_mid_declaration = getFunction_declaration(list_func_body)  #Every_func_mid_declaration每个Func前的函数申明
        funcsname_sum = []
        for i in range(0, len(list_func_body)):
            funcsname_sum.append(findlabel(list_func_body[i]))
        filesname=[]
        for i in range(0, len(list_func_body)):
            temp = []
            temp.append(list_func_body[i])

            basicblock_set = getBasicBlockSlice(temp,'w')

            replace_call(basicblock_set, funcsname_sum, call_result, 'w')

            Create_every_bb(basicblock_set, Every_func_mid_declaration, Total_Function_Declarations, WCETList, filesname, output_filename)
        WCET_Output(WCETList,os.path.splitext(Enter_File_Name)[0])
        print('Create ALF file Success!')

    else:
        print('It\'s not a file')

def Generate_taskalf(input_filename, output_filename):#'b':'Generate ALF for every OpenMP task.',
    '''
    针对每个TaskFunc生成alf文件
    :param input_filename: 输入文件名
    :param output_filename: 输出文件名
    :return:
    '''
    try:

        Enter_File_Name = input_filename

    except:
        print('Please Input ALF file u\'d like to analyze.\nAborted.')
        sys.exit(0)

    WCETList={}

    if os.path.isfile(Enter_File_Name) :
        file = open(Enter_File_Name, 'r')
        content = file.readlines()
        Total_Function_Declarations=getInitialHeader(content)  #Total_Function_Declarations：alf代码总的函数声明
        file.close()

        DATA=readalf(Enter_File_Name)#DATA：将代码保存为一个字符串

        list_func_body=getFunc(DATA)#将DATA里的每一个func提取出来组合为一个列表（含注释）
        Delete_Note(list_func_body)#将list_func的注释清除
        Every_func_mid_declaration=getFunction_declaration(list_func_body)
        funcs_sum = {}
        callFunc_sum={}
        for i in range(0, len(list_func_body)):
            funcs_sum[findlabel(list_func_body[i])]=list_func_body[i]
        filesname=[]

        for i in range(0,len(list_func_body)):
            list_func_temp=[]
            list_func_temp.append(list_func_body[i])
            funcname_start_place=list_func_temp[0].find('"')
            funcname_end_place=list_func_temp[0].find('"',funcname_start_place+1)

            if (list_func_temp[0][funcname_start_place:funcname_end_place+1].find('taskFunc')!=-1) or (list_func_temp[0][funcname_start_place:funcname_end_place+1].find('thrFunc')!=-1):
                callFunc_sum={}             #callFunc_sum：函数各个节点调用关系字典（key：节点，value：被调用函数）
                basicblock_set=getBasicBlockSlice(list_func_temp,'b')

                callFunc_names=replace_call(basicblock_set, funcs_sum, callFunc_sum, 'b')

                Create_every_task(basicblock_set, Every_func_mid_declaration, Total_Function_Declarations, filesname, callFunc_names, funcs_sum, output_filename)
                funcrelation_end_placee = list_func_temp[0].find(':', funcname_start_place + 1)
                GenerateFileName = output_filename + '/' + list_func_temp[0][funcname_start_place + 1:funcrelation_end_placee] + 'relation.txt'

                f = open(GenerateFileName, 'w')
                for i in callFunc_sum.keys():
                    f.write(i+'    ')
                    f.write(callFunc_sum[i]+'\n')


        print('Create ALF file Success!')

    else:
        print('It\'s not a file')
def findlabel(str):
    '''
    寻找该段代码对应的函数名（""内的为函数名）
    :param str: 代码
    :return: 函数名
    '''
    flag_1='"'
    flag_2=':'

    start_place=str.find(flag_1)
    end_place=str.find(flag_2,start_place+1)
    result = str[start_place+1:end_place]

    return result
