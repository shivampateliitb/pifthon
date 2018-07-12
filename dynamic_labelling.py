from rwfm import Label
from rwfm import label_operations
from rwfm import flow_operations
import label_function
import sys
import logging
import inspect
import traceback


statements = ['Assign', 'Compare', 'While', 'Call', 'Return']
keywords = ['endloop', 'Return', 'downgrade', 'print', 'FunctionDef', 'endfunc']
functions = dict()


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

def is_a_list(word):
    if word == 'List':
        return True
    elif word.split(':')[0] == 'List':
        return True
    else:
        return False

#to check if there is a list among the source variables
#eg: type([1,2,3]) = list
def is_list_in_source_variable(list_item):
    if type(list_item) == list:
        return True
    else:
        return False

#to see if it is a list index
#eg: list[0] or list[e], where e can be a local or global variable
def is_a_index(list_index):
    if list_index.split(':')[0] == 'index':
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

#to check if it is an end of a list 
def is_an_endlist(word):
    if word == 'endlist':
        return True
    else:
        return False

def is_a_downgrade(word):
    if word == 'downgrade':
        return True
    else:
        return False

def is_a_print_function(current_line):
    if lines[current_line].split(":")[1] == 'print':
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

def is_a_num(current_line):
    if lines[current_line].split(':')[0] == 'num':
        return True
    else:
        return False


def is_a_function(current_line):
    if lines[current_line].split(':')[0] == 'func':
        return True
    else:
        return False

def is_an_argument_inside_a_function(current_line):
	if lines[current_line].split(':')[1] == 'Call':
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

def is_end_of_function_arguments(current_line):
    if lines[current_line] == 'func_arg_close:':
        return True
    else:
        return False
#to check the number of items in a nested list call
#eg: list1[list1[list1[0]]]
def is_start_index(word):
    if word.split(':')[0] == 'start_index':
        return True
    else:
        return False

def is_end_index(word):
	if word.split(':')[0] == 'end_index':
		return True
	else:
		return False

#function to obtain the target values 
#called for both single target variables or a tuple of target variables
def general_obtain_target_variables(current_line, clearance, lbl_function):
    targets = list()
    #for an isolated(individual) variable eg: a
    if is_a_variable(current_line): 
        targets.append(get_the_id(current_line))
    #for a list as a target variable
    #can be a list name or list[0]
    elif is_a_list(lines[current_line]):
                saved_line = current_line
                if lines[current_line] == 'List':
                    target = "list"+str(current_line)   
                else:
                    target = get_the_id(saved_line)
                    current_line = next_line(current_line)
                #if we have a index variable immediately after the list i.e, list[0]
                if is_a_index(lines[current_line]) or is_start_index(lines[current_line]):
                    #if we have an expression in the index place
                    if is_start_index(lines[current_line]):
                        #move to next line as current line is the word start_index:
                        current_line = next_line(current_line)
                        #variable to store the join of target labels in the expression form in the index place
                        join_of_label = Label(clearance.get_owner(), ['*'], [])
                        #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                        #the list calling that index
                        #taking join of all the labels in the expression
                        while not is_end_index(lines[current_line]):
                            #gives the entity for which the label is getting extracted
                            index = get_the_id(current_line)
                            #gives the label of the entity
                            index_label = find_general_label(index, clearance, lbl_function, "Target index variable in the index expression")
                            #checking if the individual index can flow to the executing subject
                            if flow_operations.can_flow(index_label, clearance):
                                #if index is global then the PC label is updated
                                if lbl_function.is_global(index):
                                    readers, writers = label_operations.join(index_label, 
                                                                             lbl_function.get_pc_label())
                                    logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                    lbl_function.get_pc_label().update_readers(readers)
                                    lbl_function.get_pc_label().update_writers(writers)
                                    logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            #if the program counter can read the index then taking the join with the join_label so far
                            readers, writers = label_operations.join(join_of_label, index_label)
                            join_of_label.update_readers(readers)
                            join_of_label.update_writers(writers)
                            current_line = next_line(current_line)
                        #finally appending the joined labels by replacing the expression in the index
                        #with a new label "index"+str(current_line)
                        index_label = join_of_label
                        #then inserting this list name and the nested index in the dictionary of list names 
                        lbl_function.insert_into_list_group(target, "index"+str(current_line))

                    else:
                        lbl_function.insert_into_list_group(target, get_the_id(current_line))#insert the key-value pair in the dictionary
                    #"list_name":"index"
                    index = lbl_function.index_from_list_group(target)
                    try:
                        if index is not None:#if the index exists then finding the index label 
                            index_label = find_general_label(index, clearance, lbl_function, "Target index Variable")#getting the index label
                    except Exception as e:
                        logging.debug('Function %s : fails reading target variables' %inspect.stack()[0][3])
                        logging.warning('%s'%e)
                        logging.warning('****** Monitor Aborted ******')
                        sys.exit()

                    #checking whether the label of the index can flow to the clearance
                    #checking if index_label can flow to the clearance
                    if flow_operations.can_flow(index_label, clearance):
                        if lbl_function.is_global(index):
                            readers, writers = label_operations.join(index_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            index, 
                                            "",
                                            index_label,
                                            clearance)
                    #checking whether the temp_target_label can flow to the clearance
                    temp_target_label = find_general_label(get_the_id(saved_line), clearance, lbl_function, "Target Variable")
                    if flow_operations.can_flow(temp_target_label, clearance):
                        if lbl_function.is_global(target):
                            readers, writers = label_operations.join(temp_target_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(target, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(target, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            target, 
                                            "",
                                            temp_target_label,
                                            clearance)
                    #checking whether the index label can flow to the list label
                    #if both the index and the list lable can flow to the clearance
                    target_label = Label(clearance.get_owner(), ['*'], [])
                    if flow_operations.can_flow(index_label, temp_target_label):
                        logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), target, temp_target_label.to_string()))
                        readers, writers = label_operations.join(target_label, index_label)
                        target_label.update_readers(readers)
                        target_label.update_writers(writers)
                        logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), temp_target_label.to_string(), target_label.to_string()))

                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            "Nested Index Label", 
                                            get_the_id(saved_line),
                                            index_label,
                                            temp_target_label)  
                    lbl_function.insert_into_list_group(get_the_id(saved_line), str(index))
                    #adding it to the local list
                    lbl_function.update_local_label_list(str(index), target_label)
                elif is_a_list(lines[current_line]):
                    list_of_nested_lists = list()
                    print("Entered the list")
                    while not is_a_index(lines[current_line]):#appending all the list variables and the index in another list except for the outermost list name
                        current_line = next_line(current_line)
                        if is_start_index(lines[current_line]):
                            #variable to store the join of target labels in the expression form in the index place
                            join_of_label = Label(clearance.get_owner(), ['*'], [])
                            #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                            #the list calling that index
                            while not is_end_index(lines[current_line]):
                                index = get_the_id(current_line)
                                index_label = find_general_label(index, clearance, lbl_function, "Target index variable in the index expression")
                                if flow_operations.can_flow(index_label, clearance):
                                    if lbl_function.is_global(index) and not lbl_function.is_local(index):
                                        readers, writers = label_operations.join(index_label, 
                                                                                 lbl_function.get_pc_label())
                                        logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                        lbl_function.get_pc_label().update_readers(readers)
                                        lbl_function.get_pc_label().update_writers(writers)
                                        logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                readers, writers = label_operations.join(join_of_label, index_label)
                                join_of_label.update_readers(readers)
                                join_of_label.update_writers(writers)
                                current_line = next_line(current_line)
                            if flow_operations.can_flow(join_of_label, clearance):
	                            label_of_last_element_0f_list = find_general_label(list_of_nested_lists[len(list_of_nested_lists)-1], clearance, lbl_function, "last element in the nested list before the index expression")
	                            if not flow_operations.can_flow(join_of_label, label_of_last_element_0f_list):
	                                error_type = 0
	                                print_misuse_message(error_type, 
	                                                     "index expression", 
	                                                      list_of_nested_lists[len(list_of_nested_lists)-1],
	                                                      join_of_label,
	                                                      label_of_last_element_0f_list)
                        elif not is_an_endlist(lines[current_line]):
                            list_of_nested_lists.append(get_the_id(current_line))
                            print(get_the_id(current_line)+" ")

                        else:
                            break
                    #list containing all the lists and indexes in the nested form so as to enable their lable checking
                    if is_a_index(lines[current_line]):
                        list_of_nested_lists.append(get_the_id(current_line))
                    length = len(list_of_nested_lists)
                    #checking if the labels can flow into the label immediately before them in the list
                    #thus taking length-i-1
                    logging.debug("Label of Nested indices is being checked")
                    for i in range(length-1):
                        target = list_of_nested_lists[length-i-2]
                        index = list_of_nested_lists[length-i-1]
                        target_label = find_general_label(list_of_nested_lists[length-i-2], clearance, lbl_function, "Target Variable")
                        index_label = find_general_label(list_of_nested_lists[length-i-1], clearance, lbl_function, "Target Nested Index")
                        #checking if index_label can flow to the clearance
                        if flow_operations.can_flow(index_label, clearance):
                            if lbl_function.is_global(index) and not lbl_function.is_local(index):
                                readers, writers = label_operations.join(index_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                index, 
                                                "",
                                                index_label,
                                                clearance)
                        #checking if target_label can flow to the clearance
                        if flow_operations.can_flow(target_label, clearance):
                            if lbl_function.is_global(target) and not lbl_function.is_local(target):
                                readers, writers = label_operations.join(target_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(target, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(target, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                target, 
                                                "",
                                                target_label,
                                                clearance)
                        #checking if the index can flow to the outside list name
                        if flow_operations.can_flow(index_label, target_label):
                            logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), target, target_label.to_string()))
                            readers, writers = label_operations.join(target_label, index_label)
                            target_label.update_readers(readers)
                            target_label.update_writers(writers)
                            logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), target_label.to_string(), target_label.to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                "Nested Index Label", 
                                                get_the_id(saved_line),
                                                index_label,
                                                target_label)
                    logging.debug("Label of nested indices is done checking")
                    #inserting the outermost list name at saved_line and the join of labels obtained from the list into the global dictionary list_group
                    #in the form of "list_name":"object_with_the_label_equal_to_the_join_of_labels_calculated_above"
                    lbl_function.insert_into_list_group(get_the_id(saved_line), "nestedList"+str(saved_line))
                    #adding it to the local list
                    lbl_function.update_local_label_list("nestedList"+str(saved_line), target_label)
                targets.append(get_the_id(saved_line))

    return targets, current_line

