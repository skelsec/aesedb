import io

class CRYPTED_HASH:
	def __init__(self):
		self.Header = None
		self.KeyMaterial = None
		self.EncryptedHash = None

	@staticmethod
	def from_bytes(data):
		return CRYPTED_HASH.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = CRYPTED_HASH()
		res.Header = buff.read(8)
		res.KeyMaterial = buff.read(16)
		res.EncryptedHash = buff.read(16)
		return res
	
class CRYPTED_HASHW16:
	def __init__(self):
		self.Header = None
		self.KeyMaterial = None
		self.Unknown = None
		self.EncryptedHash = None

	@staticmethod
	def from_bytes(data):
		return CRYPTED_HASHW16.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = CRYPTED_HASHW16()
		res.Header = buff.read(8)
		res.KeyMaterial= buff.read(16)
		res.Unknown = buff.read(4)
		res.EncryptedHash = buff.read()
		return res

class CRYPTED_HISTORY:
	def __init__(self):
		self._len = 24
		self.Header = None
		self.KeyMaterial = None
		self.EncryptedHash = None

	@staticmethod
	def from_bytes(data):
		return CRYPTED_HISTORY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = CRYPTED_HISTORY()
		res.Header = buff.read(8)
		res.KeyMaterial = buff.read(16)
		res.EncryptedHash = buff.read()
		res._len += len(res.EncryptedHash)
		return res

class CRYPTED_BLOB:
	def __init__(self):
		self.Header = None
		self.KeyMaterial = None
		self.EncryptedHash = None

	@staticmethod
	def from_bytes(data):
		return CRYPTED_BLOB.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = CRYPTED_BLOB()
		res.Header = buff.read(8)
		res.KeyMaterial= buff.read(16)
		res.EncryptedHash = buff.read()
		return res