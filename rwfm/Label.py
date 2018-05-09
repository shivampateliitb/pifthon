class Label:
	'Represents a security label'

	def __init__(self, owner, readers, writers):
		'Initializing a security label on creation'
		self._owner = owner
		self._readers = readers
		self._writers = writers

	def get_owner(self):
		return self._owner

	def get_readers(self):
		return self._readers

	def get_writers(self):
		return self._writers

	def update_readers(self, readers):
		self._readers = list(readers)
		
	def update_writers(self, writers):
		self._writers = list(writers)
		
	def is_equal_to(self, label):
		if (self._owner == label.get_owner()) and (set(self._readers) == set(label.get_readers())) and (set(self._writers) == set(label.get_writers())):
			return True
		else:
			return False
	
	def to_string(self):
		lbl = str(self.get_owner()) + ',' + str(self.get_readers()) + ',' + str(self.get_writers())
		return lbl
	
	