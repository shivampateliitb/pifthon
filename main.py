import logging
from fileinput import filename
import parse_input_file
import create_ast
from visitor import Visitor
#from dynamic_labelling import DynamicLabelling

def main():
    logging.basicConfig(filename='pifthon.log', level=logging.DEBUG)
   
    logging.info('Parsing input.xml started')
    
    #Obtain the input program to test from input.xml
    input_program = parse_input_file.getSourceFileName('inputs/input.json')
    
    logging.debug('program file name:'+ input_program)
    
    #Obtain security label of executing subject
    
    #logging.debug('highest achievable label by the execution subject = '+ highest_label.printLabel())
    logging.info('Parsing input.json is completed')
    
    tree=create_ast.CreateAST(input_program)
    
    #Following statement prints the AST dump into console
    create_ast.PrintAST(tree)
    v=Visitor('test.temp')
    v.visit(tree)
    
    #dynlabelling = DynamicLabelling()
    
    #dynlabelling.labelling('test.temp', highest_label)
 
    logging.info("Program completed")


    
if __name__ == '__main__':
    main()