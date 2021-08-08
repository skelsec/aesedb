import io

class ESENT_SPACE_TREE_HEADER:
	def __init__(self):
		self.Unknown = None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_SPACE_TREE_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_SPACE_TREE_HEADER()
		res.Unknown = int.from_bytes(buff.read(8), byteorder='little', signed=False)
		return res
