import ast
import logging

global tree


def create_ast(program_name):
	'''Method that receives a python program and create an AST of the program''' 
	tree = ast.parse(open(program_name).read())	
	return tree


def write_ast_into_file(tree, filename):		
    with open(filename,'w') as file:
        v=Visitor(file)	
        for statement in tree.body:
            v.visit(statement)
            # print(ast.dump(statement))

class Visitor(ast.NodeVisitor):
    '''Class responsible to visit each node from the AST dump and create an 
    easily comprehensible AST dump''' 
    global _file_object


    def __init__(self, file):
        '''Method accepts the file name as argument and open the file while 
        initializing class object'''
        self._file_object = file

    
    def generic_visit(self, node):
    	super().generic_visit(node)


    def visit_Name(self, node):
        self._file_object.write('name:'+ node.id + "\n")
         
    def visit_Num(self, node):
        self._file_object.write('num:'+ str(node.__dict__['n']) + "\n")


    def visit_Str(self, node):
        self._file_object.write('str:'+ node.s + "\n")


    def visit_Assign(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)


    def visit_Tuple(self, node):
    	self._file_object.write(type(node).__name__ + "\n")
    	super().generic_visit(node)
    	self._file_object.write("endtuple\n")

    def visit_List(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)
        self._file_object.write("endlist\n")
    
    def visit_Subscript(self, node):
        #print(ast.dump(node.value.id))
        self._file_object.write("List:"+ str(node.value.id) + "\n")
        data_type = type(node.slice.value).__name__
        if data_type == 'Num':
            self._file_object.write('index:' + str(node.slice.value.n) + '\n')
        elif data_type == 'Str':
            self._file_object.write('index:' + node.slice.value.s + '\n')
        elif data_type == 'Subscript':
            ast.NodeVisitor.visit(self, node.slice.value)
        elif data_type == 'BinOp':
            self._file_object.write('start_index:\n')
            ast.NodeVisitor.visit(self, node.slice.value)
            self._file_object.write('end_index:\n')
        elif data_type == 'Name':
        	self._file_object.write('index:' + node.slice.value.id + '\n')


    def visit_Dict(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)
        self._file_object.write("endictionary\n")

    def visit_Compare(self, node):
    	self._file_object.write(type(node).__name__ + "\n")
    	super().generic_visit(node)


    def visit_While(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)
        self._file_object.write('endloop\n')


    def visit_Return(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)
    
    def visit_Call(self, node):
        self._file_object.write(type(node).__name__ + '\n')
        # self._file_object.write('func:' + node.func.id + '\n')
        #to check if print statement or write statement
        if(type(node.func).__name__ == 'Attribute' and type(node.func.value).__name__ == 'Name'):
            self._file_object.write('func:' + node.func.attr + '\n')

        elif(type(node.func).__name__ == 'Attribute' and type(node.func.value).__name__ == 'Attribute'):
            temp = node
            node = node.func
            func_name = node.attr
            while not type(node.value).__name__ == 'Name':
                node = node.value
            node = temp
            self._file_object.write('func:' + func_name + '\n')
        else:
            self._file_object.write('func:' + node.func.id + '\n') 
        self._file_object.write('func_arg_open:\n')
        for arg in node.args:
            data_type = type(arg).__name__
            if data_type == 'Num':
                self._file_object.write('arg:' + str(arg.n) + '\n')
            elif data_type == 'Str':
                self._file_object.write('arg:' + arg.s + '\n')
            elif data_type == 'List':
                self._file_object.write('arg:')
                for i in range(len(arg.elts)):
                    sub_data_type = type(arg.elts[i]).__name__
                    if sub_data_type == 'Num':
                        self._file_object.write(str(arg.elts[i].n))
                    elif sub_data_type == 'Str':
                        self._file_object.write(arg.elts[i].s)
                    if not i == (len(arg.elts)-1):
                        self._file_object.write(',')
                self._file_object.write('\n')
            elif data_type == 'Subscript':#for an argument of the type list1[0]
                ast.NodeVisitor.visit(self,arg)
            elif data_type == 'Call':#for function call as one of the arguments
                #print(ast.dump(arg))
                ast.NodeVisitor.visit(self,arg)

            else:
                self._file_object.write('arg:' + arg.id + '\n')
        self._file_object.write('func_arg_close:\n')


    def visit_FunctionDef(self, node):
    	self._file_object.write(type(node).__name__ + '\n')
    	self._file_object.write('func:' + node.name + '\n')
    	for arg in node.args.args:
    		self._file_object.write('arg:' + arg.arg + '\n')
    	super().generic_visit(node)
    	self._file_object.write('endfunc\n')


    class FunctionCallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            print(ast.dump(node))

    def visit_Expr(self, node):
        if node.value == 'Str':
            super().generic_visit(node)
        else:
            ast.NodeVisitor.visit(self, node.value)

    def visit_BinOp(self, node):
        ast.NodeVisitor.visit(self, node.left)
        ast.NodeVisitor.visit(self, node.right)


