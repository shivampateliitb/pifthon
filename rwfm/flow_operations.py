from rwfm.Label import *

def canFlow(from_label, to_label):
	'''Function checks if from_label can flow to to_label and return true
	or false either'''
	# If readers set of from label contain * or is super set of to label then 
	if from_label.getReaders()==['*'] or from_label.getReaders().issuperset(to_label.getReaders()):
		# If writers set of to label contains * or is superset of from label then return true
		if to_label.getWriters()==['*'] or to_label.getWriters().issuperset(from_label.getWriters()):
			return True
		else:
			return False
	else:
		return False
	
	
def downgrade(subject_label, owner, object_label, principals):
	'''Downgrade function declassifies the label of an object and return the declassified label and a boolean
	value indicating a successful downgrading''' 
	# If owner of the subject label executing the operation is same as "owner" then
	if subject_label.getOwner() == owner:
		#If the set principals is a subset of writers set of object_label or If owner is the sole writer 
		# of object_label then also return True then return True
		if principals.issubset(object_label.getWriters()) or object_label.getWriters().equal(set(owner)):
			# Update the readers set of object_label
			object_label.updateReaders(principals)
			return object_label, True
		else:
			return None, False
	else:
		return None, False