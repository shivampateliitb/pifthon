import logging
from fileinput import filename
import parse_xml
import create_ast
from visitor import Visitor
from dynamic_labelling import DynamicLabelling

def main():
    logging.basicConfig(filename='pifthon.log', level=logging.DEBUG)
   
    logging.info('Parsing input.xml started')
    
    #Get the package name from input.xml
    package = parse_xml.getPackagePath()
    
    #Get the highest achievable security label of executing subject
    highest_label = parse_xml.getHighestLabel()
    
    #Obtain the input program to test from input.xml
    input_program = 'inputs/'+parse_xml.getInputProgram()
    
    logging.debug('input program = '+input_program)
    logging.debug('package = '+package)
    logging.debug('highest achievable label by the execution subject = '+ highest_label.printLabel())
    logging.info('Parsing input.xml completed')
    
    tree=create_ast.CreateAST(input_program)
    
    #Uncomment the following line to print the AST dump into console
#     create_ast.PrintAST(tree)
    v=Visitor('ast.temp')
    v.visit(tree)
    DynamicLabelling('ast.temp',highest_label)
    
    logging.info("Program completed")


    
if __name__ == '__main__':
    main()