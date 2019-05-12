import os
import re as r
import sys
def Delete_Note(func_list):
    '''

    :param func_list: 所有Func的集合（含注释）
    :return: 所有Func的集合（不含注释）
    '''
    for i in range(0, len(func_list)):
        string = func_list[i]
        note_start='/*'
        note_end='*/'
        start_place=0
        end_place=0
        start_place=string.find(note_start)
        while start_place!=-1:
            end_place=string.find(note_end,start_place)
            string=string[:start_place]+string[end_place+2:]
            start_place=string.find(note_start,end_place)
        start_place=string.find(note_start)
        while start_place!=-1:
            end_place=string.find(note_end,start_place)
            string=string[:start_place]+string[end_place+2:]
            start_place=string.find(note_start,end_place)

        func_list[i]=string

