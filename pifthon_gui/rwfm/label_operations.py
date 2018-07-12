
def join(label_1, label_2):
	'''Derives the Least Upper Bound of two labels and returns 
	the new label'''
	# if readers set of either of the label contain * then new readers set is equal to the other one
	if label_1.get_readers()==['*']:
		_readers = label_2.get_readers()
	elif label_2.get_readers()==['*']:
		_readers = label_1.get_readers()
	# otherwise the new readers set is equal to the intersection of readers set of two labels
	else:	
		_readers = list(set(set(label_1.get_readers()) & set(label_2.get_readers())))
	
	# if writers set of any of the label contain * then new writers set shall contain *
	if label_1.get_writers()==['*'] or label_2.get_writers()==['*']:
		_writers = ['*']
	# else new writers set is equal to the union of writers set of two labels
	else:				
		_writers = list(set(set(label_1.get_writers()) | set(label_2.get_writers())))
		
	return _readers, _writers

			
def meet(label_1, label_2):
	'''Derives the Greatest Lower Bound of two labels and returns 
	the new label'''
	# if readers set of either of the label contain * then new readers set is equal to *
	if label_1.get_readers()==['*'] or label_2.get_readers()==['*']:
		_readers = ['*']
	#else new readers set is equal to the union of readers set of two labels
	else:
		_readers = list(set(set(label_1.get_readers()) | set(label_2.get_readers())))
	
	#if writers set of either of the label contain * then new writers set is equal to the other one
	if label_1.get_writers()==['*']:
		_writers = label_2.get_writers()
	elif label_2.get_writers()==['*']:
		_writers = label_1.get_writers()
	# otherwise the new writers set is equal to the intersection of writers set of two labels
	else:		
		_writers = list(set(set(label_1.get_writers()) & set(label_2.get_writers())))
		
	return _readers, _writers
