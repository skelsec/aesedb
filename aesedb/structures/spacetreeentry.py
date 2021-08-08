import io

class ESENT_SPACE_TREE_ENTRY:
	def __init__(self):
		self.PageKeySize = None
		self.LastPageNumber = None
		self.NumberOfPages = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_SPACE_TREE_ENTRY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_SPACE_TREE_ENTRY()
		res.PageKeySize = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.LastPageNumber = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.NumberOfPages = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res
