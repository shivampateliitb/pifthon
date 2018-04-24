from rwfm import *
import label_function

class DynamicLabelling:
    global _lblfunction
    
    def __init__(self):
        self._lblfunction = label_function.LabelFunction()
    
        
    def labelling(self, filename, highest_label):
        with open(filename) as file:
            lines=file.readlines()  
            for line in lines:
                print(line)
        
    def DL(self, line, highest_label):
        pass