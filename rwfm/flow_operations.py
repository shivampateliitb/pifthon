from rwfm.Label import *
import logging

def can_flow(from_label, to_label):
	'''Function checks if from_label can flow to to_label and return true
	or false either'''
	# If readers set of from label contain * or is super set of to label then 
	if from_label.get_readers()==['*'] or set(from_label.get_readers()).issuperset(set(to_label.get_readers())):
		# If writers set of to label contains * or is superset of from label then return true
		if to_label.get_writers()==['*'] or set(to_label.get_writers()).issuperset(set(from_label.get_writers())):
			return True
		else:
			return False
	else:
		return False
	
	
def downgrade(subject_label, object_name, object_label, principals):
	'''Downgrade function declassifies the label of an object and return the declassified label and a boolean
	value indicating a successful downgrading''' 
	# If owner of the subject label executing the operation is not the owner
	# of the object label that is going to be downgraded
	if subject_label.get_owner() == object_label.get_owner():			
		# If the set principals is a subset of writers set of object_label 
		# or If owner is the sole writer  of object_label then also return 
		# True then return True
		if set(principals).issubset(set(object_label.get_writers())) \
		or set(object_label.get_writers()) == list(set(subject_label.get_owner())) \
		or set(principals) == set(object_label.get_writers()):
			# Update the readers set of object_label
			object_label.insert_into_readers(principals)
			return object_label
		else:
			logging.debug('downgrade(%s, %s)  error: new readers are not the current writers of %s' 
			 	%(object_name, principals, object_name))
			return None
	else:
		logging.debug('downgrade(%s, %s)  error: owner is not the owner of the object' 
			 %(object_name, principals))
		return None