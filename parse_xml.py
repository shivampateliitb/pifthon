from xml.etree import ElementTree as ET
from inputs.rwfm.label import Label

global _highest_label
global _package_path
global _program_name

def getHighestLabel(): 
    '''Method returns the highest security label achievable by the executing subject''' 
    #Insert code to read from the input.xml file 
    _subject_label = Label('A',['A','B'],['A'])
    return _subject_label

def getPackagePath():
    '''Method returns the path of the input package'''
    _package_path = 'inputs.rwfm'
    return _package_path

def getInputProgram():
    '''Method returns the name of the input program'''
    _program_name = "test.py"
    return _program_name
    
    
    '''
    tree = ET.parse('inputs/input.xml')
    root = tree.getroot()
    
    print(root[0][1].__getitem__(0))
    '''