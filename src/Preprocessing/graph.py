import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import re

#=========================
from src.Preprocessing.PreprocessDot import preprocess
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
wctPath=root+''
#========输出================================
#=======dot输出==========
dotOutput=root+'thrFunc0_pro.dot'
#=======特征输出==========
Edges=0
Nodes=0
Call_TaskFunc=0
ConditionBranch=0
AverageWCET=0
WCET_Varies=0
#===========WCET Config=========
Program_RUN=33
WCET_Total=0
#===============================

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
        count=0
        # 结点连接的结点
        neighbour=nx.neighbors(graph,node)
        for n in neighbour:
            #判断是否是task创建
            if n.startswith('CREATE'):
                continue
            else:
                count=count+1
        if count>1:
            graph.node[node]['shape']='diamond'

def deleteTaskReturnNode(graph):
    '''
    :param graph: CFG图
    :return: None （处理后的，删去taskFunc return结点的图）
    '''
    NodeNeedTobeDelete=[]
    for node in nx.nodes(graph):
        if node.endswith('exit') and (node.startswith('_taskFunc') or node.startswith('_thrFunc')):
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
    # 删除returnNode
    for node in NodeNeedTobeDelete:
        graph.remove_node(node)

def NodeWait(graph):
    # 这里先手动写吧
    graph.add_edge('_taskFunc0__exit','knapsack_par__bb45__2')
    # # 从串行角度看
    # for node in nx.nodes(graph):
    #     if graph.node[node]['label'].endswith('taskwait'):
    #         # 遇到taskwait结点
    #
    #         pass
    pass


def parrallel(graph):
    '''
    :param graph: CFG图
    :return: None （处理后的，具有并行意义的图）
    '''
    #改并行
    for node in nx.nodes(graph):
        if graph.node[node]['label'].startswith('CREATE'):
            for ne in nx.all_neighbors(graph,node):
                if ne.endswith('exit'):
                    # task 并行
                    # node(entry) -> ne(起点)
                    # tmp = taskFuncXX_exit
                    tmp=ne
                    nameToBeFind='CREATE '+ne.replace('_exit','')
                    for nodeName in nx.nodes(graph):
                        if(graph.node[nodeName]['label']==nameToBeFind):
                            ne=nodeName
                            break
                    taiList=[]

                    for mother in nx.neighbors(graph,ne):
                        taiList.append(mother)

                    for mother in nx.all_neighbors(graph,ne):
                        if mother not in taiList:
                            graph.add_edge(mother,node)
                            graph.remove_edge(tmp,node)



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
            graph.node[callBlock]['label']='('+callBlock.split('__bb')[0]+')'+relationDict[callBlock][4:]
            continue
            #callBlockNode = nx.get_node_attributes(graph, callBlock)
        elif relationDict[callBlock].startswith('_taskFunc'):
            # task creation
            graph.node[callBlock]['label'] = 'CREATE ' + relationDict[callBlock]
            graph.node[callBlock]['style'] = 'filled'
            graph.node[callBlock]['color'] = 'aquamarine'
        else:
            graph.node[callBlock]['label'] = 'CALL ' + relationDict[callBlock]

        Function_entry=relationDict[callBlock]+'_entry'
        Function_exit=relationDict[callBlock]+'_exit'
        nextNode=None

        for nod in nx.neighbors(graph,callBlock):
            nextNode=nod
        graph.add_edge(Function_exit,nextNode)
        graph.add_edge(callBlock, Function_entry)
        # 删去不必要的边
        graph.remove_edge(callBlock,nextNode)
    # 处理CFG
    deleteTaskReturnNode(graph)
    changeShapeOfCondition(graph)
    NodeWait(graph)
    parrallel(graph)
    # 输出
    printFeatureOfGraph(graph)

def printFeatureOfGraph(graph):
    # 计算处理完后的结点
    Edges = nx.number_of_edges(graph)
    Nodes = nx.number_of_nodes(graph)
    # 输出
    print('Vertex:', Nodes)
    print('Edges:', Edges)
    print('Call_TaskFunc:', Call_TaskFunc)
    print('Average WCET:', AverageWCET)
    print('WCET_Varies:', WCET_Varies)




if __name__=='__main__':
    relation = parseRelation(relationPath)
    preprocess(dotPath)
    graph = nx.nx_pydot.read_dot(dotPath+'tmp')#'Preprocessing/knapsack_ompi_trim.Preprocessing')
    parse(parseFunction,graph,relation)
    write_dot(graph,dotOutput)
















