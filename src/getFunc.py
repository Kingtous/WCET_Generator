import os
import re as r
import sys
# stri ='{ alf { macro_defs } { least_addr_unit 8 } little_endian { exports  { frefs }  { lrefs { lref 64 "f" } { lref 64 "_taskFunc0_" } { lref 64 "Circle" } { lref 64 "__original_main" } { lref 64 "_taskFunc1_" } } } { imports  { frefs   { fref 64 "$null" }   { fref 64 "$mem" }  }  { lrefs } } { decls } { inits } { funcs/* Definition of function Circle */  { func   { label 64 { lref 64 "Circle" } { dec_unsigned 64 0 } }   { arg_decls }   { scope    { decls     { alloc 64 "%i.0" 32 } /* Local Variable (PHI node) */      { alloc 64 "%tmp4" 32 } /* Local Variable (Non-Inlinable Instruction) */     }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "Circle::bb" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb::0      *   br label %bb1 */     { store { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } with { dec_unsigned 32 0 } }     { label 64 { lref 64 "Circle::bb::0:::1" } { dec_unsigned 64 0 } }     { jump { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb1 ---------- */     { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb1::2      *   %tmp = icmp slt i32 %i.0, 100      *   br i1 %tmp, label %bb2, label %bb5 */     { switch      { s_lt 32 { load 32 { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } } { dec_unsigned 32 100 } }      { target { dec_signed 1 { minus 1 } } { label 64 { lref 64 "Circle::bb2" } { dec_unsigned 64 0 } } }      { default { label 64 { lref 64 "Circle::bb5" } { dec_unsigned 64 0 } } }     }     /* --------- BASIC BLOCK bb2 ---------- */     { label 64 { lref 64 "Circle::bb2" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb2::0      *   br label %bb3 */     { jump { label 64 { lref 64 "Circle::bb3" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb3 ---------- */     { label 64 { lref 64 "Circle::bb3" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb3::0      *   %tmp4 = add nsw i32 %i.0, 1 */     { store { addr 64 { fref 64 "%tmp4" } { dec_unsigned 64 0 } } with      { add 32 { load 32 { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } } { dec_unsigned 32 1 } { dec_unsigned 1 0 } }     }     /* STATEMENT Circle::bb3::1      *   br label %bb1 */     { label 64 { lref 64 "Circle::bb3::1" } { dec_unsigned 64 0 } }     { store { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } with { load 32 { addr 64 { fref 64 "%tmp4" } { dec_unsigned 64 0 } } } }     { label 64 { lref 64 "Circle::bb3::1:::1" } { dec_unsigned 64 0 } }     { jump { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb5 ---------- */     { label 64 { lref 64 "Circle::bb5" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb5::0      *   ret void */     { return }    }   }  } }}'    #例子
# stri ='{ alf { macro_defs } { least_addr_unit 8 } little_endian { exports  { frefs }  { lrefs { lref 64 "f" } { lref 64 "_taskFunc0_" } { lref 64 "Circle" } { lref 64 "__original_main" } { lref 64 "_taskFunc1_" } } } { imports  { frefs   { fref 64 "$null" }   { fref 64 "$mem" }  }  { lrefs } } { decls } { inits } { funcs  /* Definition of function f */  { func   { label 64 { lref 64 "f" } { dec_unsigned 64 0 } }   { arg_decls    { alloc 64 "%p" 32 }   }   { scope    { decls }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "f::bb" } { dec_unsigned 64 0 } }     /* STATEMENT f::bb::0      *   ret void */     { return }    }   }  }  /* Definition of function _taskFunc0_ */  { func   { label 64 { lref 64 "_taskFunc0_" } { dec_unsigned 64 0 } }   { arg_decls    { alloc 64 "%__arg" 64 }   }   { scope    { decls }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "_taskFunc0_::bb" } { dec_unsigned 64 0 } }     /* STATEMENT _taskFunc0_::bb::0      *   br label %bb1 */     { jump { label 64 { lref 64 "_taskFunc0_::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb1 ---------- */     { label 64 { lref 64 "_taskFunc0_::bb1" } { dec_unsigned 64 0 } }     /* STATEMENT _taskFunc0_::bb1::0      *   ret i8* null */     { return { addr 64 { fref 64 "$null" } { dec_unsigned 64 0 } } }    }   }  }  /* Definition of function Circle */  { func   { label 64 { lref 64 "Circle" } { dec_unsigned 64 0 } }   { arg_decls }   { scope    { decls     { alloc 64 "%i.0" 32 } /* Local Variable (PHI node) */      { alloc 64 "%tmp4" 32 } /* Local Variable (Non-Inlinable Instruction) */     }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "Circle::bb" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb::0      *   br label %bb1 */     { store { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } with { dec_unsigned 32 0 } }     { label 64 { lref 64 "Circle::bb::0:::1" } { dec_unsigned 64 0 } }     { jump { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb1 ---------- */     { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb1::2      *   %tmp = icmp slt i32 %i.0, 100      *   br i1 %tmp, label %bb2, label %bb5 */     { switch      { s_lt 32 { load 32 { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } } { dec_unsigned 32 100 } }      { target { dec_signed 1 { minus 1 } } { label 64 { lref 64 "Circle::bb2" } { dec_unsigned 64 0 } } }      { default { label 64 { lref 64 "Circle::bb5" } { dec_unsigned 64 0 } } }     }     /* --------- BASIC BLOCK bb2 ---------- */     { label 64 { lref 64 "Circle::bb2" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb2::0      *   br label %bb3 */     { jump { label 64 { lref 64 "Circle::bb3" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb3 ---------- */     { label 64 { lref 64 "Circle::bb3" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb3::0      *   %tmp4 = add nsw i32 %i.0, 1 */     { store { addr 64 { fref 64 "%tmp4" } { dec_unsigned 64 0 } } with      { add 32 { load 32 { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } } { dec_unsigned 32 1 } { dec_unsigned 1 0 } }     }     /* STATEMENT Circle::bb3::1      *   br label %bb1 */     { label 64 { lref 64 "Circle::bb3::1" } { dec_unsigned 64 0 } }     { store { addr 64 { fref 64 "%i.0" } { dec_unsigned 64 0 } } with { load 32 { addr 64 { fref 64 "%tmp4" } { dec_unsigned 64 0 } } } }     { label 64 { lref 64 "Circle::bb3::1:::1" } { dec_unsigned 64 0 } }     { jump { label 64 { lref 64 "Circle::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb5 ---------- */     { label 64 { lref 64 "Circle::bb5" } { dec_unsigned 64 0 } }     /* STATEMENT Circle::bb5::0      *   ret void */     { return }    }   }  }  /* Definition of function __original_main */  { func   { label 64 { lref 64 "__original_main" } { dec_unsigned 64 0 } }   { arg_decls    { alloc 64 "%_argc_ignored" 32 }    { alloc 64 "%_argv_ignored" 64 }   }   { scope    { decls }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "__original_main::bb" } { dec_unsigned 64 0 } }     /* STATEMENT __original_main::bb::0      *   call void @Circle() */     { call { label 64 { lref 64 "Circle" } { dec_unsigned 64 0 } } result }     /* STATEMENT __original_main::bb::1      *   ret i32 0 */     { label 64 { lref 64 "__original_main::bb::1" } { dec_unsigned 64 0 } }     { return { dec_unsigned 32 0 } }    }   }  }  /* Definition of function _taskFunc1_ */  { func   { label 64 { lref 64 "_taskFunc1_" } { dec_unsigned 64 0 } }   { arg_decls    { alloc 64 "%__arg" 64 }   }   { scope    { decls }    { inits }    { stmts     /* --------- BASIC BLOCK bb ---------- */     { label 64 { lref 64 "_taskFunc1_::bb" } { dec_unsigned 64 0 } }     /* STATEMENT _taskFunc1_::bb::0      *   call void @f(i32 0) */     { call { label 64 { lref 64 "f" } { dec_unsigned 64 0 } } { dec_unsigned 32 0 } result }     /* STATEMENT _taskFunc1_::bb::1      *   br label %bb1 */     { label 64 { lref 64 "_taskFunc1_::bb::1" } { dec_unsigned 64 0 } }     { jump { label 64 { lref 64 "_taskFunc1_::bb1" } { dec_unsigned 64 0 } } leaving 0 }     /* --------- BASIC BLOCK bb1 ---------- */     { label 64 { lref 64 "_taskFunc1_::bb1" } { dec_unsigned 64 0 } }     /* STATEMENT _taskFunc1_::bb1::0      *   ret i8* null */     { return { addr 64 { fref 64 "$null" } { dec_unsigned 64 0 } } }    }   }  } }}'
def getFunc(string):
    '''
    将alf文件中的Func逐个取出
    :param string: alf文件
    :return: 若干个func的集合
    '''

    func_sum = []
    #建立空列表
    num = 1;    #num为括号个数
    func_flag = 'func'    #被匹配的字符串
    start_place=string.find(func_flag)    #start_place为需要截取的第一个func的起始位置
    while string[start_place+4]!=' ':
        start_place=string.find(func_flag,start_place+4)
    while start_place!=-1:   #如果起始位置不为-1，则字符串内还有func
        i=start_place
        for i in range(start_place,len(string)+1):    #从本func的起始位置开始匹配“{}”个数
            if num!=0:    #如果num不为0，则一直往后匹配括号
                if string[i]=='{':
                    num+=1
                elif string[i]=='}':
                    num-=1             #对于num，有“{”加1，有“}”减1
            else:    #此时num为0，代表func内的全部内容到此为止
                num = 1;    #num归为1，供下次使用
                break    #跳出for循环

        end_place = i-1    #end_place为本func包含内容的最后一位的位置
        list_items = '{ '+string[start_place:end_place]+'}'    #将本次匹配的func提取为list_items
        func_sum.append(list_items)    #列表添加元素
        start_place=string.find(func_flag,end_place)    #start_place重新定位到下一个func的起始位置
        while start_place!=-1 and string[start_place+4]!=' ':
            start_place=string.find(func_flag,start_place+4)
    return func_sum


# for i in range(0,len(getFunc(stri))):
#     print(i)
# print(getFunc(stri))
