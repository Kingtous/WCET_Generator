import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import re

#=========================
from PreprocessDot import preprocess
#=========================

#设置工作目录
root='/Users/kingtous/PycharmProjects/dot/src/Preprocessing/dot/thrFunc0/'
#=======DOT存放位置===============
dotPath=root+'_thrFunc0_CFG.dot'
#=======relation.txt存放位置======
relationPath=root+'_thrFunc0_relation.txt'
#=======需要处理的函数入口（暂时不用）======
parseFunction='_thrFunc0_'
#=======WCET目录====================
wctPath=root+'knapsack.wct'
#===========cluster_定义==========
Definition=''
#========输出================================
#=======dot输出==========
dotOutput=root+'thrFunc0_pro.dot'
#=======特征输出==========
Edges=0
Nodes=0
Call_TaskFunc=0
ConditionVertex=0
AverageConditionBranch=0
AverageWCET=0
WCET_Varies=0
Wait_Vertex=0
#========辅助计算数据
TotalConditionBranch=0
DEBUG=True
#===========WCET Config=========
Program_RUN=33
WCET_Total=0
#===============================


def NodeWait(graph):
    # 这里手动写...
    pass

def parseRelation(Path):
    '''
    :param Path: path to relation file
    :return: Dict [key:basic block] [value: Function to be called]
    '''
    relationDict={}
    file=open(Path,'r')
    while True:
        line=file.readline().strip()
        if line=='':
            break
        else:
            KeyValue=re.split('\s+',line.replace(':','_'))
            relationDict[KeyValue[0]]=KeyValue[1]
    return relationDict


def changeShapeOfCondition(graph):
    '''
    :param graph: CFG 图
    :return: None （处理后的带有判断的CFG图）
    '''
    for node in nx.nodes(graph):

        if 'CREATE' in graph.node[node]['label'] :
            # 顺带计算 Task Creation (Call_TaskFunc)
            global Call_TaskFunc
            Call_TaskFunc=Call_TaskFunc+1
            continue
        elif 'taskwait' in graph.node[node]['label']:
            global Wait_Vertex
            Wait_Vertex=Wait_Vertex+1
            continue
        count=0
        # 结点连接的结点
        neighbour=nx.neighbors(graph,node)
        for n in neighbour:
            #判断是否是task创建
            if 'CREATE' in n:
                continue
            else:
                count=count+1
        if count>1:
            graph.node[node]['shape']='diamond'
            global ConditionVertex
            ConditionVertex=ConditionVertex+1

def deleteTaskReturnNode(graph):
    '''
    :param graph: CFG图
    :return: None （处理后的，删去taskFunc return结点的图）
    '''
    NodeNeedTobeDelete=[]
    for node in nx.nodes(graph):
        if node.endswith('exit'):
            if (node.startswith('_taskFunc') or node.startswith('_thrFunc')):
                # return 结点
                allNB=nx.all_neighbors(graph,node)
                for returnNode in allNB:
                    #returnNode
                    nebrs=nx.all_neighbors(graph,returnNode)
                    for n in nebrs:
                        #判断是否是_exit，不是的话加一条边
                        if n!=node:
                            graph.add_edge(n,node)
                    NodeNeedTobeDelete.append(returnNode)
                    break
            else:
                # 加 return 标识
                allNB = nx.all_neighbors(graph, node)
                for returnNode in allNB:
                    if graph.has_edge(returnNode,node):
                        graph.node[returnNode]['label']=\
                            graph.node[returnNode]['label']+'\nRETURN\n'



    # 删除returnNode
    for node in NodeNeedTobeDelete:
        graph.remove_node(node)

        global Definition
        Definition=Definition.replace('"'+node+'"', '')



