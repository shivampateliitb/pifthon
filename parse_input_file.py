import json
from rwfm import Label

global _subject_label
global _source_file
global _input_data


def getSourceFileName(json_file):
    _input_data = json.load(open(json_file))
    return 'inputs/'+ _input_data["source_file"]["name"]


def getSubjectLabel():
    '''Method returns the security label of executing subject given in the input file'''
    pass



