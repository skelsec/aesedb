import io

class PEKLIST_ENC:
	def __init__(self):
		self.Header = None
		self.KeyMaterial = None
		self.EncryptedPek = None

	@staticmethod
	def from_bytes(data):
		return PEKLIST_ENC.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = PEKLIST_ENC()
		res.Header = buff.read(8)
		res.KeyMaterial= buff.read(16)
		res.EncryptedPek= buff.read()
		return res
	
	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s : %s\r\n' % (k, self.__dict__[k])
		return t


class PEKLIST_PLAIN:
	def __init__(self):
		self.Header = None
		self.DecryptedPek = None

	@staticmethod
	def from_bytes(data):
		return PEKLIST_PLAIN.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = PEKLIST_PLAIN()
		res.Header = buff.read(32)
		res.DecryptedPek= buff.read()
		return res

class PEK_KEY:
	def __init__(self):
		self._len = 20
		self.Header = None
		self.Padding = None
		self.Key = None

	@staticmethod
	def from_bytes(data):
		return PEK_KEY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = PEK_KEY()
		res.Header = buff.read(1)
		res.Padding= buff.read(3)
		res.Key= buff.read(16)
		return res

