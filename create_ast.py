import ast
from _operator import length_hint
#object that holds the Abstract Syntax Tree
global tree
	
def CreateAST(program_name):
	'''Method that receives a python program and create an AST of the program''' 
	
	#Parse the program
	tree = ast.parse(open(program_name).read())
	
	#Return the tree object
	return tree

def PrintAST(tree):
	'''Method that prints AST dump into console'''
	print('########### AST dump ###########\n')
	print(ast.dump(tree))
	print('\n')
	print('############ Program statements ###########\n')
	for statement in tree.body:
		for child in ast.iter_child_nodes(statement):
			print(ast.dump(child))
	