def obtain_target_variables(current_line, clearance, lbl_function):
    targets = list()
    if is_a_variable(current_line) or is_a_list(lines[current_line]):
        targets, current_line = general_obtain_target_variables(current_line, clearance, lbl_function)

    elif is_a_tuple(lines[current_line]):
        # go to the next line where it starts to defining variables
        current_line = next_line(current_line)
        # if the line is defining a returned variable inside Tuple and
        # endtuple then collect them. Iterate the while loop until
        # it stop finding any new variable
        while is_a_variable(current_line) or is_a_list(lines[current_line])\
            and not is_an_endtuple(lines[current_line]):
            # populate the variables list
            target, current_line = general_obtain_target_variables(current_line, clearance, lbl_function)
            targets.append(target[0])
            current_line = next_line(current_line)
    return targets, current_line

def general_obtain_source_variables(current_line, clearance, lbl_function):
    sources = list()
    while (not is_end_of_file(current_line)) and \
            (not is_a_statement(lines[current_line])) and\
            (not is_a_keyword(lines[current_line])) and\
            (not is_an_endlist(lines[current_line])):
        if is_a_variable(current_line) or is_a_num(current_line):
            sources.append(get_the_id(current_line))
            
        elif is_a_list(lines[current_line]):
            #increment current line only if it is the beginning of the list
            if len(lines[current_line]) == 4:
                current_line = next_line(current_line)
                #code to deal with nested list
                #if statement to deal with a nested list at the index zero
                if is_a_list(lines[current_line]):
                    source, current_line = obtain_source_variables(current_line, clearance, lbl_function)
                    sources.append(source)
                else:
                    #if the nested list is not at index zero it can be at any other index hence the recursive call inside the else inside while loop
                    while not is_an_endlist(lines[current_line]):
                        if is_a_list(lines[current_line]):
                            source, current_line = obtain_source_variables(current_line, clearance, lbl_function)
                            sources.append(source)
                        else: 
                            sources.append(get_the_id(current_line))
                            current_line = next_line(current_line)
            else:#if it is a simple list with no nested lists then this is executed
                saved_line = current_line
                source = get_the_id(saved_line)
                current_line = next_line(current_line)
                #if we have a index variable immediately after the list i.e, list[0] or contains an expression as an index
                if is_a_index(lines[current_line]) or is_start_index(lines[current_line]): 
                    if is_start_index(lines[current_line]):
                        current_line = next_line(current_line)
                        #variable to store the join of target labels in the expression form in the index place
                        join_of_label = Label(clearance.get_owner(), ['*'], [])
                        #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                        #the list calling that index
                        while not is_end_index(lines[current_line]):
                            index = get_the_id(current_line)
                            index_label = find_general_label(index, clearance, lbl_function, "Source index variable in the index expression")
                            if flow_operations.can_flow(index_label, clearance):
                                if lbl_function.is_global(index):
                                    readers, writers = label_operations.join(index_label, 
                                                                             lbl_function.get_pc_label())
                                    logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                    lbl_function.get_pc_label().update_readers(readers)
                                    lbl_function.get_pc_label().update_writers(writers)
                                    logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            readers, writers = label_operations.join(join_of_label, index_label)
                            join_of_label.update_readers(readers)
                            join_of_label.update_writers(writers)
                            current_line = next_line(current_line)
                            logging.debug('Join of label read uptil now in the index: %s'%(join_of_label.to_string()))
                        index_label = join_of_label
                        lbl_function.insert_into_list_group(source, "index"+str(current_line))
                    else:
                        lbl_function.insert_into_list_group(source, get_the_id(current_line))#insert the key-value pair in the dictionary
                    #"list_name":"index"
                    index = lbl_function.index_from_list_group(source)
                    try:
                        if index is not None:#if the index exists then finding the index label 
                            index_label = find_general_label(index, clearance, lbl_function, "Source index Variable")#getting the index label
                    except Exception as e:
                        logging.debug('Function %s : fails reading source variables' %inspect.stack()[0][3])
                        logging.warning('%s'%e)
                        logging.warning('****** Monitor Aborted ******')
                        sys.exit()

                    #checking if index_label can flow to the clearance
                    if flow_operations.can_flow(index_label, clearance):
                        if lbl_function.is_global(index):
                            readers, writers = label_operations.join(index_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            index, 
                                            "",
                                            index_label,
                                            clearance)
                    #checking whether the index label can flow to the list label
                    temp_source_label = find_general_label(get_the_id(saved_line), clearance, lbl_function, "Source Variable")
                    #if the index can flow to the clearance then checking whether the listname can flow to the clearance
                    if flow_operations.can_flow(temp_source_label, clearance):
                        if lbl_function.is_global(source):
                            readers, writers = label_operations.join(temp_source_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(source, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(source, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            source, 
                                            "",
                                            temp_source_label,
                                            clearance)
                    #if both the list and the index can flow to the clearance then check whether the index can flow to the list
                    source_label = Label(clearance.get_owner(), ['*'], [])
                    if flow_operations.can_flow(index_label, temp_source_label):
                        logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), source, temp_source_label.to_string()))
                        readers, writers = label_operations.join(temp_source_label, index_label)
                        source_label.update_readers(readers)
                        source_label.update_writers(writers)
                        logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), temp_source_label.to_string(), source_label.to_string()))

                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            "Nested Index Label", 
                                            get_the_id(saved_line),
                                            index_label,
                                            temp_source_label)  
                elif is_a_list(lines[current_line]):#if there is a nested list case : list1[list1[....0]]
                    list_of_nested_lists = list()
                    while not is_a_index(lines[current_line]) and not is_end_index(lines[current_line]):#appending all the list variables and the index in another list except for the outermost list name
                        if is_start_index(lines[current_line]):
                            current_line = next_line(current_line)
                            #variable to store the join of target labels in the expression form in the index place
                            join_of_label = Label(clearance.get_owner(), ['*'], [])
                            #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                            #the list calling that index
                            while not is_end_index(lines[current_line]):
                                index = get_the_id(current_line)
                                index_label = find_general_label(index, clearance, lbl_function, "Source index variable in the index expression")
                                if flow_operations.can_flow(index_label, clearance):
                                    if lbl_function.is_global(index):
                                        readers, writers = label_operations.join(index_label, 
                                                                                 lbl_function.get_pc_label())
                                        logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                        lbl_function.get_pc_label().update_readers(readers)
                                        lbl_function.get_pc_label().update_writers(writers)
                                        logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                readers, writers = label_operations.join(join_of_label, index_label)
                                join_of_label.update_readers(readers)
                                join_of_label.update_writers(writers)
                                current_line = next_line(current_line)
                            if flow_operations.can_flow(join_of_label, clearance):
                                label_of_last_element_0f_list = find_general_label(list_of_nested_lists[len(list_of_nested_lists)-1], clearance, lbl_function, "last element in the nested list before the index expression")
                                if not flow_operations.can_flow(join_of_label, label_of_last_element_0f_list):
                                    error_type = 0
                                    print_misuse_message(error_type, 
                                                        "index expression", 
                                                        list_of_nested_lists[len(list_of_nested_lists)-1],
                                                        join_of_label,
                                                        label_of_last_element_0f_list)
                            else:
                                error_type = 0
                                print_misuse_message(error_type, 
                                                    index, 
                                                    "",
                                                    index_label,
                                                    clearance)
                        
                        else:
                            list_of_nested_lists.append(get_the_id(current_line))
                            current_line = next_line(current_line)
                    #list containing all the lists and indexes in the nested form so as to enable their lable checking
                    
                    if is_a_index(lines[current_line]):
                        list_of_nested_lists.append(get_the_id(current_line))
                    length = len(list_of_nested_lists)
                    #checking if the labels can flow into the label immediately before them in the list
                    #thus taking length-i-1
                    logging.debug("Label of Nested indices is being checked")
                    for i in range(length-1):
                        index = list_of_nested_lists[length-i-1]
                        source = list_of_nested_lists[length-i-2]
                        list_of_nested_lists[length-i-1]
                        source_label = find_general_label(list_of_nested_lists[length-i-2], clearance, lbl_function, "Source Variable")
                        index_label = find_general_label(list_of_nested_lists[length-i-1], clearance, lbl_function, "Nested Index")

                        #checking if index_label can flow to the clearance
                        if flow_operations.can_flow(index_label, clearance):
                            if lbl_function.is_global(index):
                                readers, writers = label_operations.join(index_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                index, 
                                                "",
                                                index_label,
                                                clearance)
                        #if the index can flow to the clearance then checking whether the listname can flow to the clearance
                        if flow_operations.can_flow(source_label, clearance):
                            if lbl_function.is_global(source):
                                readers, writers = label_operations.join(source_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(source, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(source, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                source, 
                                                "",
                                                source_label,
                                                clearance)
                        if flow_operations.can_flow(index_label, source_label):
                            logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), source, source_label.to_string()))
                            readers, writers = label_operations.join(source_label, index_label)
                            source_label.update_readers(readers)
                            source_label.update_writers(writers)
                            logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), source_label.to_string(), source_label.to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                "Nested Index Label", 
                                                get_the_id(saved_line),
                                                index_label,
                                                source_label)
                    logging.debug("Label of nested indices is done checking")
                    #inserting the outermost list name at saved_line and the join of labels obtained from the list into the global dictionary list_group
                    #in the form of "list_name":"object_with_the_label_equal_to_the_join_of_labels_calculated_above"
                    lbl_function.insert_into_list_group(get_the_id(saved_line), "nestedList"+str(saved_line))
                    #adding it to the local list
                    lbl_function.update_local_label_list("nestedList"+str(saved_line), source_label)

                sources.append(get_the_id(saved_line))
        current_line = next_line(current_line)
    return sources, current_line

