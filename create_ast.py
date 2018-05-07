import ast
from _operator import length_hint
from visitor import Visitor
#object that holds the Abstract Syntax Tree
global tree
	
def CreateAST(program_name):
	'''Method that receives a python program and create an AST of the program''' 
	#Parse the program
	tree = ast.parse(open(program_name).read())
	
	#Return the tree object
	return tree

def writeAST(tree, filename):
	with open(filename,'w') as file:
		v=Visitor(file)	
		for statement in tree.body:
			block = type(statement).__name__
			file.write(block+'\n')
			for child in ast.iter_child_nodes(statement):
				v.visit(child)
			if block == 'While':
				file.write('endloop\n')

# 	'''Method that prints AST dump into console'''
# 	print('########### AST dump ###########\n')
# 	print(ast.dump(tree))
# 	print('\n')
# 	print('############ Program statements ###########\n')
# 	for statement in tree.body:
# 		for child in ast.iter_child_nodes(statement):
# 			print(ast.dump(child))
	
