from rwfm import *
import label_function

class DynamicLabelling:
    
    def __init__(self):
        self._lblfunction = label_function.LabelFunctions()
    
        
    def labelling(self, filename, clearance):
        print(filename)
        with open(filename,'r') as file:
            for line in file.readlines():
                self._lblfunction = self.DL(line, clearance. self._lblfunction)
        
        
    def DL(self, line, clearance, label_function):
        if 'Assign\n' == line:
            
            