def obtain_source_variables(current_line, clearance, lbl_function):
        sources = list()
        if is_a_variable(current_line) or is_a_num(current_line) or is_a_list(lines[current_line]):
            sources, current_line = general_obtain_source_variables(current_line, clearance, lbl_function)

        elif is_a_tuple(lines[current_line]):
        # go to the next line where it starts to defining variables
            current_line = next_line(current_line)
        # if the line is defining a returned variable inside Tuple and
        # endtuple then collect them. Iterate the while loop until
        # it stop finding any new variable
            while is_a_variable(current_line) \
                or is_a_num(current_line) \
                or is_a_list(lines[current_line])\
                and not is_an_endtuple(lines[current_line]):

                source, current_line = general_obtain_source_variables(current_line, clearance, lbl_function)
                sources.append(source[0])
                current_line = next_line(current_line)
        return sources,current_line

#it deals with arguments of type:str, num, function calls
def obtain_arguments(current_line, clearance, lbl_function):
    arguments = list()
    #arguments start with func_arg_open: and end with func_arg_close:
    current_line = next_line(current_line)
    while  (not is_end_of_function_arguments(current_line)):
        #check if any function definition has been passed as an argument
        if (not is_a_function_call(lines[current_line])) and \
           (is_an_argument(current_line)):
            arguments.append(get_the_id(current_line))

        elif is_a_list(lines[current_line]):
             #increment current line only if it is the beginning of the list
            if len(lines[current_line]) == 4:
                current_line = next_line(current_line)
                #code to deal with nested list
                #if statement to deal with a nested list at the index zero eg : [1,[2,3],4]
                if is_a_list(lines[current_line]):
                    argument, current_line = obtain_source_variables(current_line, clearance, lbl_function)
                    arguments.append(argument)
                else:
                    #if the nested list is not at index zero it can be at any other index hence the recursive call inside the else inside while loop
                    while not is_an_endlist(lines[current_line]):
                        if is_a_list(lines[current_line]):
                            argument, current_line = obtain_source_variables(current_line, clearance, lbl_function)
                            arguments.append(argument)
                        else: 
                            arguments.append(get_the_id(current_line))
                            current_line = next_line(current_line)
            else:#if it is a simple list with no nested lists then this is executed but nested list in the form of list names 
            #eg: [list1[list1[0]]]
                saved_line = current_line
                current_line = next_line(current_line)
                argument = get_the_id(saved_line)
                #if we have a index variable immediately after the list i.e, list[0]
                if is_a_index(lines[current_line]):
                	#for mathematical expressions like a+2, a/2 etc..
                	# start_index:
                	# ...
                	# ...
                	# end_index:
                    if is_start_index(lines[current_line]):
                        current_line = next_line(current_line)
                        #variable to store the join of target labels in the expression form in the index place
                        join_of_label = Label(clearance.get_owner(), ['*'], [])
                        #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                        #the list calling that index
                        while not is_end_index(lines[current_line]):
                            index = get_the_id(current_line)
                            index_label = find_general_label(index, clearance, lbl_function, "Argument index variable in the index expression")
                            if flow_operations.can_flow(index_label, clearance):
                            	#if any internmediate index is global then it will affect the pc label
                                if lbl_function.is_global(index):
                                    readers, writers = label_operations.join(index_label, 
                                                                             lbl_function.get_pc_label())
                                    logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                    lbl_function.get_pc_label().update_readers(readers)
                                    lbl_function.get_pc_label().update_writers(writers)
                                    logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            #the join_of_label contains the join of all the labels from the expression statement
                            readers, writers = label_operations.join(index_label, join_of_label)
                            join_of_label.update_readers(readers)
                            join_of_label.update_writers(writers)
                            current_line = next_line(current_line)
                            
                        index_label = join_of_label
                        #inserting this join into the global list group(a dictionary) so that we can obtain the join labelled later if needed 
                        lbl_function.insert_into_list_group(argument, "index"+str(current_line))
                    else:#inserts the nested list calls 
                    #if the list call is list1[list1[list1[0]]]
                    #this will append list1, list1 into the list leaving the innermost and outermost identities
                        lbl_function.insert_into_list_group(argument, get_the_id(current_line))#insert the key-value pair in the dictionary
                    #"list_name":"index"

                    index = lbl_function.index_from_list_group(argument)
                    try:
                        if index is not None:#if the index exists then finding the index label 
                            index_label = find_general_label(index, clearance, lbl_function, "Argument list index")#getting the index label
                    except Exception as e:
                        logging.debug('Function %s : fails reading source variables' %inspect.stack()[0][3])
                        logging.warning('%s'%e)
                        logging.warning('****** Monitor Aborted ******')
                        sys.exit()
                    
                    #checking if index_label can flow to the clearance
                    if flow_operations.can_flow(index_label, clearance):
                        if lbl_function.is_global(index):
                            readers, writers = label_operations.join(index_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            index, 
                                            "",
                                            index_label,
                                            clearance)
                    #checking whether the joined index label obtained from all the nested list names and the innermost index , can flow to the outermost list label
                    temp_argument_label = find_general_label(get_the_id(saved_line), clearance, lbl_function, "List Argument Variable")#stores the label of the 
                    #argument
                    #if the index can flow to the clearance then checking whether the outermost list label can flow to the clearance
                    if flow_operations.can_flow(temp_argument_label, clearance):
                        if lbl_function.is_global(argument):
                            readers, writers = label_operations.join(temp_argument_label, 
                                                                     lbl_function.get_pc_label())
                            logging.debug('PC label before reading %s is %s'%(argument, lbl_function.get_pc_label().to_string()))
                            lbl_function.get_pc_label().update_readers(readers)
                            lbl_function.get_pc_label().update_writers(writers)
                            logging.debug('PC label after reading %s is %s'%(argument, lbl_function.get_pc_label().to_string()))
                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            argument, 
                                            "",
                                            temp_argument_label,
                                            clearance)
                    argument_label = Label(clearance.get_owner(), ['*'], [])#stores the join of the label
                    if flow_operations.can_flow(index_label, temp_argument_label):
                        logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), argument, temp_argument_label.to_string()))
                        readers, writers = label_operations.join(temp_argument_label, index_label)
                        argument_label.update_readers(readers)
                        argument_label.update_writers(writers)
                        logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), temp_argument_label.to_string(), argument_label.to_string()))

                    else:
                        error_type = 0
                        print_misuse_message(error_type, 
                                            "Nested Index Label", 
                                            get_the_id(saved_line),
                                            index_label,
                                            argument_label)  
                    lbl_function.insert_into_list_group(get_the_id(saved_line), str(index))
                    #adding it to the local list
                    lbl_function.update_local_label_list(str(index), argument_label)
                elif is_a_list(lines[current_line]):#if there is a nested list case : list1[list1[....0]]
                    list_of_nested_lists = list()
                    while not is_a_index(lines[current_line]):#appending all the list variables and the index in another list except for the outermost list name
                        if is_start_index(lines[current_line]):
                            current_line = next_line(current_line)
                            #variable to store the join of target labels in the expression form in the index place
                            join_of_label = Label(clearance.get_owner(), ['*'], [])
                            #reading all the target variables in the expression to get their label and ultimately take their join to see if they can flow to 
                            #the list calling that index
                            while not is_end_index(lines[current_line]):
                                index = get_the_id(current_line)
                                index_label = find_general_label(index, clearance, lbl_function, "Argument index variable in the index expression")
                                if flow_operations.can_flow(index_label, clearance):
                                    if lbl_function.is_global(index):
                                        readers, writers = label_operations.join(index_label, 
                                                                                 lbl_function.get_pc_label())
                                        logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                        lbl_function.get_pc_label().update_readers(readers)
                                        lbl_function.get_pc_label().update_writers(writers)
                                        logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                readers, writers = label_operations.join(join_of_label, index_label)
                                join_of_label.update_readers(readers)
                                join_of_label.update_writers(writers)
                                current_line = next_line(current_line)
                            if flow_operations.can_flow(join_of_label, clearance):
	                            label_of_last_element_0f_list = find_general_label(list_of_nested_lists[len(list_of_nested_lists)-1], clearance, lbl_function, "last element in the nested list before the index expression")
	                            if not flow_operations.can_flow(join_of_label, label_of_last_element_0f_list):
	                                error_type = 0
	                                print_misuse_message(error_type, 
	                                                     "index expression", 
	                                                      list_of_nested_lists[len(list_of_nested_lists)-1],
	                                                      join_of_label,
	                                                      label_of_last_element_0f_list)
                        else:
                            list_of_nested_lists.append(get_the_id(current_line))
                            current_line = next_line(current_line)

                    #list containing all the lists and indexes in the nested form so as to enable their lable checking
                    list_of_nested_lists.append(get_the_id(current_line))
                    length = len(list_of_nested_lists)
                    #checking if the labels can flow into the label immediately before them in the list
                    #thus taking length-i-1
                    temp_argument_label = Label(clearance.get_owner(), ['*'], [])
                    logging.debug("Label of Nested indices is being checked")
                    for i in range(length-1):
                        argument = list_of_nested_lists[length-i-2]
                        index = list_of_nested_lists[length-i-1]
                        argument_label = find_general_label(list_of_nested_lists[length-i-2], clearance, lbl_function, "ARGUMENT ")
                        index_label = find_general_label(list_of_nested_lists[length-i-1], clearance, lbl_function, "Nested Index")

                        #checking if index_label can flow to the clearance
                        if flow_operations.can_flow(index_label, clearance):
                            if lbl_function.is_global(index):
                                readers, writers = label_operations.join(index_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                index, 
                                                "",
                                                index_label,
                                                clearance)
                        #if the index can flow to the clearance then checking whether the listname can flow to the clearance
                        if flow_operations.can_flow(argument_label, clearance):
                            if lbl_function.is_global(argument):
                                readers, writers = label_operations.join(argument_label, 
                                                                         lbl_function.get_pc_label())
                                logging.debug('PC label before reading %s is %s'%(argument, lbl_function.get_pc_label().to_string()))
                                lbl_function.get_pc_label().update_readers(readers)
                                lbl_function.get_pc_label().update_writers(writers)
                                logging.debug('PC label after reading %s is %s'%(argument, lbl_function.get_pc_label().to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                argument, 
                                                "",
                                                argument_label,
                                                clearance)
                        if flow_operations.can_flow(index_label, argument_label):
                            logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), argument, argument_label.to_string()))
                            readers, writers = label_operations.join(argument_label, index_label)
                            temp_argument_label.update_readers(readers)
                            temp_argument_label.update_writers(writers)
                            logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), argument_label.to_string(), argument_label.to_string()))
                        else:
                            error_type = 0
                            print_misuse_message(error_type, 
                                                "Nested Index Label", 
                                                get_the_id(saved_line),
                                                index_label,
                                                argument_label)
                    logging.debug("Label of nested indices is done checking")
                    #inserting the outermost list name at saved_line and the join of labels obtained from the list into the global dictionary list_group
                    #in the form of "list_name":"object_with_the_label_equal_to_the_join_of_labels_calculated_above"
                    lbl_function.insert_into_list_group(get_the_id(saved_line), "nestedList"+str(saved_line))
                    #adding it to the local list
                    lbl_function.update_local_label_list("nestedList"+str(saved_line), temp_argument_label)

                arguments.append(get_the_id(saved_line)) 

        elif is_a_function_call(lines[current_line]):
            #saved_line contains {arg:Call} but we need to get to the next line to get the function name in order to name the 
            #local argument to replace this function in the parent function call
            saved_line = current_line
            current_line = next_line(current_line)
            function_name = get_the_id(current_line)
            current_line = saved_line
            #function will have to be evaluated and replaced with a new object that will have
            logging.debug("Function "+function_name+" detected as argument hence will be executed"); 
            lbl_function, current_line = DL(current_line, clearance, lbl_function)
            #to get the subject label for the new_argument_name
            if is_defined(function_name):
                if lbl_function.find_in_functions_list(function_name):
                    subject_label = lbl_function.label_from_functions_list(function_name)
                # otherwise function is executed with the label of main 
                # executing subject
                else:
                    subject_label = clearance

            elif is_a_downgrade(function_name):
                subject_label = clearance
            logging.debug("Current line is :"+str(current_line))
            #The new argument name that will replace the function call inside the parent function will have the current line number in its suffix
            #holds the label of the new_argument name which will replace the function call expression after executing the function
            new_object_label = Label(subject_label.get_owner(), ['*'], [])
            readers, writers = label_operations.join(subject_label, new_object_label)
            new_object_label.update_writers(writers)
            new_object_label.update_readers(readers)
            #to replace the name of the function in the list of arguments
            new_argument_name = function_name+"Object"+str(current_line)
            lbl_function.update_local_label_list(new_argument_name, new_object_label)
            arguments.append(new_argument_name) 
        current_line = next_line(current_line)
    return arguments, current_line

