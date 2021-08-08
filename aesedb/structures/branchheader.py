import io

class ESENT_BRANCH_HEADER:
	def __init__(self):
		self.CommonPageKey = None #('CommonPageKey',':'), ?????
	
	@staticmethod
	def from_bytes(data):
		return ESENT_BRANCH_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_BRANCH_HEADER()
		res.CommonPageKey = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res
