
def join(label_1, label_2):
	'''Derives the Least Upper Bound of two labels and returns 
	the new label'''
	# if readers set of either of the label contain * then new readers set is equal to the other one
	if label_1.getReaders()==['*']:
		_readers = label_2.getReaders()
	elif label_2.getReaders()==['*']:
		_readers = label_1.getReaders()
	# otherwise the new readers set is equal to the intersection of readers set of two labels
	else:	
		_readers = list(set(label_1.getReaders()) & set(label_2.getReaders()))
	
	# if writers set of any of the label contain * then new writers set shall contain *
	if label_1.getWriters()==['*'] or label_2.getWriters()==['*']:
		_writers = ['*']
	# else new writers set is equal to the union of writers set of two labels
	else:				
		_writers = list(set(label_1.getWriters()) | set(label_2.getWriters()))
	return _readers, _writers

			
def meet(label_1, label_2):
	'''Derives the Greatest Lower Bound of two labels and returns 
	the new label'''
	# if readers set of either of the label contain * then new readers set is equal to *
	if label_1.getReaders()==['*'] or label_2.getReaders()==['*']:
		_readers = ['*']
	#else new readers set is equal to the union of readers set of two labels
	else:
		_readers = list(set(label_1.getReaders()) | set(label_2.getReaders()))
	
	#if writers set of either of the label contain * then new writers set is equal to the other one
	if label_1.getWriters()==['*']:
		_writers = label_2.getWriters()
	elif label_2.getWriters()==['*']:
		_writers = label_1.getWriters()
	# otherwise the new writers set is equal to the intersection of writers set of two labels
	else:		
		_writers = list(set(label_1.getWriters()) & set(label_2.getWriters()))
		
	return _readers, _writers
