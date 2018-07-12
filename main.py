import sys
import logging
import datetime
import parse_input_file
import abstract_syntax_tree

import dynamic_labelling

def main():
    # create a log file name with timestamp
    log_file = 'log/pifthon' + str(datetime.datetime.now()).split(' ')[1] + '.log'
    #logging.getLogger().addHandler(logging.StreamHandler())
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    
    logging.info("\n\n*********** Monitor started **********\n\n")
    logging.info('Parsing %s started' % sys.argv[1])
    
    #Obtain the name of the source file
    #input_program contain the path to the source file
    try:
        if len(sys.argv) == 2:
            json_file = str(sys.argv[1])
            input_program = parse_input_file.parse_source_filename(json_file)
            print(input_program)
            logging.info('program file name:'+ input_program)
    
            #Obtain security label of executing subject
            #clearance is the highest achievable security label by the executing subject
            clearance = parse_input_file.parse_subject_label(json_file)
            logging.info('highest achievable label by the executing subject = %s',  clearance.to_string())
    
            #Obtain global variables and their respective security label
            #global_vars is a dictionary containing variable as key and mapped to it's security label
            global_vars = parse_input_file.parse_globals(json_file)
            
            # Obtain subject label given for each function
            func_labels = parse_input_file.parse_function_labels(json_file)

            #the file in which the output is to be printed
            output_file = parse_input_file.parse_output_file(json_file)
        
    except ValueError as e:
        print('ERROR: invalid json: %s' %e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()
        
    logging.info('Parsing %s is completed' % json_file)
    
    #A abstract syntax tree (AST) named tree is created and populated with the AST of the given program
    tree=abstract_syntax_tree.create_ast(input_program)
    
    ast_file = input_program + '.ast'
    abstract_syntax_tree.write_ast_into_file(tree, ast_file)
    logging.info('AST written into file: %s' % ast_file)
    
    lbl_function = dynamic_labelling.create_labelling_function()
    
    # initialize the functions dictionary of the labelling function
    if func_labels:
        for key in func_labels.keys():
            lbl_function.insert_into_function_list(key, func_labels[key])
    # print(lbl_function.print_function_labels())
    logging.info('%s', lbl_function.print_function_labels())
    
    # initialize the global dictionary of the labelling function
    if global_vars:
        for key in global_vars.keys():
            lbl_function.insert_into_global_list(key, global_vars[key])
    # print(lbl_function.print_global_labels())
    logging.info('%s', lbl_function.print_global_labels())

    #initialize the output_file dictionary
    if output_file:
        for key in output_file.keys():
            lbl_function.insert_into_output_file_list(key, output_file[key])

    logging.info('%s', lbl_function.print_output_file_list())
    
    logging.info('Starting dynamic labelling')
    # Call the labelling function of DynamicLabelling class    
    lbl_function = dynamic_labelling.perform_labelling(ast_file, clearance, lbl_function)
    logging.info('Dynamic labelling completed')
    
    # print('Derived labels of local variables from main file:')
    # print(lbl_function.print_local_labels())
    logging.info("Derived labels of local variables from main file:")
    logging.info('%s' %lbl_function.print_local_labels())
    
    print('Program is information flow secure')
    logging.info("Program is information flow secure")
    logging.info("\n\n*********** Monitor stopped **********\n\n")


    
if __name__ == '__main__':
    main()