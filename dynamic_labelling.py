from rwfm import Label
from rwfm import label_operations
from rwfm  import flow_operations
import label_function
import sys
import logging

class DynamicLabelling:
    
    def __init__(self):
        self._lblfunction = label_function.LabelFunctions()
        self._lines = list()
    
    def getFunction(self):
        return self._lblfunction
    
    # labelling function is responsible to call the main DL function    
    def labelling(self, filename, clearance):
        with open(filename,'r') as file:
            self._lines = file.read().splitlines()
            current_line=0
            while current_line < len(self._lines):
                if self.isNewStatement(current_line):
                    self._lblfunction, current_line = self.DL(current_line, clearance, self._lblfunction)
                else:
                    current_line = current_line+1
                    
                
    # check if current line encounters another statement
    def isNewStatement(self, current_line):
        if self._lines[current_line] == 'Assign' or self._lines[current_line] == 'While' or self._lines[current_line] == 'Compare':
            return True
        else:
            return False
        
    # Gather all the source objects for a statement and return the sources list along with the current line number
    def obtainSourceObjects(self, current_line):
        sources = []
        while (current_line < len(self._lines)) and (self.isNewStatement(current_line)==False) and self._lines[current_line]!= 'endloop':
            if self._lines[current_line].split(':')[0] == 'name':
                sources.append(self._lines[current_line].split(':')[1])
            current_line = current_line + 1
        return sources, current_line
    
    # read the global source variables of the statement
    def readGlobalSources(self, sources, clearance, label_function):
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
        return label_function
        
    # Print the message if there is any misuse of information
    def printMisuse(self, from_label, to_label):
        print('MISUSE: '+ from_label.printLabel() +' can not flow to '+ to_label.printLabel())
        sys.exit()
    
    def DL(self, current_line, clearance, lbl_function):
        # if current_line encounter an assignment statement
        if self._lines[current_line] == 'Assign':
            # increase the current line
            current_line = current_line + 1
            # obtain the target object
            target = self._lines[current_line].split(':')[1]
            # obtain the list of source objects in the assignment statement
            sources, current_line = self.obtainSourceObjects(current_line + 1)
            lbl_function = self.readGlobalSources(sources, clearance, lbl_function)
            # check if the target variable is a local variable
            if lbl_function.isLocal(target):
                # then obtain the label of the target variable
                target_label = lbl_function.findInLocal(target)
                # update the readers and writers set of target variable by pc label
                target_label.updateReaders(lbl_function.getPC().getReaders())
                target_label.updateWriters(lbl_function.getPC().getWriters())     
            # if target variable is a global variable then     
            elif lbl_function.isGlobal(target):
                # obtain the label of the target variable
                target_label = lbl_function.findInGlobal(target)
                # check if the pc label can flow to target label
                if flow_operations.canFlow(lbl_function.getPC(), target_label) == False:
                    # if cannot flow print the misuse message
                    self.printMisuse(lbl_function.getPC(), target_label)
            # if it is a new variable declared locally
            else:
                target_label = Label(clearance.getOwner(), lbl_function.getPC().getReaders(),lbl_function.getPC().getWriters()) 
                lbl_function.updateLocal(target, target_label) 
                  
            # return the new labelling function and current line
            return lbl_function, current_line
        
        # if current_line encounters an compare statement
        elif self._lines[current_line] == 'Compare':
            # increase the current line
            current_line = current_line + 1
            sources, current_line = self.obtainSourceObjects(current_line)
            lbl_function = self.readGlobalSources(sources, clearance, lbl_function)
            return lbl_function, current_line
        # if current_line encounters a while statement
        elif self._lines[current_line] == 'While':
            # Keep track of the starting line of While loop
            start_line = current_line
            # Create another labelling function to hold the old function mapping values
            old_lbl_function = label_function.LabelFunctions()
            lbl_function.copy(old_lbl_function)
            
            # increase the current line
            current_line = current_line + 1
            
            while self._lines[current_line]!= 'endloop':
                if self.isNewStatement(current_line):
                    lbl_function, current_line = self.DL(current_line, clearance, lbl_function)
                else:
                    current_line = current_line + 1
            
            if lbl_function.isEqual(old_lbl_function)==False:
                current_line = start_line
                lbl_function, current_line = self.DL(current_line, clearance, lbl_function)
            else:
                return lbl_function, current_line
        else:
            return lbl_function, current_line            
            
            