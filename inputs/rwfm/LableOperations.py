
def LUB(label_1, label_2):
	'''Derives the Least Upper Bound of two labels and returns 
	the new label'''
	_readers = list(set(label_1.getReaders()) & set(label_2.getReaders()))
					
	_writers = list(set(label_1.getWriters()) | set(label_2.getWriters()))
	return _readers, _writers

			
def GLB(label_1, label_2):
	'''Derives the Greatest Lower Bound of two labels and returns 
	the new label'''
	_readers = list(set(label_1.getReaders()) | set(label_2.getReaders()))
					
	_writers = list(set(label_1.getWriters()) & set(label_2.getWriters()))
	return _readers, _writers