#function to get the parameters of any function definition
def obtain_parameters(current_line):
    parameters = list()
    while (not is_end_of_file(current_line)) and \
            (not is_a_statement(lines[current_line])) and \
            (not is_a_keyword(lines[current_line])):
        if is_an_argument(current_line):
            parameters.append(get_the_id(current_line))
        current_line = next_line(current_line)
    return parameters, current_line

#to find the label in the following two functions as they used the same code to find the label hence made a function find_general_label 
#for reusable code
def find_general_label(sources, clearance, lbl_function, variable_type):
    if lbl_function.is_local(sources):
        source_label = lbl_function.label_from_local_list(sources)
        logging.debug('%s %s is a local having label %s' %(variable_type, sources, source_label.to_string()))
    elif lbl_function.is_global(sources):
        source_label = lbl_function.label_from_global_list(sources)
        logging.debug('%s %s is a global having label %s' %(variable_type, sources, source_label.to_string()))
    else:
        source_label = Label(clearance.get_owner(), ['*'], [])
        logging.debug('%s %s is created with label %s' %(variable_type, sources, source_label.to_string()))
    return source_label

#in order to find the join of all the elements of the list and also to deal with nested lists
#a function read_lists_as_source_variables is used so that recursive calls are made and all the lists are accessed
def read_lists_as_source_variables(source, clearance, lbl_function):
    new_label = Label(clearance.get_owner(),['*'], [])
    #each element of a list will be an individual variable/item
    #list of list are ultimately converted into a single list
    for j in range(len(source)):
        if is_list_in_source_variable(source[j]):
            source_label = read_lists_as_source_variables(source[j], clearance, lbl_function)
        else:
            source_label = find_general_label(source[j], clearance, lbl_function,"Source variable")
        readers, writers = label_operations.join(new_label, source_label)
        new_label.update_readers(readers)
        new_label.update_writers(writers)
    return new_label

