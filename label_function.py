from inputs.rwfm import label

class LabelFunction:
    global _local
    global _global
    global _pc
    
    def __init__(self):
        self._pc = label.Label('PC',['*'],[])
        
    def updateLocal(self, id, label_object):
        self._local[id]=label_object
        
    def updateGlobal(self, id, label_object):
        self._global[id]=label_object
        
    def isLocal(self, id):
        if self._local.has_key(id):
            return True
        else:
            return False
    
    def isGlobal(self, id):
        if self._global.has_key(id):
            return True
        else:
            return False
        
    def findInLocal(self, id):
        if self._local.has_key(id):
            return self._local[id]
        else:
            return None
        
    def findInGlobal(self, id):
        if self._global.has_key(id):
            return self._global[id]
        else:
            return None