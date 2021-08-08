
import io

class KERB_STORED_CREDENTIAL_NEW:
	def __init__(self):
		self.Revision = None
		self.Flags = None
		self.CredentialCount = None
		self.ServiceCredentialCount = None
		self.OldCredentialCount = None
		self.OlderCredentialCount = None
		self.DefaultSaltLength = None
		self.DefaultSaltMaximumLength = None
		self.DefaultSaltOffset = None
		self.DefaultIterationCount = None
		self.Buffer = None
	
	@staticmethod
	def from_bytes(data):
		return KERB_STORED_CREDENTIAL_NEW.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = KERB_STORED_CREDENTIAL_NEW()
		res.Revision = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Flags = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.CredentialCount = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.ServiceCredentialCount = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.OldCredentialCount = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.OlderCredentialCount = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.DefaultSaltLength = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.DefaultSaltMaximumLength = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.DefaultSaltOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.DefaultIterationCount = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Buffer = buff.read()
		return res

	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s : %s\r\n' % (k, self.__dict__[k])
		return t



class KERB_KEY_DATA_NEW:
	def __init__(self):
		self._len = 24
		self.Reserved1 = None
		self.Reserved2 = None
		self.Reserved3 = None
		self.IterationCount = None
		self.KeyType = None
		self.KeyLength = None
		self.KeyOffset = None
	
	@staticmethod
	def from_bytes(data):
		return KERB_KEY_DATA_NEW.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = KERB_KEY_DATA_NEW()
		res.Reserved1 = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Reserved2 = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Reserved3 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.IterationCount = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.KeyType = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.KeyLength = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.KeyOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		return res

	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s : %s\r\n' % (k, self.__dict__[k])
		return t