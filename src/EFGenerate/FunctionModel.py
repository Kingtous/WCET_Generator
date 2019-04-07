import queue


class functionModel:

    def __init__(self, name, pathModel,nodesList):
        self.name = name
        self.pathModel = pathModel
        self.nodesList=nodesList

class pathModel:

    def __init__(self):
        self.pathList = []
        self.subgraphList = []
        self.createList = []
        self.callList = []
        self.pathSelectedNow = None
        self.pathNoneSelected = queue.Queue()
        pass

    def addPathModel(self, path, subgraph, relation):
        self.pathList.append(path)
        self.pathNoneSelected.put(path)
        self.subgraphList.append(subgraph)
        tmpCreateList = []
        tmpCallCreateList = []
        for node in subgraph.nodes:
            if (relation.get(node, -1) != -1):
                if ('CREATE' in subgraph.node[node]['label']):
                    tmpCreateList.append(relation[node])
                else:
                    tmpCallCreateList.append(relation[node])
        self.createList.append(tmpCreateList)
        self.callList.append(tmpCallCreateList)

    def clear(self):
        self.pathList.clear()
        self.subgraphList.clear()
        self.createList.clear()
        self.callList.clear()
        while not self.pathNoneSelected.empty():
             self.pathNoneSelected.get()
        self.pathSelectedNow = None
