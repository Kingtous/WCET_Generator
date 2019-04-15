class infoModel:

    def __init__(self, name, pre, succ, isStart, isExit):
        self.name = name
        self.pre = pre
        self.succ = succ
        self.isStart = isStart
        self.isExit = isExit
        self.sign = set()
        self.type = None

    def insertSign(self, sign):
        self.sign.add(sign)


class startPointModel:

    def __init__(self, graph, start, end,type):
        self.v = set()
        self.type=type
        self.includes = set()
        self.start = start
        self.end = end
        self.startValue = None
        self.endValue = None
        self.getFunctionNameAndValue()
        self.findV(graph)

    def getFunctionNameAndValue(self):
        import re as r
        if self.start != None:
            result = r.split('[_]{2,}', self.start)
            self.function = result[0]
            self.startValue=getValue(self.start)
        if self.end != None:
            self.endValue=getValue(self.end)

    def findV(self, graph):
        for node in graph:
            if getFunctionName(node)!= self.function:
                continue
            value=getValue(node)
            if value>self.startValue and value<self.endValue:
                self.v.add(node)


    def isInclude(self, model):
        if self.v.issubset(model.v):
            return True
        return False

    def include(self, oriModel, model):
        if oriModel.v.isdisjoint(model.v):
            # 那就在其中的include列表中
            for ori in oriModel.includes:
                oriModel.include(ori, model)
        else:
            oriModel.v = oriModel.v - model.v
        #考虑结束结点相同的情况
        oriModel.includes.add(model.start)
        oriModel.v.add(oriModel.end)

def getBB(nodeName):
    import re as r
    if nodeName != None:
        if nodeName.endswith('_entry'):
            return None
        if nodeName.endswith('_exit'):
            return None
        result = r.split('__bb', nodeName)

        if len(result) == 2:
            if result[1].startswith('__'):
                return result[1].split('__')[1]
            elif result[1] == '':
                return 0
            else:
                return result[1].split('__')[0]

def getValue(nodeName):
    import re as r
    if nodeName != None:
        if nodeName.endswith('_entry'):
            return -1
        if nodeName.endswith('_exit'):
            return 9999
        result = r.split('__bb', nodeName)

        if len(result) == 2:
            if result[1].startswith('__'):
                return float('0.'+result[1].split('__')[1])
            elif result[1]=='':
                return 0
            else:
                return float(result[1].replace('__','.'))


def getFunctionName(name):
    import re as r
    result = r.split('__bb', name)
    return result[0]