def read_source_labels(sources, clearance, lbl_function):
    for i in range(0, len(sources)):
        #if a source[i] is in the form of a nested list and not the name of a list
        if is_list_in_source_variable(sources[i]):
            source_label = read_lists_as_source_variables(sources[i], clearance, lbl_function)
            logging.debug('Source variable %s is a list having label %s'%(sources[i], source_label.to_string()))
        
        elif lbl_function.find_in_list_group(sources[i]):
            #this elif is exxecuted when the list name is used along with an index
            source_label = find_general_label(sources[i], clearance, lbl_function, "Source Variable")
            #getting the index of the list which is called using the dictionary _list_group which stores
            #{'listname':'index'} form
            index = lbl_function.index_from_list_group(sources[i])
            try:
                if index is not None:#if the index exists then fincding the index label 
                    index_label = find_general_label(index, clearance, lbl_function, "Source Variable")
            except Exception as e:
                logging.debug('Function %s : fails during reading source labels' %inspect.stack()[0][3])
                logging.warning('%s'%e)
                logging.warning('****** Monitor Aborted ******')
                sys.exit()
            #checking if index_label can flow to the clearance
            if flow_operations.can_flow(index_label, clearance):
                if lbl_function.is_global(index) and not lbl_function.is_local(index):
                    readers, writers = label_operations.join(index_label, 
                                                             lbl_function.get_pc_label())
                    logging.debug('PC label before reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
                    lbl_function.get_pc_label().update_readers(readers)
                    lbl_function.get_pc_label().update_writers(writers)
                    logging.debug('PC label after reading %s is %s'%(index, lbl_function.get_pc_label().to_string()))
            else:
                error_type = 0
                print_misuse_message(error_type, 
                                    index, 
                                    "",
                                    index_label,
                                    clearance)
            #if the index can flow to the clearance then checking whether the listname can flow to the clearance
            if flow_operations.can_flow(source_label, clearance):
                if lbl_function.is_global(sources[i]) and not lbl_function.is_local(sources[i]):
                    readers, writers = label_operations.join(source_label, 
                                                             lbl_function.get_pc_label())
                    logging.debug('PC label before reading %s is %s'%(sources[i], lbl_function.get_pc_label().to_string()))
                    lbl_function.get_pc_label().update_readers(readers)
                    lbl_function.get_pc_label().update_writers(writers)
                    logging.debug('PC label after reading %s is %s'%(sources[i], lbl_function.get_pc_label().to_string()))
            else:
                error_type = 0
                print_misuse_message(error_type, 
                                    sources[i], 
                                    "",
                                    source_label,
                                    clearance)
            #if the listname can flow to the clearance then checking whether the index_label can flow to the listname_label
            #checking if in list[index] expression whether index can flow to list and then taking their join
            #to check if the join can flow to the pc label
            join_of_two_labels = Label(clearance.get_owner(), ['*'], [])
            if flow_operations.can_flow(index_label, source_label):
                logging.debug('Index: %s with Index label: %s can flow to the list(%s) label: %s'%(str(index), index_label.to_string(), sources[i], source_label.to_string()))
                readers, writers = label_operations.join(source_label, index_label)
                join_of_two_labels = Label(source_label.get_owner(), ['*'], []);
                join_of_two_labels.update_readers(readers)
                join_of_two_labels.update_writers(writers)
                logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), source_label.to_string(), join_of_two_labels.to_string()))
            else:
                error_type = 0
                print_misuse_message(error_type, 
                                    index, 
                                    sources[i],
                                    index_label,
                                    source_label)
        
        else:#executed for individual elements
            source_label = find_general_label(sources[i], clearance, lbl_function, "Source Variable")
        if flow_operations.can_flow(source_label, clearance):
            if lbl_function.is_global(str(sources[i])) and not lbl_function.is_local(str(sources[i])):
                readers, writers = label_operations.join(source_label, 
                                                         lbl_function.get_pc_label())
                logging.debug('PC label before reading %s is %s'%(sources[i], lbl_function.get_pc_label().to_string()))
                lbl_function.get_pc_label().update_readers(readers)
                lbl_function.get_pc_label().update_writers(writers)
                logging.debug('PC label after reading %s is %s'%(sources[i], lbl_function.get_pc_label().to_string()))
        else:
            error_type = 0
            print_misuse_message(error_type, 
                                sources[i], 
                                "",
                                source_label,
                                clearance)
    return lbl_function     