def AddWCETValue(graph):

    WCET_Varies_Dict={}

    global wctPath
    text=''
    file = open(wctPath, 'r')
    try:
        text=file.readlines()
        # Add Label
        for line in text:
            line=line.strip()
            if line!='':
                line=line.split(' ')

                statement=re.split(r'_+',line[1])
                if len(statement) ==3:
                    statement=statement[0]+'__'+statement[1]+'___'+statement[2]
                elif len(statement) ==2:
                    statement=statement[0]+'__'+statement[1]
                else:
                    statement=statement[0]
                name=line[0]+'__'+statement
                try:
                    value=line[2]
                    try:
                        wctLine=str(int(value)-Program_RUN)
                        WCET_Varies_Dict[wctLine]= WCET_Varies_Dict.get(wctLine,0)+1
                    except:
                        wctLine='ERROR'

                    if graph.node[name] != None:
                        # 加Nodes
                        global Nodes,WCET_Total
                        Nodes=Nodes+1
                        if wctLine!='ERROR':
                            WCET_Total=WCET_Total+int(wctLine)
                        graph.node[name]['label']=\
                        graph.node[name]['label']+'\n'+\
                            'WCET='+wctLine

                    global WCET_Varies,AverageWCET
                    WCET_Varies=len(WCET_Varies_Dict)
                    AverageWCET=WCET_Total/Nodes



                except:
                    continue

    except:
        print('WCET FILE ERROR')
    finally:
        file.close()


def parrallel(graph):
    '''
    :param graph: CFG图
    :return: None （处理后的，具有并行意义的图）
    '''
    #改并行
    for node in nx.nodes(graph):
        name= graph.node[node]['label']
        if 'CREATE' in name:
            for ne in nx.all_neighbors(graph,node):
                if ne.endswith('exit'):
                    # task 并行
                    # node(entry) -> ne(起点)
                    # tmp = taskFuncXX_exit
                    tmp=ne
                    nameToBeFind='CREATE '+ne.replace('_exit','')
                    for nodeName in nx.nodes(graph):
                        if(graph.node[nodeName]['label'].split('\n')[-1]==nameToBeFind):
                            ne=nodeName
                            break
                    taiList=[]

                    for mother in nx.neighbors(graph,ne):
                        taiList.append(mother)

                    edgeToBeAdd=[]
                    edgeToBeDelete=[]

                    for mother in nx.all_neighbors(graph,ne):
                        if mother not in taiList:
                            # graph.add_edge(mother,node)
                            edgeToBeAdd.append(mother)
                            # graph.remove_edge(tmp,node)
                            edgeToBeDelete.append(node)

                    for edge in edgeToBeAdd:
                        graph.add_edge(edge, node)
                    for edge in edgeToBeDelete:
                        graph.remove_edge(tmp,edge)

def deleteUndependNode(graph):
    NodetoBeDelete=[]
    nodeIter=nx.nodes(graph)
    for node in nodeIter:
        count=0
        iter=nx.all_neighbors(graph,node)
        for elem in iter:
            count=count+1
        if count==0:
            NodetoBeDelete.append(node)
    #删除结点
    for node in NodetoBeDelete:
        graph.remove_node(node)

        global Definition
        Definition=Definition.replace('"'+node+'"','')


def parse(parseFunction,graph,relationDict):
    '''
    :param parseFunction: 要处理的函数
    :param graph: networkx处理生成的图数据
    :param relationDict: 关系字典，basicblock:callFunction
    :return: graph 拼接的图文件
    '''
    #获取图中所有节点

    for callBlock in relationDict.keys():
        #查找图中的callBlock,连接callBlock以及函数entry,exit连接callBlock的下一条边
        if relationDict[callBlock].startswith('ort_'):
            # taskwait judgement
            if relationDict[callBlock]=='ort_taskwait':
                graph.node[callBlock]['style'] = 'filled'
                graph.node[callBlock]['color'] = 'green'
            graph.node[callBlock]['label']=callBlock+'\n('+callBlock.split('__bb')[0]+')'+relationDict[callBlock][4:]
            continue
            #callBlockNode = nx.get_node_attributes(graph, callBlock)
        elif relationDict[callBlock].startswith('_taskFunc'):
            # task creation
            graph.node[callBlock]['label'] = callBlock+'\n'+'CREATE ' + relationDict[callBlock]
            graph.node[callBlock]['style'] = 'filled'
            graph.node[callBlock]['color'] = 'aquamarine'
        else:
            graph.node[callBlock]['label'] = callBlock+'\n'+'CALL ' + relationDict[callBlock]

        Function_entry=relationDict[callBlock]+'_entry'
        Function_exit=relationDict[callBlock]+'_exit'
        nextNode=None

        for nod in nx.neighbors(graph,callBlock):
            nextNode=nod
        if not relationDict[callBlock].startswith('_taskFunc'):
            graph.add_edge(Function_exit,nextNode,color='red')
            # 删去不必要的边
            graph.remove_edge(callBlock, nextNode)
        graph.add_edge(callBlock, Function_entry,color='blue')

    # 处理 CFG
    deleteTaskReturnNode(graph)
    changeShapeOfCondition(graph)
    NodeWait(graph)
    parrallel(graph)
    deleteUndependNode(graph)
    AddWCETValue(graph)
    # 输出
    printFeatureOfGraph(graph)

