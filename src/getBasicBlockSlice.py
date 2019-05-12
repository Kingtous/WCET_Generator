# getBasicBlockSlice
import os
import re as r #正则表达式库
import sys
def getBasicBlockSlice(BasicBlock_list_sum, style):
    '''
    将一个Func分为若干个basicblock
    :param BasicBlock_list_sum:一个Func（包含若干个Basicblock）
    :param style: 两种模式：w/b
    :return: 该Func里所有Basicblock的字典集合
    '''
    if style == 'w':

        for basicblock in BasicBlock_list_sum:
            BasicBlock_dictionary = {}  # 创建字典
            start_flag = 'return'                       #先查找"return"节点
            return_start_place = basicblock.find(start_flag)
            partcode_beforreturn=basicblock[:return_start_place-1]
            reverse_partcode_beforreturn=partcode_beforreturn[::-1]        #字符串反转找到最前的"label"
            returnlabel_start_place =reverse_partcode_beforreturn.find('lebal')
            for j in range(returnlabel_start_place,len(reverse_partcode_beforreturn)):
                if reverse_partcode_beforreturn[j] == '{':
                    returnlabel_start_place=j
                    break
            return_start_place=len(partcode_beforreturn)-len(reverse_partcode_beforreturn[:returnlabel_start_place])-1

            temp_end_place=basicblock.find('return',return_start_place)
            bracketsnum=1
            for i in range(temp_end_place+5,len(basicblock)):
                if basicblock[i]=='{':
                    bracketsnum+=1
                elif basicblock[i]=='}':
                    bracketsnum-=1
                    if bracketsnum==-1:
                        return_end_place=i
                        break

            # return语句结束部分
            BasicBlock_dictionary['return'] = basicblock[return_start_place:return_end_place]

            # 将return语句写入字典


            BasicBlock_mainpart=basicblock[:return_start_place]    #将return节点去除

            BasicBlock_start_place=0
            BasicBlock_end_place = 0
            BasicBlocklabel_start_place=BasicBlock_mainpart.find("label")
            while BasicBlocklabel_start_place!=-1:          #每有一个"label"就含有一个basiblock
                BasicBlock_temp = ''
                BasicBlock_temp=findPosFromPoint(BasicBlock_mainpart,BasicBlock_start_place)
                BasicBlock_start_place = BasicBlock_mainpart.find(BasicBlock_temp, BasicBlock_start_place)
                BasicBlock_end_place=BasicBlock_mainpart.find(BasicBlock_temp,BasicBlock_start_place)+len(BasicBlock_temp)
                BasicBlock_temp = findPosFromPoint(BasicBlock_mainpart, BasicBlock_end_place)
                BasicBlock_end_place = BasicBlock_mainpart.find(BasicBlock_temp,BasicBlock_end_place)+len(BasicBlock_temp)
                BasicBlock_temp=BasicBlock_mainpart[BasicBlock_start_place:BasicBlock_end_place+1]
                BasicBlock_start_place=BasicBlock_end_place
                BasicBlock_name=(r.search('bb\d*', BasicBlock_temp)).group()
                name_start_place=BasicBlock_temp.find(BasicBlock_name)
                name_end_place=BasicBlock_temp.find('"',name_start_place)
                BasicBlock_name_part=BasicBlock_temp[name_start_place:name_end_place]
                BasicBlock_realname=''
                basicblock_number=0    #查找basicblock序号
                while BasicBlock_name_part.find(":",basicblock_number)!=-1:
                    for i in range(BasicBlock_name_part.find(":",basicblock_number), len(BasicBlock_name_part)):
                        if BasicBlock_name_part[i]!=":":
                            BasicBlock_realname = BasicBlock_realname+BasicBlock_name_part[basicblock_number:BasicBlock_name_part.find(":",basicblock_number)] +'_'
                            basicblock_number=i
                            break
                BasicBlock_realname=BasicBlock_realname+BasicBlock_name_part[basicblock_number:]
                BasicBlock_dictionary[BasicBlock_realname]=BasicBlock_temp
                BasicBlocklabel_start_place = BasicBlock_mainpart.find("label",BasicBlock_start_place)
                # dict[(r.search('bb\d*', temp)).group()] = temp
        return BasicBlock_dictionary
    elif style == 'b':
        for basicblock in BasicBlock_list_sum:
            BasicBlock_dictionary = {}
            BasicBlock_mainpart = basicblock
            task_start_place=BasicBlock_mainpart.find('"')
            task_end_place=BasicBlock_mainpart.find('"',task_start_place+1)
            BasicBlock_dictionary[BasicBlock_mainpart[task_start_place:task_end_place+1]]=BasicBlock_mainpart
        return BasicBlock_dictionary


def findPosFromPoint(string,startPoint):
    '''
    按照括号匹配的原则对代码切割
    :param string: 代码
    :param startPoint: 起始点
    :return: 切割出的文本
    '''
    FindText=''
    point=startPoint
    cnt=0
    flag=False #找到了
    while True:
        if(point>=len(string)):
            break
        if(flag==True):
            if(string[point]=='{'):
                cnt=cnt+1
            elif(string[point]=='}'):
                cnt=cnt-1
            FindText=FindText+string[point]
            #print(string[point])
            if (cnt==0):
                break
        else:
            #还没到
            if(string[point]=='{'):
                flag=True
                cnt=cnt+1
                FindText=FindText+string[point]
        point=point+1
    return FindText