''' Check if the information can flow from arguments to executing subject i.e.
executing subject should be able to read the function arguments otherwise
throw misuse message'''
def read_arguments(subject_label, arguments, lbl_function):
    logging.debug("reading arguments")
    for i in range(0, len(arguments)):
        if lbl_function.is_local(arguments[i]):
            argument_label = lbl_function.label_from_local_list(arguments[i])
            logging.debug('Local variable %s has label %s' %(arguments[i], argument_label.to_string()))
        if lbl_function.is_global(arguments[i]):
            argument_label = lbl_function.label_from_global_list(arguments[i])
            logging.debug('Global variable %s has label %s' %(arguments[i], argument_label.to_string()))
        # if the argument has neither a local nor a globally defined label
        # then it is a constant literal e.g., integer, float or string 
        if 'argument_label' in locals():    
            if not flow_operations.can_flow(argument_label, subject_label):
                error_type = 0
                print_misuse_message(error_type,
                                     arguments[i],
                                     "",
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
        logging.debug('Function %s raised an exception' % inspect.stack()[0][3])
        logging.warning('%s'%e)
        
    message_2 = 'Information from ' + source_label.to_string() + ' cannot flow to ' + target_label.to_string()  
    logging.warning('%s\n%s'%(message_1, message_2))
    #print('iteration performed: ' + str(iteration))
    logging.warning('****** Monitor Aborted ******')
    sys.exit()


def perform_downgrading(current_line, clearance, lbl_function):
    try:
        logging.debug('current node: %s at line %s' %(lines[current_line], current_line))
        # at this point current line is calling the downgrading, hence 
        # move to next line to fetch its arguments
        current_line = next_line(current_line)
        # in the next three iteration get the owner, object label and
        # list of principals to be added in the downgraded label
        for i in range(2):
            if i == 0:
                object_name = lines[current_line].split(':')[1]
                if lbl_function.is_local(object):
                    logging.debug('Variable %s has a dynamic label'%object_name)
                    object_label = lbl_function.label_from_local_list(object_name)
                else:
                    logging.debug('Variable %s has a fixed label'%object_name)
                    object_label = lbl_function.label_from_global_list(object_name)
            else:
                new_readers = lines[current_line].split(':')[1].split(',')
            current_line = next_line(current_line)
        logging.debug('Variable %s having label %s is going to be downgraded to %s'%(object_name, object_label.to_string(), new_readers))
        # make target label same as object label only with added readers
        target_label = Label(object_label.get_owner(),
                             object_label.get_readers(),
                             object_label.get_writers())
        target_label.insert_into_readers(new_readers)
        # now call downgrade operation
        new_label = flow_operations.downgrade(clearance, 
                                              object_name,
                                              object_label, 
                                              new_readers)
        
        # downgrading is successfull if:    
        # if object label is global then check if new label and object label is same
        # otherwise if new label and target label is same and new label is not none
        if (lbl_function.is_global(object_name) and new_label.is_equal_to(object_label)) \
        or (not new_label == None and new_label.is_equal_to(target_label)):
            logging.debug('New label of variable %s is %s' %(object_name, new_label.to_string()))
            return new_label, current_line
        else:
            error_type = 2
            print_misuse_message(error_type, 
                                 object_name, 
                                 "", 
                                 object_label, 
                                 target_label)
            
    except Exception as e:
        logging.debug('Function %s : fails during downgrading' %inspect.stack()[0][3])
        logging.warning('%s'%e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()

''' Perform labelling for an assignment statement'''
def perform_assignment(current_line, clearance, lbl_function):
    try:
        # go to the next line
        current_line = next_line(current_line)
        # fetch the target variable from the current line, the function can
        # fetch a single target variable as well as a tuple of target variables
        # and store them in a list called targets
        targets, current_line = obtain_target_variables(current_line, clearance, lbl_function)
        logging.debug('Target variables of the assignment statement are: %s' %targets)
        # go to the next line to start fetching the source variables or
        # if it is a function call then execute that function
        current_line = next_line(current_line)
        # if current line encounters a source variable of the form "name:a"
        # where 'a' is a source variable
        if is_a_variable(current_line) or is_a_num(current_line) or is_a_tuple(lines[current_line]) or is_a_list(lines[current_line]):
            # obtain source variables of an assignment statement and store them
            # into a list called sources
            sources, current_line = obtain_source_variables(current_line, clearance, lbl_function)

            logging.debug('Source variables of the assignment statement are: %s' %sources)
            # read the source variables' labels , check if the 
            # label of each variable can flow to executing subject and if yes
            # then update the PC label, finally return the updated labelling
            # function
            lbl_function = read_source_labels(sources, clearance, lbl_function)

        # if current line encounters a function call i.e. a "Call" statement
        # then call the DL function to execute the mentioned call
        elif is_a_function_call(lines[current_line]):
            # call the DL algorithm for "Call" statement and receive the updated
            # labelling function
            lbl_function, current_line = DL(current_line,
                                            clearance,
                                            lbl_function)
            # the returned statement would perform an implicit downgrading when
            # and store the downgraded labels into a list. Iterate that list
            # to read each label and update the PC label accordingly
            for label in lbl_function.get_downgrade_list():
                readers, writers = label_operations.join(lbl_function.remove_from_downgrade_list(), 
                                                     lbl_function.get_pc_label())
                lbl_function.get_pc_label().update_readers(readers)
                lbl_function.get_pc_label().update_writers(writers)
        # obtain the new PC label
        pc_label = lbl_function.get_pc_label()
        logging.debug('Updated PC label %s' %(pc_label.to_string()))
        # now iterate the targets list and for each target variables check if
        # the PC label can flow to target label (if global) or update the target
        # label if local or create a new target label if that variable is not
        # already defined earlier
        for target in targets:
            if lbl_function.find_in_list_group(target):
                target_label = find_general_label(target, clearance, lbl_function, "Target Variable")
                index = lbl_function.index_from_list_group(target)
                index_label = find_general_label(index, clearance, lbl_function, "Index")
                if flow_operations.can_flow(index_label, target_label):
                    logging.debug('Nested Index with Index label: %s can flow to the list(%s) label: %s'%(index_label.to_string(), target, target_label.to_string()))
                    readers, writers = label_operations.join(target_label, index_label)
                    target_label.update_readers(readers)
                    target_label.update_writers(writers)
                    logging.debug('Join of Index label: %s with list label:%s is %s '%(index_label.to_string(), target_label.to_string(), target_label.to_string()))

                else:
                    error_type = 0
                    print_misuse_message(error_type, 
                                        "Nested Index Label", 
                                        get_the_id(saved_line),
                                        index_label,
                                        target_label)
            # if the label is in the local list then update the local label
            if lbl_function.is_local(target):
                target_label = lbl_function.label_from_local_list(target)
                logging.debug('Old label of target %s is %s'%(target, target_label.to_string()))
                target_label.update_readers(pc_label.get_readers())
                target_label.update_writers(pc_label.get_writers())
                logging.debug('New label of target %s is %s'%(target, target_label.to_string()))
            # if the label is in global list then check if the new PC label
            # can flow into the target label
            elif lbl_function.is_global(target):
                target_label = lbl_function.label_from_global_list(target)
                logging.debug('Label of target %s is a given as %s' %(target, target_label.to_string()))
                # check if PC label can flow to target label otherwise print the
                # misuse message
                if not flow_operations.can_flow(pc_label, target_label):
                    error_type = 1
                    print_misuse_message(error_type, 
                                         ":PC", 
                                         target, 
                                         pc_label,
                                         target_label)
            
            # if the target variable does not exist in neither of local or global
            # label list then create a new label and store into local label list
            else:
                target_label = Label(clearance.get_owner(),
                                     pc_label.get_readers(),
                                     pc_label.get_writers())
                logging.debug('Target %s is a new variable created with label %s' %(target, target_label.to_string()))
                lbl_function.update_local_label_list(target, target_label)
    except Exception as e:
        logging.debug('Function %s : fails in Assignment statement'%( inspect.stack()[0][3]))
        logging.warning('%s' %e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()
        
    return lbl_function, current_line


''' The function perform the labelling operation for a comparison statement'''
def perform_comparison(current_line, clearance, lbl_function):
    try:
        # go to the next line to fetch the variables participate in a comparison
        # statement
        current_line = next_line(current_line)
        # fetch the source variables involved in the comparison statement
        sources, current_line = obtain_source_variables(current_line, clearance, lbl_function)
        logging.debug('Source variables of comparison statements are: %s' %sources)
        # read the label of each variable and check if their label can flow
        # to executing subject as well as PC and update PC label accordingly
        lbl_function = read_source_labels(sources, clearance, lbl_function)
    except Exception as e:
        logging.debug('Function %s : fails in Comparison statement' % inspect.stack()[0][3])
        logging.warn('%s'%e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()
            
    return lbl_function, current_line
        

''' The function perform labelling for iterative statement'''
def perform_iteration(current_line, clearance, lbl_function):
    try:
        # first save the current line as we might need to execute from this point
        # again in future
        start_line = current_line
        logging.debug('Save the starting line of loop is: %s' %start_line)
        # now also create another new labelling function to make a copy of
        # existing labelling function
        start_lbl_function = create_labelling_function()
        logging.debug('New labelling function is created')
        lbl_function.copy_into(start_lbl_function)
        logging.debug('Old labelling function is copied into new labelling function')
        # go to the next line to start operating on the body of a While statement
        current_line = next_line(current_line)
        logging.debug('Start executing the loop body at line %s' % current_line)
        # iterate until it reach the end of the While body
        while not is_an_endloop(lines[current_line]):
            if is_a_statement(lines[current_line]):
                # call the DL function if the current line found any new statement
                # inside the loop body
                lbl_function, current_line = DL(current_line,
                                                clearance, 
                                                lbl_function)
            # otherwise skip to the next line
            else:
                current_line = next_line(current_line)
        logging.debug('Stop executing the loop body at line %s' %current_line)
        # after completing the execution of loop body the monitor will check if
        # the new labelling function is same as the old labelling function. If 
        # it is not same then again execute the loop body
        if not lbl_function.is_equal_to(start_lbl_function):
            logging.debug('New labels are not same as old labels')
            # restore the current line to start the loop body execution again
            current_line = start_line
            logging.debug('Restore the starting line of loop is %s' %current_line)
            # this is a global variable to note down number of iteration
            return DL(current_line, clearance, lbl_function)
        # if the labelling function is unchanged then skip to the next line
        # and return the labelling function
        else:
            logging.debug('New labels are same as old labels')
            current_line = next_line(current_line)
            return lbl_function, current_line
    except Exception as e:
        logging.debug('Function %s fails in Iteration statement' %inspect.stack()[0][3])
        logging.warning('%s' %e) 
        logging.warning('****** Monitor Aborted ******')
        sys.exit()


''' Perform labelling operation for a function call statement'''
def perform_function_call(current_line, clearance, lbl_function):
    try:
        
        # the current line is at Call statement, hence go to the next line
        current_line = next_line(current_line)
        # get the function name
        function_name = get_the_id(current_line)
        logging.debug('Function name: %s' %function_name)
        # check if the function is defined earlier before executing
        if is_defined(function_name):
            # if the function is executed with different subject label 
            # given as input then obtain the subject label
            if lbl_function.find_in_functions_list(function_name):
                subject_label = lbl_function.label_from_functions_list(function_name)
            # otherwise function is executed with the label of main 
            # executing subject
            else:
                subject_label = clearance
            logging.debug('Function is executed with subject label %s' % subject_label.to_string())
            # current line is at the function name, go to the next line
            current_line = next_line(current_line)
            # obtain the list of arguments, this list will be
            # used during executing function to match the total number and
            # order of the arguments with parameters in function definition
            #number of parameters in obtain_arguments changed so as to take care of any function calls as parameters itself
            #the function call as a parameter will be executed with clearance = subject_label(of current function) 

            arguments, current_line = obtain_arguments(current_line, subject_label, lbl_function)
            logging.debug('Function arguments are %s'%arguments)
            # if the list argument has elements then check if 
            # information can flow from them to executing subject
            if len(arguments) > 0:
                read_arguments(subject_label, arguments, lbl_function)
            # create a new labelling function copying the labels of 
            # global variables from the current labelling function
            new_lbl_function = create_labelling_function()
            logging.debug('New labelling function is created')
            # save the current line number to resume execution after 
            # the called function is executed
            saved_current_line = current_line
            logging.debug('Saved current line is : %s' % saved_current_line)
            # set the current label with the line number where the function
            # is defined
            current_line = functions[function_name]
            logging.debug('Function %s is defined at line number %s' %(function_name, current_line))
            # obtain the parameters defined in the function definition
            parameters, current_line = obtain_parameters(current_line)
            logging.debug('Function parameters are %s'%parameters)
            # if length of both the parameters and arguments lists matches
            # then copy label of arguments into local list of new labelling
            # function
            if len(arguments) == len(parameters):
                logging.debug('Length of arguments and parameters are same = %s' %len(arguments))
                for i in range(len(parameters)):
                    if lbl_function.is_local(arguments[i]):
                        logging.debug('Argument %s is local' % arguments[i])
                        temp_argument_label = lbl_function.label_from_local_list(arguments[i])     
                    elif lbl_function.is_global(arguments[i]):
                        logging.debug('Argument %s is global' % arguments[i])
                        temp_argument_label = lbl_function.label_from_global_list(arguments[i])
                        readers, writers = label_operations.join(temp_argument_label, 
                                                                 lbl_function.get_pc_label())
                        logging.debug('PC label before reading %s is %s'%(arguments[i], lbl_function.get_pc_label().to_string()))
                        lbl_function.get_pc_label().update_readers(readers)
                        lbl_function.get_pc_label().update_writers(writers)
                        logging.debug('PC label after reading %s is %s'%(arguments[i], lbl_function.get_pc_label().to_string()))
                    else:
                        logging.debug('Argument %s is not defined' % arguments[i])
                        temp_argument_label = Label(subject_label.get_owner(),
                                                    ['*'], [])
                    #logging.debug('Label of parameter %s before reading the argument %s is %s'%(parameters[i], arguments[i], subject_label.to_string()))

                    #the final parameter_label will be that of the argument label
                    #join of argument labels is the same as argument label
                    #parameter_label = temp_argument_label cannot be used as then both the variables will point to same object and changes in one will\
                    #reflected in the other
                    readers, writers = label_operations.join(temp_argument_label, temp_argument_label)
                    #create a new parameter_label to hold the join of the argument label and that of the callee function label
                    parameter_label = Label(subject_label.get_owner(), readers, writers)
                    logging.debug('Label of parameter %s after reading the argument %s is %s'%(parameters[i], arguments[i], parameter_label.to_string()))
                    # print('Label of parameter %s after reading the argument %s having label %s is %s'%(parameters[i], arguments[i], temp_argument_label.to_string(), parameter_label.to_string()))
                    #add the parameter_label to the local list of variables of the label function of the callee function
                    new_lbl_function.update_local_label_list(parameters[i], 
                                                                 parameter_label)
                    #also when the parameter label s checked then the local pc label should also be updated
                    logging.debug('Function PC label before reading parameter %s is %s'%(parameters[i], new_lbl_function.get_pc_label().to_string()))
                    readers, writers = label_operations.join(parameter_label, new_lbl_function.get_pc_label())
                    new_lbl_function.get_pc_label().update_readers(readers)
                    new_lbl_function.get_pc_label().update_writers(writers)
                    logging.debug('Function PC label after reading parameter %s is %s'%(parameters[i], new_lbl_function.get_pc_label().to_string()))

            else:
                logging.warning('Function %s parameters do not match with arguments' % function_name)
                sys.exit()
            # now execute each statement within the function until it
            # reaches the endfunc keyword
            logging.debug('Starting Execution of the body of function %s' % function_name)
            while not is_end_of_function(lines[current_line]): 
                # if current line encounters a new statement
                if is_a_statement(lines[current_line]):
                    new_lbl_function, current_line = DL(current_line,
                                                        subject_label,
                                                        new_lbl_function)
                    #to keep a track of the final downgrade list after the complete execution of the function takes place;everytime a new list is generated
                    lbl_function.make_downgrade_list_empty()
                    for label in new_lbl_function.get_downgrade_list():
                        lbl_function.insert_into_downgrade_list(label)
                else:
                    current_line = next_line(current_line)
            #end of the function reached , hence checking for the flow of labels of return values to the callee function
            logging.debug('All the return statements have been read')
            logging.debug('Checking if the labels in the downgrade list can flow to the function %s'%(function_name))
            #check if the join of the labels stored in the downgrade list of lbl_function can flow to the subject label of the callee function 
            #list return_values stores the result true/ flase
            global return_values
            return_values = list()
            for label in lbl_function.get_downgrade_list():
                check_label_can_flow = flow_operations.can_flow(label, subject_label)
                return_values.append(check_label_can_flow)
            #checking if the joined labels can flow to the callee function
            #if can flow : continue
            #else :exit; insecure information flow
            #the count of return values begins from zero
            for i in range(len(lbl_function._downgraded_label)):
                if return_values[i] is True and flow_operations.can_flow(lbl_function._downgraded_label[i], subject_label):
                    logging.debug('The label %s of return value at place %s can flow to function %s'%(lbl_function._downgraded_label[i].to_string(), str(i), function_name))
                else:
                    logging.debug('The label %s of return value at place %s cannot flow to function %s'%(lbl_function._downgraded_label[i].to_string(), str(i), function_name))
                    error_type = 0
                    print_misuse_message(error_type, 
                                         ":return value", 
                                         function_name, 
                                         lbl_function._downgraded_label[i],
                                         subject_label)                  
            logging.debug('Function %s execution completed' %function_name)
            # print('Derived labels of local variables from function: %s' % function_name)
            # print(new_lbl_function.print_local_labels())
            logging.info('Derived labels of local variables from function: %s' % function_name)
            logging.info('%s' % new_lbl_function.print_local_labels())
            # copy the downgrade list from new labelling function to old 
            # labelling function after the completion of function call
            # execution
            
            # restore the saved current line to resume the execution after
            # the function is executed
            current_line = saved_current_line
            logging.debug('Current line is now back to %s' %current_line)
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

        elif is_a_print_function(current_line):
            new_label, current_line = perform_print(current_line, clearance, lbl_function)
            return new_label, current_line

        else:
            function_name = get_the_id(current_line)
            logging.warning('Function %s is a built-in function' % function_name)
            if lbl_function.find_in_functions_list(function_name):
                subject_label = lbl_function.label_from_functions_list(function_name)
            # otherwise function is executed with the label of main 
            # executing subject
            else:
                subject_label = clearance
            logging.debug('Function is executed with subject label %s' % subject_label.to_string())
            arguments, current_line = obtain_arguments(current_line, subject_label, lbl_function)
            logging.debug('Function arguments are %s'%arguments)
            # if the list argument has elements then check if 
            # information can flow from them to executing subject
            if len(arguments) > 0:
                read_arguments(subject_label, arguments, lbl_function)
            join_of_label = Label(subject_label.get_owner(), ['*'], [])
            temp_argument_label = Label(subject_label.get_owner(), ['*'], [])
            for i in range(len(arguments)):
                if lbl_function.is_local(arguments[i]):
                    logging.debug('Argument %s is local' % arguments[i])
                    temp_argument_label = lbl_function.label_from_local_list(arguments[i])     
                elif lbl_function.is_global(arguments[i]):
                    logging.debug('Argument %s is global' % arguments[i])
                    temp_argument_label = lbl_function.label_from_global_list(arguments[i])
                    readers, writers = label_operations.join(temp_argument_label, 
                                                            lbl_function.get_pc_label())
                    logging.debug('PC label before reading %s is %s'%(arguments[i], lbl_function.get_pc_label().to_string()))
                    lbl_function.get_pc_label().update_readers(readers)
                    lbl_function.get_pc_label().update_writers(writers)
                    logging.debug('PC label after reading %s is %s'%(arguments[i], lbl_function.get_pc_label().to_string()))
                else:
                    logging.debug('Argument %s is not defined' % arguments[i])
                    temp_argument_label = Label(subject_label.get_owner(),
                                                ['*'], [])

                readers, writers = label_operations.join(temp_argument_label,
                                                      join_of_label)
                join_of_label.update_writers(writers)
                join_of_label.update_readers(readers)
            if flow_operations.can_flow(join_of_label, subject_label):
                logging.debug('The join of label %s of arguments of built-in function can flow to function %s'%(join_of_label.to_string(), function_name))
            else:
                logging.debug('The join of label %s of arguments of built-in function can flow to function %s'%(join_of_label.to_string(), function_name))
                error_type = 0
                print_misuse_message(error_type, 
                                     "argument label", 
                                     function_name, 
                                     join_of_label,
                                     subject_label)
            
            lbl_function.update_local_label_list(function_name, subject_label)

            return lbl_function, current_line
    except Exception as e:
        logging.debug('Function %s fails in Call statement' % inspect.stack()[0][3] )
        logging.warning('%s' %e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()


''' Perform labelling for a 'return' statement'''
def perform_return(current_line, clearance, lbl_function):
    try:
        # current line currently on the Return keyword, hence move to next line
        # print("return on line "+str(current_line)+" ")
        current_line = next_line(current_line)
        # flush the downgrade stack everytime a new Return statement is 
        # encountered
        # print("label inside return statement \n")
        # for label in lbl_function._downgraded_label:
        #     print(str(current_line)+" "+label.to_string()+" ")
        # fetch the returned variables 
        variables, current_line = obtain_target_variables(current_line, clearance, lbl_function)
        logging.debug('Returning variables are %s'%variables)
        # now iterate the variables list and start downgrading label of each
        # variable inside the list
        for variable in variables:
            # if the variable is from local list
            if lbl_function.is_local(variable):
                logging.debug('Local variable: %s' % variable)
                variable_label = lbl_function.label_from_local_list(variable)
            # if the variable is from the global list
            elif lbl_function.is_global(variable):
                logging.debug('Global variable: %s' % variable)
                variable_label = lbl_function.label_from_global_list(variable)
            else:
                variable_label = Label(clearance.get_owner(), ['*'], [])

            # print('Before downgrading : Variable %s and label %s' %(variable, variable_label.to_string()))
            logging.debug('Label of %s before downgrading %s' %(variable, variable_label.to_string()))

            #implicit downgrading i.e adding the owner from clearance to the reader set of returning variable
            new_readers = clearance.get_owner()
            # downgrade the label of each variable and obtain the new label
            # new_label = flow_operations.downgrade(clearance,
            #                                       variable,
            #                                       variable_label,
            #                                       new_readers)
            # if new_label is None:
            new_label = variable_label
            #inserting the labels of the variables from the first return statement in the list
            # print('After downgrading : Variable %s and label %s' %(variable, new_label.to_string()))
            # logging.debug('Label of %s after downgrading %s' %(variable, new_label.to_string()))
            if not len(lbl_function._downgraded_label) == len(variables):
                lbl_function._downgraded_label.append(new_label)
                #* denotes list getting populated for the first time 


            elif len(lbl_function._downgraded_label) == len(variables):
                readers, writers = label_operations.join(new_label, lbl_function._downgraded_label[0])
                logging.debug('Label after joining label in the list %s and new downgraded label %s is below :' %(lbl_function._downgraded_label[0].to_string(), new_label.to_string()))
                #we treat the list as a queue, taking the join of new label and the label at index 0 ,everytime a new variable comes
                #delete the entry in the list at index 0 and replace this new joined label at the end of the list
                del lbl_function._downgraded_label[0]
                readers = list(set(readers))
                writers = list(set(writers))
                new_label.update_readers(readers)
                new_label.update_writers(writers)
                lbl_function.insert_into_downgrade_list(new_label)
                logging.debug(' %s' %(new_label.to_string()))

        return lbl_function, current_line
    except Exception as e:
        logging.debug('Function %s: fails in Call statement'% inspect.stack()[0][3])
        logging.warning('%s' %e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()

#to check if the information to be printed can flow to the console/file to receive the output
def perform_print(current_line, clearance, lbl_function):
    try:
        subject_label = lbl_function.label_from_output_list("print_file")
        logging.debug("Label of print file is %s "%(subject_label.to_string()))
        current_line = next_line(current_line)
        arguments, current_line = obtain_arguments(current_line, subject_label, lbl_function)
        logging.debug(len(arguments))
        for i in range(len(arguments)):
                    if lbl_function.is_local(arguments[i]):
                        logging.debug('Argument %s is local' % arguments[i])
                        temp_argument_label = lbl_function.label_from_local_list(arguments[i])     
                    elif lbl_function.is_global(arguments[i]):
                        logging.debug('Argument %s is global' % arguments[i])
                        temp_argument_label = lbl_function.label_from_global_list(arguments[i])
                    else:
                        logging.debug('Argument %s is not defined' % arguments[i])
                        temp_argument_label = Label(subject_label.get_owner(),
                                                    ['*'], [])

                    if flow_operations.can_flow(temp_argument_label, subject_label):
                        logging.debug("%s with label %s can flow to the print file with label %s and can be printed"%(arguments[i], temp_argument_label.to_string(), subject_label.to_string()))
                    else:
                        logging.debug('%s with label %s cannot flow to the print file with label %s and cannot be printed'%(arguments[i], temp_argument_label.to_string(), subject_label.to_string()))
                        error_type = 0
                        print_misuse_message(error_type, 
                                            arguments[i], 
                                            "print file", 
                                            temp_argument_label,
                                            subject_label) 

    except Exception as e:
        logging.debug('Function %s: fails in Print statement'% inspect.stack()[0][3])
        logging.warning('%s' %e)
        logging.warning('****** Monitor Aborted ******')
        sys.exit()

    return lbl_function, current_line

#DL function responsible for calling appropriate function for labelling each
#kind of statement'''
def DL(current_line, clearance, lbl_function):
    logging.debug('current node: %s at line %s' %(lines[current_line], current_line))
    # first check if it has already gone beyond the total length of the lines
    if is_end_of_file(current_line):
        return lbl_function, current_line 
    # if the current line is an assignment statement
    elif is_an_assignment(lines[current_line]):
        return perform_assignment(current_line, clearance, lbl_function) 
    # if the current line is a comparison statement   
    elif is_a_comparison(lines[current_line]):
        return perform_comparison(current_line, clearance, lbl_function)
    # if the current line is an iteration statement i.e. "While"
    elif is_an_iteration(lines[current_line]):
        return perform_iteration(current_line, clearance, lbl_function)
    # if the current line is a function call
    elif is_a_function_call(lines[current_line]):
        return perform_function_call(current_line, clearance, lbl_function)
    # if the current line is a return statement
    elif is_a_return(lines[current_line]):
        return perform_return(current_line, clearance, lbl_function)
    #if the current line is a print statement
    elif is_a_print_function(lines[current_line]):
        return perform_print(current_line, clearance, lbl_function)
    else:
        return lbl_function, current_line
        

''' This function is responsible to call the main DL function and provide the
interface to be called by the main function for performing the labelling of
program of interest'''
def perform_labelling(filename, clearance, lbl_function):
    with open(filename, 'r') as file:
        global lines
        lines = file.read().splitlines()
        current_line = 0
        while not is_end_of_file(current_line):
            if is_a_function_def(lines[current_line]):
                logging.debug('Starting the function current node: %s at line %s' %(lines[current_line], current_line))
                current_line = next_line(current_line)
                lbl_function.make_downgrade_list_empty()
                global functions
                functions[get_the_id(current_line)] = current_line
                # skip everything until the end of function is reached
                while not is_end_of_function(lines[current_line]):
                    current_line = next_line(current_line)
                logging.debug('Ending the function current node: %s at line %s' %(lines[current_line], current_line))
            if is_a_statement(lines[current_line]):
                lbl_function, current_line = DL(current_line,
                                                clearance,
                                                lbl_function)
            else:
                current_line = next_line(current_line)
        return lbl_function
