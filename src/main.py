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
from WCET_Generator import WCET_Output
from method import  Generate_evealf
from method import  Generate_taskalf


if __name__=="__main__":
    #Input Text
    File_Name=''
    WCET_File_Name=''
    Task_ALF_Output_Directiory=''
    #Flag
    op_i=False
    op_t=False
    op_w=False
    op_h=False
    #Process
    getArgs={}
    options,args=getopt.getopt(sys.argv[1:],"hi:w:t:o:")
    for op,value in options:
        if op == '-h':
            ShowOptions()
            sys.exit(0)
        if op == '-i':
            op_i=True
            File_Name=value
            getArgs['i']=value
            continue
        if op == '-w':
            op_w=True
            getArgs['w']=value
            WCET_File_Name=value
            continue
        if op == '-t':
            op_t=True
            getArgs['w']=value
            Task_ALF_Output_Directiory=value
    if (op_i == False):
        print('Please Import the file u\'d like to analyze.\nAborted.')
    else:
        if op_w!=False:
            Generate_evealf(getArgs['i'],WCET_File_Name)
        elif op_t!=False:
            Generate_taskalf(getArgs['i'],Task_ALF_Output_Directiory)

else:
    print("Please run this scripts directly.")
