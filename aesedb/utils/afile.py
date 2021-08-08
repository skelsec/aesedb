class AFile:
	"""
	Utility class since most OSes don't yet support async file read operations
	"""
	def __init__(self, filepath):
		self.filepath = filepath
		self.fd = open(filepath, 'rb')
		
	async def seek(self, pos, whence = 0):
		return self.fd.seek(pos, whence)
	
	async def read(self, n = -1):
		return self.fd.read(n)
	
	def tell(self):
		return self.fd.tell()
	
	async def close(self):
		return self.fd.close()