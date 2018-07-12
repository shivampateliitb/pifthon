import sqlite3
import time
import datetime
import random
import json
from rwfm.Label import Label
import parse_input_file_1


conn = sqlite3.connect('INPUT.db')
c = conn.cursor()

def create_table(file_name):
    c.execute('CREATE TABLE IF NOT EXISTS '+file_name+'(object_type TEXT, object TEXT, owner TEXT, readers TEXT, writers TEXT)')


def data_entry():
    conn.commit()
    c.close()
    conn.close()

def dynamic_data_entry(file_name, object_type, object_name, owner, reader, writer):
    c.execute('INSERT INTO '+file_name+'(object_type, object, owner, readers, writers) VALUES(?, ?, ?, ?, ?)',
              (object_type, object_name, owner, reader, writer))
    conn.commit()

def read_from_db_global_vars(file_name):
    #fetching all the rows from the table
    conn.row_factory = dict_factory
    #making a cursor object to read the data extracted
    cursor = conn.cursor()
    #selecting all the rows
    cursor.execute("select * from "+file_name)
    # fetch all or one we'll go for all.
    results = cursor.fetchall()
    _globals={}

    if results:
        for row in results:
            if row["object_type"] == "global_vars":
                _label = parse_input_file_1.parse_globals(row)
                _globals[row["object"]] = _label
    return _globals  

def read_from_db_function_label(file_name):
    #fetching all the rows from the table
    conn.row_factory = dict_factory
    #making a cursor object to read the data extracted
    cursor = conn.cursor()
    #selecting all the rows
    cursor.execute("select * from "+file_name)
    # fetch all or one we'll go for all.
    results = cursor.fetchall()
    _functions = {}
    
    if results:
        for row in results:
            if row["object_type"] == "function_name":
                _label = parse_input_file_1.parse_function_labels(row)
                _functions[row["object"]] = _label
    return _functions

def read_from_db_outputfile(file_name):

    #fetching all the rows from the table
    conn.row_factory = dict_factory
    #making a cursor object to read the data extracted
    cursor = conn.cursor()
    #selecting all the rows
    cursor.execute("select * from "+file_name)
    # fetch all or one we'll go for all.
    results = cursor.fetchall()
    
    _output_file = {}
    
    if results:
        for row in results:
            if row["object_type"] == "outputfile":
                _label = parse_input_file_1.parse_output_file(row)
                _output_file[row["object"]] = _label 
    return _output_file

def read_from_db_file(file_name):
    #fetching all the rows from the table
    conn.row_factory = dict_factory
    #making a cursor object to read the data extracted
    cursor = conn.cursor()
    #selecting all the rows
    cursor.execute("select * from "+file_name)
    # fetch all or one we'll go for all.
    results = cursor.fetchall()
    _file = {}
    if results:
        for row in results:
            if row["object_type"] == "file":
                return parse_input_file_1.parse_subject_label(row)


def del_and_update(file_name):
    conn.row_factory = dict_factory
    #making a cursor object to read the data extracted
    cursor = conn.cursor()
    cursor.execute('DROP TABLE '+file_name)
    conn.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
