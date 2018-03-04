from inputs.rwfm import *
import label_function

class DynamicLabelling:
    global _lblfunction
    
    def __init__(self, filename, highest_label):
        self._lblfunction = label_function.LabelFunction()
        
    def DL(self, line, highest_label):
#         while line:
#             print(line)
#             line=self._file_object.readline()
#             #DL(line, highest_label)
#         self._file_object.close()
        pass