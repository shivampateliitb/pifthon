from rwfm import Label
from rwfm import label_operations
from rwfm import flow_operations
import label_function
import sys
import logging
import inspect
import traceback
from symbol import argument

statements = ['Assign', 'Compare', 'While', 'Call', 'Return']
keywords = ['endloop', 'Tuple', 'Return', 'endtuple', 'downgrade', 'print', 'FunctionDef', 'endfunc']
functions = dict()
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


def is_a_function_call(word):
    if word == "Call":
        return True
    else:
        return False


def is_defined(name):
    if name in functions.keys():
        return True
    else:
        return False


def is_end_of_function(word):
    if word == 'endfunc':
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

def is_a_tuple(word):
    if word == 'Tuple':
        return True
    else:
        return False


def is_a_return(word):
    if word == 'Return':
        return True
    else:
        return False


def is_an_endtuple(word):
    if word == 'endtuple':
        return True
    else:
        return False


def is_a_downgrade(word):
    if word == 'downgrade':
        return True
    else:
        return False


def is_a_function_def(word):
    if word == 'FunctionDef':
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


def is_a_function(current_line):
    if lines[current_line].split(':')[0] == 'func':
        return True
    else:
        return False


def is_an_argument(current_line):
    if lines[current_line].split(':')[0] == 'arg':
        return True
    else:
        return False


def get_the_id(current_line):
    return lines[current_line].split(':')[1]


def next_line(current_line):
    return (current_line + 1)


def obtain_target_variables(current_line):
    targets = list()
    if is_a_variable(current_line):    
        targets.append(get_the_id(current_line))
    # if current line is defining a tuple of multiple target variables then
    # populate the targets list
    if is_a_tuple(lines[current_line]):
        # go to the next line where it starts to defining variables
        current_line = next_line(current_line)
        # if the line is defining a returned variable inside Tuple and
        # endtuple then collect them. Iterate the while loop until
        # it stop finding any new variable
        while is_a_variable(current_line) \
            and not is_an_endtuple(lines[current_line]):
            # populate the variables list
            targets.append(get_the_id(current_line))
            # go to the next line
            current_line = next_line(current_line)
    return targets, current_line


def obtain_source_variables(current_line):
    sources = list()
    while (not is_end_of_file(current_line)) and \
            (not is_a_statement(lines[current_line])) and \
            (not is_a_keyword(lines[current_line])):
        if is_a_variable(current_line):
            sources.append(get_the_id(current_line))
        current_line = next_line(current_line)
    return sources, current_line


def obtain_arguments(current_line):
    arguments = list()
    while (not is_end_of_file(current_line)) and \
            (not is_a_statement(lines[current_line])) and \
            (not is_a_keyword(lines[current_line])):
        if is_an_argument(current_line):
            arguments.append(get_the_id(current_line))
        current_line = next_line(current_line)
    return arguments, current_line


def read_source_labels(sources, clearance, lbl_function):
    for i in range(0, len(sources)):
        if lbl_function.is_local(sources[i]):
            source_label = lbl_function.label_from_local_list(sources[i])
        elif lbl_function.is_global(sources[i]):
            source_label = lbl_function.label_from_global_list(sources[i])
        else:
            source_label = Label(clearance.get_owner(), ['*'], [])

        if flow_operations.can_flow(source_label, clearance):
            readers, writers = label_operations.join(source_label, 
                                                     lbl_function.get_pc_label())
            lbl_function.get_pc_label().update_readers(readers)
            lbl_function.get_pc_label().update_writers(writers)
        else:
            error_type = 0
            print_misuse_message(error_type, 
                                sources[i], 
                                None,
                                source_label,
                                clearance)
    return lbl_function     


''' Check if the information can flow from arguments to executing subject i.e.
executing subject should be able to read the function arguments otherwise
throw misuse message'''
def read_arguments(subject_label, arguments, lbl_function):
    for i in range(0, len(arguments)):
        if lbl_function.is_local(arguments[i]):
            argument_label = lbl_function.label_from_local_list(arguments[i])
        if lbl_function.is_global(arguments[i]):
            argument_label = lbl_function.label_from_global_list(arguments[i])
        # if the argument has neither a local nor a globally defined label
        # then it is a constant literal e.g., integer, float or string 
        if 'argument_label' in locals():    
            if not flow_operations.can_flow(argument_label, subject_label):
                error_type = 0
                print_misuse_message(error_type,
                                     arguments[i],
                                     None,
                                     argument_label,
                                     subject_label)

    
