import io

class ESENT_ROOT_HEADER:
	def __init__(self):
		self.InitialNumberOfPages = None
		self.ParentFatherDataPage = None
		self.ExtentSpace= None
		self.SpaceTreePageNumber= None
	
	@staticmethod
	def from_bytes(data):
		return ESENT_ROOT_HEADER.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_ROOT_HEADER()
		res.InitialNumberOfPages = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ParentFatherDataPage = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.ExtentSpace= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.SpaceTreePageNumber= int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res
