from rwfm.Label import Label

class LabelFunctions:
    _global=dict()
    
    def __init__(self):
        self._pc = Label('PC',['*'],[])
        self._local=dict()
        
        
    def updateLocal(self, id, label_object):
        self._local[id]=label_object
        
    def updateGlobal(self, id, label_object):
        LabelFunctions._global[id]=label_object
        
    def isLocal(self, id):
        if id in self._local.keys():
            return True
        else:
            return False
    
    def isGlobal(self, id):
        if id in LabelFunctions._global.keys():
            return True
        else:
            return False
        
    def findInLocal(self, id):
        if id in self._local.keys():
            return self._local[id]
        else:
            return None
        
    def findInGlobal(self, id):
        if id in LabelFunctions._global.keys():
            return self._global[id]
        else:
            return None
        
    def getPC(self):
        return self._pc
    
    def setPC(self, pc_label):
        self._pc = pc_label
        
    def isEqual(self, label_function):
        try:
            if self.getPC().isEqual(label_function.getPC()):
                for key in label_function._local.keys():
                    if self._local[key].isEqual(label_function._local[key]):
                        return True
                    else:
                        return False
            else:
                return False
        except Exception:
            return False
                
    
    def copy(self, label_function):
        label_function.setPC(self.getPC())
        for key in self._local.keys():
            label_function.updateLocal(key, self._local[key])
    
    def printGlobals(self):
        str=''
        for key in LabelFunctions._global.keys():
            str = str + key + ' : ' + LabelFunctions._global[key].printLabel() + '\n'
        return str
    