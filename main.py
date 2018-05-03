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
    
    create_ast.writeAST(tree, 'test.temp')
    
    # create an object of DynamicLabelling class
    dynlabelling = DynamicLabelling()
    
    # obtain the labelling function from the created object
    lbl_function = dynlabelling.getFunction()
    
    # initialize the global dictionary of the labelling function
    for key in global_vars.keys():
        lbl_function.updateGlobal(key, global_vars[key])
    
    
    # Call the labelling function of DynamicLabelling class    
    dynlabelling.labelling('test.temp', clearance)
    
    
    print('Program is information flow secure')
    logging.info("Program completed")


    
if __name__ == '__main__':
    main()