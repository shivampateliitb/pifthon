import ast


global tree


def create_ast(program_name):
	'''Method that receives a python program and create an AST of the program''' 
	tree = ast.parse(open(program_name).read())	
	return tree


def write_ast_into_file(tree, filename):		
	with open(filename,'w') as file:
		v=Visitor(file)	
		for statement in tree.body:
# 			print(ast.dump(statement))
			v.visit(statement)


class Visitor(ast.NodeVisitor):
    '''Class responsible to visit each node from the AST dump and create an 
    easily comprehensible AST dump''' 
    global _file_object


    def __init__(self, file):
        '''Method accepts the file name as argument and open the file while 
        initializing class object'''
        self._file_object = file

    
    def generic_visit(self, node):
#         self._file_object.write(type(node).__name__ + "\n")
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
    	self._file_object.write('func:' + node.func.id + '\n')
    	for arg in node.args:
    		data_type = type(arg).__name__
    		if data_type == 'Num':
    			self._file_object.write('arg:' + str(arg.n) + '\n')
    		elif data_type == 'Str':
    			self._file_object.write('arg:' + arg.s + '\n')
    		elif data_type == 'List':
    			self._file_object.write('arg:')
    			for i in range(len(arg.elts)):
    				self._file_object.write(arg.elts[i].s)
    				if not i == (len(arg.elts)-1):
    					self._file_object.write(',')
    			self._file_object.write('\n')
    		else:
    			self._file_object.write('arg:' + arg.id + '\n')


    def visit_FunctionDef(self, node):
    	self._file_object.write(type(node).__name__ + '\n')
    	self._file_object.write('func:' + node.name + '\n')
    	for arg in node.args.args:
    		self._file_object.write('arg:' + arg.arg + '\n')
    	super().generic_visit(node)
    	self._file_object.write('endfunc\n')
    	
