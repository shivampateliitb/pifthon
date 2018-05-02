class Label:
	'Represents a security label'

	def __init__(self, owner, readers, writers):
		'Initializing a security label on creation'
		self._owner = owner
		self._readers = readers
		self._writers = writers

	def getOwner(self):
		return self._owner

	def getReaders(self):
		return self._readers

	def getWriters(self):
		return self._writers
	
	def updateReaders(self, readers):
		self._readers.update(set(readers))
		
	def updateWriters(self, writers):
		self._writers(set(writers))
	
	def printLabel(self):
		lbl = str(self.getOwner()) + ',' + str(self.getReaders()) + ',' + str(self.getWriters())
		return lbl