# Create_every_bb
import os
import platform
import re as r #正则表达式库
import sys
from callFunction import GenerateCallFunction
from callFunction import findPosFromPoint
import shutil
def Create_every_bb (dic,dicti,li,WCETList,filesname,outname):
    outname='/tmp'+outname+'/'
    # outname =outname + '/'
    sysstr = platform.system()#system
    for bb in dic:
        if len(dic)!=1:
            if bb!='return':
                if sysstr=="Linux":
                    getfunc_name = dic[bb]
                    FuncLabel = findlabel(getfunc_name)
                    path = outname + FuncLabel
                    folder = os.path.exists(path)
                    if not folder:
                        os.makedirs(path)
                    GenerateFileName = outname + FuncLabel + '/' + bb + '.alf'
                    # 'Generate_file/'
                else:
                    getfunc_name=dic[bb]
                    FuncLabel=findlabel(getfunc_name)
                    for i in range(0,len(filesname)):
                        if filesname[i] == FuncLabel.lower():
                            FuncLabel=FuncLabel+"_other"
                            break
                    path=outname+FuncLabel
                    folder = os.path.exists(path)
                    if not folder:
                        os.makedirs(path)
                    # f = open('Generate_file/'+'Circle_'+bb+'.txt', 'w')
                    GenerateFileName=outname+FuncLabel+'/'+bb+'.alf'


                f = open(GenerateFileName, 'w')
                for i in range(0,len(li)):
                    #print(i)
                    if type(li[i]) is str:
                        f.write(li[i]+'\n')
                        #print(type(list[i]))
                    elif isinstance(li[i],dict):
                        t=dic[bb]
                        templabel=findlabel(t)
                        # print(templabel)
                        # temp=li[i][templabel]
                        temp=" { lref 64 \""+templabel+"\" }"
                        # print(temp)
                        f.write(temp)
                    else:
                        for j in range(0,len(li[i])):
                            f.write(li[i][j]+'\n')
                f.write(dicti[findlabel(getfunc_name)]+'\n')
                f.write(dic[bb]+'\n')
                call_body=find_call_body(dic[bb])
                if(call_body==0):
                    f.write(dic['return']+'\n')
                    for i in range(0,5):
                        for j in range(0,5-i):
                            f.write(' ')
                        f.write('}\n')
                else:
                    f.write(dic['return'] + '\n')
                    for i in range(0,3):
                        for j in range(0,3-i):
                            f.write(' ')
                        f.write('}\n')
                    f.write(GenerateCallFunction(call_body))
                    f.write('  }\n')
                    f.write(' }\n')
                f.close()
                WCET_Generator(FuncLabel,bb,GenerateFileName,WCETList)
                # os.remove(GenerateFileName)
                # os.removedirs(path)
                # shutil.rmtree(path)
            else:
                if sysstr=="Linux":
                    getfunc_name = dic[bb]
                    FuncLabel = findlabel(getfunc_name)
                    path = outname + FuncLabel
                    folder = os.path.exists(path)
                    if not folder:
                        os.makedirs(path)
                    GenerateFileName = outname + FuncLabel + '/' + bb + '.alf'
                    # 'Generate_file/'
                else:
                    getfunc_name=dic[bb]
                    FuncLabel=findlabel(getfunc_name)
                    for i in range(0,len(filesname)):
                        if filesname[i] == FuncLabel.lower():
                            FuncLabel=FuncLabel+"_other"
                            break
                    path=outname+FuncLabel
                    folder = os.path.exists(path)
                    if not folder:
                        os.makedirs(path)
                    # f = open('Generate_file/'+'Circle_'+bb+'.txt', 'w')
                    GenerateFileName=outname+FuncLabel+'/'+bb+'.alf'

  
                f = open(GenerateFileName, 'w')
                for i in range(0,len(li)):
                    #print(i)
                    if type(li[i]) is str:
                        f.write(li[i]+'\n')
                        #print(type(list[i]))
                    elif isinstance(li[i],dict):
                        t=dic[bb]
                        templabel=findlabel(t)
                        # print(templabel)
                        # temp=li[i][templabel]
                        temp=" { lref 64 \""+templabel+"\" }"
                        # print(temp)
                        f.write(temp)
                    else:
                        for j in range(0,len(li[i])):
                            f.write(li[i][j]+'\n')
                f.write(dicti[findlabel(getfunc_name)]+'\n')
                f.write(dic[bb]+'\n')
                call_body=find_call_body(dic[bb])
                # if(call_body==0):
                #     f.write(dic['return']+'\n')
                #     for i in range(0,5):
                #         for j in range(0,5-i):
                #             f.write(' ')
                #         f.write('}\n')
                # else:
                #     f.write(dic['return'] + '\n')
                #     for i in range(0,3):
                #         for j in range(0,3-i):
                #             f.write(' ')
                #         f.write('}\n')
                #     f.write(GenerateCallFunction(call_body))
                #     f.write('  }\n')
                #     f.write(' }\n')
                for i in range(0,5):
                    f.write(' }\n')
                f.close()
                WCET_Generator(FuncLabel, bb, GenerateFileName, WCETList)
        else:
            #Only have return statement
            if sysstr == "Linux":
                getfunc_name = dic[bb]
                FuncLabel = findlabel(getfunc_name)
                path = outname + FuncLabel
                folder = os.path.exists(path)
                if not folder:
                    os.makedirs(path)
                GenerateFileName = outname + FuncLabel + '/' + bb + '.alf'
                # 'Generate_file/'
            else:
                getfunc_name = dic[bb]
                FuncLabel = findlabel(getfunc_name)
                for i in range(0, len(filesname)):
                    if filesname[i] == FuncLabel.lower():
                        FuncLabel = FuncLabel + "_other"
                        break
                path = outname + FuncLabel
                folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            # f = open('Generate_file/'+'Circle_'+bb+'.txt', 'w')

            GenerateFileName=outname+FuncLabel+'/'+bb+'.alf'
            f = open(GenerateFileName, 'w')
            for i in range(0,len(li)):
                #print(i)
                if type(li[i]) is str:
                    f.write(li[i]+'\n')
                    #print(type(list[i]))
                elif isinstance(li[i],dict):
                    t=dic[bb]
                    templabel=findlabel(t)
                    temp=li[i][templabel]
                    f.write(temp)
                else:
                    for j in range(0,len(li[i])):
                        f.write(li[i][j]+'\n')
            f.write(dicti[findlabel(getfunc_name)]+'\n')
            f.write(dic[bb]+'\n')
            for i in range(0,5):
                for j in range(0,5-i):
                    f.write(' ')
                f.write('}\n')
            f.close()
            WCET_Generator(FuncLabel,bb,GenerateFileName,WCETList)
            # os.remove(GenerateFileName)
            # shutil.rmtree(path)
    funcname=findlabel(dic['return'])
    filesname.append(funcname.lower())

