from tkinter.ttk import _list_from_layouttuple
def CanFlow(from_label, to_label):
	'''Function checks if from_label can flow to to_label and return true
	or false either'''
	if (set(from_label.getReaders()) < set(to_label.getReaders())):
		'''If readers list of label_1 is a subset	
	