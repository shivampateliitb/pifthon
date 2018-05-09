import json
import collections
from rwfm.Label import Label


def parse_owner(data):
    '''Parse the owner field from the JSON Object'''
    return data["owner"]

def parse_readers(data):
    '''Parse the readers field from the JSON Object'''
    _readers = []
    for readers in data["readers"]:
        for key in readers:
            _readers.append(readers[key])
    return _readers

def parse_writers(data):
    '''Parse the writers field from the JSON Object'''
    _writers = []
    for writers in data["writers"]:
        for key in writers:
            _writers.append(writers[key])
    return _writers
    
def parse_source_filename(json_file):
    '''Method returns a list containing name of the source files'''
    _input_data = json.load(open(json_file))
    return "inputs/"+ _input_data["source_file"]["name"]


def parse_subject_label(json_file):
    '''Method returns the security label of executing subject given in the input file'''
    _input_data = json.load(open(json_file))
    _owner = parse_owner(_input_data["source_file"]["label"])
    _readers = parse_readers(_input_data["source_file"]["label"])
    _writers = parse_writers(_input_data["source_file"]["label"])      
    subject_label = Label(_owner,_readers,_writers)
    return subject_label
        
def parse_globals(json_file):
    '''Method returns a dictionary having global variables as key that is mapped to respective static label '''
    _input_data = json.load(open(json_file))
    _globals={}
    for globals in _input_data["source_file"]["global_vars"]:
        _id = globals["id"]
        _owner = parse_owner(globals["label"])
        _readers = parse_readers(globals["label"])
        _writers = parse_writers(globals["label"])
        _label = Label(_owner,_readers,_writers)
        _globals[_id]=_label
        
    return _globals

def print_globals(globals):
    str=''
    for key in globals.keys():
        str = str + key + ' : ' + globals[key].to_string() + '\n'
    return str