def Create_every_task(dic, dicti, li, filesname,call_names,func_body,outname):# (dict_temp,Every_func_mid_declaration,head,filesname,call_names,filesname_sum)
    outname = outname + '/'
    sysstr = platform.system()  # system
    for bb in dic:
        FuncLabel=findlabel(bb)
        path = outname
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        GenerateFileName = outname + FuncLabel + '.alf'
        f = open(GenerateFileName, 'w')
        for i in range(0, len(li)):
            # print(i)
            if type(li[i]) is str:
                f.write(li[i] + '\n')
                # print(type(list[i]))
            elif isinstance(li[i], dict):
                t = dic[bb]
                templabel = findlabel(t)
                # print(templabel)
                # temp=li[i][templabel]
                temp = " { lref 64 \"" + templabel + "\" }"
                # print(temp)
                f.write(temp)
            else:
                for j in range(0, len(li[i])):
                    f.write(li[i][j] + '\n')
        f.write(dicti[FuncLabel] + '\n')
        f.write(dic[bb] + '\n')
        list=[]
        for i in call_names.keys():
            list.append(call_names[i])
        for i in range(0,len(list)):
            if list[i]!=FuncLabel:
                f.write(dicti[list[i]] + '\n')
                f.write(func_body[list[i]] + '\n')
        f.write('  }\n')
        f.write(' }\n')




def findlabel(str):
    strex='"';
    stren=':';
    s_place=0;
    e_place=0;
    s_place=str.find(strex)
    e_place=str.find(stren,s_place+1)
    result = str[s_place+1:e_place]

    return result


def find_call_body(str):
    string=str.strip()
    start_call_place=string.find("call")
    while(start_call_place != -1 ):
        if string[start_call_place-1]=='_':
            start_call_place=string.find("call",start_call_place+4)
        else:
            call_body=string[len(findPosFromPoint(string,0)):].strip()
            return call_body
    return 0

def WCET_Generator(FuncName,BasicBlock,ALFile,WCETList):
    #call SWEET
    import subprocess
    std_hll=os.path.dirname(os.path.abspath(__file__))+'/Support/std_hll.alf'
    clt=os.path.dirname(os.path.abspath(__file__))+'/Support/CostTimeTable.clt'
    #ALF File=ALFile
    try:
        output = subprocess.Popen('sweet -i='+ALFile+','+std_hll+\
            ' -c extref=off -ae pu aac='+clt+' tc=st,op merge=all'\
                ,stdout=subprocess.PIPE,shell=True).communicate()
        WCET_Time=int(str(output[0]).split('table:')[-1].strip('\\n\"\ '))
        WCETList[FuncName+' '+BasicBlock]=WCET_Time
        print('WCET for '+FuncName+''+BasicBlock+'------'+str(WCET_Time))
    except:
        WCETList[FuncName+' '+BasicBlock]='ERROR'
        print('\n---'+FuncName+' '+BasicBlock+'---Output ERROR---\n')
