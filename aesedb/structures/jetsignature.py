import io


class ESENT_JET_SIGNATURE:
	def __init__(self):
		self.Random = None
		self.CreationTime = None
		self.NetBiosName = b""
	
	@staticmethod
	def from_bytes(data):
		return ESENT_JET_SIGNATURE.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = ESENT_JET_SIGNATURE()
		res.Random = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.CreationTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
		res.NetBiosName = buff.read(16)
		return res
	