import logging
import parse_input_file
import abstract_syntax_tree

import dynamic_labelling

def main():
    logging.basicConfig(filename='pifthon.log', level=logging.DEBUG)
    
    logging.info('Parsing input.json started')
    
    #Obtain the name of the source file
    #input_program contain the path to the source file
    input_program = parse_input_file.parse_source_filename('inputs/input.json')
    logging.debug('program file name:'+ input_program)
    
    #Obtain security label of executing subject
    #clearance is the highest achievable security label by the executing subject
    clearance = parse_input_file.parse_subject_label('inputs/input.json')
    logging.debug('highest achievable label by the executing subject = '+ clearance.to_string())
    
    #Obtain global variables and their respective security label
    #global_vars is a dictionary containing variable as key and mapped to it's security label
    global_vars = parse_input_file.parse_globals('inputs/input.json')
    logging.debug('given labels of variables are \n'+ parse_input_file.print_globals(global_vars))
    
    
    logging.info('Parsing input.json is completed')
    
    #A abstract syntax tree (AST) named tree is created and populated with the AST of the given program
    tree=abstract_syntax_tree.create_ast(input_program)
    
    abstract_syntax_tree.write_ast_into_file(tree, 'test.temp')
    
    lbl_function = dynamic_labelling.create_labelling_function()
    
    # initialize the global dictionary of the labelling function
    for key in global_vars.keys():
        lbl_function.insert_into_global_list(key, global_vars[key])
    
    
    # Call the labelling function of DynamicLabelling class    
    dynamic_labelling.perform_labelling('test.temp', clearance, lbl_function)
    
    
    print('Program is information flow secure')
    logging.info("Program completed")


    
if __name__ == '__main__':
    main()