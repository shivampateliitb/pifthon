from rwfm import Label
from rwfm import label_operations
from rwfm import flow_operations
import label_function
import sys
import logging
import inspect
import traceback

statements = ['Assign', 'Compare', 'While']
keywords = ['endloop']
iteration = 1

def is_a_statement(word):
    if word in statements:
        return True
    else:
        return False


def is_an_assignment(word):
    if word == 'Assign':
        return True
    else:
        return False


def is_a_comparison(word):
    if word == 'Compare':
        return True
    else:
        return False


def is_an_iteration(word):
    if word == 'While':
        return True
    else:
        return False


def is_a_keyword(word):
    if word in keywords:
        return True
    else:
        return False


def is_an_endloop(word):
    if word == 'endloop':
        return True
    else:
        return False


def create_labelling_function():
    lbl_function = label_function.LabelFunctions()
    return lbl_function


def is_end_of_file(current_line):
    if current_line >= len(lines):
        return True
    else:
        return False


def is_a_variable(current_line):
    if lines[current_line].split(':')[0] == 'name':
        return True
    else:
        return False


def get_the_variable(current_line):
    print(current_line)
    return lines[current_line].split(':')[1]


def next_line(current_line):
    return (current_line + 1)


def obtain_source_variables(current_line):
    sources = list()
    while (not is_end_of_file(current_line)) and \
            (not is_a_statement(lines[current_line])) and \
            (not is_a_keyword(lines[current_line])):
        if is_a_variable(current_line):
            sources.append(get_the_variable(current_line))
        current_line = next_line(current_line)
    return sources, current_line


def read_global_labels(sources, clearance, lbl_function):
    for i in range(0, len(sources)):
        if lbl_function.is_global(sources[i]):
            source_label = lbl_function.label_from_global_list(sources[i])
            if flow_operations.can_flow(source_label, clearance):
                readers, writers = label_operations.join(source_label, 
                                                         lbl_function.get_pc_label())
                lbl_function.get_pc_label().update_readers(readers)
                lbl_function.get_pc_label().update_writers(writers)
            else:
                error_type = 0
                print_misuse_message(error_type, 
                                     source[i], 
                                     None,
                                     source_label,
                                     clearance)
    return lbl_function     


def print_misuse_message(error_type,
                         source_variable,
                         target_variable,
                         source_label,
                         target_label):
    try:
        if error_type == 0:
            message_1 = ('MISUSE: Label of the source variable ' + 
                         source_variable + ' is higher than that of'
                         'executing subject')
        elif error_type == 1:
            message_1 = ('MISUSE: Illegal information flow from PC to '
                         + target_variable)
        else:
            pass
    except Exception as e:
        print('Function ' + inspect.stack()[0][3] + 'raised an exception')
        print(str(e))
        
    message_2 = source_label.to_string() + ' cannot flow to ' + target_label.to_string()  
    print(message_1 + '\n' + message_2)
    print('iteration performed: ' + str(iteration))
    sys.exit()


def perform_labelling(filename, clearance, lbl_function):
    with open(filename, 'r') as file:
        global lines
        lines = file.read().splitlines()
        current_line = 0
        while not is_end_of_file(current_line):
            if is_a_statement(lines[current_line]):
                lbl_function, current_line = DL(current_line,
                                                clearance,
                                                lbl_function)
            else:
                current_line = next_line(current_line)
        return lbl_function
                    

def DL(current_line, clearance, lbl_function):
    if is_an_assignment(lines[current_line]):
        current_line = next_line(current_line)
        target = get_the_variable(current_line)
        current_line = next_line(current_line)
        sources, current_line = obtain_source_variables(current_line)
        lbl_function = read_global_labels(sources, clearance, lbl_function)
        pc_label = lbl_function.get_pc_label()
        try:
            if lbl_function.is_local(target):
                target_label = lbl_function.label_from_local_list(target)
                target_label.update_readers(pc_label.get_readers())
                target_label.update_writers(pc_label.get_writers())
            elif lbl_function.is_global(target):
                target_label = lbl_function.label_from_global_list(target)
                if not flow_operations.can_flow(pc_label, target_label):
                    error_type = 1
                    print_misuse_message(error_type, 
                                         None, 
                                         target, 
                                         pc_label, 
                                         target_label)
            else:
                target_label = Label(clearance.get_owner(),
                                     pc_label.get_readers(),
                                     pc_label.get_writers())
                lbl_function.update_local_label_list(target, target_label)
        except Exception as e:
            print('Function ' + inspect.stack()[0][3] + 
                  ': fails to access ' + target +
                  ' in Assignment statement')
            print(str(e))
            
        return lbl_function, current_line
    
    elif is_a_comparison(lines[current_line]):
        try:
            current_line = next_line(current_line)
            sources, current_line = obtain_source_variables(current_line)
            lbl_function = read_global_labels(sources, clearance, lbl_function)
        except Exception as e:
            print('Function ' + inspect.stack()[0][3] + 
                  ': fails in Comparison statement')
            print(str(e))
            
        return lbl_function, current_line
    
    elif is_an_iteration(lines[current_line]):
        try:
            start_line = current_line
            start_lbl_function = create_labelling_function()
            lbl_function.copy_into(start_lbl_function)
            current_line = next_line(current_line)
            while not is_an_endloop(lines[current_line]):
                if is_a_statement(lines[current_line]):
                    lbl_function, current_line = DL(current_line,
                                                    clearance, 
                                                    lbl_function)
                else:
                    current_line = next_line(current_line)
            if not lbl_function.is_equal_to(start_lbl_function):
                current_line = start_line
                global iteration
                iteration = iteration + 1
                return DL(current_line, clearance, lbl_function)
            else:
                current_line = next_line(current_line)
                return lbl_function, current_line
        except Exception as e:
            print('Function ' + inspect.stack()[0][3] + 
                  ': fails in Iteration statement')
            print(str(e))
    
    else:
        return lbl_function, current_line 
            