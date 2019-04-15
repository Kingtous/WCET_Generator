class infoModel:

    def __init__(self,name,pre,succ,isStart,isExit):
        self.name=name
        self.pre=pre
        self.succ=succ
        self.isStart=isStart
        self.isExit=isExit
        self.sign=set()
        self.type=None

    def insertSign(self,sign):
        self.sign.add(sign)

