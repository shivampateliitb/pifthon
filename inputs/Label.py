class Label:
	'Represents a security label'

	def __init__(self, owner, readers, writers):
		'Initializing a security label on creation'
		self._owner = owner
		self._readers = readers
		self._writers = writers

	def _getOwner(self):
		return self._owner

	def _getReaders(self):
		return self._readers

	def _getWriters(self):
		return self._writers

