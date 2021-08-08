import io

class ESENT_LEAF_HEADER:
	def __init__(self):
		self.CommonPageKey = None #('CommonPageKey',':'), ???
	
	@staticmethod
	def from_bytes(data):
		return ESENT_LEAF_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_LEAF_HEADER()
		res.CommonPageKey = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res