def printFeatureOfGraph(graph):
    # 计算处理完后的结点,Nodes在生成WCET时数
    Edges = nx.number_of_edges(graph)
    # 输出--Terminal
    if DEBUG:
        print('========Debug Message Start=========')
        print('Vertex(|V|): ' + str(Nodes))
        print('Edges(|E|): ' + str(Edges))
        print('Call_TaskFunc(N_ce): ' + str(Call_TaskFunc))
        print('Wait Vertex(N_we): ' + str(Wait_Vertex))
        print('Condition Vertex(N_cd): ' + str(ConditionVertex))
        print('AverageConditionalBranch(N_br): ' + str(AverageConditionBranch))
        print('Average WCET(C): ' + str(AverageWCET))
        print('WCET_Varies(e): ' + str(WCET_Varies))
        print('-----------Extra Message------------')
        print('TotalConditionBranch:',TotalConditionBranch)
        print('========Debug Message End=========')
    # 输出--文件
    file=open(root+'FeatureOfPCFG.txt','w')
    try:
        file.write('Vertex(|V|): '+str(Nodes))
        file.write('\nEdges(|E|): '+str(Edges))
        file.write('\nCall_TaskFunc(N_ce): '+str(Call_TaskFunc))
        file.write('\nWait Vertex(N_we): '+str(Wait_Vertex))
        file.write('\nCondition Vertex(N_cd): '+str(ConditionVertex))
        file.write('\nAverageConditionalBranch(N_br): '+str(AverageConditionBranch))
        file.write('\nAverage WCET(C): '+str(AverageWCET))
        file.write('\nWCET_Varies(e): '+str(WCET_Varies))
        file.write('\nTotalConditionBranch:'+str(TotalConditionBranch))
    except:
        print('I/O Error.')
    finally:
        file.close()


def pdfPrint(Path):
    import os
    os.system('dot -Tpdf '+Path+' -o '+os.path.dirname(Path)+'/FinalOutput.pdf')


def calcBranch(graph):
    global TotalConditionBranch

    result=nx.weakly_connected_component_subgraphs(graph)
    for gh in result:
        # 对于每一个子图，先得到entry结点
        entryNode=''
        for node in gh.node:
            if node.endswith('_entry'):
                entryNode=node
                break
        numset = set()
        # 从起点一个一个尝试 simple path
        for node in gh.node:
            pathGen=nx.all_simple_paths(gh,entryNode,node)
            count=0
            for path in pathGen:
                count=count+1
            if count!=0:
                numset.add(count)
        print("Debug: "+entryNode.replace('_entry',' numset:'),max(numset))
        if max(numset)>1:
            # >1 表示有条件分支
            TotalConditionBranch=TotalConditionBranch+max(numset)

if __name__=='__main__':
    print("处理Relation表...")
    relation = parseRelation(relationPath)
    # 预处理
    print("预处理CFG...")
    preprocess(dotPath)
    # ================计算 AverageConditionBranch,先算出总分支数，之后除以N_we========
    print("计算总分支数...")
    ori_graph = nx.nx_pydot.read_dot(dotPath+'_pd')
    calcBranch(ori_graph)
    # 得到cluster定义
    print("获取图的Cluster__定义...")
    Definition=open(dotPath+'_dec').read()
    # 调用networkx处理CFG
    print("处理CFG图...")
    graph = nx.nx_pydot.read_dot(dotPath+'_pd')#'Preprocessing/knapsack_ompi_trim.Preprocessing')
    parse(parseFunction,graph,relation)
    write_dot(graph,dotOutput)
    #加入定义
    print("加入图的Cluster__定义...")
    fileContext=open(dotOutput,'r').readlines()
    FinalOutput=open(dotOutput+'_Final','w')
    for line in fileContext[:-1]:
        FinalOutput.write(line)
    print("生成最终Dot图...")
    FinalOutput.write(Definition)
    FinalOutput.close()
    print("生成最终PDF...")
    # 调用系统 graphviz生成最终的dot
    pdfPrint(dotOutput+'_Final')