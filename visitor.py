import ast


class Visitor(ast.NodeVisitor):
    '''Class responsible to visit each node from the AST dump and create an easily comprehensible 
    AST dump''' 
    global _file_object
    
    def __init__(self, file):
        '''Method accepts the file name as argument and open the file while initializing class object'''
        self._file_object = file
              
    def generic_visit(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)

    def visit_Name(self, node):
        self._file_object.write('name:'+ node.id + "\n")
         
    def visit_Num(self, node):
        self._file_object.write('num:'+ str(node.__dict__['n']) + "\n")
         
    def visit_Str(self, node):
        self._file_object.write('str:'+ node.s + "\n")
        
# import contextlib
# with contextlib.closing(Visitor('ast.dump')) as program:
#     program.check()