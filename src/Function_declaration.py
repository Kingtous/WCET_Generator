import os
import re as r
import sys
def getFunction_declaration(Func_sum):
    '''

    :param Func_sum:alf文件中所有func的集合
    :return: 每个func前的函数申明
    '''
    declaration_dict={}
    for i in range(0, len(Func_sum)):
        func_part = Func_sum[i]
        flag='label'
        label_start_place=func_part.find(flag)
        label_start_place=func_part.find(flag,label_start_place+4)   #找到第二个"label"
        end_place=0
        for j in range(0,label_start_place):               #找到第二个"label"前的第一个"{"
            if func_part[label_start_place-j]=='{':
                end_place=label_start_place-j
                break
        flag_2='"'
        name_start_place=func_part.find(flag_2)
        name_end_place=func_part.find(flag_2,name_start_place+1)
        declaration_name=func_part[name_start_place+1:name_end_place]
        declaration_dict[declaration_name] = func_part[0:end_place]
        Func_sum[i] = func_part[end_place:]

    return declaration_dict