''' Print a message for a possible information flow violation'''
def print_misuse_message(error_type,
                         source_variable,
                         target_variable,
                         source_label,
                         target_label):
    try:
        if error_type == 0:
            message_1 = ('MISUSE: Label of the source variable ' + 
                         source_variable + ' is higher than that of '
                         'executing subject')
        elif error_type == 1:
            message_1 = ('MISUSE: Illegal information flow from PC to '
                         + target_variable)
        elif error_type == 2:
            message_1 = ('MISUSE: Downgrading of ' + source_variable + 
                         ' might cause illegal information flow')
        else:
            pass
    except Exception as e:
        print('Function ' + inspect.stack()[0][3] + 'raised an exception')
        print(str(e))
        
    message_2 = source_label.to_string() + ' cannot flow to ' + target_label.to_string()  
    print(message_1 + '\n' + message_2)
    print('iteration performed: ' + str(iteration))
    sys.exit()


def perform_downgrading(current_line, clearance, lbl_function):
    try:
        # at this point current line is calling the downgrading, hence 
        # move to next line to fetch its arguments
        current_line = next_line(current_line)
        # in the next three iteration get the owner, object label and
        # list of principals to be added in the downgraded label
        for i in range(3):
            if i == 0:
                owner = lines[current_line].split(':')[1]
            elif i == 1:
                object = lines[current_line].split(':')[1]
                if lbl_function.is_local(object):
                    object_label = lbl_function.label_from_local_list(object)
                else:
                    object_label = lbl_function.label_from_global_list(object)
            else:
                new_readers = lines[current_line].split(':')[1].split(',')
            current_line = next_line(current_line)
        # make target label same as object label only with added readers
        target_label = Label(object_label.get_owner(),
                             object_label.get_readers(),
                             object_label.get_writers())
        target_label.insert_into_readers(new_readers)
        # now call downgrade operation
        new_label = flow_operations.downgrade(clearance, 
                                              owner, 
                                              object,
                                              object_label, 
                                              new_readers) 
        # downgrading is successfull if returned label is equal with target label
        if not new_label == None and new_label.is_equal_to(target_label):
            return new_label, current_line
        else:
            error_type = 2
            print_misuse_message(error_type, 
                                 object, 
                                 None, 
                                 object_label, 
                                 target_label)
            
    except Exception as e:
        print('Function ' + inspect.stack()[0][3] + 
              ': fails during downgrading')
        print(e)


def perform_labelling(filename, clearance, lbl_function):
    with open(filename, 'r') as file:
        global lines
        lines = file.read().splitlines()
        current_line = 0
        while not is_end_of_file(current_line):
            if is_a_function_def(lines[current_line]):
                current_line = next_line(current_line)
                global functions
                functions[get_the_id(current_line)] = current_line
                # skip everything until the end of function is reached
                while not is_end_of_function(lines[current_line]):
                    current_line = next_line(current_line)
            if is_a_statement(lines[current_line]):
                lbl_function, current_line = DL(current_line,
                                                clearance,
                                                lbl_function)
            else:
                current_line = next_line(current_line)
        return lbl_function
                    

