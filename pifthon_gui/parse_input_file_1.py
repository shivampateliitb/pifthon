import json
import collections
from rwfm.Label import Label


def parse_owner(data):
    '''Parse the owner field from the JSON Object'''
    return data["owner"]

def parse_readers(data):
    '''Parse the readers field from the JSON Object'''
    _readers = []
    #data["readers"] is a string thus we can get a list of readers using the split function
    _readers = data["readers"]
    return _readers.split(",")

def parse_writers(data):
    '''Parse the writers field from the JSON Object'''
    _writers = []
    _writers = data["writers"]
    return _writers.split(",")
    
# def parse_source_filename(json_file):
#     '''Method returns a list containing name of the source files'''
#     _input_data = json.load(open(json_file))
#     return  _input_data["source_file"]["path"]

def parse_subject_label(row):
    '''Method returns the security label of executing subject given in the input file'''
    try:
        _id = row["object"]
        _owner = parse_owner(row)
        _readers = parse_readers(row)
        _writers = parse_writers(row)      
        subject_label = Label(_owner,_readers,_writers)
    except KeyError as e:
        return None
    else:
        return subject_label
        
def parse_globals(row):
    '''Method returns a dictionary having global variables as key that is mapped to respective static label '''
    _globals={}
    try:
        glob = row
        _id = glob["object"]
        _owner = parse_owner(glob)
        _readers = parse_readers(glob)
        _writers = parse_writers(glob)
        _label = Label(_owner,_readers,_writers)
        _globals[_id]=_label
    except KeyError as e:
        return None
    else:
        return _label


def parse_function_labels(row):
    _functions = {}
    try:
        function = row    
        _name = function["object"]
        _owner = parse_owner(function)
        _readers = parse_readers(function)
        _writers = parse_writers(function)
        _label = Label(_owner, _readers, _writers)
        _functions[_name] = _label
    except KeyError as e:
        return None
    else:
        return _label

def parse_output_file(row):
    _output_file = {}
    try:
        file = row
        _name = file["object"]
        _owner = parse_owner(file)
        _readers = parse_readers(file)
        _writers = parse_writers(file)
        _label = Label(_owner, _readers, _writers)
        _output_file[_name] = _label
    except KeyError as e:
        return None
    else:
        return _label




# def print_globals(globals):
#     str=''
#     if globals:
#         for key in globals.keys():
#             str = str + key + ' : ' + globals[key].to_string() + '\n'
#         return str
#     else:
#         return 'Not Given'

