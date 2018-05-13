from rwfm.Label import Label


class LabelFunctions:
    _global = dict()
    _functions = dict()

    def __init__(self):
        self._pc = Label('PC',['*'],[])
        self._local = dict()
        self._downgraded_label = list()

    def update_local_label_list(self, id, label_object):
        new_label = Label(label_object.get_owner(),
                          label_object.get_readers(),
                          label_object.get_writers())
        self._local[id]=new_label


    def insert_into_global_list(self, id, label_object):
        LabelFunctions._global[id]=label_object


    def insert_into_function_list(self, function_name, label_object):
        LabelFunctions._functions[function_name] = label_object
        

    def find_in_functions_list(self, function_name):
        if function_name in LabelFunctions._functions.keys():
            return True
        else:
            return False


    def label_from_functions_list(self, function_name):
        if function_name in LabelFunctions._functions.keys():
            return LabelFunctions._functions[function_name]
        else:
            return None


    def insert_into_downgrade_list(self, label):
        self._downgraded_label.append(label)


    def remove_from_downgrade_list(self):
        return self._downgraded_label.pop(0)


    def make_downgrade_list_empty(self):
        self._downgraded_label = list()


    def get_downgrade_list(self):
        return self._downgraded_label


    def is_local(self, id):
        if id in self._local.keys():
            return True
        else:
            return False

  
    def is_global(self, id):
        if id in LabelFunctions._global.keys():
            return True
        else:
            return False


    def label_from_local_list(self, id):
        if id in self._local.keys():
            return self._local[id]
        else:
            return None

    
    def label_from_global_list(self, id):
        if id in LabelFunctions._global.keys():
            return LabelFunctions._global[id]
        else:
            return None

   
    def get_pc_label(self):
        return self._pc


    def set_pc_label(self, pc_label):
        self._pc = Label(pc_label.get_owner(), 
                         pc_label.get_readers(), 
                         pc_label.get_writers())


    def is_equal_to(self, label_function):
        try:
            if self.get_pc_label().is_equal_to(label_function.get_pc_label()):
                for key in label_function._local.keys():
                    if not self._local[key].is_equal_to(label_function._local[key]):
                        return False
            else:
                return False
            return True
        except Exception:
            return False
                


    def copy_into(self, label_function):
        label_function.set_pc_label(self.get_pc_label())
        for key in self._local.keys():
            label_function.update_local_label_list(key, self._local[key])


    def print_global_labels(self):
        str=''
        for key in LabelFunctions._global.keys():
            str = str + key + ' : ' + LabelFunctions._global[key].to_string() + '\n'
        return str


    def print_local_labels(self):
        str=''
        for key in LabelFunctions._local.keys():
            str = str + key + ' : ' + LabelFunctions._local[key].to_string() + '\n'
        return str
    

    def print_function_labels(self):
        str = ''
        for key in LabelFunctions._functions.keys():
            str = str + key + ' : ' + LabelFunctions._functions[key].to_string() + '\n'
        return str