def DL(current_line, clearance, lbl_function):
    # first check if it has already gone beyond the total length of the lines
    if is_end_of_file(current_line):
        return lbl_function, current_line 
    # if the current line is an assignment statement
    elif is_an_assignment(lines[current_line]):
        # go to the next line
        current_line = next_line(current_line)
        # fetch the target variable from the current line
        targets, current_line = obtain_target_variables(current_line)
        # go to the next line
        current_line = next_line(current_line)
        if is_a_variable(current_line):
            # obtain source variables of an assignment statement
            sources, current_line = obtain_source_variables(current_line)
            # read the source variables' labels
            lbl_function = read_source_labels(sources, clearance, lbl_function)
        elif is_a_function_call(lines[current_line]):
            lbl_function, current_line = DL(current_line,
                                            clearance,
                                            lbl_function)
            for label in lbl_function.get_downgrade_list():
                readers, writers = label_operations.join(lbl_function.remove_from_downgrade_list(), 
                                                     lbl_function.get_pc_label())
                lbl_function.get_pc_label().update_readers(readers)
                lbl_function.get_pc_label().update_writers(writers)
        # obtain the pc label
        pc_label = lbl_function.get_pc_label()
        try:
            for target in targets:
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
            lbl_function = read_source_labels(sources, clearance, lbl_function)
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
            print('current line:' + str(current_line))
            print('Function ' + inspect.stack()[0][3] + 
                  ': fails in Iteration statement')
            print(str(e))

    elif is_a_function_call(lines[current_line]):
        try:
            # the current line is at Call statement, hence go to the next line
            current_line = next_line(current_line)
            # get the function name
            function_name = get_the_id(current_line)
            # check if the function is defined before calling
            if is_defined(function_name):
                # if the function is executed with different subject label 
                # given as input then obtain the subject label
                if lbl_function.find_in_functions_list(function_name):
                    subject_label = lbl_function.label_from_functions_list(function_name)
                # otherwise function is executed with the label of main 
                # executing subject
                else:
                    subject_label = clearance
                # current label is at the function name, go to the next line
                current_line = next_line(current_line)
                # obtain the list of arguments, this list will be
                # used during executing function to match the order of the
                # arguments
                arguments, current_line = obtain_arguments(current_line)
                # if the list argument has elements then check if 
                # information can flow from them to executing subject
                if len(arguments) > 0:
                    read_arguments(subject_label, arguments, lbl_function)
                # create a new labelling function copying the labels of 
                # global variables from the current labelling function
                new_lbl_function = create_labelling_function()
                # save the current line number to resume execution after 
                # the called function is executed
                saved_current_line = current_line
                # set the current label with the line number where the function
                # is defined
                current_line = functions[function_name]
                parameters, current_line = obtain_arguments(current_line)
                # if length of both the parameters and arguments lists matches
                # then copy label of arguments into local list of new labelling
                # function
                if len(arguments) == len(parameters):
                    for i in range(len(arguments)):
                        if lbl_function.is_local(arguments[i]):
                            parameter_label = lbl_function.label_from_local_list(arguments[i])     
                        elif lbl_function.is_global(arguments[i]):
                            parameter_label = lbl_function.label_from_global_list(arguments[i])
                        else:
                            parameter_label = Label(subject_label.get_owner(),
                                                    ['*'], [])
                        new_lbl_function.update_local_label_list(parameters[i], 
                                                                 parameter_label)
                else:
                    print('Function '+ function_name + ' : ' +
                            'parameters do not match with arguments')
                    sys.exit()
                # now execute each statement within the function until it
                # reaches the endfunc keyword
                while not is_end_of_function(lines[current_line]):
                    # if current line encounters a new statement
                    if is_a_statement(lines[current_line]):
                        new_lbl_function, current_line = DL(current_line,
                                                        subject_label,
                                                        new_lbl_function)
                    else:
                        current_line = next_line(current_line)
                # copy the downgrade list from new labelling function to old 
                # labelling function after the completion of function call
                # execution
                for label in new_lbl_function.get_downgrade_list():
                    lbl_function.insert_into_downgrade_list(label)
                # restore the saved current line to resume the execution after
                # the function is executed
                current_line = saved_current_line
                # return the labelling function and current label after
                # executing the Call statement
                return lbl_function, current_line
            # if the function is a call to downgrading operation 
            elif is_a_downgrade(function_name):
                new_label, current_line = perform_downgrading(current_line, 
                                                clearance, 
                                                lbl_function)
                lbl_function.insert_into_downgrade_list(new_label)
                return lbl_function, current_line
            else:
                print('Function ' + function_name + ' is not defined')
                sys.exit()
        except Exception as e:
            print('Function ' + inspect.stack()[0][3] + 
                  ': fails in Call statement')
            print(str(e))
    elif is_a_return(lines[current_line]):
        # current line currently on the Return keyword, hence move to next line
        current_line = next_line(current_line)
        # flush the downgrade stack everytime a new Return statement is 
        # encountered
        lbl_function.make_downgrade_list_empty()
        # fetch the returned variables 
        variables, current_line = obtain_target_variables(current_line)
        # now iterate the variables list and start downgrading label of each
        # variable inside the list
        for variable in variables:
            # if the variable is from local list
            if lbl_function.is_local(variable):
                variable_label = lbl_function.label_from_local_list(variable)
            # if the variable is from the global list
            elif lbl_function.is_global(variable):
                variable_label = lbl_function.label_from_global_list(variable)
            # new readers would be the principals already there in the writers
            # set for each variable
            new_readers = variable_label.get_writers()
            # downgrade the label of each variable and obtain the new label
            new_label = flow_operations.downgrade(clearance, 
                                                  clearance.get_owner(),
                                                  variable,
                                                  variable_label,
                                                  new_readers)
            # insert the new label into the downgrade stack
            lbl_function.insert_into_downgrade_list(new_label)
            
        return lbl_function, current_line
    else:
        return lbl_function, current_line 
            