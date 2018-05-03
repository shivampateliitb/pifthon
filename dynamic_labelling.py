from rwfm import Label
from rwfm import label_operations
from rwfm  import flow_operations
import label_function
import sys

class DynamicLabelling:
    
    def __init__(self):
        self._lblfunction = label_function.LabelFunctions()
        
    def getFunction(self):
        return self._lblfunction
    
    # labelling function is responsible to call the main DL function    
    def labelling(self, filename, clearance):
        print(filename)
        with open(filename,'r') as file:
            lines = file.read().splitlines()
            start_line=0
            current_line=1
            while current_line != len(lines):
                self._lblfunction, current_line = self.DL(start_line, current_line, lines, clearance, self._lblfunction)
                
    
    # Gather all the source objects for a statement and return the sources list along with the current line number
    def obtainSourceObjects(self, current_line, lines):
        sources = []
        while (current_line < len(lines)) and (lines[current_line] != 'Assign' and lines[current_line] != 'If' and lines[current_line] != 'While' and lines[current_line] != 'Compare'):
            if lines[current_line].split(':')[0] == 'name':
                sources.append(lines[current_line].split(':')[1])
            current_line = current_line + 1
        return sources, current_line
    
    # Print the message if there is any misuse of information
    def printMisuse(self, from_label, to_label):
        print('MISUSE: '+ from_label.printLabel() +' can not flow to '+ to_label.printLabel())
        sys.exit()
    
    def DL(self, start_line, current_line, lines, clearance, label_function):
        # if the current_line reaches at the end of the file
        if current_line == len(lines):
            return label_function
        # if current_line encounter an assignment statement
        elif lines[current_line] == 'Assign':
            # initialize the start line of the statement with current line
            start_line = current_line
            # increase the current line
            current_line = current_line + 1
            # obtain the target object
            target = lines[current_line].split(':')[1]
            # obtain the list of source objects in the assignment statement
            sources, current_line = self.obtainSourceObjects(current_line + 1, lines)
            # for each source object in the list
            for i in range(0,len(sources)):
                # if the source object is a global variable
                if label_function.isGlobal(sources[i]):
                    # obtain the label of the global source variable
                    source_label = label_function.findInGlobal(sources[i])
                    # if the label of the global source variable is readable by the executing subject
                    if flow_operations.canFlow(source_label, clearance):
                        # obtain the new readers and writers set of new label after joining the source label and PC label
                        readers, writers = label_operations.join(source_label, label_function.getPC())
                        # update the PC label
                        label_function.getPC().updateReaders(readers)
                        label_function.getPC().updateWriters(writers)
                    # if the global variable is not readable by the subject
                    else:
                        print('MISUSE: illegal information flow while reading '+ sources[i])
                        self.printMisuse(source_label, clearance)
            # check if the target variable is a local variable
            if label_function.isLocal(target):
                # then obtain the label of the target variable
                target_label = label_function.findInLocal(target)
                # update the readers and writers set of target variable by pc label
                target_label.updateReaders(label_function.getPC().getReaders())
                target_label.updateWriters(label_function.getPC().getWriters())     
            # if target variable is a global variable then     
            elif label_function.isGlobal(target):
                # obtain the label of the target variable
                target_label = label_function.findInGlobal(target)
                # check if the pc label can flow to target label
                if flow_operations.canFlow(label_function.getPC(), target_label) == False:
                    # if cannot flow print the misuse message
                    self.printMisuse(label_function.getPC(), target_label)
            # if it is a new variable declared locally
            else:
                target_label = Label(clearance.getOwner(), label_function.getPC().getReaders(),label_function.getPC().getWriters()) 
                label_function.updateLocal(target, target_label)       
            # return the new labelling function and current line
        return label_function, current_line
                    
            
            