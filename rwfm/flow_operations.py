
def canFlow(from_label, to_label):
	'''Function checks if from_label can flow to to_label and return true
	or false either'''	
	if (from_label.getReaders().issuperset(to_label.getReaders()) and from_label.getWriters().issubset(to_label.getWriters())):
		#If readers list of from_label is a superset of readers list of to_label
		#and writers list of from_label is a subset of writers list of to_label then return true
		return True
	else:
		return False
	
def downgrade(subject_label, owner, object_label, principals):
	'''Downgrade function declassifies the label of an object and return the declassified''' 
	pass