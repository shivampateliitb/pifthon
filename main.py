import logging
import parse_input_file
import create_ast

from visitor import Visitor
from fileinput import filename
from dynamic_labelling import DynamicLabelling

def main():
    logging.basicConfig(filename='pifthon.log', level=logging.DEBUG)
    
    logging.info('Parsing input.json started')
    
    #Obtain the name of the source file
    #input_program contain the path to the source file
    input_program = parse_input_file.parseSourceFileName('inputs/input.json')
    logging.debug('program file name:'+ input_program)
    
    #Obtain security label of executing subject
    #clearance is the highest achievable security label by the executing subject
    clearance = parse_input_file.parseSubjectLabel('inputs/input.json')
    logging.debug('highest achievable label by the executing subject = '+ clearance.printLabel())
    
    #Obtain global variables and their respective security label
    #global_vars is a dictionary containing variable as key and mapped to it's security label
    global_vars = parse_input_file.parseGlobals('inputs/input.json')
    logging.debug('given labels of variables are \n'+ parse_input_file.printGlobals(global_vars))
    
    logging.info('Parsing input.json is completed')
    
    #A abstract syntax tree (AST) named tree is created and populated with the AST of the given program
    tree=create_ast.CreateAST(input_program)
    
    #Following statement prints the AST dump into console
    #create_ast.PrintAST(tree)
    
    #Following pair of commands parse the AST and write into a file called "test.temp" after nicely formatting
    #and extracting the nodes
    with open('test.temp','w') as file:
        v=Visitor(file)
        v.visit(tree)
    
    dynlabelling = DynamicLabelling()
    
    dynlabelling.labelling('test.temp', clearance)
    
 
    logging.info("Program completed")


    
if __name__ == '__main__':
    main()