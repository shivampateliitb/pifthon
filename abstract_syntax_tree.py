import ast

global tree
	
def create_ast(program_name):
	'''Method that receives a python program and create an AST of the program''' 
	#Parse the program
	tree = ast.parse(open(program_name).read())	
	#Return the tree object
	return tree

def write_ast_into_file(tree, filename):		
	with open(filename,'w') as file:
		v=Visitor(file)	
		for statement in tree.body:
			v.visit(statement)


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
    
    def visit_Arg(self, node):
        self._file_object.write('arg:'+ node.s + '\n')
    
    def visit_While(self, node):
        self._file_object.write(type(node).__name__ + "\n")
        super().generic_visit(node)
        self._file_object.write('endloop\n')
    
#     def visit_Call(self,node):
# 		self._file_object.write(type(node).__name__ + '\n')


# 	def visit_FunctionDef(self, node):
# 		self._file_object.write(type(node).__name__ + '\n')
# 		super().generic_visit(node)
# 		self._file_object.write('endfunc\n')
		
		
		
# 			block = type(statement).__name__
# 			file.write(block+'\n')
# 			for child in ast.iter_child_nodes(statement):
# 				v.visit(child)
# 			if block == 'While':
# 				file.write('endloop\n')
# 	'''Method that prints AST dump into console'''
# 	print('########### AST dump ###########\n')
# 	print(ast.dump(tree))
# 	print('\n')
# 	print('############ Program statements ###########\n')
# 	for statement in tree.body:
# 		for child in ast.iter_child_nodes(statement):
# 			print(ast.dump(child))
# class RecursiveVisitor(ast.NodeVisitor):
#     """ example recursive visitor """
#     '''Class responsible to visit each node from the AST dump and create an easily comprehensible AST dump''' 
# 
#     global _file_object
# 
#     def __init__(self, file):
#         '''Method accepts the file name as argument and open the file while initializing class object'''
#         self._file_object = file
# 
# 
#     def recursive(func):
#         """ decorator to make visitor work recursive """
#         def wrapper(self, node):
#             func(self, node)
#             for child in ast.iter_child_nodes(node):
#                 self.visit(child)
#         return wrapper
#        
#     @recursive
#     def generic_visit(self, node):
#         self._file_object.write(type(node).__name__ + "\n")
#         super().generic_visit(node)
#         block = type(node).__name__
#         if block == 'While':
#             self._file_object.write('endloop\n')
# 
# 
#     @recursive
#     def visit_Name(self, node):
#         self._file_object.write('name:' +  node.id + "\n")
# 
# 
#     @recursive   
#     def visit_Num(self, node):
#         self._file_object.write('num:'+ str(node.__dict__['n']) + "\n")
# 
# 
#     @recursive     
#     def visit_Str(self, node):
#         self._file_object.write('str:'+ node.s + "\n")  
# 
# 
#     @recursive
#     def visit_Arg(self, node):
#         self._file_object.write('arg:'+ node.s + '\n')
# 
# 
#     @recursive
#     def visit_Call(self,node):
#         """ visit a Call node and visits it recursively"""
#         print(type(node).__name__)

#     @recursive
#     def visit_Lambda(self,node):
#         """ visit a Function node """
#         print(type(node).__name__)
# 
#     @recursive
#     def visit_FunctionDef(self,node):
#         """ visit a Function node and visits it recursively"""
#         print(type(node).__name__)
# 
#     @recursive
#     def visit_Module(self,node):
#         """ visit a Module node and the visits recursively"""
#         pass
