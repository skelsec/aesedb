import io

class USER_PROPERTIES:
	def __init__(self):
		self.Reserved1 = None
		self.Length  = None
		self.Reserved2  = None
		self.Reserved3 = None
		self.Reserved4 = None
		self.PropertySignature = None
		self.PropertyCount = None
		self.UserProperties = []
	
	@staticmethod
	def from_bytes(data):
		return USER_PROPERTIES.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = USER_PROPERTIES()
		res.Reserved1 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Length  = int.from_bytes(buff.read(4), byteorder='little', signed=False)
		res.Reserved2  = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Reserved3 = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Reserved4 = buff.read(96)
		res.PropertySignature = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PropertyCount = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		for _ in range(res.PropertyCount):
			prop = USER_PROPERTY.from_buffer(buff)
			res.UserProperties.append(prop)
		return res
	
	def __str__(self):
		t = ''
		for k in self.__dict__:
			if isinstance(self.__dict__[k], list):
				for e in self.__dict__[k]:
					t += '%s : %s %s' % (k, self.__dict__[k], str(e))
			else:
				t += '%s : %s' % (k, self.__dict__[k])
		return t


class USER_PROPERTY:
	def __init__(self):
		self.NameLength = None
		self.ValueLength = None
		self.Reserved = None
		self.PropertyName = None
		self.PropertyValue = None
	
	@staticmethod
	def from_bytes(data):
		return USER_PROPERTY.from_buffer(io.BytesIO(data))
	
	@staticmethod
	def from_buffer(buff):
		res = USER_PROPERTY()
		res.NameLength = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.ValueLength = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.Reserved = int.from_bytes(buff.read(2), byteorder='little', signed=False)
		res.PropertyName = buff.read(res.NameLength).decode('utf-16le')
		res.PropertyValue = buff.read(res.ValueLength)
		return res

	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s : %s' % (k, self.__dict__[k])
		return t